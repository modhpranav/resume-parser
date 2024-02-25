import os
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from app.routers import authentication, features, templates
from fastapi.staticfiles import StaticFiles





app = FastAPI(
    title='Resume Parser APP',
    description=os.getenv("APP_DESCRIPTION"),
    version="1.0.0",
    docs_url="/v1/documentation",
    redoc_url="/v1/redocs",
)

app.mount("/staticfiles", StaticFiles(directory="staticfiles/"), name="static")

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))
app.add_middleware(
    CORSMiddleware, 
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=["*"]
)
app.include_router(templates.router)
app.include_router(authentication.router)
app.include_router(features.router)