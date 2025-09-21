from datetime import datetime, timedelta, timezone
import os
from jose import jwt, JWTError
from fastapi.testclient import TestClient
import pytest
from passlib.context import CryptContext
from app.main import app
from app.utils.auth import create_access_token, hash_password, verify_password


client = TestClient(app)


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# Password Hashing Configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ============================================================================
# PASSWORD HASHING AND VERIFICATION TESTS
# ============================================================================

def test_hashed_password():
    """Test password hashing produces different hash than original password"""
    password = "testpass123"
    hashed = hash_password(password)
    assert password != hashed
    assert verify_password(password, hashed) == True


def test_verify_password_valid():
    """Test password verification with correct password"""
    plain = "secret123"
    hashed = pwd_context.hash(plain)
    assert verify_password(plain, hashed) is True


def test_verify_password_invalid():
    """Test password verification with incorrect password"""
    plain = "secret123"
    hashed = pwd_context.hash(plain)
    assert verify_password("wrongpassword", hashed) is False


def test_hash_password_unique():
    """Test that same password produces different hashes (salt is working)"""
    password = "samepassword"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    assert hash1 != hash2  # Different hashes due to salt
    assert verify_password(password, hash1) is True
    assert verify_password(password, hash2) is True


# ============================================================================
# JWT TOKEN CREATION AND VALIDATION TESTS
# ============================================================================

def test_create_access_token():
    """Test JWT token creation with default expiration"""
    data = {"sub": "user123"}
    access_token = create_access_token(data)

    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == data["sub"]
    assert "exp" in payload
    assert datetime.fromtimestamp(payload["exp"], tz=timezone.utc) > datetime.now(timezone.utc)

    # Test invalid algorithm rejection
    with pytest.raises(JWTError):
        jwt.decode(access_token, SECRET_KEY, algorithms=["HS512"])


def test_create_access_token_custom_expiry():
    """Test JWT token creation with custom expiration time"""
    data = {"sub": "user123"}
    access_token = create_access_token(data, expires_delta=timedelta(minutes=5))
    
    payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    assert "exp" in payload
    assert datetime.fromtimestamp(payload["exp"], tz=timezone.utc) > datetime.now(timezone.utc)


def test_create_access_token_expired():
    """Test that expired tokens are properly rejected"""
    data = {"sub": "user123"}
    expired_token = create_access_token(data, expires_delta=timedelta(seconds=-1))
    
    with pytest.raises(JWTError):
        jwt.decode(expired_token, SECRET_KEY, algorithms=[ALGORITHM])


def test_jwt_token_tampering():
    """Test that tampered JWT tokens are rejected"""
    data = {"sub": "user123"}
    access_token = create_access_token(data)
    
    # Tamper with the signature
    parts = access_token.split(".")
    tampered = parts[0] + "." + parts[1] + ".WRONGSIGNATURE"
    
    with pytest.raises(JWTError):
        jwt.decode(tampered, SECRET_KEY, algorithms=[ALGORITHM])


# ============================================================================
# AUTHENTICATION ENDPOINT TESTS
# ============================================================================

def test_login_success(test_user):
    """Test successful login with valid credentials"""
    login_data = {
        "username": test_user["username"],
        "password": "testpassword123"
    }
    
    response = client.post("/auth/login-json", json=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    # Verify token is valid
    payload = jwt.decode(data["access_token"], SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == str(test_user["_id"])


def test_login_invalid_username():
    """Test login failure with non-existent username"""
    login_data = {
        "username": "nonexistent_user",
        "password": "anypassword"
    }
    
    response = client.post("/auth/login-json", json=login_data)
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_invalid_password(test_user):
    """Test login failure with incorrect password"""
    login_data = {
        "username": test_user["username"],
        "password": "wrongpassword"
    }
    
    response = client.post("/auth/login-json", json=login_data)
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_login_oauth2_form(test_user):
    """Test OAuth2 form-based login endpoint"""
    form_data = {
        "username": test_user["username"],
        "password": "testpassword123"
    }
    
    response = client.post("/auth/login", data=form_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_empty_credentials():
    """Test login failure with empty credentials"""
    login_data = {
        "username": "",
        "password": ""
    }
    
    response = client.post("/auth/login-json", json=login_data)
    assert response.status_code == 401


# ============================================================================
# PROTECTED ENDPOINT TESTS
# ============================================================================

def test_get_me_success(test_user, auth_headers):
    """Test getting current user profile with valid token"""
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == str(test_user["_id"])
    assert data["username"] == test_user["username"]
    assert data["email"] == test_user["email"]
    assert data["full_name"] == test_user["full_name"]


def test_get_me_no_token():
    """Test accessing protected endpoint without token"""
    response = client.get("/auth/me")
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]


def test_get_me_invalid_token():
    """Test accessing protected endpoint with invalid token"""
    headers = {"Authorization": "Bearer invalid_token_here"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]


def test_get_me_expired_token(test_user):
    """Test accessing protected endpoint with expired token"""
    expired_token = create_access_token(
        data={"sub": str(test_user["_id"])}, 
        expires_delta=timedelta(seconds=-1)
    )
    headers = {"Authorization": f"Bearer {expired_token}"}
    
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 401


# ============================================================================
# PYTEST FIXTURES
# ============================================================================

@pytest.fixture
def test_user():
    """Create a test user in the database"""
    from app.database import users_collection
    from bson import ObjectId
    
    # Clean up any existing test user
    users_collection.delete_many({"username": "testuser"})
    
    # Create test user
    test_user_data = {
        "_id": ObjectId(),
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "hashed_password": hash_password("testpassword123"),
        "is_active": True,
        "is_admin": False,
        "created_at": datetime.now(timezone.utc)
    }
    
    users_collection.insert_one(test_user_data)
    yield test_user_data
    
    # Cleanup
    users_collection.delete_one({"_id": test_user_data["_id"]})


@pytest.fixture
def auth_headers(test_user):
    """Generate authorization headers with valid JWT token"""
    token = create_access_token(data={"sub": str(test_user["_id"])})
    return {"Authorization": f"Bearer {token}"}


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

def test_malformed_json_login():
    """Test login endpoint with malformed JSON"""
    response = client.post("/auth/login-json", content="invalid json")
    assert response.status_code == 422  # Validation error


def test_missing_required_fields():
    """Test login with missing required fields"""
    incomplete_data = {"username": "testuser"}  # Missing password
    response = client.post("/auth/login-json", json=incomplete_data)
    assert response.status_code == 422