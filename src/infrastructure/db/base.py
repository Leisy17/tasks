from sqlalchemy.orm import Session
from typing import TypeVar, Generic, List

T = TypeVar('T')

class Base(Generic[T]):
    def __init__(self, db_session: Session, model_class: T):
        self.db_session = db_session
        self.model_class = model_class

    def create(self, obj: T) -> T:
        db_obj = obj
        self.db_session.add(db_obj)
        self.db_session.commit()
        self.db_session.refresh(db_obj)
        return db_obj
    
    def get_custom_query(self, query) -> List[T]:
        return query.all()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        return self.db_session.query(self.model_class).offset(skip).limit(limit).all()
    
    def get_by(self, **filters) -> T:
        return self.db_session.query(self.model_class).filter_by(**filters).first()
    
    def get_all_by(self, **filters) -> List[T]:
        query = self.db_session.query(self.model_class)
        conditions = []

        for field, value in filters.items():
            column_attr = getattr(self.model_class, field)

            if isinstance(value, list):
                conditions.append(column_attr.in_(value))
            elif isinstance(value, str) and "%" in value:
                conditions.append(column_attr.ilike(value))
            else:
                conditions.append(column_attr == value)

        return query.filter(*conditions).all()

    def update(self, obj_id: int, obj: T) -> T:
        db_obj = self.db_session.query(self.model_class).filter(self.model_class.id == obj_id).first()
        if db_obj:
            for column in self.model_class.__table__.columns:
                key = column.name
                if hasattr(obj, key):
                    value = getattr(obj, key)
                    setattr(db_obj, key, value)
            self.db_session.commit()
            self.db_session.refresh(db_obj)
            return db_obj
        return None

    def delete(self, obj_id: int) -> None:
        db_obj = self.db_session.query(self.model_class).filter(self.model_class.id == obj_id).first()
        if db_obj:
            self.db_session.delete(db_obj)
            self.db_session.commit()
