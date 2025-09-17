from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, HttpUrl


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
    title: str                          # Blog post title (required)
    slug: str                           # URL-friendly unique identifier (required)
    author: Author                      # Author information (nested model)
    cover_image: Optional[str] = None   # Featured image URL/path (optional)
    date_published: Optional[datetime] = None  # Publication date (auto-set in API if None)
    content: str                        # Main blog content (required)
    tags: List[str] = []               # Category/topic tags (default: empty list)
    is_published: bool = True          # Publication status (default: published)


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