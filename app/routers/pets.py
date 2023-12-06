from fastapi import APIRouter, Depends, Request
from app.model import Pet
from app.db import get_conn
from app.routers import users
from psycopg2.extras import RealDictCursor
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter(dependencies=[Depends(users.authenticate_jwt)])

@router.get("/pets")
async def getPets(request: Request):
    user_id = request.state.user_id
    conn = get_conn()
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute("SELECT pet_id,first_name,done FROM pets WHERE user_id=%s ORDER BY pet_id DESC",[user_id])
        pets = curs.fetchall()
    return JSONResponse(content=jsonable_encoder(pets))

@router.get("/pets/{id}")
async def getPet(request: Request, pet_id: int):
    user_id = request.state.user_id
    conn = get_conn()
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute("SELECT * FROM pets WHERE pet_id=%s AND user_id=%s", [pet_id, user_id])
        pet = curs.fetchall()
    return JSONResponse(content=jsonable_encoder(pet))

@router.post("/pets")
async def createPet(request: Request, pet: Pet):
    user_id = request.state.user_id
    conn = get_conn()
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute("INSERT INTO pets(user_id, first_name) VALUES (%s, %s) RETURNING *;", [user_id, pet.first_name])
        conn.commit()
        new_pet = curs.fetchall()
    return JSONResponse(content=jsonable_encoder(new_pet))

@router.put("/pets")
async def updatePet(request: Request, pet: Pet):
    user_id = request.state.user_id
    conn = get_conn()
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute("UPDATE pets SET first_name=%s, done=%s WHERE pet_id=%s AND user_id=%s RETURNING *;",
                    [pet.first_name, pet.done, pet.pet_id, user_id])
        conn.commit()
        updated_pet = curs.fetchall()
    return JSONResponse(content=jsonable_encoder(updated_pet))

@router.delete("/pets/{id}")
async def deletePet(id: int):
    conn = get_conn()
    with conn.cursor() as curs:
        curs.execute("DELETE FROM pets WHERE pet_id=%s",
                    [id])
        conn.commit()
    return {"message": "todo successfully deleted"}
