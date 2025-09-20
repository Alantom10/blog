from datetime import datetime, timedelta, timezone
from typing import Optional

import os
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from pydantic import BaseModel

from app.database import users_collection
from bson import ObjectId
from app.models.user import UserResponse
from app.middleware.rate_limit import limiter

# Create router for authentication endpoints
router = APIRouter(
    prefix='/auth',  # All endpoints will be prefixed with /auth
    tags=['auth']    # Groups endpoints in API docs
)


# Pydantic models for request/response validation
class Token(BaseModel):
    """Response model for login endpoints - returns JWT token"""
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    """Request model for JSON-based login endpoint"""
    username: str
    password: str


# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY")  # Secret key from environment variables
ALGORITHM = 'HS256'                   # JWT signing algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 60      # Token expiration time

# Password Hashing Configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt
    
    Args:
        password: Plain text password to hash
        
    Returns:
        str: Bcrypt hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password
    
    Args:
        plain_password: The plain text password to verify
        hashed_password: The stored hashed password from database
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


# OAuth2 scheme for Swagger UI authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    """
    Dependency to get current authenticated user from JWT token
    Used to protect endpoints that require authentication
    
    Args:
        token: JWT token from Authorization header
        
    Returns:
        UserResponse: Current authenticated user data
        
    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise credentials_exception
    
    # Convert MongoDB document to UserResponse model
    response_dict = {
        "id": str(user["_id"]),
        "email": user["email"],
        "username": user["username"],
        "full_name": user["full_name"],
        "profile_image": user.get("profile_image"),
        "is_active": user.get("is_active", True),
        "is_admin": user.get("is_admin", False),
        "created_at": user["created_at"]
    }
    
    return UserResponse(**response_dict)


@router.post("/login", response_model=Token)
@limiter.limit("10/minute")  # Max 10 login attempts per minute
def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible login endpoint for Swagger UI
    
    Accepts form data (username/password) and returns JWT token
    This endpoint is used by FastAPI's built-in OAuth2 authentication in Swagger docs
    
    Args:
        form_data: OAuth2PasswordRequestForm with username and password
        
    Returns:
        Token: JWT access token and token type
        
    Raises:
        HTTPException: 401 if credentials are invalid
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create JWT token with user ID as subject
    access_token = create_access_token(
        data={"sub": str(user["_id"])}  # Use user ID, not username
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login-json", response_model=Token)
def login_with_json(login_data: LoginRequest):
    """
    Alternative login endpoint that accepts JSON body
    
    Useful for frontend applications that prefer JSON over form data
    
    Args:
        login_data: LoginRequest with username and password
        
    Returns:
        Token: JWT access token and token type
        
    Raises:
        HTTPException: 401 if credentials are invalid
    """
    user = authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    access_token = create_access_token(
        data={"sub": str(user["_id"])}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: UserResponse = Depends(get_current_user)):
    """
    Get current authenticated user's profile information
    
    Protected endpoint that requires valid JWT token
    
    Args:
        current_user: Current authenticated user (injected by dependency)
        
    Returns:
        UserResponse: Current user's profile data
    """
    return current_user


def authenticate_user(username: str, password: str):
    """
    Authenticate user credentials against database
    
    Args:
        username: Username to authenticate
        password: Plain text password to verify
        
    Returns:
        dict|bool: User document from database if authentication succeeds,
                   False if authentication fails
    """
    # Find user by username
    user = users_collection.find_one({"username": username})
    if not user:
        return False
    
    # Verify password against stored hash
    if not verify_password(password, user["hashed_password"]):
        return False
    
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token
    
    Args:
        data: Dictionary of claims to encode in token (usually contains user ID)
        expires_delta: Optional custom expiration time, defaults to ACCESS_TOKEN_EXPIRE_MINUTES
        
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})  # Add expiration time to token
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)