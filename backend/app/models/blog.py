from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class Author(BaseModel):
    name: str
    image: Optional[HttpUrl] = None


class Blog(BaseModel):
    title: str
    slug: str
    author: Author
    cover_image: Optional[HttpUrl] = None
    date_published: datetime
    content: str
    tags: List[str] = []


class BlogResponse(Blog):
    id: str
    is_published: bool = True

    class Config:
        from_attributes = True