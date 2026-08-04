from fastapi import FastAPI, HTTPException, Response, Query
from pydantic import BaseModel
from database import conn, cursor

app = FastAPI()

@app.get("/", summary = 'Get API information')
def root():
    return {
        'name':'CRUD Task API',
        'version':'1.0',
        'endpoints':["/tasks"]
    }
    
@app.get("/health", summary="Check server health")
def getHealth():
    return {'status':"OK"}

@app.get("/tasks", summary="Get tasks list")
def getTasks(done: bool | None = Query(None),
             search : str | None = Query(None),
             limit: int | None = Query(None, ge=1),
             offset: int = Query (0, ge=0)):
    
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    
    result = []
    
    for row in rows:
        result.append(
            {
                "id": row[0],
                "title" : row[1],
                "done" : row[2]
            }
        )

    if done is not None:
        return [task for task in result if task["done"]== done]
    
    if search is not None:
        result = [
            task for task in result 
            if search.lower() in task["title"].lower()
        ]
        
    if limit is not None:
        result = result[offset: offset + limit]
    else:
        result = result[offset:]
        
    return result

@app.get("/tasks/{task_id}", summary="Get a specific task")
def get_one_task(task_id: int):
    
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    
    if row is None:
        raise HTTPException(
            status_code = 404,
            detail = "Task not found"
        )
    
    return{
        "id" : row[0],
        "title" : row[1],
        "done" : row[2]
    }
        
@app.get("/stats", summary="Check tasks stats")
def getStats():
    
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = 1")
    done = cursor.fetchone()[0]
    
    open = total - done
    
    return {
        "total": total,
        "done": done,
        "open": open
    }
    
class TaskCreate(BaseModel):
    title : str
    
@app.post("/tasks", status_code=201, summary="Create a new task")
def createTask(task: TaskCreate):
    
    if task.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )
    
    cursor.execute("""
                   INSERT INTO tasks(title, done)
                   VALUES (?, ?)
                   """, (task.title, False))
    
    conn.commit()
    
    new_id = cursor.lastrowid
    
    return {
        "id":new_id,
        "title": task.title,
        "done" : False
    }

class TaskUpdate(BaseModel):
    title : str
    done : bool
    
@app.put("/tasks/{task_id}", summary="Update an existing task")
def updateTask(task_id: int, update_task: TaskUpdate):
    
    if update_task.title.strip() == "":
        raise HTTPException(
            status_code = 400,
            detail = "Title cannot be empty"
        )
        
    cursor.execute("""
                   UPDATE tasks
                   SET title = ?, done = ?
                   WHERE id = ?""", (update_task.title, update_task.done, task_id))

        
    if cursor.rowcount == 0:
        raise HTTPException(
                status_code = 404,
                detail = f"Task {task_id} not found"
            )
        
    conn.commit()
    
    return{
        "id":task_id,
        "title": update_task.title,
        "done": update_task.done
    }
    
@app.delete("/tasks/{task_id}", status_code=204, summary="Delete an existing task")
def delete_task(task_id: int):

    cursor.execute("""
                   DELETE FROM tasks
                   WHERE id = ?""", (task_id,))

    if cursor.rowcount == 0:
        raise HTTPException(
                status_code=404,
                detail=f"Task {task_id} not found."
            )
        
    conn.commit()
    