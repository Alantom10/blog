from fastapi import FastAPI
from app.routes import blogs, users
from app.utils import auth
from app.database import blogs_collection, users_collection
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

# --- CREATE UNIQUE INDEX ON EMAIL & USERNAME (users) ---
users_collection.create_index("email", unique=True)
users_collection.create_index("username", unique=True)

# --- ROUTERS ---
app.include_router(blogs.router)
app.include_router(users.router)
app.include_router(auth.router)

handler = Mangum(app)