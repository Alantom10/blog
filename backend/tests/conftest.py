# conftest.py
import os
import pytest
import uuid
from datetime import datetime, timezone
from app.database import users_collection, blogs_collection

# ---------------------------------------------------------
# 1️⃣ Set testing environment variable
# ---------------------------------------------------------
os.environ["TESTING"] = "1"

# ---------------------------------------------------------
# 2️⃣ Auto-cleanup fixture
#    Cleans test users and blogs before and after each test
# ---------------------------------------------------------
@pytest.fixture(autouse=True)
def cleanup_test_data():
    """Automatically clean up test data before and after each test"""
    # Clean up before test
    users_collection.delete_many({"email": {"$regex": r"test|example\.com"}})
    blogs_collection.delete_many({"author_id": {"$exists": True}})
    
    yield  # Run the test
    
    # Clean up after test
    users_collection.delete_many({"email": {"$regex": r"test|example\.com"}})
    blogs_collection.delete_many({"author_id": {"$exists": True}})

# ---------------------------------------------------------
# 3️⃣ Helper functions for tests
# ---------------------------------------------------------
def create_unique_email():
    """Generate a unique email for testing"""
    return f"test-{uuid.uuid4().hex[:8]}@example.com"

def cleanup_user(identifier: str, field: str = "email"):
    """Remove a test user from the database"""
    from bson import ObjectId
    if field == "id":
        users_collection.delete_one({"_id": ObjectId(identifier)})
    else:
        users_collection.delete_one({field: identifier})
