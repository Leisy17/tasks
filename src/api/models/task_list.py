from datetime import datetime
from pydantic import BaseModel, StrictInt, ValidationInfo, field_validator
from typing import Optional

from api.validators import validate_not_empty_string, validate_positive_id

class TaskListContextDTO(BaseModel):
    id: StrictInt
    name: str
    active: int
    completed_percentage: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TaskListDTO(BaseModel):
    id: StrictInt
    name: str
    active: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskListResponseDTO(BaseModel):
    id: StrictInt

    class Config:
        from_attributes = True


class TaskListCreateDTO(BaseModel):
    name: str

    class Config:
        from_attributes = True

    @field_validator('name')
    def validate_title(cls: type, v: str) -> str:
        return validate_not_empty_string(v, 'name', min_length=3)


class TaskListUpdateDTO(BaseModel):
    id: StrictInt
    name: str

    class Config:
        from_attributes = True

    @field_validator('id')
    def validate_ids(cls: type, v: StrictInt, info: ValidationInfo) -> int:
        return validate_positive_id(v, info.field_name)

    @field_validator('name')
    def validate_title(cls: type, v: str) -> str:
        return validate_not_empty_string(v, 'name', min_length=5)


class TaskListDeleteDTO(BaseModel):
    id: int

    class Config:
        from_attributes = True

    @field_validator('id')
    def validate_ids(cls: type, v: StrictInt, info: ValidationInfo) -> int:
        return validate_positive_id(v, info.field_name)

