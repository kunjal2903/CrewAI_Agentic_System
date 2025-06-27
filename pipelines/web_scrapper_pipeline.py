from agents.web_scrapper_agent import CombinedScraperAgent

async def run_scraper_pipeline(url: str, max_depth: int = 2):
     agent = CombinedScraperAgent()
     results = await agent.search_and_scrape(url, max_depth=max_depth)

     return results
