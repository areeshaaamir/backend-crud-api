from fastapi import FastAPI

app = FastAPI()

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