from bs4 import BeautifulSoup
import requests

# standard headers to fetch a web page
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def fetch_page_content(url):
    """Fetches the content of a web page given its URL. Truncate to 4,000 characters."""
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No Title"
    print(f"Fetched page title: {title}")
    if soup.body:
        for irrelevant in soup(["script", "style", "noscript", "iframe", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    
    else:
        text = ""
    return (title + "\n\n" + text)[:4000]
