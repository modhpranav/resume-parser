from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Request, Body
from fastapi.responses import JSONResponse
from app.utils import extract_text_from_pdf, get_insights, extract_skills
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime
from typing import Optional

import os
import shutil

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates/")
app.mount("/staticfiles", StaticFiles(directory="staticfiles/"), name="static")

app.add_middleware(SessionMiddleware, secret_key="!secret")


@app.get("/")
def get(request: Request):
    return templates.TemplateResponse(
        "resume-parser.html", context={"request": request}
    )


@app.get("/job-desc/")
def get_skills(request: Request):
    return templates.TemplateResponse("get-skills.html", context={"request": request})


@app.get("/my-resume/")
def get_resume(request: Request):
    return templates.TemplateResponse(
        "resume-parser.html", context={"request": request}
    )


@app.get("/get-insights/")
def get_insightstemplate(request: Request):
    return templates.TemplateResponse(
        "resume-insights.html", context={"request": request}
    )


@app.post("/upload-pdf/")
async def parse_pdf(request: Request, pdf_file: UploadFile = File(...)):
    if pdf_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File provided is not a PDF")
    try:
        save_path = os.path.join("staticfiles/uploads", pdf_file.filename)
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(pdf_file.file, buffer)
        request.session["file_path"] = f"/{save_path}"

        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        text = await extract_text_from_pdf(save_path)
        request.session["resume_text"] = text
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        return JSONResponse(
            content={"pdf_path": f"/{save_path}", "resume_text": text},
            media_type="application/json",
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze-match/")
async def analyze_match(
    job_description: str = Body(..., embed=True),
    resume_text: Optional[str] = Body(..., embed=True),
):
    try:
        insights = await get_insights(resume_text, job_description)
        return JSONResponse(content=insights, media_type="application/json")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get-skills/")
async def get_skills_from_text(
    request: Request, text: Optional[str] = Body(..., embed=True)
):
    try:
        if not text:
            text = request.session["resume_text"]
        skills = await extract_skills(text)
        return JSONResponse(content={"skills": skills}, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
