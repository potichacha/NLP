import requests, os, re
from bs4 import BeautifulSoup

BASE_URL = "https://eur-lex.europa.eu/search.html?type=named&qid=1686138519786&DD_YEAR=2023"
HEADERS = {'User-Agent': 'Mozilla/5.0'}
BASE_DIR_RAW = "../data/raw/juridique"
BASE_DIR_PROCESSED = "../data/processed/juridique"
MAX_CHARS = 3000

def clean_and_trim_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:MAX_CHARS]

def scrape_eurlex(max_files=1000):
    os.makedirs(BASE_DIR_RAW, exist_ok=True)
    os.makedirs(BASE_DIR_PROCESSED, exist_ok=True)

    downloaded = 0
    page = 1

    while downloaded < max_files:
        url = f"{BASE_URL}&page={page}"
        soup = BeautifulSoup(requests.get(url, headers=HEADERS).text, 'html.parser')
        links = soup.select("a.title")

        if not links:
            break

        for link in links:
            if downloaded >= max_files:
                break

            doc_url = "https://eur-lex.europa.eu" + link['href']
            doc_soup = BeautifulSoup(requests.get(doc_url, headers=HEADERS).text, 'html.parser')
            text = doc_soup.get_text(separator=' ', strip=True)

            with open(f"{BASE_DIR_RAW}/{downloaded+1}.txt", "w", encoding="utf-8") as f:
                f.write(text)

            processed = clean_and_trim_text(text)
            with open(f"{BASE_DIR_PROCESSED}/{downloaded+1}.txt", "w", encoding="utf-8") as f:
                f.write(processed)

            print(f"{downloaded+1}: {link.text.strip()}")
            downloaded += 1

        page += 1

if __name__ == "__main__":
    scrape_eurlex()