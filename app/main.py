from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
from app.utils import extract_text_from_pdf, get_insights, get_skills
from app import nlp

app = FastAPI()


@app.post("/parse-pdf/")
async def parse_pdf(pdf_file: UploadFile = File(...)):
    if pdf_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File provided is not a PDF")

    try:
        text = await extract_text_from_pdf(pdf_file)

        skills = await get_skills(text)

        return JSONResponse(content={"Skills": skills}, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze-match/")
async def analyze_match(
    resume: UploadFile = File(...), job_description: str = Form(...)
):
    if resume.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Resume file provided is not PDF")

    try:
        insights = await get_insights(resume, job_description)
        return JSONResponse(content=insights, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
