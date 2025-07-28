from fastapi import FastAPI
from api.v1.endpoints import task
from api.v1.endpoints import task_status
from api.v1.endpoints import task_list

app = FastAPI()

app.include_router(task.router, prefix="/tasks", tags=["tasks"])
app.include_router(task_status.router, prefix="/task_status", tags=["task_status"])
app.include_router(task_list.router, prefix="/task_list", tags=["task_list"])
