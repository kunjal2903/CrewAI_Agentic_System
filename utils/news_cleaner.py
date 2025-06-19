from bs4 import BeautifulSoup

def clean_html(raw_html : str)->str:
    try:
        return BeautifulSoup(raw_html , "html.parser").get_text()
    except Exception:
        return str(raw_html)
