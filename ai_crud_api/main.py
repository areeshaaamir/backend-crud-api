"""
To-Do List CRUD API
--------------------
A simple in-memory CRUD API for managing a to-do list, built with FastAPI.

Endpoints:
    GET    /tasks            -> list all tasks
    GET    /tasks/{task_id}  -> get a specific task
    POST   /tasks            -> create a new task (title required, non-empty)
    PUT    /tasks/{task_id}  -> update a task (404 if not found)
    DELETE /tasks/{task_id}  -> delete a task (404 if not found)
    GET    /stats            -> total / done / open task counts
    POST   /reset            -> reset the task list back to the original seed data

Run with:
    pip install fastapi uvicorn
    uvicorn main:app --reload
"""

import copy
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="To-Do List API")


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class Task(BaseModel):
    id: int
    title: str
    done: bool = False


class TaskCreate(BaseModel):
    title: str
    done: bool = False

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        return value.strip()


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("Title cannot be empty")
        return value.strip() if value is not None else value


class Stats(BaseModel):
    total: int
    done: int
    open: int


# ---------------------------------------------------------------------------
# "Database" (in-memory) — seeded with some original tasks so /reset has
# something meaningful to restore.
# ---------------------------------------------------------------------------

ORIGINAL_TASKS: List[dict] = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Clean the house", "done": False},
    {"id": 3, "title": "Finish homework", "done": False},
]

tasks: List[dict] = copy.deepcopy(ORIGINAL_TASKS)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def find_task(task_id: int) -> Optional[dict]:
    return next((t for t in tasks if t["id"] == task_id), None)


def get_next_id() -> int:
    """Return the smallest positive integer not currently used as an id,
    so that ids freed up by deletions get reused (the 'next empty id')."""
    used_ids = sorted(t["id"] for t in tasks)
    next_id = 1
    for uid in used_ids:
        if uid == next_id:
            next_id += 1
        elif uid > next_id:
            break
    return next_id


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/tasks", response_model=List[Task])
def get_all_tasks():
    """Show all tasks."""
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Get a single task by id."""
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(new_task: TaskCreate):
    """Create a new task. Title cannot be empty; id is auto-assigned."""
    task = {
        "id": get_next_id(),
        "title": new_task.title,
        "done": new_task.done,
    }
    tasks.append(task)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated: TaskUpdate):
    """Update an existing task's title and/or done status."""
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

    if updated.title is not None:
        task["title"] = updated.title
    if updated.done is not None:
        task["done"] = updated.done

    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Delete a task by id."""
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

    tasks.remove(task)
    return {"message": f"Task with id {task_id} deleted successfully"}


@app.get("/stats", response_model=Stats)
def get_stats():
    """Show total, done, and open task counts."""
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    open_count = total - done
    return {"total": total, "done": done, "open": open_count}


@app.post("/reset", response_model=List[Task])
def reset_tasks():
    """Reset the task list back to the original seed data."""
    global tasks
    tasks = copy.deepcopy(ORIGINAL_TASKS)
    return tasks