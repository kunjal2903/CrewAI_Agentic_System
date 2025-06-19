from bs4 import BeautifulSoup

def clean_html(html_content: str) -> str:
    if not isinstance(html_content, str):
        raise ValueError("Expected HTML content as a string")

    soup = BeautifulSoup(html_content, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator=' ', strip=True)
    return text

