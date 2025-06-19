import asyncio
from agents.news_agent import NewsAgent
from utils.news_cleaner import clean_html
from utils.embedding_utils import EmbeddingModel
from vectorstore.faiss_handler import FAISSHandler

async def run_pipeline():
    agent = NewsAgent()
    news_items = await agent.get_latest_news(topic="AI")

    if not news_items:
        print("❌ No news fetched. Check your API key or internet.")
        return

    texts = []
    metadatas = []

    for item in news_items:
        title = clean_html(item.get("title", ""))
        description = clean_html(item.get("description", ""))
        text = f"{title} - {description}"
        texts.append(text)
        metadatas.append({
            "title": title,
            "url": item.get("link"),
            "published": item.get("pubDate")
        })

    embedder = EmbeddingModel()
    vectors = embedder.embed_texts(texts)

    if vectors is None or len(vectors) == 0 :
        print("❌ No vectors generated.")
        return

    faiss_handler = FAISSHandler(dim=len(vectors[0]))
    faiss_handler.add_texts(vectors, metadatas)
    print(f"✅ Stored {len(vectors)} news items in FAISS.")

if __name__ == "__main__":
    asyncio.run(run_pipeline())

