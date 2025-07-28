from typing import List
from fastapi import APIRouter, Depends
from domain.services.task_status_service import TaskStatusService
from infrastructure.db.deps import get_db
from api.models.task_status import TaskStatusCreateDTO, TaskStatusDTO, TaskStatusResponseDTO
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=List[TaskStatusDTO])
def get_task(db: Session = Depends(get_db)):
    task_service = TaskStatusService(db)
    get_task = task_service.get_all_task_status()
    return get_task

@router.post("/", response_model=TaskStatusResponseDTO)
def create_task(task: TaskStatusCreateDTO, db: Session = Depends(get_db)):
    task_service = TaskStatusService(db)
    created_task = task_service.create_task_status(
        name=task.name,
    )
    return created_task

