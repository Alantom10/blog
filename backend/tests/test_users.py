from datetime import datetime
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.database import users_collection
from app.utils.auth import hash_password
import pytest
from bson import ObjectId

# Create test client for FastAPI application
client = TestClient(app)


def cleanup_user(identifier: str, field: str = "email"):
    """
    Utility function to remove test users from database after tests
    
    Args:
        identifier: User identifier to delete (email, username, or id)
        field: Field type to search by ('email', 'username', or 'id')
    """
    if field == "id":
        users_collection.delete_one({"_id": ObjectId(identifier)})
    else:
        users_collection.delete_one({field: identifier})


async def create_test_user(email: str, username: str, is_admin: bool = False):
    """
    Helper function to create a test user in the database
    
    Args:
        email: User's email address
        username: User's username
        is_admin: Whether user should have admin privileges
        
    Returns:
        str: The created user's ObjectId as string
    """
    user_data = {
        "email": email,
        "username": username,
        "full_name": "Test User",
        "hashed_password": hash_password("testpassword123"),
        "created_at": datetime.now(),
        "is_active": True,
        "is_admin": is_admin
    }
    
    result = await users_collection.insert_one(user_data)
    return str(result.inserted_id)


def get_auth_headers(username: str = "testuser", password: str = "testpassword123"):
    """
    Helper function to get authentication headers for protected endpoints
    
    Args:
        username: Username for login
        password: Password for login
        
    Returns:
        dict: Headers with Bearer token for authentication
    """
    # Login to get access token
    login_response = client.post("/auth/login-json", json={
        "username": username,
        "password": password
    })
    
    if login_response.status_code == 200:
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    return {}


def test_create_user():
    """
    Test POST /users endpoint - create new user
    
    Tests the complete user registration workflow:
    1. Send POST request with user registration data
    2. Verify API response contains correct user data (excluding password)
    3. Verify user was actually saved in database with hashed password
    4. Clean up test data
    """
    # Sample user registration data
    user_data = {
        "email": "test@example.com",
        "username": "testuser123",
        "full_name": "Test User",
        "password": "securepassword123"
    }
    
    try:
        # Send POST request to create user
        response = client.post("/users", json=user_data)
        
        # Verify API response
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert data["full_name"] == user_data["full_name"]
        assert data["is_active"] == True
        assert data["is_admin"] == False
        assert "password" not in data  # Password should not be in response
        assert "hashed_password" not in data  # Hashed password should not be in response
        assert "id" in data  # Should have generated ID
        assert "created_at" in data  # Should have timestamp
        
        # Verify user was saved in database with hashed password
        db_user = users_collection.find_one({"email": user_data["email"]})
        assert db_user is not None
        assert db_user["email"] == user_data["email"]
        assert db_user["username"] == user_data["username"]
        assert "hashed_password" in db_user  # Should have hashed password
        assert db_user["hashed_password"] != user_data["password"]  # Should be hashed, not plain text
        
    finally:
        # Clean up test data
        cleanup_user(user_data["email"])


def test_create_user_duplicate_email():
    """
    Test POST /users endpoint - handle duplicate email
    
    Verifies that attempting to register with an existing email returns 400 error.
    """
    user_data = {
        "email": "duplicate@example.com",
        "username": "user1",
        "full_name": "User One",
        "password": "password123"
    }
    
    try:
        # Create first user
        response1 = client.post("/users", json=user_data)
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Try to create second user with same email
        user_data_duplicate = user_data.copy()
        user_data_duplicate["username"] = "user2"  # Different username
        
        response2 = client.post("/users", json=user_data_duplicate)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert response2.json()["detail"] == "Email already registered"
        
    finally:
        cleanup_user(user_data["email"])


def test_create_user_duplicate_username():
    """
    Test POST /users endpoint - handle duplicate username
    
    Verifies that attempting to register with an existing username returns 400 error.
    """
    user_data = {
        "email": "user1@example.com",
        "username": "duplicateuser",
        "full_name": "User One",
        "password": "password123"
    }
    
    try:
        # Create first user
        response1 = client.post("/users", json=user_data)
        assert response1.status_code == status.HTTP_201_CREATED
        
        # Try to create second user with same username
        user_data_duplicate = user_data.copy()
        user_data_duplicate["email"] = "user2@example.com"  # Different email
        
        response2 = client.post("/users", json=user_data_duplicate)
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert response2.json()["detail"] == "Username already taken"
        
    finally:
        cleanup_user(user_data["email"])


@pytest.mark.asyncio
async def test_get_users_admin():
    """
    Test GET /users endpoint - admin retrieves all users
    
    Tests that admin users can retrieve a list of all users in the system.
    """
    # Create admin user
    admin_id = await create_test_user("admin@example.com", "adminuser", is_admin=True)
    
    # Create regular user
    user_id = await create_test_user("user@example.com", "regularuser", is_admin=False)
    
    try:
        # Get auth headers for admin
        headers = get_auth_headers("adminuser")
        
        # Request all users
        response = client.get("/users", headers=headers)
        
        # Verify response
        assert response.status_code == status.HTTP_200_OK
        users = response.json()
        assert isinstance(users, list)
        assert len(users) >= 2  # At least admin and regular user
        
        # Verify user data structure
        for user in users:
            assert "id" in user
            assert "email" in user
            assert "username" in user
            assert "is_active" in user
            assert "is_admin" in user
            assert "password" not in user
            assert "hashed_password" not in user
            
    finally:
        cleanup_user(admin_id, "id")
        cleanup_user(user_id, "id")


@pytest.mark.asyncio
async def test_get_users_non_admin():
    """
    Test GET /users endpoint - non-admin user forbidden
    
    Tests that regular users cannot access the list of all users.
    """
    # Create regular user
    user_id = await create_test_user("user@example.com", "regularuser", is_admin=False)
    
    try:
        # Get auth headers for regular user
        headers = get_auth_headers("regularuser")
        
        # Try to request all users
        response = client.get("/users", headers=headers)
        
        # Verify forbidden response
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Admin privileges required" in response.json()["detail"]
        
    finally:
        cleanup_user(user_id, "id")


@pytest.mark.asyncio
async def test_get_my_profile():
    """
    Test GET /users/me endpoint - get current user's profile
    
    Tests that authenticated users can retrieve their own profile information.
    """
    # Create test user
    user_id = await create_test_user("me@example.com", "meuser", is_admin=False)
    
    try:
        # Get auth headers
        headers = get_auth_headers("meuser")
        
        # Request own profile
        response = client.get("/users/me", headers=headers)
        
        # Verify response
        assert response.status_code == status.HTTP_200_OK
        user_data = response.json()
        assert user_data["email"] == "me@example.com"
        assert user_data["username"] == "meuser"
        assert user_data["is_admin"] == False
        assert "password" not in user_data
        assert "hashed_password" not in user_data
        
    finally:
        cleanup_user(user_id, "id")


@pytest.mark.asyncio
async def test_get_user_by_id_admin():
    """
    Test GET /users/{user_id} endpoint - admin gets specific user
    
    Tests that admin users can retrieve any user's profile by ID.
    """
    # Create admin user
    admin_id = await create_test_user("admin@example.com", "adminuser", is_admin=True)
    
    # Create target user
    user_id = await create_test_user("target@example.com", "targetuser", is_admin=False)
    
    try:
        # Get auth headers for admin
        headers = get_auth_headers("adminuser")
        
        # Request specific user
        response = client.get(f"/users/{user_id}", headers=headers)
        
        # Verify response
        assert response.status_code == status.HTTP_200_OK
        user_data = response.json()
        assert user_data["email"] == "target@example.com"
        assert user_data["username"] == "targetuser"
        assert user_data["id"] == user_id
        
    finally:
        cleanup_user(admin_id, "id")
        cleanup_user(user_id, "id")


@pytest.mark.asyncio
async def test_get_user_by_id_non_admin():
    """
    Test GET /users/{user_id} endpoint - non-admin user forbidden
    
    Tests that regular users cannot access other users' profiles.
    """
    # Create regular user
    user_id = await create_test_user("user@example.com", "regularuser", is_admin=False)
    
    # Create target user
    target_id = await create_test_user("target@example.com", "targetuser", is_admin=False)
    
    try:
        # Get auth headers for regular user
        headers = get_auth_headers("regularuser")
        
        # Try to request other user's profile
        response = client.get(f"/users/{target_id}", headers=headers)
        
        # Verify forbidden response
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Admin privileges required" in response.json()["detail"]
        
    finally:
        cleanup_user(user_id, "id")
        cleanup_user(target_id, "id")


def test_get_user_not_found():
    """
    Test GET /users/{user_id} endpoint - handle non-existent user
    
    Tests that requesting a non-existent user returns 404.
    """
    # Create admin user for authentication
    admin_data = {
        "email": "admin@example.com",
        "username": "adminuser",
        "full_name": "Admin User",
        "password": "password123"
    }
    
    try:
        # Create admin user
        response = client.post("/users", json=admin_data)
        assert response.status_code == status.HTTP_201_CREATED
        
        # Make user admin (this would normally be done through database directly)
        users_collection.update_one(
            {"email": admin_data["email"]},
            {"$set": {"is_admin": True}}
        )
        
        # Get auth headers
        headers = get_auth_headers("adminuser")
        
        # Try to get non-existent user
        fake_id = str(ObjectId())
        response = client.get(f"/users/{fake_id}", headers=headers)
        
        # Verify not found response
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "User not found"
        
    finally:
        cleanup_user(admin_data["email"])


def test_get_user_invalid_id():
    """
    Test GET /users/{user_id} endpoint - handle invalid user ID format
    
    Tests that providing an invalid ObjectId format returns 400.
    """
    # Create admin user for authentication
    admin_data = {
        "email": "admin@example.com",
        "username": "adminuser", 
        "full_name": "Admin User",
        "password": "password123"
    }
    
    try:
        # Create admin user
        response = client.post("/users", json=admin_data)
        assert response.status_code == status.HTTP_201_CREATED
        
        # Make user admin
        users_collection.update_one(
            {"email": admin_data["email"]},
            {"$set": {"is_admin": True}}
        )
        
        # Get auth headers
        headers = get_auth_headers("adminuser")
        
        # Try to get user with invalid ID
        response = client.get("/users/invalid-id", headers=headers)
        
        # Verify bad request response
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid user ID format" in response.json()["detail"]
        
    finally:
        cleanup_user(admin_data["email"])


@pytest.mark.asyncio
async def test_update_own_profile():
    """
    Test PUT /users/{user_id} endpoint - user updates own profile
    
    Tests that users can update their own profile information.
    """
    # Create test user
    user_id = await create_test_user("update@example.com", "updateuser", is_admin=False)
    
    try:
        # Get auth headers
        headers = get_auth_headers("updateuser")
        
        # Update data
        update_data = {
            "full_name": "Updated Full Name",
            "profile_image": "https://example.com/new-image.jpg"
        }
        
        # Send update request
        response = client.put(f"/users/{user_id}", json=update_data, headers=headers)
        
        # Verify response
        assert response.status_code == status.HTTP_200_OK
        user_data = response.json()
        assert user_data["full_name"] == update_data["full_name"]
        assert user_data["profile_image"] == update_data["profile_image"]
        assert "updated_at" in user_data
        
        # Verify database was updated
        db_user = users_collection.find_one({"_id": ObjectId(user_id)})
        assert db_user["full_name"] == update_data["full_name"]
        assert db_user["profile_image"] == update_data["profile_image"]
        
    finally:
        cleanup_user(user_id, "id")


@pytest.mark.asyncio
async def test_update_other_user_forbidden():
    """
    Test PUT /users/{user_id} endpoint - regular user cannot update others
    
    Tests that regular users cannot update other users' profiles.
    """
    # Create regular user
    user_id = await create_test_user("user@example.com", "regularuser", is_admin=False)
    
    # Create target user
    target_id = await create_test_user("target@example.com", "targetuser", is_admin=False)
    
    try:
        # Get auth headers for regular user
        headers = get_auth_headers("regularuser")
        
        # Try to update other user
        update_data = {"full_name": "Hacked Name"}
        response = client.put(f"/users/{target_id}", json=update_data, headers=headers)
        
        # Verify forbidden response
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "You can only update your own profile" in response.json()["detail"]
        
    finally:
        cleanup_user(user_id, "id")
        cleanup_user(target_id, "id")


@pytest.mark.asyncio
async def test_delete_user_admin():
    """
    Test DELETE /users/{user_id} endpoint - admin deletes user
    
    Tests that admin users can delete other user accounts.
    """
    # Create admin user
    admin_id = await create_test_user("admin@example.com", "adminuser", is_admin=True)
    
    # Create target user to delete
    target_id = await create_test_user("delete@example.com", "deleteuser", is_admin=False)
    
    try:
        # Get auth headers for admin
        headers = get_auth_headers("adminuser")
        
        # Delete user
        response = client.delete(f"/users/{target_id}", headers=headers)
        
        # Verify successful deletion
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify user was actually deleted from database
        db_user = users_collection.find_one({"_id": ObjectId(target_id)})
        assert db_user is None
        
    finally:
        cleanup_user(admin_id, "id")
        # target_id should already be deleted


@pytest.mark.asyncio
async def test_delete_user_non_admin():
    """
    Test DELETE /users/{user_id} endpoint - non-admin user forbidden
    
    Tests that regular users cannot delete user accounts.
    """
    # Create regular user
    user_id = await create_test_user("user@example.com", "regularuser", is_admin=False)
    
    # Create target user
    target_id = await create_test_user("target@example.com", "targetuser", is_admin=False)
    
    try:
        # Get auth headers for regular user
        headers = get_auth_headers("regularuser")
        
        # Try to delete user
        response = client.delete(f"/users/{target_id}", headers=headers)
        
        # Verify forbidden response
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "Admin privileges required" in response.json()["detail"]
        
        # Verify user was not deleted
        db_user = users_collection.find_one({"_id": ObjectId(target_id)})
        assert db_user is not None
        
    finally:
        cleanup_user(user_id, "id")
        cleanup_user(target_id, "id")


def test_delete_user_not_found():
    """
    Test DELETE /users/{user_id} endpoint - handle non-existent user
    
    Tests that attempting to delete a non-existent user returns 404.
    """
    # Create admin user for authentication
    admin_data = {
        "email": "admin@example.com",
        "username": "adminuser",
        "full_name": "Admin User", 
        "password": "password123"
    }
    
    try:
        # Create admin user
        response = client.post("/users", json=admin_data)
        assert response.status_code == status.HTTP_201_CREATED
        
        # Make user admin
        users_collection.update_one(
            {"email": admin_data["email"]},
            {"$set": {"is_admin": True}}
        )
        
        # Get auth headers
        headers = get_auth_headers("adminuser")
        
        # Try to delete non-existent user
        fake_id = str(ObjectId())
        response = client.delete(f"/users/{fake_id}", headers=headers)
        
        # Verify not found response
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "User not found"
        
    finally:
        cleanup_user(admin_data["email"])