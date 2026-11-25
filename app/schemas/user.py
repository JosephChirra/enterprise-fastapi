from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    age:int
    password : str

class UserResponse(BaseModel):
    id:int
    name:str
    email:EmailStr
    age: int

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    age: int | None = None