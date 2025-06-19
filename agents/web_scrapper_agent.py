
import httpx
import certifi
import asyncio
import fitz # PyMuPDF
from utils.html_cleaner import clean_html
from vectorstore.faiss_handler import FAISSHandler
from bs4 import BeautifulSoup

class WebScraperAgent:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        self.vector_store = FAISSHandler()

    async def fetch(self, url):
        try:
            async with httpx.AsyncClient(verify=certifi.where(), headers=self.headers, timeout=10.0) as client:
                resp = await client.get(url)
                return resp.text, url, resp.headers.get("content-type", ""), resp.status_code
        except Exception as e:
            print(f"⚠️ Fetch failed for {url}: {e}")
            return "", url, "", 0

    def extract_text_from_pdf(self, content_bytes: bytes):
        try:
            doc = fitz.open(stream=content_bytes, filetype="pdf")
            return "\n".join([page.get_text() for page in doc])
        except Exception as e:
            print("PDF parsing error:", e)
            return ""

    async def process_url(self, url):
        try:
            async with httpx.AsyncClient(verify=certifi.where(), headers=self.headers, timeout=15.0) as client:
                response = await client.get(url)

            if response.status_code != 200:
                return None

            content_type = response.headers.get("content-type", "")
            if "application/pdf" in content_type:
                text = self.extract_text_from_pdf(response.content)
            else:
                soup = BeautifulSoup(response.text, "html.parser")
                cleaned = clean_html(str(soup))
                text = cleaned

            if text:
                return {"url": url, "content": text}
        except Exception as e:
            print(f"Error scraping {url}:", e)
            return None

    async def scrape_all(self, urls: list[str]):
        tasks = [self.process_url(url) for url in urls]
        results = await asyncio.gather(*tasks)
        valid_docs = [res for res in results if res]
        self.vector_store.add_documents(valid_docs)
        return valid_docs
