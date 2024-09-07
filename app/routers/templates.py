import os

from fastapi import Depends, APIRouter, Request, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.databases.postgresdb.authentication import get_current_user
from app.databases.postgresdb.models import User
from app.databases.mongodb.database import mongo_database
from dotenv import load_dotenv
from app.databases.mongodb.schemas import JobStatus

load_dotenv()

SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", "default_session_cookie_name")

templates = Jinja2Templates(directory="templates/")
router = APIRouter()


@router.get("/")
def get(request: Request, user: User = Depends(get_current_user)):
    print("Request recieved")
    return templates.TemplateResponse(
        "resume-parser.html", context={"request": request, "user": user}, status_code=200
    )


@router.get("/job-desc/")
def get_skills(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse(
        "get-skills.html", context={"request": request, "user": user}, status_code=200
    )


@router.get("/my-resume/")
def get_resume(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse(
        "resume-parser.html", context={"request": request, "user": user}, status_code=200
    )


@router.get("/get-insights/")
def get_insightstemplate(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse(
        "resume-insights.html", context={"request": request, "user": user}, status_code=200
    )


@router.get("/contact-us/")
def get_insightstemplate(request: Request, user: User = Depends(get_current_user)):
    return templates.TemplateResponse(
        "pages-contact.html", status_code=200, context={"request": request, "user": user}
    )


@router.get("/job-applications/")
def get_job_applications(request: Request, user: User = Depends(get_current_user)):
    try:
        if not user:
            data = []
        else:
            query_res = list(
                mongo_database["job_applications"]
                .find({"userid": user.id}, {"userid": 0})
                .sort("dateapplied", -1)
            )
            data = []
            for res in query_res:
                res["Application Date"] = res["Application Date"].strftime("%Y-%m-%d")
                res["id"] = str(res["_id"])
                del res["_id"]
                data.append(res)
        return templates.TemplateResponse(
            "job-applications.html",
            context={
                "request": request,
                "user": user,
                "data": data,
                "statuses": list(JobStatus),
            }, status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)}, media_type="application/json", status_code=500
        )


@router.get("/logout/")
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response
