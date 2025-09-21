from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from typing import Any, Dict, List
from pymongo.errors import DuplicateKeyError
from pydantic import BaseModel, HttpUrl
from starlette import status

from app.utils.serialization import serialize_for_mongo
from app.utils.security import sanitize_dict
from app.models.blog import Blog, BlogResponse
from app.database import blogs_collection

from pymongo.errors import DuplicateKeyError, PyMongoError
import logging


# Create router for blog endpoints
router = APIRouter(
    prefix="/blogs",  # All endpoints will be prefixed with /blogs
    tags=["blogs"]    # Groups endpoints in API docs
)

logger = logging.getLogger(__name__)


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
    blogs = list(blogs_collection.find()
                .sort("date_published", -1)
                .skip(skip)
                .limit(limit))
    
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
    try:
        # Convert Pydantic model to dictionary for MongoDB
        blog_dict = serialize_for_mongo(blog)
        blog_dict = sanitize_dict(blog_dict)
        
        # Set publication date if not provided
        if not blog_dict.get('date_published'):
            blog_dict['date_published'] = datetime.now(timezone.utc)
        
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
    
    except HTTPException:
        # Re-raise HTTP exceptions (these are expected)
        raise
    except PyMongoError as e:
        # Database connection/operation errors
        logger.error(f"Database error during user creation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service temporarily unavailable"
        )
    except Exception as e:
        # Unexpected errors
        logger.error(f"Unexpected error during user creation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user account"
        )


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
    try:
        # Convert Pydantic model to dictionary for MongoDB
        blog_dict = serialize_for_mongo(blog)
        blog_dict = sanitize_dict(blog_dict)
        
        # Update blog in database using slug as filter
        result = blogs_collection.update_one({"slug": slug}, {"$set": blog_dict})
        
        if result.matched_count == 0:
            # No blog found with this slug - return 404 error
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
        
        # Fetch and return updated blog
        updated_blog = blogs_collection.find_one({"slug": slug})
        return BlogResponse(**updated_blog, id=str(updated_blog["_id"]))
    
    except HTTPException:
        # Re-raise HTTP exceptions (these are expected)
        raise
    except PyMongoError as e:
        # Database connection/operation errors
        logger.error(f"Database error during user creation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service temporarily unavailable"
        )
    except Exception as e:
        # Unexpected errors
        logger.error(f"Unexpected error during user creation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user account"
        )

    

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
    try:
        # Delete blog from database using slug as filter
        result = blogs_collection.delete_one({"slug": slug})
        
        if result.deleted_count == 0:
            # No blog found with this slug - return 404 error
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
        
        # Return success message
        return {"detail": "Deleted Successfully"}

    except HTTPException:
        # Re-raise HTTP exceptions (these are expected)
        raise
    except PyMongoError as e:
        # Database connection/operation errors
        logger.error(f"Database error during user creation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service temporarily unavailable"
        )
    except Exception as e:
        # Unexpected errors
        logger.error(f"Unexpected error during user creation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user account"
        )
