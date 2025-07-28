from sqlalchemy import Column, DateTime, Integer, String
from infrastructure.db.database import Base
from sqlalchemy.orm import relationship

import app.models.task

class TaskListModel(Base):
    __tablename__ = "task_list"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    active = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    tasks = relationship("TaskModel", back_populates="task_list")


