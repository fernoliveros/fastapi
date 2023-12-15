import bcrypt
import jwt
import os
from fastapi import APIRouter, HTTPException, Depends,Request
from app.model import User, LoginCreds, JwtPayload
from app.db import get_conn
from psycopg2.extras import RealDictCursor
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()
security = HTTPBearer()
jwt_key = os.getenv('JWT_KEY')
jwt_alg = os.getenv('JWT_ALG')

async def authenticate_jwt(request: Request, auth: HTTPAuthorizationCredentials= Depends(security)):
    token = auth.credentials
    try:
        print('======================= jwtalg %s ==========================' %jwt_alg)
        decoded_jwt = jwt.decode(token, jwt_key, algorithms=[jwt_alg])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Sorry!") 
    request.state.user_id = decoded_jwt['user_id'] 
    return

def create_jwt(payload: JwtPayload):
    return jwt.encode(payload, jwt_key, algorithm=jwt_alg)

@router.post("/login", tags=["auth"])
async def login(creds: LoginCreds):
    conn = get_conn()
    with conn.cursor() as curs:
        curs.execute("SELECT user_id, nickname, passhash FROM users WHERE email=%s",
                    [creds.email])
        conn.commit()
        user = curs.fetchall()

    if not user:
        raise HTTPException(status_code=404, detail="Email not found") 
    
    user_id, nickname, passhash = user[0]

    if not bcrypt.checkpw(creds.password, passhash):
        raise HTTPException(status_code=401, detail="NOPE! Try again") 
    
    return {"jwt": create_jwt({"email": creds.email, "nickname": nickname, "user_id": user_id})}

@router.post("/users", tags=["auth"])
async def createUser(user: User):
    hashed_pass = bcrypt.hashpw(user.password, bcrypt.gensalt( 12 ))
    conn = get_conn()
    with conn.cursor() as curs:
        curs.execute("SELECT user_id FROM users WHERE email=%s",
                    [user.email])
        conn.commit()
        existing_user = curs.fetchall()
        if existing_user:
            raise HTTPException(status_code=409, detail="Account with that email already exists") 
        
        curs.execute("INSERT INTO users(nickname, passhash, email) VALUES (%s,%s,%s) RETURNING email, nickname, user_id;",
                    [user.nickname, hashed_pass, user.email])
        conn.commit()
        new_user = curs.fetchall()

    email, nickname, user_id = new_user[0]
    return {"jwt": create_jwt({"email": email,"nickname": nickname, "user_id": user_id})}

@router.get("/users/{username}", tags=["auth"])
async def read_user(username: str):
    return {"username": username}
