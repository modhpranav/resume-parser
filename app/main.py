from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Request
from fastapi.responses import JSONResponse
from app.utils import extract_text_from_pdf, get_insights, get_skills
from fastapi.responses import FileResponse
from pydantic import BaseModel
import shutil

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


class ImageData(BaseModel):
    pdf_path: str
    metadata: dict

app = FastAPI()
templates = Jinja2Templates(directory="templates/")
app.mount("/assets", StaticFiles(directory="templates/assets"), name="static")



@app.get("/")
def get(request: Request):
    return templates.TemplateResponse('index.html', context={"request": request})

@app.post("/parse-pdf/", response_model=ImageData)
async def parse_pdf(pdf_file: UploadFile = File(...)):
    if pdf_file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File provided is not a PDF")

    # try:
        # text = await extract_text_from_pdf(pdf_file)
        # skills = await get_skills("text")
        # Save the PDF temporarily
    print(pdf_file.filename, pdf_file)
    resume_path = pdf_file.filename
    return ImageData(pdf_path="Chandni_Asnani_Resume_15-04-2023-00-41-02.pdf", metadata={"skills": "skills"})
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))


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
