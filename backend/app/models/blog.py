from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class Author(BaseModel):
    name: str
    image: Optional[HttpUrl] = None


class Blog(BaseModel):
    id: Optional[str]
    title: str
    slug: str
    author: Author
    cover_image: Optional[HttpUrl] = None
    date_published: datetime
    content: str
    tags: List[str] = []
    is_published: bool = False