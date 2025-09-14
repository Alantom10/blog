from datetime import datetime
from fastapi import APIRouter, HTTPException
from typing import Any, Dict, List
from pymongo.errors import DuplicateKeyError
from pydantic import BaseModel, HttpUrl
from starlette import status

from app.utils.serialization import serialize_for_mongo
from app.models.blog import Blog, BlogResponse
from app.database import blogs_collection


router = APIRouter(
    prefix="/blogs",
    tags=["blogs"]
)


# READ ALL
@router.get("", response_model=List[BlogResponse], status_code=status.HTTP_200_OK)
async def get_blogs(skip: int = 0, limit: int = 10):
    blogs = await blogs_collection.find().skip(skip).limit(limit).to_list(length=None)
    for blog in blogs:
        blog["id"] = str(blog["_id"])
        del blog["_id"]
    return blogs


# READ ONE (by slug)
@router.get("/{slug}", response_model=BlogResponse, status_code=status.HTTP_200_OK)
async def get_blog(slug: str):
    blog = await blogs_collection.find_one({"slug": slug})
    if blog:
        blog["id"] = str(blog["_id"])
        del blog["_id"]
        return blog
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')

# CREATE
@router.post("", response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
async def create_blog(blog: Blog):
    blog_dict = serialize_for_mongo(blog)
    if not blog_dict.get('date_published'):
        blog_dict['date_published'] = datetime.now()
    try:
        result = await blogs_collection.insert_one(blog_dict)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A blog with this slug already exists."
        )
    created_blog = await blogs_collection.find_one({"_id": result.inserted_id})
    return BlogResponse(**created_blog, id=str(created_blog["_id"]))


# UPDATE
@router.put("/{slug}", response_model=BlogResponse, status_code=status.HTTP_200_OK)
async def update_blog(slug: str, blog: Blog):
    blog_dict = serialize_for_mongo(blog)
    result = await blogs_collection.update_one({"slug": slug}, {"$set": blog_dict})
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    updated_blog = await blogs_collection.find_one({"slug": slug})
    return BlogResponse(**updated_blog, id=str(updated_blog["_id"]))
    

#DELETE
@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(slug: str):
    result = await blogs_collection.delete_one({"slug": slug})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    return {"detail": "Deleted Successfully"}