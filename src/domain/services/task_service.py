from typing import List

from fastapi import HTTPException, status
from sqlalchemy import and_
from api.models.task import TaskFiltersDTO, TaskResponseDTO, TaskResponseEntitiesDTO
from app.models.task import TaskModel as Task
from datetime import datetime

from app.models.task_list import TaskListModel
from app.models.task_status import TaskStatusModel
from domain.services.task_list_service import TaskListService
from domain.services.task_status_service import TaskStatusService
from infrastructure.db.base import Base

class TaskService:
    def __init__(self, db_session):
        self.db = db_session
        self.task_repository = Base(db_session, Task)

    def create_task(self, title: str, description: str, status_id: int, task_list_id: int) -> Task:
        if not TaskStatusService(self.db).get_task_status_by_id(status_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El estado de la tarea especificado no existe."
            )

        if not TaskListService(self.db).get_task_list_by_id(task_list_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La lista '{task_list_id}' no existe."
            )
        task = Task(
            title=title,
            description=description,
            status_id=status_id,
            task_list_id=task_list_id,
            created_at=datetime.now()
        )
        return self.task_repository.create(task)

    def get_task_by_id(self, task_id: int) -> Task:
        query = (
            self.db.query(
                Task,
                TaskListModel.name.label("task_list_name"),
                TaskStatusModel.name.label("status_name"),)
            .join(
                TaskListModel,
                and_(Task.task_list_id == TaskListModel.id,
                TaskListModel.active == 1)
            )
            .join(
                TaskStatusModel,
                and_(Task.status_id == TaskStatusModel.id,
                TaskStatusModel.active == 1)
            )
            .filter(Task.id == task_id, Task.active == 1)
        )
        result = query.all()
        if not result:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        task, task_list_name, status_name = result[0]

        return TaskResponseEntitiesDTO(
            id=task.id,
            title=task.title,
            description=task.description,
            status_id=task.status_id,
            task_list_id=task.task_list_id,
            active=task.active,
            created_at=task.created_at,
            updated_at=task.updated_at,
            task_list_name=task_list_name,
            status_name=status_name
        )
        
    def get_task_by_filters(self, task: TaskFiltersDTO) -> Task:
        filters = {
            "active": 1
        }
        if task.status_id is not None:
            filters["status_id"] = task.status_id
        if task.task_list_id is not None:
            filters["task_list_id"] = task.task_list_id
        if task.title:
            filters["title"] = f"%{task.title}%"
        if task.description:
            filters["description"] = f"%{task.description}%"

        tasks = self.task_repository.get_all_by(**filters)

        if not tasks:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron tareas con esos filtros")

        return tasks

    def get_all_tasks(self, skip: int = 0, limit: int = 100) -> List[Task]:
        return self.task_repository.get_all(skip=skip, limit=limit)

    def update_task(self, task_id: int, status_id: int) -> Task | None:
        if not TaskStatusService(self.db).get_task_status_by_id(status_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El estado de la tarea especificado no existe."
            )
        task = self.task_repository.get_by(id=task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La tarea especificada no existe."
            )
        task.status_id = status_id
        task.updated_at = datetime.now()
        task_updated = self.task_repository.update(task_id, task)
        if not task_updated:
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar la tarea en la base de datos"
        )
        return task_updated

    def delete_task(self, task_id: int) -> None:
        task = self.task_repository.get_by(id=task_id)
        if not task:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La tarea especificada no existe."
        )
        task.active = 0
        task.updated_at = datetime.now()
        task_deleted = self.task_repository.update(task_id, task)
        if not task_deleted:
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar la tarea en la base de datos"
        )
        
