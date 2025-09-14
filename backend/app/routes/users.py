from datetime import datetime
from typing import Any, Dict, List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, HttpUrl
from starlette import status

from app.models.user import User, UserCreate, UserResponse, UserUpdate
from app.utils.serialization import serialize_for_mongo
from app.utils.auth import get_current_user, hash_password
from app.database import users_collection


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


if users_collection is None:
    raise RuntimeError("users_collection is None - database connection failed")


# CREATE USER
@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate):
    # Check duplicates
    if await users_collection.find_one({"email": user_create.email}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    if await users_collection.find_one({"username": user_create.username}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    # Hash password
    hashed_pw = hash_password(user_create.password)

    # Serialize for MongoDB
    user_dict = serialize_for_mongo(user_create)

    # Remove password and add additional fields
    user_dict.pop("password", None)  # Remove plain password
    user_dict.update({
        "hashed_password": hashed_pw,
        "created_at": datetime.now(),
        "is_active": True,
        "is_admin": False
    })

    # Insert
    result = await users_collection.insert_one(user_dict)

    # Prepare response data (only fields that belong to UserResponse)
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


# READ ALL
@router.get("", response_model=List[UserResponse])
async def get_users(current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    users = await users_collection.users.find().to_list(100)
    for user in users:
        user["id"] = str(user["_id"])
    return [UserResponse(**u) for u in users]


# READ CURRENT
@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user=Depends(get_current_user)):
    return current_user


# READ ONE (by ID)
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    user = await users_collection.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user["id"] = str(user["_id"])
    return UserResponse(**user)


# UPDATE
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, update: UserUpdate, current_user=Depends(get_current_user)):
    if not current_user.is_admin and str(current_user.id) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    update_data = {k: v for k, v in update.dict().items() if v is not None}
    if "password" in update_data:
        update_data["password_hash"] = hash_password(update_data.pop("password"))

    result = await users_collection.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user = await users_collection.users.find_one({"_id": ObjectId(user_id)})
    user["id"] = str(user["_id"])
    return UserResponse(**user)


# DELETE
@router.delete("/{user_id}")
async def delete_user(user_id: str, current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    result = await users_collection.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"detail": "User deleted"}