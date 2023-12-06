from fastapi import FastAPI, Depends, APIRouter
from app.routers import pets, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(users.router)
app.include_router(pets.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
