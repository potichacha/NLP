import requests
from bs4 import BeautifulSoup
import os
import re

BASE_URL = "https://www.marmiton.org/recettes/index/categorie/plat-principal/?page={}"
HEADERS = {'User-Agent': 'Mozilla/5.0'}
OUTPUT_DIR = "data/processed/recette"
MAX_CHARS = 3000

os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_and_trim_text(text):
    return re.sub(r'\s+', ' ', text).strip()[:MAX_CHARS]

def scrape_recipes(max_recipes=1000):
    count, page = 0, 1
    while count < max_recipes:
        response = requests.get(BASE_URL.format(page), headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")

        recipes = soup.select("a.recipe-card-link")
        if not recipes:
            print("Aucune recette trouvée sur cette page, fin du scraping.")
            break

        for recipe in recipes:
            if count >= max_recipes:
                break

            recipe_url = "https://www.marmiton.org" + recipe["href"]
            recipe_page = requests.get(recipe_url, headers=HEADERS)
            recipe_soup = BeautifulSoup(recipe_page.content, "html.parser")

            title_tag = recipe_soup.select_one("h1.recipe-header__title")
            steps_tags = recipe_soup.select("div.recipe-step-list__container p")

            if title_tag and steps_tags:
                title = title_tag.text.strip()
                steps = ' '.join(step.text.strip() for step in steps_tags)
                content = clean_and_trim_text(title + "\n\n" + steps)

                with open(f"{OUTPUT_DIR}/recette_{count + 1}.txt", "w", encoding="utf-8") as file:
                    file.write(content)

                print(f"Recette {count+1}: {title}")
                count += 1
            else:
                print(f"Échec extraction pour {recipe_url}")

        page += 1

if __name__ == "__main__":
    scrape_recipes(max_recipes=1)