from typing import List
from fastapi import APIRouter, Depends, Query
from domain.services.task_list_service import TaskListService
from infrastructure.db.deps import get_db
from api.models.task_list import TaskListContextDTO, TaskListCreateDTO, TaskListDTO, TaskListResponseDTO
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/tasks", response_model=TaskListContextDTO)
def get_tasks_list_filter_filters(
    task_list_id: int = Query(None),
    status: List[str] = Query(None),
    db: Session = Depends(get_db)
):
    task_service = TaskListService(db)
    result = task_service.list_tasks_with_filters(task_list_id, status_filter=status)
    return result


@router.get("/", response_model=List[TaskListDTO])
def get_task_list(db: Session = Depends(get_db)):
    task_service = TaskListService(db)
    get_task = task_service.get_all_task_list()
    return get_task

@router.post("/", response_model=TaskListResponseDTO)
def create_task_list(task: TaskListCreateDTO, db: Session = Depends(get_db)):
    task_service = TaskListService(db)
    created_task = task_service.create_task_list(
        name=task.name,
    )
    return created_task


@router.delete("/{id}")
def delete_task_list(id: int, db: Session = Depends(get_db)):
    task_service = TaskListService(db)
    task_service.delete_task_list(id)
    return {"message": "Task list deleted successfully"}

