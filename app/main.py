from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.routes import (authentication)

app = FastAPI()


origins = [
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentication.router, tags=["authentication"], prefix="/api/users")