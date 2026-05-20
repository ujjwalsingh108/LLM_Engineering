import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_page_content(url: str) -> str:
    """
    Fetches the content of a web page given its URL.
    - Normalizes missing schemes (adds https:// if needed).
    - Removes irrelevant tags (script, style, etc.).
    - Returns title + cleaned body text, truncated to 4000 characters.
    """
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()  # fail fast on bad responses

    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string.strip() if soup.title else "No Title"

    if soup.body:
        for irrelevant in soup(["script", "style", "noscript", "iframe", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""

    return (title + "\n\n" + text)[:4000]


def fetch_page_links(url: str) -> list[str]:
    """
    Fetches all absolute links from a web page.
    - Converts relative links to absolute using urljoin.
    - Filters only http/https links.
    - Returns a unique list of links.
    """
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    links = set()

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"].strip()
        absolute_url = urljoin(url, href)
        if absolute_url.startswith(("http://", "https://")):
            links.add(absolute_url)

    return sorted(links)
