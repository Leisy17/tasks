from datetime import datetime
from typing import Dict, List, Optional

from fastapi import HTTPException, status
from sqlalchemy import and_
from api.models.task_list import TaskListContextDTO
from app.models.task_list import TaskListModel as TaskList
from app.models.task_status import COMPLETED, IN_PROGRESS, TaskStatusModel as TaskStatus
from app.models.task import TaskModel as Task

from infrastructure.db.base import Base

class TaskListService:
    def __init__(self, db_session):
        self.db = db_session
        self.task_list_repository = Base(db_session, TaskList)

    def create_task_list(self, name: str) -> TaskList:
        task = TaskList(
            name=name,
            created_at=datetime.now()
        )
        return self.task_list_repository.create(task)

    def get_task_list_by_id(self, task_list_id: int) -> TaskList:
        return self.task_list_repository.get_by(id=task_list_id)

    def get_all_task_list(self, skip: int = 0, limit: int = 100) -> List[TaskList]:
        return self.task_list_repository.get_all(skip=skip, limit=limit)
    
    def list_tasks_with_filters(
        self,
        task_list_id: Optional[int] = None,
        status_filter: Optional[List[str]] = None,
    ) -> TaskListContextDTO:
        query = (
            self.db.query(
                TaskList,
                Task,
                TaskStatus.name.label("status_name")
            )
            .join(
                Task,
                and_(
                    TaskList.id == Task.task_list_id,
                    Task.active == 1
                )
            )
            .join(
                TaskStatus,
                and_(
                    Task.status_id == TaskStatus.id,
                    TaskStatus.active == 1
                )
            )
            .filter(Task.active == 1)
        )

        if status_filter:
            query = query.filter(TaskStatus.name.in_(status_filter))
        if task_list_id:
            query = query.filter(TaskList.id == task_list_id)

        list_task = query.all()

        if not list_task:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La lista especificada no existe."
        )

        completion_score = 0
        total_tasks = 0

        for _, task, __ in list_task:
            total_tasks += 1
            if task.status_id == COMPLETED[0]:
                completion_score += COMPLETED[1]
            elif task.status_id == IN_PROGRESS[0]:
                completion_score += IN_PROGRESS[1]

        percentage_completed = (completion_score / total_tasks) if total_tasks > 0 else 0


        task_list, _, _ = list_task[0]

        result = TaskListContextDTO(
            id=task_list.id,
            name=task_list.name,
            active=task_list.active,
            completed_percentage=percentage_completed,
            created_at=task_list.created_at,
            updated_at=task_list.updated_at
        )

        return result

    
    def delete_task_list(self, task_list_id: int) -> None:
        task = self.task_list_repository.get_by(id=task_list_id)
        if not task:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La lista especificada no existe."
        )
        tasks = Base(self.db, Task).get_all_by(**{"active": 1, "task_list_id": task_list_id})
        if tasks:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La lista especificada no puede ser eliminada por tener tareas adscritas."
        )
        task.active = 0
        task_deleted = self.task_list_repository.update(task_list_id, task)
        if not task_deleted:
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar la lista en la base de datos"
        )
