from pipelines.rag_pipeline import build_rag_graph
import asyncio
# Define the reusable function
# async def run_pipeline(query: str = "AI"):
#     graph = build_rag_graph()

#     initial_state = {
#         "query":query,
#         "pdf_results" :[],
#         "news_results" :[],
#         "final_results" :[]
#     }
#     result  =  await graph.ainvoke(initial_state)

#     return {
#         "status" : "success",
#         "query" : query,
#         "results" : result["final_results"]
#     }


async def run_pipeline(query: str = "latest AI trends"):
    graph = build_rag_graph()
    result = await graph.ainvoke({"query": query})
    return result


# Optional: for standalone testing
if __name__ == "__main__":
    import asyncio

    async def main():
        result = await run_pipeline()
        print("\nFinal Combined Results:")
        for idx, item in enumerate(result["final_results"], 1):
            print(f"{idx}. {item}\n")

    asyncio.run(main())
import asyncio
from agents.news_agent import NewsAgent

async def run_pipeline1():
    agent  =  NewsAgent()
    news_items = await agent.get_latest_news(topic = "AI")

    if not news_items:
        print("No news fetched .  Check the API key or connection")
        return {"status" : "error" , "message" : "No news Fetched"}
    
    print(f"Retrieved {len(news_items)} news articles")

    for item in news_items:
        print(f"{item.get('title')}")

    return {"status" : "Success" , "count" : len(news_items)}