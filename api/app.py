from fastapi import FastAPI,UploadFile , File , Form
import asyncio
from pipelines.run_pipeline import run_pipeline
from agents.pdf_agent import PDFProcessingAgent
import shutil
import os
from pipelines.pdf_pipeline import ingest_all_pdfs , ingest_pdf_from_path , query_pdf_index


app = FastAPI()
pdf_agent = PDFProcessingAgent()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok =True)

@app.get("/")
def root():
    return {"message" : "News Agent API is running  "}

@app.post("/run_news_pipeline")
async def trigger_pipeline():
    await run_pipeline()
    return {"status" : "News Pipeline executed Successfully"}

@app.post("/upload-pdf")
async def upload_pdf(file:UploadFile =  File(...)):
    file_path = os.path.join(UPLOAD_DIR , file.filename)

    with open(file_path , "wb") as f:
        shutil.copyfileobj(file.file , f)
    result = ingest_pdf_from_path(file_path)
    return result

@app.post("/ingest-all-pdfs")
def ingest_all():
    return ingest_all_pdfs()

@app.post("/query-pdf")
def query_pdf(query:str = Form(...) , top_k:int = Form(5)):
    return query_pdf_index(query=query , k = top_k)

