
from pydantic import BaseModel

class Pet(BaseModel): 
    user_id: int | None = None
    pet_id: int | None = None
    first_name: str
    done: bool | None = False

class User(BaseModel):
    user_id: int | None = None
    nickname: str
    password: str
    email: str
    disabled: bool | None = None
    
class LoginCreds(BaseModel):
    email: str
    password: str

class JwtPayload(BaseModel):
    email: str
    nickname: str
    user_id: int
    