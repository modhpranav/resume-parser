from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Request, Body
from fastapi.responses import JSONResponse
from app.utils import extract_text_from_pdf, get_insights, extract_skills
from fastapi.responses import FileResponse
import os
import shutil

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates/")
app.mount("/staticfiles", StaticFiles(directory="staticfiles/"), name="static")



@app.get("/")
def get(request: Request):
    return templates.TemplateResponse('resume-parser.html', context={"request": request})

@app.get('/job-desc/')
def get_skills(request: Request):
    return templates.TemplateResponse('get-skills.html', context={"request": request})

@app.get('/my-resume/')
def get_resume(request: Request):
    return templates.TemplateResponse('resume-parser.html', context={"request": request})

@app.post("/parse-pdf/")
async def parse_pdf(pdf_file: UploadFile = File(...)):
    if pdf_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File provided is not a PDF")
    try:
        save_path = os.path.join('staticfiles/uploads', pdf_file.filename)
        with open(save_path, 'wb') as buffer:
            shutil.copyfileobj(pdf_file.file, buffer)

        text = await extract_text_from_pdf(save_path)
        skills = await extract_skills(text)
        return JSONResponse(content={"pdf_path": f"/{save_path}", "skills": skills}, media_type="application/json")
    except Exception as e:
        print(e)
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


@app.post("/get-skills/")
async def get_skills_from_text(text: str = Body(..., embed=True)):
    try:
        skills = await extract_skills(text)
        return JSONResponse(content={"skills": skills}, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
