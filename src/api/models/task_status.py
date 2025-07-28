from pydantic import BaseModel, StrictInt, field_validator

from api.validators import validate_not_empty_string

class TaskStatusDTO(BaseModel):
    id: StrictInt
    name: str
    active: int

    class Config:
        from_attributes = True


class TaskStatusResponseDTO(BaseModel):
    id: StrictInt

    class Config:
        from_attributes = True


class TaskStatusCreateDTO(BaseModel):
    name: str

    class Config:
        from_attributes = True

    @field_validator('name')
    def validate_title(cls: type, v: str) -> str:
        return validate_not_empty_string(v, 'name', min_length=3)

