from fastapi import FastAPI
from routes import blogs

app = FastAPI()

app.include_router(blogs.router)