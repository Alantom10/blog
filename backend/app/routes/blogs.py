from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, HTTPException
from typing import List
from models.blog import Blog, BlogResponse
from starlette import status


router = APIRouter(
    prefix="/blogs",
    tags=["blogs"]
)


mock_posts: List[BlogResponse] = []


# CREATE
@router.post("", response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
def create_blog(blog: Blog):
    new_blog = BlogResponse(
        id=str(uuid4()),  # generate unique id
        title=blog.title,
        slug=blog.slug,
        author=blog.author,
        cover_image=blog.cover_image,
        date_published=blog.date_published or datetime(),
        content=blog.content,
        tags=blog.tags,
        is_published=True
    )
    mock_posts.append(new_blog)
    return new_blog


# READ ALL
@router.get("", response_model=List[BlogResponse], status_code=status.HTTP_200_OK)
def get_blogs():
    return mock_posts


# READ ONE (by slug)
@router.get("/{slug}", response_model=BlogResponse, status_code=status.HTTP_200_OK)
def get_blog(slug: str):
    for post in mock_posts:
        if post.slug == slug:
            return post
    raise HTTPException(status_code=404, detail='Item not found')


# UPDATE
@router.put("/{slug}", response_model=BlogResponse, status_code=status.HTTP_204_NO_CONTENT)
def update_blog(slug: str, blog: Blog):
    for i in range(len(mock_posts)):
        if mock_posts[i].slug == slug:
            updated_blog = BlogResponse(
                id=mock_posts[i].id,  # keep same id
                title=blog.title,
                slug=blog.slug,
                author=blog.author,
                cover_image=blog.cover_image,
                date_published=blog.date_published or datetime(),
                content=blog.content,
                tags=blog.tags,
                is_published=mock_posts[i].is_published  # keep original publish state
            )
            mock_posts[i] = updated_blog
            return updated_blog
    raise HTTPException(status_code=404, detail='Item not found')
    

#DELETE
@router.delete("/{slug}")
def delte_blog(slug: str):
    for i in range(len(mock_posts)):
        if mock_posts[i].slug == slug:
            mock_posts.pop(i)
            return
    raise HTTPException(status_code=404, detail='Item not found')