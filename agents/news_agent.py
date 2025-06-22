 
import os
import httpx
from dotenv import load_dotenv
import certifi

load_dotenv()

class NewsAgent:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsdata.io/api/1/news"

    async def get_latest_news(self, topic="AI", country="us", language="en"):
        params = {
            "apikey": self.api_key,
            "q": topic,
            "country": country,
            "language": language
        }
        try:
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.get(self.base_url, params=params)
                if response.status_code == 200:
                    return response.json().get("results" , [])
                else:
                    print(" News API Error:", response.status_code, response.text)
                    return []
        except Exception as e :
            print("Exception during request" , e)
            return  []
        
  
# import asyncio
# from agents.news_agent import NewsAgent
# from utils.embedding_utils import get_embedding_model, get_embeddings
# from vectorstore.faiss_handler import FAISSEngine

# async def ingest_news_pipeline():
#     agent = NewsAgent()
#     articles = await agent.get_latest_news(topic="AI")

#     if not articles:
#         print("❌ No articles fetched.")
#         return

#     model = get_embedding_model()
#     texts = [a.get("description", "") for a in articles if a.get("description")]
#     metadatas = [{"title": a.get("title", ""), "url": a.get("link", "")} for a in articles]

#     embeddings = get_embeddings(model, texts)
#     faiss_news = FAISSEngine("vectorstore/news_index")
#     faiss_news.add(embeddings, metadatas)

#     print(f"✅ Ingested {len(embeddings)} articles into FAISS.")

# if __name__ == "__main__":
#     asyncio.run(ingest_news_pipeline())
