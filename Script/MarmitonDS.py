import requests
from bs4 import BeautifulSoup
import os
import re

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
BASE_URL = "https://www.marmiton.org/recettes/index/categorie/plat-principal/page/{}"
OUTPUT_DIR = "data/processed/recette"
MAX_CHARS = 3000

os.makedirs(OUTPUT_DIR, exist_ok=True)


def clean_and_trim_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:MAX_CHARS]


def scrape_recipes(max_recipes=1000):
    recipe_count = 0
    page = 1

    while recipe_count < max_recipes:
        response = requests.get(BASE_URL.format(page), headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")

        recipes = soup.select(".recipe-card-link")
        if not recipes:
            break

        for recipe in recipes:
            if recipe_count >= max_recipes:
                break

            recipe_url = "https://www.marmiton.org" + recipe["href"]
            recipe_response = requests.get(recipe_url, headers=HEADERS)
            recipe_soup = BeautifulSoup(recipe_response.content, "html.parser")

            title = recipe_soup.select_one("h1").text.strip()
            steps = recipe_soup.select(".recipe-step-list__container p")

            recipe_text = title + "\n\n" + "\n".join(step.text.strip() for step in steps)

            processed_text = clean_and_trim_text(recipe_text)
            filename_processed = f"{OUTPUT_DIR}/Recette_{recipe_count + 1}.txt"
            with open(filename_processed, "w", encoding="utf-8") as file:
                file.write(processed_text)

            recipe_count += 1
            print(f"Recette {recipe_count}: {title} téléchargée et traitée")

        page += 1


if __name__ == "__main__":
    scrape_recipes(1000)