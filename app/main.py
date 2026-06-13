from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

app = FastAPI(
    title="CI/CD Demo API",
    description="A demo API to practice CI/CD pipelines with GitHub Actions",
    version="1.0.0"
)

# ---- In-memory database ----
tasks_db = []
task_counter = 1

# ---- Models ----
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    priority: Optional[str] = "medium"  # low, medium, high

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    completed: Optional[bool] = None

class Task(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    completed: bool
    created_at: str

# ---- Routes ----

@app.get("/")
def root():
    return {
        "message": "CI/CD Pipeline Demo API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "GET /",
            "GET /health",
            "GET /tasks",
            "POST /tasks",
            "GET /tasks/{id}",
            "PUT /tasks/{id}",
            "DELETE /tasks/{id}"
        ]
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "total_tasks": len(tasks_db)
    }

@app.get("/tasks")
def get_tasks(
    completed: Optional[bool] = None,
    priority: Optional[str] = None
):
    filtered = tasks_db
    if completed is not None:
        filtered = [t for t in filtered if t["completed"] == completed]
    if priority:
        filtered = [t for t in filtered if t["priority"] == priority]
    return {
        "total": len(filtered),
        "tasks": filtered
    }

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    global task_counter
    new_task = {
        "id": task_counter,
        "title": task.title,
        "description": task.description,
        "priority": task.priority,
        "completed": False,
        "created_at": datetime.utcnow().isoformat()
    }
    tasks_db.append(new_task)
    task_counter += 1
    return new_task

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if update.title is not None:
        task["title"] = update.title
    if update.description is not None:
        task["description"] = update.description
    if update.priority is not None:
        task["priority"] = update.priority
    if update.completed is not None:
        task["completed"] = update.completed
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    global tasks_db
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks_db = [t for t in tasks_db if t["id"] != task_id]
    return {"success": True, "message": f"Task {task_id} deleted"}

@app.get("/stats")
def get_stats():
    total = len(tasks_db)
    completed = len([t for t in tasks_db if t["completed"]])
    pending = total - completed
    high = len([t for t in tasks_db if t["priority"] == "high"])
    medium = len([t for t in tasks_db if t["priority"] == "medium"])
    low = len([t for t in tasks_db if t["priority"] == "low"])
    return {
        "total_tasks": total,
        "completed": completed,
        "pending": pending,
        "by_priority": {
            "high": high,
            "medium": medium,
            "low": low
        }
    }