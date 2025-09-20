from datetime import datetime, timezone
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.database import blogs_collection


# Create test client for FastAPI application
client = TestClient(app)


def cleanup_blog(slug: str):
    """
    Utility function to remove test blogs from database after tests
    
    Args:
        slug: Blog slug to delete from database
    """
    blogs_collection.delete_one({"slug": slug})


def test_read_all():
    """
    Test GET /blogs endpoint - retrieve all blogs
    
    Verifies that the endpoint returns 200 OK status.
    This test assumes there are existing blogs in the database.
    """
    response = client.get("/blogs")
    assert response.status_code == status.HTTP_200_OK


def test_read_one():
    """
    Test GET /blogs/{slug} endpoint - retrieve single blog
    
    Tests retrieval of a specific blog by slug.
    This test assumes a blog with slug "first-blog" exists.
    """
    # First insert a test blog into the database
    test_data = {
        "title": "Test Blog",
        "slug": "test-blog",
        "author": {
            "name": "Author",
            "image": None
        },
        "date_published": datetime.now(timezone.utc).isoformat(),
        "content": "Test content",
        "tags": ["test", "blog"]  
    }

    blogs_collection.insert_one(test_data)

    try:
        response = client.get("/blogs/test-blog")
        assert response.status_code == status.HTTP_200_OK
    
    finally:
        # Clean up test data
        cleanup_blog(test_data["slug"])



def test_read_one_not_found():
    """
    Test GET /blogs/{slug} endpoint - handle non-existent blog
    
    Verifies that requesting a non-existent blog returns 404 with proper error message.
    """
    response = client.get("/blogs/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Item not found",
        "status_code": 404
    }


def test_create_blog():
    """
    Test POST /blogs endpoint - create new blog
    
    Tests the complete blog creation workflow:
    1. Send POST request with blog data
    2. Verify API response matches sent data
    3. Verify blog was actually saved in database
    4. Clean up test data
    """
    # Sample blog data for testing
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
        # Send POST request to create blog
        response = client.post("/blogs", json=request_data)

        # Verify API response
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == request_data["title"]
        assert data["content"] == request_data["content"]
        assert data["slug"] == request_data["slug"]
        assert data["author"] == request_data["author"]

        # Verify blog was saved in database
        db_blog = blogs_collection.find_one({"slug": request_data["slug"]})
        assert db_blog is not None
        assert db_blog["title"] == request_data["title"]
        assert db_blog["content"] == request_data["content"]

    finally:
        # Clean up test data regardless of test outcome
        cleanup_blog(request_data["slug"])


def test_update_blog():
    """
    Test PUT /blogs/{slug} endpoint - update existing blog
    
    Tests the complete blog update workflow:
    1. Create a test blog in database
    2. Send PUT request with updated data
    3. Verify API response contains updated data
    4. Verify database was actually updated
    5. Clean up test data
    """
    # First insert a test blog into the database
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

    # Updated blog data
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
        # Send PUT request to update blog
        response = client.put("/blogs/update-blog", json=update_data)

        # Verify API response
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["content"] == update_data["content"]
        assert data["author"] == update_data["author"]

        # Verify database was updated
        db_blog = blogs_collection.find_one({"slug": "update-blog"})
        assert db_blog["title"] == update_data["title"]
        assert db_blog["content"] == update_data["content"]
        assert db_blog["author"] == update_data["author"]

    finally:
        # Clean up test data
        cleanup_blog(update_data["slug"])


def test_update_blog_not_found():
    """
    Test PUT /blogs/{slug} endpoint - handle non-existent blog update
    
    Verifies that attempting to update a non-existent blog returns 404 error.
    """
    request_data = {
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

    # Try to update non-existent blog
    response = client.put('/blogs/1', json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Item not found",
        "status_code": 404
    }


def test_delete_blog():
    """
    Test DELETE /blogs/{slug} endpoint - delete existing blog
    
    Tests the complete blog deletion workflow:
    1. Create a test blog
    2. Delete the blog via API
    3. Verify deletion was successful (blog no longer accessible)
    """
    # Sample blog data for deletion test
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

    # Create test blog
    create_response = client.post("/blogs", json=blog_data)

    if create_response.status_code != status.HTTP_201_CREATED:
        print(f"Error: {create_response.status_code}")
        print(f"Response: {create_response.json()}")

    assert create_response.status_code == status.HTTP_201_CREATED

    # Delete the blog
    delete_response = client.delete(f"/blogs/{blog_data['slug']}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    # Verify blog was deleted - should return 404
    get_response = client.get(f"/blogs/{blog_data['slug']}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    assert get_response.json() == {
        "detail": "Item not found",
        "status_code": 404
    }


def test_delete_blog_not_found():
    """
    Test DELETE /blogs/{slug} endpoint - handle non-existent blog deletion
    
    Verifies that attempting to delete a non-existent blog returns 404 error.
    """
    response = client.delete('/blogs/1')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Item not found",
        "status_code": 404
    }