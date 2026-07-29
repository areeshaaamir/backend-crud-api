# Backend CRUD API

A simple CRUD Task API built using FastAPI for the FlyRank AI Internship assignment.

The API allows users to create, read, update and delete tasks while demonstrating REST API principles, HTTP status codes and input validation.

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/backend-crud-api.git
```

Move into the project

```bash
cd backend-crud-api
```

Install dependencies

```bash
pip install fastapi uvicorn
```

Run the server

```bash
uvicorn main:app --reload
```

Open

```
http://127.0.0.1:8000/docs
```

## Endpoints

| Method | Endpoint      | Description     |
| ------ | ------------- | --------------- |
| GET    | `/`           | API information |
| GET    | `/health`     | Health check    |
| GET    | `/tasks`      | Get all tasks   |
| GET    | `/tasks/{id}` | Get one task    |
| POST   | `/tasks`      | Create task     |
| PUT    | `/tasks/{id}` | Update task     |
| DELETE | `/tasks/{id}` | Delete task     |
| GET    | `/stats`      | Stats Info      |
| POST   | `/reset`      | Reset tasks     |

## Curl Output

Run:

```bash
curl -i http://127.0.0.1:8000/tasks
```

Output:

```text
HTTP/1.1 200 OK
date: Tue, 28 Jul 2026 12:49:14 GMT
server: uvicorn
content-length: 175
content-type: application/json

[
  {
    "id": 1,
    "title": "Complete the FlyRank AI Assignment",
    "done": false
  },
  {
    "id": 2,
    "title": "Farm 1000 Primogems in Genshin",
    "done": false
  },
  {
    "id": 3,
    "title": "Make dinner",
    "done": false
  }
]
```

## Swagger UI

![Swagger](swagger.png)

## Mortality Experiment

After creating a new task and restarting the server, the new task disappeared and only the original seed tasks remained. This happened because the API currently stores tasks in an in-memory Python list, so all changes are lost when the server process stops; a database would provide persistent storage.