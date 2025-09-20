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
from pydantic import BaseModel, EmailStr, Field, HttpUrl, field_validator
import re


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
    username: str = Field(..., min_length=3, max_length=30)
    full_name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=128)
    profile_image: Optional[HttpUrl] = None

    @field_validator('username')
    def validate_username(cls, v):
        # Allow only alphanumeric characters and underscores
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username can only contain letters, numbers, and underscores')
        # Prevent reserved usernames
        reserved = ['admin', 'root', 'api', 'www', 'mail', 'support']
        if v.lower() in reserved:
            raise ValueError('This username is reserved')
        return v

    @field_validator('password')
    def validate_password(cls, v):
        # Require at least one uppercase, lowercase, digit, and special character
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v

    @field_validator('full_name')
    def validate_full_name(cls, v):
        # Remove extra whitespace and validate length
        v = ' '.join(v.split())
        if len(v) < 1:
            raise ValueError('Full name cannot be empty')
        # Only allow letters, spaces, hyphens, and apostrophes
        if not re.match(r"^[a-zA-Z\s\-']+$", v):
            raise ValueError('Full name can only contain letters, spaces, hyphens, and apostrophes')
        return v


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