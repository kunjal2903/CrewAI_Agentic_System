import asyncio
from agents.news_agent import NewsAgent

async def run_pipeline():
    agent  =  NewsAgent()
    news_items = await agent.get_latest_news(topic = "AI")

    if not news_items:
        print("No news fetched .  Check the API key or connection")
        return {"status" : "error" , "message" : "No news Fetched"}
    
    print(f"Retrieved {len(news_items)} news articles")

    for item in news_items:
        print(f"{item.get('title')}")

    return {"status" : "Success" , "count" : len(news_items)}