from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator
import re


class Author(BaseModel):
    """
    Model for blog post author information
    
    Attributes:
        name: Full name of the author (required)
        image: Optional URL or path to author's profile image
    """
    name: str                           # Author's full name (required field)
    image: Optional[str] = None         # Profile image URL/path (optional)


class Blog(BaseModel):
    """
    Main blog post model for creating and updating blogs
    
    This model represents a complete blog post with all necessary fields
    for content management, SEO, and publishing workflow.
    
    Attributes:
        title: Blog post title
        slug: URL-friendly identifier (must be unique)
        author: Author information (nested Author model)
        cover_image: Optional featured image URL
        date_published: Publication timestamp (auto-set if not provided)
        content: Main blog content (HTML or Markdown)
        tags: List of category/topic tags for organization
        is_published: Publication status (draft vs published)
    """
    title: str = Field(..., min_length=1, max_length=200)                  # Blog post title (required)
    slug: str = Field(..., min_length=1, max_length=100)                   # URL-friendly unique identifier (required)
    author_id: str = Field(..., description="User ID of the blog author")  # Author ID to connect blog to author
    author: Author                                                         # Author information (nested model)
    cover_image: Optional[str] = None                                      # Featured image URL/path (optional)
    date_published: Optional[datetime] = None                              # Publication date (auto-set in API if None)
    content: str = Field(..., min_length=1)                                # Main blog content (required)
    tags: List[str] = []                                                   # Category/topic tags (default: empty list)
    is_published: bool = True                                              # Publication status (default: published)

    @field_validator('title')
    def validate_title(cls, v):
        # Remove extra whitespace
        v = ' '.join(v.split())
        if not v:
            raise ValueError('Title cannot be empty')
        return v

    @field_validator('slug')
    def validate_slug(cls, v):
        # Ensure slug is URL-safe
        if not re.match(r'^[a-z0-9-]+$', v):
            raise ValueError('Slug can only contain lowercase letters, numbers, and hyphens')
        if v.startswith('-') or v.endswith('-'):
            raise ValueError('Slug cannot start or end with a hyphen')
        if '--' in v:
            raise ValueError('Slug cannot contain consecutive hyphens')
        return v
    
    @field_validator('author_id')
    def validate_author_id(cls, v):
        if len(v) != 24:  # MongoDB ObjectId length
            raise ValueError('Invalid author ID format')
        return v

    @field_validator('content')
    def validate_content(cls, v):
        # Basic XSS prevention - remove/escape dangerous tags
        dangerous_tags = ['<script', '<iframe', '<object', '<embed', '<form']
        for tag in dangerous_tags:
            if tag.lower() in v.lower():
                raise ValueError('Content contains potentially dangerous HTML tags')
        return v.strip()

    @field_validator('tags')
    def validate_tags(cls, v):
        # Validate each tag
        validated_tags = []
        for tag in v:
            tag = tag.strip().lower()
            if len(tag) < 1 or len(tag) > 20:
                raise ValueError('Each tag must be 1-20 characters long')
            if not re.match(r'^[a-z0-9-]+$', tag):
                raise ValueError('Tags can only contain lowercase letters, numbers, and hyphens')
            validated_tags.append(tag)
        return list(set(validated_tags))  # Remove duplicates
    

class BlogResponse(Blog):
    """
    Response model for blog API endpoints
    
    Extends the base Blog model with an ID field for API responses.
    Used when returning blog data from GET, POST, and PUT endpoints.
    
    Attributes:
        id: String representation of MongoDB ObjectId
        (inherits all fields from Blog model)
    """
    id: str                            # MongoDB ObjectId converted to string

    # Pydantic configuration
    model_config = ConfigDict(
        from_attributes=True           # Allows creation from ORM/database objects
    )