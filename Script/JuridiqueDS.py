import requests
import os
import re
from bs4 import BeautifulSoup

BASE_URL = "https://eur-lex.europa.eu/search.html?type=named&DD_YEAR=2023"
HEADERS = {'User-Agent': 'Mozilla/5.0'}
BASE_DIR_PROCESSED = "Data/Processed/Juridique"
MAX_CHARS = 3000

os.makedirs(BASE_DIR_PROCESSED, exist_ok=True)


def clean_and_trim_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:MAX_CHARS]


def scrape_eurlex(max_files=1000):
    downloaded = 0
    page = 1

    while downloaded < max_files:
        url = f"{BASE_URL}&page={page}"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.select("a.title")

        if not links:
            break

        for link in links:
            if downloaded >= max_files:
                break

            doc_url = "https://eur-lex.europa.eu" + link['href']
            doc_response = requests.get(doc_url, headers=HEADERS)
            doc_soup = BeautifulSoup(doc_response.text, 'html.parser')
            text = doc_soup.get_text(separator=' ', strip=True)

            processed = clean_and_trim_text(text)
            with open(f"{BASE_DIR_PROCESSED}/juridique_{downloaded + 1}.txt", "w", encoding="utf-8") as f:
                f.write(processed)

            print(f"Juridique {downloaded + 1}: {link.text.strip()} téléchargé et traité")
            downloaded += 1

        page += 1


if __name__ == "__main__":
    scrape_eurlex(max_files=1000)