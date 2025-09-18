import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.utils.auth import hash_password
from app.database import users_collection
from bson import ObjectId
from pymongo import MongoClient
import uuid


# Create test client
client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_test_data():
    """Automatically clean up test data before and after each test"""
    # Clean up before test
    users_collection.delete_many({"email": {"$regex": r"test|example\.com"}})
    yield
    # Clean up after test
    users_collection.delete_many({"email": {"$regex": r"test|example\.com"}})


def create_unique_email():
    """Generate unique email for each test"""
    return f"test-{uuid.uuid4().hex[:8]}@example.com"


def cleanup_user(identifier: str, field: str = "email"):
    """Clean up test users using synchronous client"""
    if field == "id":
        users_collection.delete_one({"_id": ObjectId(identifier)})
    else:
        users_collection.delete_one({field: identifier})


def create_test_user_sync(email: str, username: str, is_admin: bool = False):
    """Create test user using synchronous client"""
    user_data = {
        "email": email,
        "username": username,
        "full_name": "Test User",
        "hashed_password": hash_password("testpassword123"),
        "created_at": datetime.now(),
        "is_active": True,
        "is_admin": is_admin
    }
    
    result = users_collection.insert_one(user_data)
    return str(result.inserted_id)


def get_auth_headers(username: str = "testuser", password: str = "testpassword123"):
    """Get authentication headers"""
    login_response = client.post("/auth/login", data={
        "username": username,
        "password": password
    })
    
    if login_response.status_code == 200:
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    return {}


def test_create_user():
    """Test POST /users endpoint - create new user"""
    email = create_unique_email()
    username = f"testuser{uuid.uuid4().hex[:8]}"
    
    user_data = {
        "email": email,
        "username": username,
        "full_name": "Test User",
        "password": "securepassword123"
    }
    
    response = client.post("/users", json=user_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert data["full_name"] == user_data["full_name"]
    assert data["is_active"] == True
    assert data["is_admin"] == False
    assert "password" not in data
    assert "hashed_password" not in data
    assert "id" in data
    assert "created_at" in data


def test_create_user_duplicate_email():
    """Test duplicate email handling"""
    email = create_unique_email()
    user_data = {
        "email": email,
        "username": "user1",
        "full_name": "User One",
        "password": "password123"
    }
    
    # Create first user
    response1 = client.post("/users", json=user_data)
    assert response1.status_code == status.HTTP_201_CREATED
    
    # Try duplicate email with different username
    user_data_dup = user_data.copy()
    user_data_dup["username"] = "user2"
    response2 = client.post("/users", json=user_data_dup)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email already registered" in response2.json()["detail"]


def test_create_user_duplicate_username():
    """Test duplicate username handling"""
    username = f"duplicateuser{uuid.uuid4().hex[:8]}"
    user_data = {
        "email": create_unique_email(),
        "username": username,
        "full_name": "User One",
        "password": "password123"
    }
    
    # Create first user
    response1 = client.post("/users", json=user_data)
    assert response1.status_code == status.HTTP_201_CREATED
    
    # Try duplicate username with different email
    user_data_dup = user_data.copy()
    user_data_dup["email"] = create_unique_email()
    response2 = client.post("/users", json=user_data_dup)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert "Username already taken" in response2.json()["detail"]


def test_get_users_admin():
    """Test GET /users - admin access"""
    admin_email = create_unique_email()
    admin_username = f"admin{uuid.uuid4().hex[:8]}"
    user_email = create_unique_email()
    user_username = f"user{uuid.uuid4().hex[:8]}"
    
    # Create admin and regular user
    admin_id = create_test_user_sync(admin_email, admin_username, True)
    user_id = create_test_user_sync(user_email, user_username, False)
    
    headers = get_auth_headers(admin_username)
    response = client.get("/users", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    users = response.json()
    assert isinstance(users, list)
    
    for user in users:
        assert "id" in user
        assert "email" in user
        assert "password" not in user
        assert "hashed_password" not in user


def test_get_users_non_admin():
    """Test GET /users - non-admin forbidden"""
    user_email = create_unique_email()
    user_username = f"user{uuid.uuid4().hex[:8]}"
    user_id = create_test_user_sync(user_email, user_username, False)
    
    headers = get_auth_headers(user_username)
    response = client.get("/users", headers=headers)
    
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Admin privileges required" in response.json()["detail"]


def test_get_my_profile():
    """Test GET /users/me"""
    user_email = create_unique_email()
    user_username = f"meuser{uuid.uuid4().hex[:8]}"
    user_id = create_test_user_sync(user_email, user_username, False)
    
    headers = get_auth_headers(user_username)
    response = client.get("/users/me", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    user_data = response.json()
    assert user_data["email"] == user_email
    assert user_data["username"] == user_username
    assert "password" not in user_data


def test_get_user_by_id_admin():
    """Test GET /users/{id} - admin access"""
    admin_email = create_unique_email()
    admin_username = f"admin{uuid.uuid4().hex[:8]}"
    target_email = create_unique_email()
    target_username = f"target{uuid.uuid4().hex[:8]}"
    
    admin_id = create_test_user_sync(admin_email, admin_username, True)
    target_id = create_test_user_sync(target_email, target_username, False)
    
    headers = get_auth_headers(admin_username)
    response = client.get(f"/users/{target_id}", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    user_data = response.json()
    assert user_data["email"] == target_email
    assert user_data["id"] == target_id


def test_update_own_profile():
    """Test PUT /users/{id} - update own profile"""
    user_email = create_unique_email()
    user_username = f"update{uuid.uuid4().hex[:8]}"
    user_id = create_test_user_sync(user_email, user_username, False)
    
    headers = get_auth_headers(user_username)
    update_data = {"full_name": "Updated Name"}
    
    response = client.put(f"/users/{user_id}", json=update_data, headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    user_data = response.json()
    assert user_data["full_name"] == "Updated Name"


def test_delete_user_admin():
    """Test DELETE /users/{id} - admin deletion"""
    admin_email = create_unique_email()
    admin_username = f"admin{uuid.uuid4().hex[:8]}"
    target_email = create_unique_email()
    target_username = f"delete{uuid.uuid4().hex[:8]}"
    
    admin_id = create_test_user_sync(admin_email, admin_username, True)
    target_id = create_test_user_sync(target_email, target_username, False)
    
    headers = get_auth_headers(admin_username)
    response = client.delete(f"/users/{target_id}", headers=headers)
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify deletion
    db_user = users_collection.find_one({"_id": ObjectId(target_id)})
    assert db_user is None


def test_unauthorized_access():
    """Test endpoints require authentication"""
    response = client.get("/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED