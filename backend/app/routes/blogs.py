from datetime import datetime
from fastapi import APIRouter, HTTPException
from typing import Any, Dict, List
from pymongo.errors import DuplicateKeyError
from pydantic import BaseModel, HttpUrl
from starlette import status

from app.utils.serialization import serialize_for_mongo
from app.models.blog import Blog, BlogResponse
from app.database import blogs_collection

# Create router for blog endpoints
router = APIRouter(
    prefix="/blogs",  # All endpoints will be prefixed with /blogs
    tags=["blogs"]    # Groups endpoints in API docs
)


# READ ALL BLOGS
@router.get("", response_model=List[BlogResponse], status_code=status.HTTP_200_OK)
def get_blogs(skip: int = 0, limit: int = 10):
    """
    Get all blogs with pagination support
    
    Args:
        skip: Number of blogs to skip (for pagination)
        limit: Maximum number of blogs to return (default: 10)
        
    Returns:
        List[BlogResponse]: List of all blog posts
    """
    # Fetch blogs from database with pagination
    blogs = list(blogs_collection.find().skip(skip).limit(limit))
    
    # Convert MongoDB _id to string id for each blog
    for blog in blogs:
        blog["id"] = str(blog["_id"])  # Convert ObjectId to string
        del blog["_id"]                # Remove original _id field
    
    return blogs


# READ SINGLE BLOG (by slug)
@router.get("/{slug}", response_model=BlogResponse, status_code=status.HTTP_200_OK)
def get_blog(slug: str):
    """
    Get a single blog by its slug
    
    Args:
        slug: Unique slug identifier for the blog
        
    Returns:
        BlogResponse: Single blog post data
        
    Raises:
        HTTPException: 404 if blog with given slug is not found
    """
    # Find blog by slug in database
    blog = blogs_collection.find_one({"slug": slug})
    
    if blog:
        # Convert MongoDB _id to string id
        blog["id"] = str(blog["_id"])
        del blog["_id"]
        return blog
    
    # Blog not found - return 404 error
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')


# CREATE NEW BLOG
@router.post("", response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
def create_blog(blog: Blog):
    """
    Create a new blog post
    
    Args:
        blog: Blog data from request body
        
    Returns:
        BlogResponse: Created blog with generated ID
        
    Raises:
        HTTPException: 400 if blog with same slug already exists
    """
    # Convert Pydantic model to dictionary for MongoDB
    blog_dict = serialize_for_mongo(blog)
    
    # Set publication date if not provided
    if not blog_dict.get('date_published'):
        blog_dict['date_published'] = datetime.now()
    
    try:
        # Insert new blog into database
        result = blogs_collection.insert_one(blog_dict)
    except DuplicateKeyError:
        # Slug already exists - return 400 error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A blog with this slug already exists."
        )
    
    # Fetch the created blog to return with proper ID
    created_blog = blogs_collection.find_one({"_id": result.inserted_id})
    return BlogResponse(**created_blog, id=str(created_blog["_id"]))


# UPDATE EXISTING BLOG
@router.put("/{slug}", response_model=BlogResponse, status_code=status.HTTP_200_OK)
def update_blog(slug: str, blog: Blog):
    """
    Update an existing blog by slug
    
    Args:
        slug: Unique slug identifier for the blog to update
        blog: Updated blog data from request body
        
    Returns:
        BlogResponse: Updated blog data
        
    Raises:
        HTTPException: 404 if blog with given slug is not found
    """
    # Convert Pydantic model to dictionary for MongoDB
    blog_dict = serialize_for_mongo(blog)
    
    # Update blog in database using slug as filter
    result = blogs_collection.update_one({"slug": slug}, {"$set": blog_dict})
    
    if result.matched_count == 0:
        # No blog found with this slug - return 404 error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    
    # Fetch and return updated blog
    updated_blog = blogs_collection.find_one({"slug": slug})
    return BlogResponse(**updated_blog, id=str(updated_blog["_id"]))
    

# DELETE BLOG
@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(slug: str):
    """
    Delete a blog by slug
    
    Args:
        slug: Unique slug identifier for the blog to delete
        
    Returns:
        dict: Success message confirming deletion
        
    Raises:
        HTTPException: 404 if blog with given slug is not found
    """
    # Delete blog from database using slug as filter
    result = blogs_collection.delete_one({"slug": slug})
    
    if result.deleted_count == 0:
        # No blog found with this slug - return 404 error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
    
    # Return success message
    return {"detail": "Deleted Successfully"}