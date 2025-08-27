from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, HTTPException
from typing import List
from app.models.blog import Author, Blog, BlogResponse
from app.database import blogs_collection
from starlette import status


router = APIRouter(
    prefix="/blogs",
    tags=["blogs"]
)



# CREATE
@router.post("", response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
def create_blog(blog: Blog):
    blog_dict = blog.model_dump()
    result = blogs_collection.insert_one(blog_dict)
    return BlogResponse(**blog_dict, id=str(result.inserted_id))


# READ ALL
@router.get("", response_model=List[BlogResponse], status_code=status.HTTP_200_OK)
def get_blogs():
    blogs = list(blogs_collection.find())
    return blogs


# READ ONE (by slug)
@router.get("/{slug}", response_model=BlogResponse, status_code=status.HTTP_200_OK)
def get_blog(slug: str):
    blog = blogs_collection.find_one({"slug": slug})
    if blog:
        return blog
    raise HTTPException(status_code=404, detail='Item not found')


# UPDATE
@router.put("/{slug}", response_model=BlogResponse, status_code=status.HTTP_200_OK)
def update_blog(slug: str, blog: Blog):
    result = blogs_collection.update_one({"slug": slug}, {"$set": blog.model_dump()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail='Item not found')
    updated_result = blogs_collection.find_one({"slug": slug})
    return BlogResponse(**updated_result, id=str(updated_result["_id"]))
    

#DELETE
@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(slug: str):
    result = blogs_collection.delete_one({"slug": slug})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail='Item not found')
    return {"detail": "Deleted Successfully"}