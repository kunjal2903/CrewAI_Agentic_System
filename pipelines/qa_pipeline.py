from agents.qa_agent import QAAgent

qa_agent  =  QAAgent()

async def run_qa_pipeline(query :str):
    return await qa_agent.answer(query)