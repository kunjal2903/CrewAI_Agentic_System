from pipelines.rag_pipeline import build_rag_graph


class QAAgent:
    def __init__(self):

        self.graph  = build_rag_graph()
    
    async def answer(self  , query:str ):
        initial_state = {
            "query" :query,
            "pdf_results" : [],
            "news_results" :[],
            "final_results" :[],
            "llm_answer" :""

        }
        result  = await self.graph.ainvoke(initial_state)
        return {
            "query" :query,
            "answer" :result.get("llm_answer" , ""),
            "source" :result.get("final_results" , [])
        }
    