"""
User Data Models

This module defines all Pydantic models for user-related operations.
These models handle data validation, serialization, and API documentation.

Model hierarchy:
- User: Base model with shared properties
- UserCreate: For user registration (includes password)
- UserUpdate: For user updates (all optional fields)
- UserInDB: Database representation (includes hashed password and ID)
- UserResponse: API response (excludes sensitive data)

Security considerations:
- Passwords are only accepted in UserCreate, never returned
- Hashed passwords are only in UserInDB, never in responses
- Email validation ensures proper format
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, HttpUrl


class User(BaseModel):
    """Base user model with shared properties."""
    email: EmailStr
    username: str
    full_name: str
    is_active: bool = True
    is_admin: bool = False
    profile_image: Optional[HttpUrl] = None


class UserCreate(BaseModel):
    """User creation model for registration endpoint."""
    email: EmailStr
    username: str
    full_name: str
    password: str = Field(..., min_length=8)
    profile_image: Optional[HttpUrl] = None


class UserUpdate(BaseModel):
    """User update model for profile modification. All fields optional."""
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    profile_image: Optional[HttpUrl] = None
    is_active: Optional[bool] = None


class UserInDB(User):
    """Database representation - includes hashed password and ID."""
    id: str
    hashed_password: str
    created_at: datetime


class UserResponse(User):
    """API response model - excludes sensitive data."""
    id: str
    created_at: datetime