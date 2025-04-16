import requests
import time
import logging
import os

# === CONFIG ===
OUTPUT_FILE = "valid_article_urls.txt"
LAST_ID_FILE = "last_successful_id.txt"
MAX_VALID = 1000          # nombre d'articles valides à trouver
MAX_TRIES = 1000000       # nombre total de tentatives (sécurité)
BASE_URL = "https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI{:012d}"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}

# === LOGGING ===
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def get_last_successful_id():
    if os.path.exists(LAST_ID_FILE):
        with open(LAST_ID_FILE, "r") as f:
            return int(f.read().strip())
    return 0


def save_last_successful_id(article_id):
    with open(LAST_ID_FILE, "w") as f:
        f.write(str(article_id))


def is_valid_article(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200 and "<h1" in response.text and "class=\"content\"" in response.text:
            return True
    except Exception as e:
        logging.debug(f"Erreur lors de la requête {url} : {e}")
    return False


def main():
    logging.info("🔍 Début de la génération de liens valides")

    valid_links = []
    tried = 0
    current = get_last_successful_id()

    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        while len(valid_links) < MAX_VALID and tried < MAX_TRIES:
            url = BASE_URL.format(current)
            tried += 1

            if is_valid_article(url):
                valid_links.append(url)
                f.write(url + "\n")
                save_last_successful_id(current)
                logging.info(f"✅ {len(valid_links)}/{MAX_VALID} - Article valide : {url}")
            else:
                logging.info(f"❌ Invalide : {url}")

            current += 1
            time.sleep(0.2)

    logging.info(f"🎯 Terminé : {len(valid_links)} liens valides sauvegardés dans {OUTPUT_FILE}")


if __name__ == "__main__":
    main()