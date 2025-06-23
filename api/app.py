from fastapi import FastAPI,UploadFile , File , Form
import asyncio
from pipelines.run_pipeline import run_pipeline
from agents.pdf_agent import PDFProcessingAgent
import shutil
import os
from pipelines.pdf_pipeline import ingest_all_pdfs , ingest_pdf_from_path , query_pdf_index
from fastapi import FastAPI
from pipelines.run_pipeline import run_pipeline , run_pipeline1

# from pipelines.rag_pipeline import build_rag_graph
# from fastapi import Form 
# from crew.carrer_crew import carrer_crew
# from pipelines.run_pipeline import run_pipeline
# from crew.carrer_crew import task_news,task_pdf , task_reflect,human_feedback_task

app = FastAPI()
pdf_agent = PDFProcessingAgent()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok =True)

@app.get("/")
def root():
    return {"message" : "News Agent API is running  "}

# @app.post("/carrer-insight")
# def get_carrer_insight(query:str = Form(...)):
#     task_pdf.description = f"Use pdf documents to provide the insight on '{query}'"
#     task_news.description = f"Use news articles to summarize the updates on  '{query}'"
#     task_reflect.description = f"campare the academic and news findings for  '{query}'"
#     task_feedback_task = f"Ask humans rfor feedback on insights'{query}'"

#     result =  carrer_crew.run()
#     return result 
    
@app.post("/run_news_pipeline")
async def trigger_pipeline():
    await run_pipeline1()
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



from fastapi.responses import JSONResponse
@app.post("/run_combined_results")
async def run_combined_results(query: str = Form(...)):
    try:
        result = await run_pipeline(query)
        return JSONResponse(content=result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})

# @app.post("/query-all")
# async def query_all(query:str = Form(...)):
#     result = await build_rag_graph.ainvoke({"query" : query})
#     return{
#         "query" : query,
#         "results" : result["final_results"]
#     }

# from fastapi import FastAPI, UploadFile, File, Form
# import os
# import shutil
# from agents.pdf_agent import PDFProcessingAgent
# from pipelines.pdf_pipeline import ingest_all_pdfs, ingest_pdf_from_path, query_pdf_index
# from pipelines.rag_pipeline import build_rag_graph

# app = FastAPI()
# pdf_agent = PDFProcessingAgent()
# UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# @app.get("/")
# def root():
#     return {"message": "News Agent API is running"}

# @app.post("/run_news_pipeline")
# async def trigger_pipeline():
#     await run_pipeline()
#     return {"status": "News Pipeline executed Successfully"}

# @app.post("/upload-pdf")
# async def upload_pdf(file: UploadFile = File(...)):
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
#     with open(file_path, "wb") as f:
#         shutil.copyfileobj(file.file, f)
#     result = ingest_pdf_from_path(file_path)
#     return result

# @app.post("/ingest-all-pdfs")
# def ingest_all():
#     return ingest_all_pdfs()

# @app.post("/query-pdf")
# def query_pdf(query: str = Form(...), top_k: int = Form(5)):
#     return query_pdf_index(query=query, k=top_k)

# @app.post("/query-all")
# async def query_all(query: str = Form(...)):
#     graph = build_rag_graph()
#     result = await graph.ainvoke({"query": query})
#     return {
#         "query": query,
#         "results": result["final_results"]
#     }
