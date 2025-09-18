import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

# Database configuration from environment variables
MONGO_URI = os.getenv("MONGO_URI")        # MongoDB connection string (e.g., mongodb://localhost:27017)
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME") # Database name (e.g., "blog_app")

# Create async MongoDB client connection
# Motor is the async driver for MongoDB that works with FastAPI
client = MongoClient(MONGO_URI)

# Database instance - contains all collections for the blog application
db = client[MONGO_DB_NAME]

# Collection references for different data types
blogs_collection = db.blogs     # Stores blog posts with title, content, author, etc.
users_collection = db.users     # Stores user profiles for authentication and author info

# Note: Collections are created automatically when first document is inserted
# Motor provides async/await support for non-blocking database operations