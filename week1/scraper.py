import requests
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

ua = UserAgent()

def get_random_headers():
    return {
        "User-Agent": ua.random, # Automatically picks a real, up-to-date user agent
        "Accept-Language": "en-US,en;q=0.5"
    }

def fetch_website_contents(url):
    """
    Return the title and contents of the website at the given url;
    dynamically rotates headers for production stability.
    """
    # Grab a fresh, randomized header set for this specific request
    current_headers = get_random_headers()
    
    response = requests.get(url, headers=current_headers)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No title found"
    
    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
        
    return (title + "\n\n" + text)[:2_000]

def fetch_website_links(url):
    """
    Return the links on the website at the given url;
    dynamically rotates headers for production stability.
    """
    # Grab a fresh, randomized header set for this specific request
    current_headers = get_random_headers()
    
    response = requests.get(url, headers=current_headers)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]
    return [link for link in links if link]
