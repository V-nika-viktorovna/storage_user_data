
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from config import toroise_orm
from routers import admin, users

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(app, config=toroise_orm, generate_schemas=True)

app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(users.router, tags=["user"])
