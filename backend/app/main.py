from fastapi import FastAPI
from app.routes import blogs
from app.database import blogs_collection


app = FastAPI()

# --- CREATE UNIQUE INDEX ON SLUG ---
blogs_collection.create_index("slug", unique=True)

app.include_router(blogs.router)