import time
from app.database import blogs_collection, users_collection

def test_query_performance():
    start_time = time.time()
    
    # Test blog lookup by slug (should be very fast with index)
    blog = blogs_collection.find_one({"slug": "building-modern-apis-with-fastapi"})
    print(f"Blog lookup by slug: {time.time() - start_time:.4f}s")
    
    start_time = time.time()
    # Test user lookup by email (should be very fast with index)
    user = users_collection.find_one({"email": "acthomas2000@gmail.com"})
    print(f"User lookup by email: {time.time() - start_time:.4f}s")
    
if __name__ == "__main__":
    test_query_performance()