from fastapi import Depends, APIRouter, Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates/")
router = APIRouter()

@router.get("/")
def get(request: Request):
    return templates.TemplateResponse(
        "resume-parser.html", context={"request": request}
    )


@router.get("/job-desc/")
def get_skills(request: Request):
    return templates.TemplateResponse("get-skills.html", context={"request": request})


@router.get("/my-resume/")
def get_resume(request: Request):
    return templates.TemplateResponse(
        "resume-parser.html", context={"request": request}
    )


@router.get("/get-insights/")
def get_insightstemplate(request: Request):
    return templates.TemplateResponse(
        "resume-insights.html", context={"request": request}
    )