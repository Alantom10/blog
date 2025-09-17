"""
User Management API Routes

This module contains all the API endpoints for user management including:
- User registration (public)
- User profile management (authenticated)
- Admin user operations (admin only)

All endpoints except user creation require authentication.
Admin-only endpoints require the user to have is_admin=True.
"""

from datetime import datetime
from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.models.user import UserCreate, UserResponse, UserUpdate
from app.utils.serialization import serialize_for_mongo
from app.utils.auth import get_current_user, hash_password
from app.database import users_collection


# Initialize router with prefix and tags for API organization
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Ensure database connection is established
if users_collection is None:
    raise RuntimeError("users_collection is None - database connection failed")


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate):
    """
    Create a new user account.
    
    This endpoint:
    - Validates that email and username are unique
    - Hashes the password for secure storage
    - Creates user with default settings (is_active=True, is_admin=False)
    - Returns user data without sensitive information
    
    Args:
        user_create: User registration data including email, username, password, etc.
        
    Returns:
        UserResponse: Created user data with generated ID and timestamps
        
    Raises:
        HTTPException 400: Email already registered or username already taken
    """
    # Check for duplicate email
    existing_email = await users_collection.find_one({"email": user_create.email})
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    
    # Check for duplicate username
    existing_username = await users_collection.find_one({"username": user_create.username})
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already taken"
        )

    # Hash password securely using bcrypt
    hashed_pw = hash_password(user_create.password)

    # Convert Pydantic model to dictionary for MongoDB storage
    user_dict = serialize_for_mongo(user_create)

    # Remove plain password and add secure/system fields
    user_dict.pop("password", None)  # Remove plain password for security
    user_dict.update({
        "hashed_password": hashed_pw,
        "created_at": datetime.now(),
        "is_active": True,      # New users are active by default
        "is_admin": False       # New users are not admin by default
    })

    # Insert user into database
    result = await users_collection.insert_one(user_dict)

    # Prepare response data (exclude sensitive information)
    response_dict = {
        "id": str(result.inserted_id),
        "email": user_dict["email"],
        "username": user_dict["username"],
        "full_name": user_dict["full_name"],
        "profile_image": user_dict.get("profile_image"),
        "is_active": user_dict["is_active"],
        "is_admin": user_dict["is_admin"],
        "created_at": user_dict["created_at"]
    }

    return UserResponse(**response_dict)


@router.get("", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_users(current_user: UserResponse = Depends(get_current_user)):
    """
    Get all users in the system.
    
    This endpoint is restricted to admin users only.
    Returns a list of all users with their public information.
    
    Args:
        current_user: Automatically injected current authenticated user
        
    Returns:
        List[UserResponse]: List of all users in the system
        
    Raises:
        HTTPException 401: User not authenticated
        HTTPException 403: User is not an admin
    """
    # Check if current user has admin privileges
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Admin privileges required to access user list"
        )
    
    # Retrieve all users from database
    users = await users_collection.find().to_list(100)  # Limit to prevent memory issues
    
    # Convert MongoDB _id to string id for each user
    for user in users:
        user["id"] = str(user["_id"])
        del user["_id"]  # Remove original _id field
    
    # Convert to UserResponse models and return
    return [UserResponse(**user) for user in users]


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_my_profile(current_user: UserResponse = Depends(get_current_user)):
    """
    Get current user's profile information.
    
    This endpoint allows authenticated users to retrieve their own profile data.
    No special permissions required - any authenticated user can access their own profile.
    
    Args:
        current_user: Automatically injected current authenticated user
        
    Returns:
        UserResponse: Current user's profile information
        
    Raises:
        HTTPException 401: User not authenticated
    """
    return current_user


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: str, current_user: UserResponse = Depends(get_current_user)):
    """
    Get a specific user by their ID.
    
    This endpoint allows admin users to retrieve any user's profile information.
    
    Args:
        user_id: The ObjectId string of the user to retrieve
        current_user: Automatically injected current authenticated user
        
    Returns:
        UserResponse: The requested user's profile information
        
    Raises:
        HTTPException 401: User not authenticated
        HTTPException 403: User is not an admin
        HTTPException 404: User with given ID not found
        HTTPException 400: Invalid user ID format
    """
    # Check admin privileges
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Admin privileges required to access other users' profiles"
        )
    
    try:
        # Convert string ID to ObjectId for MongoDB query
        object_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    
    # Find user in database
    user = await users_collection.find_one({"_id": object_id})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    # Convert _id to string for response
    user["id"] = str(user["_id"])
    del user["_id"]
    
    return UserResponse(**user)


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: str, 
    update: UserUpdate, 
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Update user information.
    
    This endpoint allows:
    - Users to update their own profile information
    - Admin users to update any user's profile information
    
    Password updates will be automatically hashed before storage.
    
    Args:
        user_id: The ObjectId string of the user to update
        update: UserUpdate model containing fields to update
        current_user: Automatically injected current authenticated user
        
    Returns:
        UserResponse: Updated user information
        
    Raises:
        HTTPException 401: User not authenticated
        HTTPException 403: User trying to update another user's profile (non-admin)
        HTTPException 404: User with given ID not found
        HTTPException 400: Invalid user ID format
    """
    # Check permissions: admin can update anyone, user can update themselves
    if not current_user.is_admin and str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="You can only update your own profile unless you are an admin"
        )
    
    try:
        object_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    
    # Prepare update data (only include non-None values)
    update_data = {k: v for k, v in update.model_dump().items() if v is not None}
    
    # Hash password if it's being updated
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))
    
    # Add update timestamp
    update_data["updated_at"] = datetime.now()

    # Update user in database
    result = await users_collection.update_one(
        {"_id": object_id}, 
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    # Retrieve and return updated user
    updated_user = await users_collection.find_one({"_id": object_id})
    updated_user["id"] = str(updated_user["_id"])
    del updated_user["_id"]
    
    return UserResponse(**updated_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, current_user: UserResponse = Depends(get_current_user)):
    """
    Delete a user account permanently.
    
    This endpoint allows admin users to permanently delete user accounts.
    This action cannot be undone and will remove all user data.
    
    Args:
        user_id: The ObjectId string of the user to delete
        current_user: Automatically injected current authenticated user
        
    Returns:
        dict: Confirmation message of successful deletion
        
    Raises:
        HTTPException 401: User not authenticated
        HTTPException 403: User is not an admin
        HTTPException 404: User with given ID not found
        HTTPException 400: Invalid user ID format
    """
    # Check admin privileges - only admins can delete users
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Admin privileges required to delete user accounts"
        )
    
    try:
        object_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    
    # Perform deletion
    result = await users_collection.delete_one({"_id": object_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

    return {"detail": "User account deleted successfully"}