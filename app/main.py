from fastapi import FastAPI
from app.model import Student
from app.db import get_conn
from psycopg2.extras import RealDictCursor
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/students")
async def getStudents():
    conn = get_conn()
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute("SELECT student_id,first_name,done FROM students ORDER BY student_id DESC")
        students = curs.fetchall()
    return JSONResponse(content=jsonable_encoder(students))

@app.get("/students/{id}")
async def getStudent(id: int):
    conn = get_conn()
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute("SELECT * FROM students WHERE student_id=%s", [id])
        student = curs.fetchall()
    return JSONResponse(content=jsonable_encoder(student))

@app.post("/students")
async def createStudent(student: Student):
    conn = get_conn()
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute("INSERT INTO students(first_name) VALUES (%s) RETURNING *;", [student.first_name])
        conn.commit()
        inStudent = curs.fetchall()
    return JSONResponse(content=jsonable_encoder(inStudent))

@app.put("/students")
async def updateStudent(student: Student):
    conn = get_conn()
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute("UPDATE students SET first_name=%s, done=%s WHERE student_id=%s RETURNING *;",
                    [student.first_name, student.done, student.student_id])
        conn.commit()
        inStudent = curs.fetchall()
    return JSONResponse(content=jsonable_encoder(inStudent))

@app.delete("/students/{id}")
async def deleteStudent(id: int):
    conn = get_conn()
    with conn.cursor() as curs:
        curs.execute("DELETE FROM students WHERE student_id=%s",
                    [id])
        conn.commit()
    return {"message": "todo successfully deleted"}
