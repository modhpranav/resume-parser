import os
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from app.routers import features, google_auth, templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.databases.postgresdb.models import Base
from app.databases.postgresdb.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield



app = FastAPI(
    title='Resume Parser APP',
    description=os.getenv("APP_DESCRIPTION"),
    version="1.0.0",
    docs_url="/documentation",
    redoc_url="/redocs",
    lifespan=lifespan
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
app.include_router(google_auth.router)
app.include_router(features.router)
