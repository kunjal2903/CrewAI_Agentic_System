from bs4 import BeautifulSoup

def clean_html(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")

    for tag in soup(["script", "style", "noscript", "iframe"]):
        tag.decompose()

    return soup.get_text(separator=" ", strip=True)
