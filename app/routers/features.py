import os
import shutil
import logging

from fastapi import APIRouter, HTTPException, Request, UploadFile, File, Body, Depends
from datetime import datetime
from typing import Optional
from fastapi.responses import JSONResponse
from app.utils.parsing import Parser
from app.utils.insights import InsightAnalysis
from app.databases.postgresdb.authentication import get_current_user
from app.databases.postgresdb.models import User
from app.databases.mongodb.query_applications import (
    create_user_application,
    update_user_application_status,
)


router = APIRouter()


@router.post("/upload-pdf/")
async def parse_pdf(
    request: Request,
    pdf_file: UploadFile = File(...),
    user: User = Depends(get_current_user),
):
    content = {}
    if user:
        content["user"] = user.as_dict
    if pdf_file.content_type != "application/pdf":
        logging.error(f"File provided is not a PDF: {pdf_file.content_type}")
        content["error"] = "File provided is not a PDF"
        raise HTTPException(status_code=400, detail=content)
    try:
        save_path = os.path.join("staticfiles/uploads", pdf_file.filename)
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(pdf_file.file, buffer)
        request.session["file_path"] = f"/{save_path}"
        content["pdf_path"] = f"/{save_path}"

        logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        text = Parser.extract_text_from_pdf(save_path)
        request.session["resume_text"] = text
        content["resume_text"] = text
        logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        return JSONResponse(
            content={"pdf_path": f"/{save_path}", "resume_text": text},
            media_type="application/json",
        )
    except Exception as e:
        logging.error(e)
        content["error"] = str(e)
        raise HTTPException(status_code=500, detail=content)


@router.post("/analyze-match/")
async def analyze_match(
    job_description: str = Body(..., embed=True),
    resume_text: Optional[str] = Body(..., embed=True),
    user: User = Depends(get_current_user),
):
    content = {}
    if user:
        content["user"] = user.as_dict
    try:
        insights = InsightAnalysis(resume_text, job_description).analyze()
        content["insights"] = insights
        return JSONResponse(content=content, media_type="application/json")
    except Exception as e:
        logging.error(e)
        content["error"] = str(e)
        raise HTTPException(status_code=500, detail=content)


@router.post("/get-skills/")
async def get_skills_from_text(
    request: Request,
    text: Optional[str] = Body(..., embed=True),
    text_type: Optional[str] = "resume",
    user: User = Depends(get_current_user),
):
    content = {}
    if user:
        content["user"] = user.as_dict
    try:
        if not text:
            text = request.session["resume_text"]
        skills = Parser().extract_skills(text, text_type)
        content["skills"] = skills
        return JSONResponse(content=content, media_type="application/json")
    except Exception as e:
        logging.error(e)
        content["error"] = str(e)
        raise HTTPException(status_code=500, detail=content)


@router.post("/insert-posting/")
def insert_job_posting(
    request: Request,
    jobtitle: str = Body(..., embed=True),
    description: str = Body(..., embed=True),
    source: str = Body(..., embed=True),
    data_applied: datetime = Body(..., embed=True),
    status: str = Body(..., embed=True),
    user: User = Depends(get_current_user),
):
    if not user:
        return HTTPException(status_code=401, detail="Please log in to use this feature.")
    else:
        content = {"user": user.as_dict}
    try:
        data = {
            "userid": user.id,
            "source": source,
            "description": description,
            "date_applied": data_applied,
            "status": status,
            "jobtitle": jobtitle,
        }
        content = create_user_application(data)
        return JSONResponse(content=content, media_type="application/json")
    except Exception as e:
        logging.error(e)
        content["error"] = str(e)
        raise HTTPException(status_code=500, detail=content)


@router.post("/update-job-status/")
def post_update_job_status(
    request: Request,
    id: str = Body(..., embed=True),
    status: str = Body(..., embed=True),
    user: User = Depends(get_current_user),
):
    if user:
        content = {"user": user.as_dict}
    else:
        content = {}
    try:
        content = update_user_application_status({"id": id, "status": status})
        return JSONResponse(content=content, media_type="application/json")
    except Exception as e:
        logging.error(e)
        print(e)
        content["error"] = str(e)
        raise HTTPException(status_code=500, detail=content)
