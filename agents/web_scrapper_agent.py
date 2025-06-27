import aiohttp
import asyncio
import hashlib
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

class CombinedScraperAgent:
    def __init__(self, serpapi_key=None):
        self.serpapi_key = serpapi_key or os.getenv("SERPAPI_KEY")
        print(f"[DEBUG] Using SerpAPI Key: {self.serpapi_key}")
        self.visited = set()
        self.nav_footer_links = set()
        self.previous_hashes = {}

    def hash_content(self, content):
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def search_with_serpapi(self, url_query):
        params = {
            "engine": "google",
            "q": url_query,
            "api_key": self.serpapi_key,
            "num": 10
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        print(f"[DEBUG] Full SerpAPI response: {results}")
        if "error" in results:
            print(f"[ERROR] SerpAPI returned an error: {results['error']}")
            return []
        links = [result["link"] for result in results.get("organic_results", []) if "link" in result]
        print(f"[DEBUG] Extracted URLs: {links}")
        return links

    async def fetch_html(self, url):
        headers = {"User-Agent": "Mozilla/5.0"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    raise Exception(f"HTTP {response.status} for {url}")
                return await response.text()

    def extract_nav_footer_links(self, soup, base_url):
        nav_footer_links = set()
        for section in soup.find_all(['nav', 'footer']):
            for a in section.find_all('a', href=True):
                absolute_link = urljoin(base_url, a['href'])
                nav_footer_links.add(absolute_link)
        return nav_footer_links

    def save_html(self, base_folder, url, html):
        parsed_url = urlparse(url)
        path = parsed_url.path.strip("/").replace("/", "_") or "home"
        folder_path = os.path.join(base_folder, path)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, "page.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

    async def scrape_recursive(self, url, base_url, depth, max_depth, results, base_folder="scraped_pages"):
        if depth > max_depth or url in self.visited:
            return
        self.visited.add(url)

        try:
            print(f"[SCRAPING] {url} (Depth: {depth})")
            html = await self.fetch_html(url)
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text()

            self.save_html(base_folder, url, html)

            results.append({
                "url": url,
                "content": text[:1000]
            })

            if depth == 0:
                self.nav_footer_links = self.extract_nav_footer_links(soup, base_url)

            for a in soup.find_all("a", href=True):
                link = urljoin(url, a["href"])
                if (
                    urlparse(link).netloc == urlparse(base_url).netloc
                    and link not in self.nav_footer_links
                ):
                    await self.scrape_recursive(link, base_url, depth + 1, max_depth, results, base_folder)

        except Exception as e:
            print(f"[ERROR] Failed to scrape {url}: {e}")
            results.append({
                "url": url,
                "error": str(e)
            })

    async def search_and_scrape(self, query, max_depth=2, output_folder="scraped_pages"):
        urls = self.search_with_serpapi(query)
        if not urls:
            return {"error": "No URLs found from SerpAPI."}

        base_url = urls[0]
        print(f"[INFO] Scraping top result: {base_url}")

        results = []
        await self.scrape_recursive(base_url, base_url, 0, max_depth, results, base_folder=output_folder)
        return results

    async def scrape_and_check(self, url):
        try:
            print(f"[DEBUG] Fetching: {url}")
            html = await self.fetch_html(url)
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text()
            new_hash = self.hash_content(text)

            if url not in self.previous_hashes or self.previous_hashes[url] != new_hash:
                print(f"[Change Detected] {url}")
                self.previous_hashes[url] = new_hash
            else:
                print(f"[No Change] {url}")
        except Exception as e:
            print(f"[Error] Failed to scrape {url}: {e}")

    async def run_realtime(self, query, interval=60):
        while True:
            print(f"\n[Cycle Start] Searching for: {query}")
            urls = self.search_with_serpapi(query)

            tasks = [self.scrape_and_check(url) for url in urls]
            await asyncio.gather(*tasks)

            print(f"[Cycle Complete] Sleeping for {interval} seconds...\n")
            await asyncio.sleep(interval)

    async def run_once(self, query):
        print(f"[Run Once] Searching for: {query}")
        urls = self.search_with_serpapi(query)
        results = []

        for url in urls:
            try:
                html = await self.fetch_html(url)
                soup = BeautifulSoup(html, "html.parser")
                text = soup.get_text()
                results.append({
                    "url": url,
                    "content": text[:1000]
                })
            except Exception as e:
                print(f"[Error] Failed to scrape {url}: {e}")
                results.append({
                    "url": url,
                    "error": str(e)
                })

        return results
