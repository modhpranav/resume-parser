import os
import shutil
import logging

from fastapi import APIRouter, HTTPException, Request, UploadFile, File, Body
from datetime import datetime
from typing import Optional
from fastapi.responses import JSONResponse
from app.utils.parsing import Parser
from app.utils.insights import InsightAnalysis


router = APIRouter()


@router.post("/upload-pdf/")
async def parse_pdf(request: Request, pdf_file: UploadFile = File(...)):
    if pdf_file.content_type != "application/pdf":
        logging.error(f"File provided is not a PDF: {pdf_file.content_type}")
        raise HTTPException(status_code=400, detail="File provided is not a PDF")
    try:
        save_path = os.path.join("staticfiles/uploads", pdf_file.filename)
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(pdf_file.file, buffer)
        request.session["file_path"] = f"/{save_path}"

        logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        text = Parser.extract_text_from_pdf(save_path)
        request.session["resume_text"] = text
        logging.info(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        return JSONResponse(
            content={"pdf_path": f"/{save_path}", "resume_text": text},
            media_type="application/json",
        )
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-match/")
async def analyze_match(
    job_description: str = Body(..., embed=True),
    resume_text: Optional[str] = Body(..., embed=True),
):
    try:
        insights = InsightAnalysis(resume_text, job_description).analyze()
        print(insights)
        return JSONResponse(content=insights, media_type="application/json")
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get-skills/")
async def get_skills_from_text(
    request: Request, text: Optional[str] = Body(..., embed=True), text_type: Optional[str] = "resume"
):
    try:
        if not text:
            text = request.session["resume_text"]
        skills = Parser().extract_skills(text, text_type)
        return JSONResponse(content={"skills": skills}, media_type="application/json")
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail=str(e))
