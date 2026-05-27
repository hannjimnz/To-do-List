from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from typing import Optional, List 

app = FastAPI(title= "To do list")

#aqui configuraremos los CORS, esto es para que no haya problema con el frontend al momento de conectarlo 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True ,
    allow_methods=["*"],
    allow_headers=["*"]
)

#creacion de los modelos de datos, esto es para validar lo que entra y sale del api

class TaskCreate(BaseModel):
    title: str

class Task(BaseModel):
    id: int
    title: str
    completed:bool

#aqui vamos a inicializar la base de datos sqlite cada vez que se arranque 

def init_db():
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
init_db()

# implementacion de las rutas de la API 

#primero obtendremos tareas 

@app.get("/tasks", response_model=List[Task])
def get_tasks(completed: Optional[bool]= None):
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()

    if completed is not None:
        cursor.execute ("SELECT id, title, completed FROM task WHERE completed = ?", (1 if completed else 0,))
    else:
        cursor.execute("SELECT id, title, completed FROM tasks")
    
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1], "completed": bool(r[2])} for r in rows]

# crear  nuesvas tareas
@app.post("/tasks", response_model=Task) 
def create_task(task: TaskCreate):
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, completed) VALUES (?, 0)", (task.title,))
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"id": task_id, "title": task.title, "completed": False}
