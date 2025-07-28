from typing import List, Dict
from fastapi import APIRouter, Depends
from domain.services.task_service import TaskService
from infrastructure.db.deps import get_db
from api.models.task import TaskCreateDTO, TaskDTO, TaskFiltersDTO, TaskResponseDTO, TaskUpdateDTO, get_task_filters, TaskResponseEntitiesDTO
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/all", response_model=List[TaskDTO])
def get_all_task(db: Session = Depends(get_db)):
    task_service = TaskService(db)
    get_task = task_service.get_all_tasks()
    return get_task


@router.get("/{task_id}", response_model=TaskResponseEntitiesDTO)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task_service = TaskService(db)
    get_task = task_service.get_task_by_id(task_id)
    return get_task


@router.get("/", response_model=List[TaskDTO])
def get_task_by_filters(
    task: TaskFiltersDTO = Depends(get_task_filters),
    db: Session = Depends(get_db)
    ) -> Dict[str, str]:
    task_list_service = TaskService(db)
    updated_task = task_list_service.get_task_by_filters(task)
    return updated_task


@router.post("/", response_model=TaskResponseDTO)
def create_task(task: TaskCreateDTO, db: Session = Depends(get_db)):
    task_service = TaskService(db)
    created_task = task_service.create_task(
        title=task.title,
        description=task.description, 
        status_id=task.status_id,
        task_list_id=task.task_list_id
    )
    return created_task

@router.put("/{task_id}", response_model=TaskUpdateDTO)
def update_task_list(task_id: int, task_update: TaskUpdateDTO, db: Session = Depends(get_db)):
    task_list_service = TaskService(db)
    updated_task = task_list_service.update_task(task_id, task_update.status_id)
    return updated_task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_service = TaskService(db)
    task_service.delete_task(task_id)
    return {"message": "Task deleted successfully"}
