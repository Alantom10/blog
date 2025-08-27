from fastapi import FastAPI
from app.routes import blogs

app = FastAPI()

app.include_router(blogs.router)