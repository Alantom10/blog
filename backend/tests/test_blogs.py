from datetime import datetime, timezone
import uuid
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.database import blogs_collection
from tests.test_users import create_test_user_sync, create_unique_email, get_auth_headers


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
    # Create a test user first
    user_email = create_unique_email()
    user_username = f"bloguser{uuid.uuid4().hex[:8]}"
    user_id = create_test_user_sync(user_email, user_username, False)

    # First insert a test blog into the database
    test_data = {
        "title": "Test Blog",
        "slug": "test-blog",
        "author_id": user_id,
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
    # Create a test user first
    user_email = create_unique_email()
    user_username = f"bloguser{uuid.uuid4().hex[:8]}"
    user_id = create_test_user_sync(user_email, user_username, False)
    
    # Sample blog data for testing
    request_data = {
        "title": "New Blog!",
        "slug": "new-blog",
        "author_id": user_id,
        "author": {
            "name": "Test Author",
            "image": None
        },
        "date_published": datetime.now(timezone.utc).isoformat(),
        "content": "This is a test blog post",
        "tags": ["test", "blog"]  
    }

    try:
        # Get auth headers
        headers = get_auth_headers(user_username)
        response = client.post("/blogs", json=request_data, headers=headers)

        # Verify API response
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == request_data["title"]
        assert data["content"] == request_data["content"]
        assert data["slug"] == request_data["slug"]

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
    # Create a test user first
    user_email = create_unique_email()
    user_username = f"bloguser{uuid.uuid4().hex[:8]}"
    user_id = create_test_user_sync(user_email, user_username, False)

    # First insert a test blog into the database
    blogs_collection.insert_one({
        "title": "Old Blog",
        "slug": "update-blog",
        "author_id": user_id,
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
        "slug": "update-blog",
        "author_id": user_id,
        "author": {
            "name": "Updated Author",
            "image": None
        },
        "date_published": datetime.now(timezone.utc).isoformat(),
        "content": "This is updated content",
        "tags": ["test", "blog"]
    }

    try:
        # Get auth headers
        headers = get_auth_headers(user_username)
        response = client.put("/blogs/update-blog", json=update_data, headers=headers)

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
    # Create a test user first
    user_email = create_unique_email()
    user_username = f"bloguser{uuid.uuid4().hex[:8]}"
    user_id = create_test_user_sync(user_email, user_username, False)

    request_data = {
        "title": "Updated Blog",
        "content": "This is updated content",
        "slug": "update-blog",
        "author_id": user_id,
        "author": {
            "name": "Updated Author",
            "image": None
        },
        "date_published": datetime.now(timezone.utc).isoformat(),
        "tags": ["test", "blog"]
    }

    # Get auth headers
    headers = get_auth_headers(user_username)
    # Try to update non-existent blog
    response = client.put('/blogs/1', json=request_data, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Blog not found",
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
    # Create a test user first
    user_email = create_unique_email()
    user_username = f"bloguser{uuid.uuid4().hex[:8]}"
    user_id = create_test_user_sync(user_email, user_username, False)

    # Sample blog data for deletion test
    blog_data = {
        "title": "Delete Me",
        "content": "This blog will be deleted.",
        "slug": "delete-me",
        "author_id": user_id,
        "author": {
            "name": "Test Author",
            "image": None
        },
        "date_published": datetime.now(timezone.utc).isoformat(),
        "tags": ["test", "blog"]
    }

    # Get auth headers
    headers = get_auth_headers(user_username)
    # Create test blog
    create_response = client.post("/blogs", json=blog_data, headers=headers)

    if create_response.status_code != status.HTTP_201_CREATED:
        print(f"Error: {create_response.status_code}")
        print(f"Response: {create_response.json()}")

    assert create_response.status_code == status.HTTP_201_CREATED

    # Delete the blog
    delete_response = client.delete(f"/blogs/{blog_data['slug']}", headers=headers)
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
    # Create a test user first
    user_email = create_unique_email()
    user_username = f"bloguser{uuid.uuid4().hex[:8]}"
    user_id = create_test_user_sync(user_email, user_username, False)

    # Get auth headers
    headers = get_auth_headers(user_username)
    response = client.delete('/blogs/1', headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Blog not found",
        "status_code": 404
    }