from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

tasks = [
    {
        'id': 1,
        'title': "Complete the FlyRank AI Assignment",
        'done': False
    },
    {
        'id': 2,
        'title': "Farm 1000 Primogems in Genshin",
        'done': False
    },
    {
        'id': 3,
        'title': "Make dinner",
        'done': False
    }
]

@app.get("/")
def root():
    return {
        'name':'CRUD Task API',
        'version':'1.0',
        'endpoints':["/tasks"]
    }
    
@app.get("/health")
def getHealth():
    return {'status':"OK"}

@app.get("/tasks")
def getTasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_one_task(task_id: int):
    
    for task in tasks:
        if task_id == task["id"]:
            return task
        
    raise HTTPException(
        status_code= 404,
        detail= f"Task {task_id} does not exist"
    )
    
class TaskCreate(BaseModel):
    title : str
    
@app.post("/tasks", status_code=201)
def createTask(task: TaskCreate):
    
    if task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )
    newTask = {
        "id" : len(tasks) + 1,
        "title" : task.title,
        'done': False
    }
    
    tasks.append(newTask)
    
    return newTask

class TaskUpdate(BaseModel):
    title : str
    done : bool
    
@app.put("/tasks/{task_id}")
def updateTask(task_id: int, update_task: TaskUpdate):
    
    if update_task.title.strip() == "":
        raise HTTPException(
            status_code = 400,
            detail = "Title cannot be empty"
        )
        
    for task in tasks:
        
        if task["id"] == task_id:
            task["title"] = update_task.title
            task["done"] = update_task.done
            
            return task
        
    raise HTTPException(
        status_code = 404,
        detail = f"Task {task_id} not found"
    )