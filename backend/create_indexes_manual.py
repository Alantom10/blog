from app.database import blogs_collection, users_collection

def create_indexes_manually():
    print("Creating indexes manually...")
    
    try:
        # Users indexes
        users_collection.create_index("email", unique=True)
        users_collection.create_index("username", unique=True)
        print("✓ Users indexes created")
        
        # Blogs indexes - simplified for Atlas free tier
        blogs_collection.create_index("slug", unique=True)
        blogs_collection.create_index("date_published")  # Remove direction parameter
        blogs_collection.create_index("author.name")
        
        print("✓ Blogs indexes created")
        
        # Skip text index for now - might not be supported on free tier
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_indexes_manually()