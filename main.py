from fastapi import FastAPI

app = FastAPI()

@app.get("/")

def root():
    return {'message': "CRUD API is Running"}