import requests
import wikipedia
import os
import re

BASE_DIR_PROCESSED = "../data/processed/wikipedia"
MAX_CHARS = 3000
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def clean_and_trim_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:MAX_CHARS]

def scrape_wikipedia_random(max_articles=1000):
    processed_dir = BASE_DIR_PROCESSED
    os.makedirs(processed_dir, exist_ok=True)
    wikipedia.set_lang("fr")

    count = 0
    while count < max_articles:
        try:
            # Page Wikipédia totalement aléatoire (aucune catégorie imposée)
            random_page_url = requests.get("https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard", headers=HEADERS).url
            title = random_page_url.split("/wiki/")[-1].replace('_', ' ')
            content = wikipedia.page(title).content

            processed = clean_and_trim_text(content)
            with open(f"{processed_dir}/{count+1}.txt", "w", encoding="utf-8") as f:
                f.write(processed)

            count += 1
            print(f"{count}: {title}")

        except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
            continue

if __name__ == "__main__":
    scrape_wikipedia_random(max_articles=1000)