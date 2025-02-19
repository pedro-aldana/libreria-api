from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import init, close
from tortoise.contrib.fastapi import register_tortoise
from routes.route_user import user_router
from routes.route_role import role_router
from routes.route_category import category_router
from routes.route_book import book_router
from utils.super_admin import create_superadmin

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes cambiar "*" por el dominio de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}



@app.on_event("startup")
async def startup_event():
    await init()
    await create_superadmin()

@app.on_event("shutdown")
async def shutdown_event():
    await close()


register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={'models': [
        'models.model_user',
        'models.model_category',
        'models.model_book',
        'models.model_comment',
        'models.model_reply'
    ]},
    generate_schemas=True,
    add_exception_handlers=True
)

app.include_router(user_router, prefix="/api")
app.include_router(role_router, prefix="/api")
app.include_router(category_router, prefix="/api/category")
app.include_router(book_router, prefix="/api/book")
