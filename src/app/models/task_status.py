from sqlalchemy import Column, Integer, String
from infrastructure.db.database import Base
from sqlalchemy.orm import relationship

import app.models.task


PENDING = (1, 0)
IN_PROGRESS = (2, 50)
COMPLETED = (3, 100)

class TaskStatusModel(Base):
    __tablename__ = "task_status"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    active = Column(Integer, nullable=False, default=1)

    tasks = relationship("TaskModel", back_populates="status")

