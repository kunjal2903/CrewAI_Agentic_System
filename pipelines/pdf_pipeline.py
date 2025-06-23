import os 
from agents.pdf_agent import PDFProcessingAgent
from vectorstore.faiss_handler import FAISSHandler
import glob
pdf_agent = PDFProcessingAgent()

def ingest_pdf_from_path(filepath:str) ->dict:
    if not os.path.exists(filepath):
        return {"status" : "error" , "message" : "File not found"}
    return pdf_agent.process_pdf(filepath)

def ingest_all_pdfs(folder:str = "uploads")->dict:
    if not os.path.exists(folder):
        return  { "status" : "error" , "message" : 'Upload folder not found'}
    
    files = [f for f in os.listdir(folder) if f.endswith('.pdf')]
    results = []
    for f  in files:
        full_path = os.path.join(folder ,f)
        result = ingest_pdf_from_path(full_path)
        result.append({"file" : f , **result})
    return{
        "status" : "completed",
        "file_processed" : len(results),
        "details" : results
    }

def query_pdf_index(query:str , k:int=5)->dict:
    results = pdf_agent.search(query , k)
    return{
        "query" : query,
        "results" :results
    }

# def run_pdf_ingestion():
#     handler =  FAISSHandler("vectorstore/pdf_index.faiss")
#     for path in glob.glob("uploads/*.pdfs"):
#         text  = extract_path(path)



                            