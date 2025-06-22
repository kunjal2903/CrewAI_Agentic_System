# from pydantic import BaseModel, Field
# from crewai.tools import BaseTool
# from crewai_tools import tool
# # from pipelines.rag_pipeline import generate_rag_answer
# from agents.news_agent import NewsAgent
# import asyncio
# from typing import ClassVar, Type

# class NewsQueryInput(BaseModel):
#     query:str = Field(... , description="Topic to fetch the news on ")
   

# class NewsTool(BaseTool):
#     name: ClassVar[str] = "NewsTool"
#     description: ClassVar[str] = "Tool to fetch latest news using News Agent"
#     args_schema: ClassVar[Type[BaseModel]] = NewsQueryInput

# @tool(name = "NameTool" , description = "Tool to ftech the latest news using News Agent ")
# def fetch_latest_news(query:str)->str:
#         agent  = NewsAgent()

#         try : 
#             loop = asyncio.get_running_loop()
#         except RuntimeError:
#             loop= asyncio.new_event_loop()
#             asyncio.set_event_loop(loop)

#         results = loop.run_until_complete(agent.get_latest_news(topic=query))

#         if not results:
#             return "No news found for the topic "
        
#         response = "Top News Resilts"
#         for i , article in enumerate(results[:5] , 1):
#             title = article.get("title" , "No title")
#             link = article.get("link" , "No link")
#             response += f"{i}.{title}\n {link}\n"
#         return response
                        
       
       
# # from typing import ClassVar, Type
# # from pydantic import BaseModel, Field
# # from crewai.tools import BaseTool
# # from agents.news_agent import NewsAgent
# # import asyncio

# # class NewsQueryInput(BaseModel):
# #     query: str = Field(..., description="Topic to fetch the news on")

# # class NewsTool(BaseTool):
# #     name: ClassVar[str] = "NewsTool"
# #     description: ClassVar[str] = "Tool to fetch latest news using News Agent"
# #     args_schema: ClassVar[Type[BaseModel]] = NewsQueryInput

# #     def _run(self, query: str) -> str:
# #         agent = NewsAgent()
# #         results = asyncio.run(agent.get_latest_news(topic=query))
# #         return "\n\n".join([f"- {item.get('title')} ({item.get('link')})" for item in results[:5]])
