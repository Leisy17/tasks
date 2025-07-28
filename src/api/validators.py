
def validate_positive_id(v: int, field_name: str) -> int:
    if v <= 0:
        raise ValueError(f'El campo "{field_name}" debe ser mayor que 0')
    return v


def validate_not_empty_string(v: str, field_name: str, min_length: int = 1) -> str:
    if not v or not v.strip():
        raise ValueError(f'El campo "{field_name}" no puede estar vacío')
    if len(v.strip()) < min_length:
        raise ValueError(f'El campo "{field_name}" debe tener al menos {min_length} caracteres')
    return v.strip()