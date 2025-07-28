from fastapi import Query
from pydantic import BaseModel, StrictInt, ValidationInfo, field_validator
from datetime import datetime
from typing import List, Optional

from api.validators import validate_not_empty_string, validate_positive_id

class TaskResponseEntitiesDTO(BaseModel):
    id: int
    title: str
    description: str
    status_id: int
    task_list_id: int
    status_name: str
    task_list_name: str
    active: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TaskDTO(BaseModel):
    id: int
    title: str
    description: str
    status_id: int
    task_list_id: int
    active: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskFiltersDTO(BaseModel):
    id: Optional[int] = Query(None)
    title: Optional[str] = Query(None)
    description: Optional[str] = Query(None)
    status_id: Optional[List[int]] = Query(None)
    task_list_id: Optional[int] = Query(None)

    class Config:
        from_attributes = True


def get_task_filters(
    id: Optional[StrictInt] = Query(None),
    title: Optional[str] = Query(None),
    description: Optional[str] = Query(None),
    status_id: Optional[List[int]] = Query(None),
    task_list_id: Optional[int] = Query(None)
) -> TaskFiltersDTO:
    return TaskFiltersDTO(
        id=id,
        title=title,
        description=description,
        status_id=status_id,
        task_list_id=task_list_id
    )


class TaskResponseDTO(BaseModel):
    id: StrictInt


class TaskCreateDTO(BaseModel):
    title: str
    description: str
    status_id: StrictInt
    task_list_id: StrictInt

    class Config:
        from_attributes = True

    @field_validator('status_id', 'task_list_id')
    def validate_ids(cls: type, v: StrictInt, info: ValidationInfo) -> int:
        return validate_positive_id(v, info.field_name)

    @field_validator('title')
    def validate_title(cls: type, v: str) -> str:
        return validate_not_empty_string(v, 'title', min_length=3)

    @field_validator('description')
    def validate_description(cls: type, v: str) -> str:
        return validate_not_empty_string(v, 'description', min_length=10)


class TaskUpdateDTO(BaseModel):
    status_id: StrictInt
    class Config:
        from_attributes = True

    @field_validator('status_id')
    def validate_ids(cls: type, v: StrictInt, info: ValidationInfo) -> StrictInt:
        return validate_positive_id(v, info.field_name)

class TaskDeleteDTO(BaseModel):
    id: int

    class Config:
        from_attributes = True

    @field_validator('id')
    def validate_ids(cls: type, v: StrictInt, info: ValidationInfo) -> StrictInt:
        return validate_positive_id(v, info.field_name)

