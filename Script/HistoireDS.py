import requests, os, re
from bs4 import BeautifulSoup

BASE_URL = "https://gallica.bnf.fr/services/ajax/action/search/"
QUERY = "histoire"
HEADERS = {'User-Agent': 'Mozilla/5.0'}
BASE_DIR_RAW = "../data/raw/gallica_histoire"
BASE_DIR_PROCESSED = "../data/processed/gallica_histoire"
MAX_CHARS = 3000

def clean_and_trim_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:MAX_CHARS]

def scrape_gallica(max_files=1000):
    os.makedirs(BASE_DIR_RAW, exist_ok=True)
    os.makedirs(BASE_DIR_PROCESSED, exist_ok=True)

    downloaded = 0
    page = 1

    while downloaded < max_files:
        params = {
            "query": QUERY,
            "page": page
        }
        response = requests.get(BASE_URL, params=params, headers=HEADERS).json()
        docs = response.get('docs', [])

        if not docs:
            break

        for doc in docs:
            if downloaded >= max_files:
                break

            title = doc['title']
            text = doc.get('texteBrut', '')

            if text:
                with open(f"{BASE_DIR_RAW}/{downloaded+1}.txt", "w", encoding="utf-8") as f:
                    f.write(text)

                processed = clean_and_trim_text(text)
                with open(f"{BASE_DIR_PROCESSED}/{downloaded+1}.txt", "w", encoding="utf-8") as f:
                    f.write(processed)

                print(f"{downloaded+1}: {title}")
                downloaded += 1

        page += 1

if __name__ == "__main__":
    scrape_gallica()