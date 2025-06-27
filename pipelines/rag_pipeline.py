# from langgraph.graph import StateGraph, END
# from agents.pdf_agent import PDFProcessingAgent
# from agents.news_agent import NewsAgent
# from utils.news_cleaner import clean_html
# from typing import Any, List , Dict

# # Define the state schema
# state = {
#     "query": str,
#     "pdf_results": List[Dict[str,Any]],
#     "news_results": List[Dict[str,Any]],
#     "final_results": List[Dict[str,Any]]
# }

# # Node to process PDF results
# def query_pdf_node(state):
#     query = state["query"]
#     agent = PDFProcessingAgent()
#     pdf_results = agent.search(query, k=5)  # Assuming this returns a list
#     return {**state, "pdf_results": pdf_results}

# # Node to process news results
# async def query_news_node(state):
#     query = state["query"]
#     agent = NewsAgent()
#     try :
#         results  = await agent.get_latest_news(topic=query)
#         descriptions = [a.get("description" , "") for a in results if a.get("description")]
#         return {**state , "news_results" : descriptions}
#     except Exception as e :
#         print("Error in query _news_node" , str(e))
#         return {**state, "news_results" : []}
#     # articles = agent.get_latest_news(topic=query)
#     # cleaned_articles = [
#     #     {
#     #         "title": a.get("title", ""),
#     #         "url": a.get("link"),
#     #         "content": clean_html(a.get("description", "") or "")
#     #     }
#     #     for a in articles if a.get("description")
#     # ]
#     # return {**state, "news_results": cleaned_articles}

# # Node to merge and rank results
# def merge_results(state):
#     all_items = []

#     for item in state.get("pdf_results", []):
#         all_items.append({
#             "source": "pdf",
#             "url": item.get("url", ""),
#             "score": round(1 / (1 + item.get("score", 1)), 3)
#         })

#     for item in state.get("news_results", []):
#         all_items.append({
#             "source": "news",
#             "url": item.get("url", ""),
#             "title": item.get("title", ""),
#             "score": 0.8
#         })

#     all_items.sort(key=lambda x: x["score"], reverse=True)
#     return {**state, "final_results": all_items[:5]}

# # Build the LangGraph
# def build_rag_graph():
#     graph = StateGraph(state)
#     graph.add_node("QueryPDF", query_pdf_node)
#     graph.add_node("QueryNews", query_news_node)
#     graph.add_node("MergeResults", merge_results)

#     graph.set_entry_point("QueryPDF")
#     graph.add_edge("QueryPDF", "QueryNews")
#     graph.add_edge("QueryNews", "MergeResults")
#     graph.add_edge("MergeResults", END)

#     return graph.compile()


# from langgraph.graph import StateGraph, END
# from agents.pdf_agent import PDFProcessingAgent
# from agents.news_agent import NewsAgent
# from typing import List, Dict, Any


# # ✅ Define LangGraph state properly
# state_schema = {
#     "query": str,
#     "pdf_results": list,
#     "news_results": list,
#     "final_results": list
# }


# # ✅ Node 1: Search PDF FAISS
# def query_pdf_node(state):
#     query = state["query"]
#     pdf_agent = PDFProcessingAgent()
#     try:
#         results = pdf_agent.search(query)
#         print(f"📄 PDF results: {results}")
#         return {**state, "pdf_results": results}
#     except Exception as e:
#         print("❌ PDF node error:", str(e))
#         return {**state, "pdf_results": []}


# # ✅ Node 2: Query News API and embed results
# async def query_news_node(state):
#     query = state["query"]
#     agent = NewsAgent()
#     try:
#         articles = await agent.get_latest_news(topic=query)
#         cleaned = [
#             {
#                 "title": a.get("title", ""),
#                 "description": a.get("description", ""),
#                 "url": a.get("link", "")
#             }
#             for a in articles if a.get("description")
#         ]
#         print(f"📰 News results: {cleaned}")
#         return {**state, "news_results": cleaned}
#     except Exception as e:
#         print("❌ News node error:", str(e))
#         return {**state, "news_results": []}


# # ✅ Node 3: Merge news and PDF results
# def merge_results(state):
#     try:
#         merged = state["pdf_results"] + state["news_results"]
#         print(f"✅ Merged results: {merged}")
#         return {**state, "final_results": merged}
#     except Exception as e:
#         print("❌ Merge error:", str(e))
#         return {**state, "final_results": []}


# # ✅ Graph builder function
# def build_rag_graph():
#     graph = StateGraph(state_schema)
#     graph.add_node("QueryPDF", query_pdf_node)
#     graph.add_node("QueryNews", query_news_node)
#     graph.add_node("MergeResults", merge_results)

#     graph.set_entry_point("QueryPDF")
#     graph.add_edge("QueryPDF", "QueryNews")
#     graph.add_edge("QueryNews", "MergeResults")
#     graph.add_edge("MergeResults", END)

#     return graph.compile()

from langgraph.graph import StateGraph, END
from agents.pdf_agent import PDFProcessingAgent
from agents.news_agent import NewsAgent
from pipelines.web_scrapper_pipeline import run_scraper_pipeline
from typing import List, Dict, TypedDict, Any
import requests
from transformers import pipeline, AutoTokenizer ,  AutoModelForSeq2SeqLM
import torch

qa_pipeline = pipeline(
    "text2text-generation" , 
    model = "google/flan-t5-base",
    tokenizer="google/flan-t5-base",
    device=0 if torch.cuda.is_available() else  -1
)

# Define LangGraph state using TypedDict
class RAGState(TypedDict):
    query: str
    pdf_results: List[Dict[str, Any]]
    news_results: List[Dict[str, Any]]
    scraper_results: List[Dict[str, Any]]
    final_results: List[Dict[str, Any]]
    llm_answer: List[Dict[str, Any]]


# Node 1: Search PDF FAISS
def query_pdf_node(state: RAGState) -> RAGState:
    query = state["query"]
    pdf_agent = PDFProcessingAgent()
    try:
        results = pdf_agent.search(query)
        print(f"📄 PDF results: {results}")
        return {**state, "pdf_results": results}
    except Exception as e:
        print("❌ PDF node error:", str(e))
        return {**state, "pdf_results": []}


# Node 2: Query News API and embed results
async def query_news_node(state: RAGState) -> RAGState:
    query = state["query"]
    agent = NewsAgent()
    try:
        articles = await agent.get_latest_news(topic=query)
        cleaned = [
            {
                "title": a.get("title", ""),
                "description": a.get("description", ""),
                "url": a.get("link", "")
            }
            for a in articles if a.get("description")
        ]
        print(f"📰 News results: {cleaned}")
        return {**state, "news_results": cleaned}
    except Exception as e:
        print("❌ News node error:", str(e))
        return {**state, "news_results": []}


# Node 3: Query web scraper node
async def query_scraper_node(state: RAGState) -> RAGState:
    query = state["query"]
    try:
        results = await run_scraper_pipeline(query)
        print(f"Scraper results: {results}")
        return {**state, "scraper_results": results}
    except Exception as e:
        print("Scraper node error:", str(e))
        return {**state, "scraper_results": []}



# Node 4: Merge news and PDF results and scraper results
def merge_results(state: RAGState) -> RAGState:
    try:
        merged = state["pdf_results"] + state["news_results"]+ state["scraper_results"]
        print(f"✅ Merged results: {merged}")
        return {**state, "final_results": merged}
    except Exception as e:
        print("❌ Merge error:", str(e))
        return {**state, "final_results": []}

#Node 5  : add the LLM response  
def llm_response_node(state):
    query =  state["query"]
    merged = state["final_results"]

    context = "\n".join([
        f"- {item.get('title' , '') or item.get('url' , '')} : {item.get('description' , '') or item.get('content' , '')}"
        for item in merged
    ])
    prompt = f"""You are helpful Assistant. Use the following context to answer the question.
    Question :{query}
    Context:
    {context}
    Answer: """
    try:
        response  = qa_pipeline(prompt, max_new_tokens = 200)
        answer = response[0]["generated_text"].strip()
        return {**state, "llm_answer": answer}
    except Exception as e:
        return {**state, "llm_answer" : f"Error from LLM :{str(e)}"}


def build_rag_graph():
    graph = StateGraph(RAGState)
    graph.add_node("QueryPDF", query_pdf_node)
    graph.add_node("QueryNews", query_news_node)
    graph.add_node("QueryScraper", query_scraper_node)
    graph.add_node("MergeResults", merge_results)
    graph.add_node("LLMResponse" , llm_response_node)

    graph.set_entry_point("QueryPDF")
    graph.add_edge("QueryPDF", "QueryNews")
    graph.add_edge("QueryNews", "QueryScraper")
    graph.add_edge("QuerScraper", "MergeResults")
    graph.add_edge("MergeResults", "LLMResponse")
    graph.add_edge("LLMResponse" , END)

    return graph.compile()