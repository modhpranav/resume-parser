import os
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from app.routers import features, google_auth, templates
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.databases.postgresdb.models import Base
from app.databases.postgresdb.database import engine
from fastapi import FastAPI, Request, Depends
from app.databases.postgresdb.authentication import get_current_user
from app.databases.postgresdb.models import User
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


Jinjatemplates = Jinja2Templates(directory="templates/")

app = FastAPI(
    title="Resume Parser APP",
    description=os.getenv("APP_DESCRIPTION"),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redocs",
    lifespan=lifespan,
)

app.mount("/staticfiles", StaticFiles(directory="staticfiles/"), name="static")

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)
app.include_router(templates.router)
app.include_router(google_auth.router)
app.include_router(features.router)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
    user: User = Depends(get_current_user),
):
    if exc.status_code == 404:
        if user:
            return Jinjatemplates.TemplateResponse(
                "pages-error-404.html", context={"request": request, "user": user}
            )
        return templates.TemplateResponse(
            "pages-error-404.html", context={"request": request}
        )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
    user: User = Depends(get_current_user),
):
    if exc.status_code == 404:
        if user:
            return Jinjatemplates.TemplateResponse(
                "pages-error-404.html", context={"request": request, "user": user}
            )
        return templates.TemplateResponse(
            "pages-error-404.html", context={"request": request}
        )
