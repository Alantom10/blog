from datetime import datetime, timezone
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.database import blogs_collection


client = TestClient(app)


def cleanup_blog(slug: str):
    blogs_collection.delete_one({"slug": slug})


def test_read_all():
    response = client.get("/blogs")
    assert response.status_code == status.HTTP_200_OK


def test_read_one():
    response = client.get("/blogs/first-blog")
    assert response.status_code == status.HTTP_200_OK


def test_read_one_not_found():
    response = client.get("/blogs/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Item not found'}


def test_create_blog():
    request_data = {
        "title": "New Blog!",
        "slug": "new-blog",
        "author": {
            "name": "Test Author",
            "image": None
        },
        "date_published": datetime.now(timezone.utc).isoformat(),
        "content": "This is a test blog post",
        "tags": ["test", "blog"]  
    }

    try:
        # Send POST request
        response = client.post("/blogs", json=request_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == request_data["title"]
        assert data["content"] == request_data["content"]
        assert data["slug"] == request_data["slug"]
        assert data["author"] == request_data["author"]

        # Verify in DB
        db_blog = blogs_collection.find_one({"slug": request_data["slug"]})
        assert db_blog is not None
        assert db_blog["title"] == request_data["title"]
        assert db_blog["content"] == request_data["content"]

    finally:
        cleanup_blog(request_data["slug"])


def test_update_blog():
    # First insert a test blog into the DB
    blogs_collection.insert_one({
        "title": "Old Blog",
        "slug": "update-blog",
        "author": {
            "name": "Old Author",
            "image": None
        },
        "date_published": datetime.now(timezone.utc).isoformat(),
        "content": "Old content",
        "tags": ["test", "blog"]  
    })

    update_data = {
        "title": "Updated Blog",
        "content": "This is updated content",
        "slug": "update-blog",
        "author": {
            "name": "Updated Author",
            "image": None
        },
        "date_published": datetime.now(timezone.utc).isoformat(),
        "tags": ["test", "blog"]
    }

    try:
        # Send PUT request
        response = client.put("/blogs/update-blog", json=update_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["content"] == update_data["content"]
        assert data["author"] == update_data["author"]

        # Verify in DB
        db_blog = blogs_collection.find_one({"slug": "update-blog"})
        assert db_blog["title"] == update_data["title"]
        assert db_blog["content"] == update_data["content"]
        assert db_blog["author"] == update_data["author"]

    finally:
         cleanup_blog(update_data["slug"])


def test_update_blog_not_found():
    request_data={
        "title": "Updated Blog",
        "content": "This is updated content",
        "slug": "update-blog",
        "author": {
            "name": "Updated Author",
            "image": None
        },
        "date_published": datetime.now(timezone.utc).isoformat(),
        "tags": ["test", "blog"]
    }

    response = client.put('/blogs/1', json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Item not found'}


def test_delete_blog():
    # Create test blog
    blog_data = {
        "title": "Delete Me",
        "content": "This blog will be deleted.",
        "slug": "delete-me",
        "author": {
            "name": "Test Author",
            "image": None
        },
        "date_published": datetime.now(timezone.utc).isoformat(),
        "tags": ["test", "blog"]
    }

    create_response = client.post("/blogs", json=blog_data)
    assert create_response.status_code == status.HTTP_201_CREATED

    # Delete the blog
    delete_response = client.delete(f"/blogs/{blog_data['slug']}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    # Try fetching the blog
    get_response = client.get(f"/blogs/{blog_data['slug']}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_response.json() == {'detail': 'Item not found'}


def test_delete_blog_not_found():
    response = client.delete('/blogs/1')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Item not found'}