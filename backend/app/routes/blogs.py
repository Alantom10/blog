from fastapi import APIRouter, HTTPException
from typing import List
from models.blog import Blog
from starlette import status


router = APIRouter()


mock_posts = []


# CREATE
@router.post("/blogs", status_code=status.HTTP_201_CREATED)
def create_blog(blog: Blog):
    new_blog = Blog()
    mock_posts.append(new_blog)


# READ ALL
@router.get("/blogs", status_code=status.HTTP_200_OK)
def get_blogs():
    return mock_posts


# READ ONE (by slug)
@router.get("/blogs/{slug}", status_code=status.HTTP_200_OK)
def get_blog(slug: str):
    for post in mock_posts:
        if post.slug == slug:
            return post
    raise HTTPException(status_code=404, detail='Item not found')


# UPDATE
@router.put("/blogs/{slug}", status_code=status.HTTP_204_NO_CONTENT)
def update_blog(slug: str, blog: Blog):
    blog_changed = False
    for i in range(len(mock_posts)):
        if mock_posts[i].slug == slug:
            mock_posts[i] = blog
            blog_changed = True
    if not blog_changed:
        raise HTTPException(status_code=404, detail='Item not found')
    

#DELETE
@router.delete("/blogs/{slug}")
def delte_blog(slug: str):
    blog_changed = False
    for i in range(len(mock_posts)):
        if mock_posts[i].slug == slug:
            mock_posts.pop(i)
            blog_changed = True
            break
    if not blog_changed:
        raise HTTPException(status_code=404, detail='Item not found')