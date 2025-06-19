from crewai import Agent, Task, Crew
from agents.web_scrapper_agent import scrape_url
from agents.pdf_agent import process_pdf
# from agents.news_agent import
# Define agents
web_agent = Agent(
    name="WebScraper",
    role="Scrapes and embeds web content",
    goal="Extract meaningful content from websites and embed it for semantic search.",
    backstory="An expert in crawling and parsing web pages for research purposes."
)

pdf_agent = Agent(
    name="PDFProcessor",
    role="Processes and embeds PDFs",
    goal="Extract and embed key insights from academic and technical PDFs.",
    backstory="A document analyst trained to understand and summarize research papers."
)

# news_agent = Agent(
#     name="NewsSummarizer",
#     role="Fetches and embeds news",
#     goal="Summarize and embed the latest AI news for real-time insights.",
#     backstory="A news analyst focused on tracking developments in artificial intelligence."
# )

# Define tasks
scrape_task = Task(
    description="Scrape and embed content from a URL",
    expected_output="Cleaned text content from the web page embedded into the vector store.",
    agent=web_agent
)

pdf_task = Task(
    description="Extract and embed content from a PDF",
    expected_output="Text extracted from the PDF and embedded into the vector store.",
    agent=pdf_agent
)

# news_task = Task(
#     description="Fetch and embed AI news",
#     expected_output="Summarized AI news articles embedded into the vector store.",
#     agent=news_agent
# )

# Define crew
research_crew = Crew(
    name="ResearchAssistant",
    agents=[web_agent, pdf_agent],
    tasks=[scrape_task, pdf_task]
)
