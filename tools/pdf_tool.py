# from pydantic import BaseModel , Field
# from crewai.tools import BaseTool
# from typing import ClassVar
# from agents.pdf_agent import PDFProcessingAgent

# class PDFQueryInput(BaseModel):
#     query :str = Field(... , description="The question to ask")
   

# class PDFTool(BaseTool):
#     name:ClassVar[str] = "PDF Tool"
#     description:ClassVar[str] = "Search academic insights from the uploaded pdf"
#     args_schema = PDFQueryInput

# def _run(self , query:str)->str:
#     agent = PDFProcessingAgent()
#     results =  agent.query_pdfs(query)


#     if not results:
#         return "No relevant results found in PDF files"
    
#     return "/n" .join([f"{i+1}, {r.get('content' , '')[:200]}..." for i , r in enumerate(results[:5])])

   