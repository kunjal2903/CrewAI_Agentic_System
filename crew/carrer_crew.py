# from crewai import Crew , Agent , Task 
# from tools.news_tool import NewsTool
# from tools.pdf_tool import PDFTool
# from tools.news_tool import fetch_latest_news
# from tools.pdf_tool import search_pdf

# news_tool = NewsTool()
# pdf_tool = PDFTool()

# pdf_agent = Agent(
#     role  = "PDF Research Analyst",
#     goal = "use Academic papers to answer the complex research questions",
#     backstory= "An expert in analayzing scholarly documents and provided academic insights",
#     tools = [pdf_tool],
#     allow_delegation=False,
# )

# news_agent = Agent(
#     role = "News Analyst",
#     goal = "Provide the real-time context from the current events and news",
#     backstory = "A journalist witrh deep undertsanding of the top  trending topics and recent developements",
#     tools = [fetch_latest_news],
#     allow_delegation=False,
# )

# reflective_agent = Agent(
#     role  = "Reflective Synthesizer",
#     goal = "Critically analyse the responses of both the pdf and News Agent  and provide the balanced final insights",
#     backstory = "An impartial AI with the task of comparing the academic and real world insights to make the thoughful decisions",

# )
# human_feedback_task= Task(
#     description="Ask the human to validate or provide the suggestions on synthesized insight before finalizing the answer",
#     expected_output="A human -reviewed insight summary"
# )
# task_pdf = Task(
#     agent  =  pdf_agent,
#     description= " provide the detailed research based insights for given query using  PDF document",
#     expected_output= "Summary of the current news articles relavent to the query"

# )

# task_news =Task(
#     agent  =  news_agent, 
#     description="SUummarize the latest development and news related to the query",
#     expected_output="Summary of current news articles relevant to the query"
# )

# task_reflect = Task(
#     agent  = reflective_agent,
#     description="Campare the outputs from PDF and News Agents . Produce the reflective and insightful synthesis",
#     expected_output= "Balanced conclusion synthesizing both academic and real-world views"
# )

# carrer_crew = Crew(
#     agents = [pdf_agent , news_agent , reflective_agent],
#     tasks = [task_pdf , task_news , task_reflect , human_feedback_task],
#     process= "sequential"
# )

