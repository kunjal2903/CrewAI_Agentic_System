import os  
import fitz 
from vectorstore.faiss_handler import FAISSHandler

class PDFProcessingAgent:
    def __init__(self):
        self.vector_store  =  FAISSHandler()

    def extract_text(self , filepath:str )->str:
        try:
            doc =  fitz.open(filepath)
            return "/n".join([page.get_text() for page in doc])
        except Exception as e :
            print(f"Error readieng the PDF: {e}")
        

    def process_pdf(self, filepath:str):
        content = self.extract_text(filepath)
        if not content.strip():
            return {"status" : "error" , "message" : "Empty or unreadable PDF"}
        
        doc = {
            "url" : filepath,
            "content" : content
        }
        self.vector_store.add_documents([doc])
        return {"status" : "success" , "message" : "PDF embedded"}
    
    def search(self , query:str , k : int=5):
        return self.vector_store.search(query , top_k=k)
    