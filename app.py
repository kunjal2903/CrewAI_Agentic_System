from fastapi import FastAPI, UploadFile, File, Form, Query
from agents.web_scrapper_agent import scrape_url
from agents.pdf_agent import process_pdf
from agents.news_agent import  NewsAgent
from utils.embedding_utils import search_embeddings
from utils.post_processor import format_news_item
from crew.orchestrator import research_crew

app = FastAPI()

@app.post("/scrape")
async def scrape_endpoint(url: str = Query(...)):
    result = await scrape_url(url)
    return result

@app.post("/research_paper")
async def research_paper(file: UploadFile = File(...)):
    return process_pdf(file)



@app.post("/search")
async def search(query: str = Form(...)):
    return search_embeddings(query)

@app.post("/orchestrate")
async def orchestrate(query: str = Form(...)):
    result = research_crew.run(query)
    return {"result": result}

# ✅ New endpoint for NewsAgent
@app.get("/latest-news")
async def get_latest_news(topic: str = "AI", country: str = "us"):
    agent = NewsAgent()
    news = await agent.get_latest_news(topic=topic, country=country)
    formatted_news = [format_news_item(item) for item in news[:5]]
    return {"news": formatted_news}
