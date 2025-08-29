from fastapi import FastAPI
from app.routes import blogs
from app.database import blogs_collection
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum


app = FastAPI()

# Allow React frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CREATE UNIQUE INDEX ON SLUG ---
blogs_collection.create_index("slug", unique=True)

app.include_router(blogs.router)

handler = Mangum(app)