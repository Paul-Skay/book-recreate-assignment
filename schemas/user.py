from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    id: str
    name: str
    email: str
    password: str = Field(..., min_length=8)
    age: int
    is_active: bool = True


class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None


class Users(BaseModel):
    books: list[User]


class Response(BaseModel):
    message: Optional[str] = None
    has_error: bool = False
    error_message: Optional[str] = None
    data: Optional[User | Users] = None
