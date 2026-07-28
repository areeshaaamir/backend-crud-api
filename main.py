from fastapi import FastAPI, HTTPException

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
