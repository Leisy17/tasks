from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.db.database import Base

import app.models.task_status
import app.models.task_list

class TaskModel(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status_id = Column(Integer, ForeignKey("task_status.id"), nullable=False)
    task_list_id = Column(Integer, ForeignKey("task_list.id"), nullable=False)
    active = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    status = relationship("TaskStatusModel", back_populates="tasks")
    task_list = relationship("TaskListModel", back_populates="tasks")