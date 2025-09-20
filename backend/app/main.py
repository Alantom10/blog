from fastapi import FastAPI, HTTPException
from app.routes import blogs, users
from app.utils import auth
from app.database import blogs_collection, users_collection
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.middleware.rate_limit import limiter
from fastapi.exceptions import RequestValidationError
from app.middleware.error_handlers import (
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler
)


app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

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