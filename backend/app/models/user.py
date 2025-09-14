from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, HttpUrl


# Shared properties
class User(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    is_active: bool = True
    is_admin: bool = False
    profile_image: Optional[HttpUrl] = None


# Properties required when creating a new user
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str = Field(..., min_length=8)
    profile_image: Optional[HttpUrl] = None


# Properties allowed when updating an existing user
class UserUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    profile_image: Optional[HttpUrl] = None
    is_active: Optional[bool] = None


# Properties stored in DB
class UserInDB(User):
    id: str
    hashed_password: str
    created_at: datetime


# Properties returned to client
class UserResponse(User):
    id: str
    created_at: datetime
