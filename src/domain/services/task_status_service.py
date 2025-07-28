from typing import List
from app.models.task_status import TaskStatusModel as TaskStatus

from infrastructure.db.base import Base

class TaskStatusService:
    def __init__(self, db_session):
        self.task_repository = Base(db_session, TaskStatus)

    def create_task_status(self, name: str) -> TaskStatus:
        task = TaskStatus(
            id=None,
            name=name
        )
        return self.task_repository.create(task)

    def get_task_status_by_id(self, task_status_id: int) -> TaskStatus:
        return self.task_repository.get_by(id=task_status_id)

    def get_all_task_status(self, skip: int = 0, limit: int = 100) -> List[TaskStatus]:
        return self.task_repository.get_all(skip=skip, limit=limit)
