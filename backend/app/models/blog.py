from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, HttpUrl


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

    model_config = ConfigDict(
        from_attributes=True
    )