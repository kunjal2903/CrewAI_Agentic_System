from fastapi import FastAPI
import asyncio
from pipelines.run_pipeline import run_pipeline

app = FastAPI()

@app.get("/")
def root():
    return {"message" : "News Agent API is running  "}

@app.post("/run_news_pipeline")
async def trigger_pipeline():
    await run_pipeline()
    return {"status" : "News Pipeline executed Successfully"}