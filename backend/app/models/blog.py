from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, HttpUrl


class Author(BaseModel):
    name: str
    image: Optional[str] = None


class Blog(BaseModel):
    title: str
    slug: str
    author: Author
    cover_image: Optional[str] = None
    date_published: Optional[datetime] = None
    content: str
    tags: List[str] = []
    is_published: bool = True


class BlogResponse(Blog):
    id: str

    model_config = ConfigDict(
        from_attributes=True
    )