from app.database import blogs_collection, users_collection
import logging

logger = logging.getLogger(__name__)

def create_indexes():
    """Create database indexes compatible with MongoDB Atlas free tier"""
    
    try:
        # USERS COLLECTION INDEXES
        users_collection.create_index("email", unique=True)
        users_collection.create_index("username", unique=True)
        
        # BLOGS COLLECTION INDEXES
        blogs_collection.create_index("slug", unique=True)
        blogs_collection.create_index("date_published") 
        blogs_collection.create_index("author.name")
        
        print("Basic indexes created successfully!")
        
    except Exception as e:
        print(f"Error creating indexes: {str(e)}")

def drop_indexes():
    """Drop all custom indexes (useful for testing/reset)"""
    try:
        # Keep only the default _id indexes
        users_collection.drop_indexes()
        blogs_collection.drop_indexes()
        logger.info("All custom indexes dropped")
    except Exception as e:
        logger.error(f"Error dropping indexes: {str(e)}")

def list_indexes():
    """List all current indexes for debugging"""
    try:
        logger.info("USERS COLLECTION INDEXES:")
        for index in users_collection.list_indexes():
            logger.info(f"  - {index}")
            
        logger.info("BLOGS COLLECTION INDEXES:")
        for index in blogs_collection.list_indexes():
            logger.info(f"  - {index}")
            
    except Exception as e:
        logger.error(f"Error listing indexes: {str(e)}")