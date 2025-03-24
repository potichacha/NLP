import requests
from bs4 import BeautifulSoup
import os
import re
import wikipedia

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
CATEGORIES = {
    "recette": "https://www.marmiton.org/recettes/index/categorie/plat-principal/page/{}",
    "histoire": "https://fr.wikipedia.org/wiki/Spécial:Page_au_hasard_dans_une_catégorie/Histoire"
}

BASE_DIR_RAW = "data/raw"
BASE_DIR_PROCESSED = "data/processed"
MAX_CHARS = 3000


def clean_and_trim_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:MAX_CHARS]


def scrape_recipes(category, url_pattern, max_recipes=200):
    output_dir_raw = f"{BASE_DIR_RAW}/{category}"
    output_dir_processed = f"{BASE_DIR_PROCESSED}/{category}"

    os.makedirs(output_dir_raw, exist_ok=True)
    os.makedirs(output_dir_processed, exist_ok=True)

    recipe_count = 0
    page = 1

    while recipe_count < max_recipes:
        response = requests.get(url_pattern.format(page), headers=HEADERS)
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

            filename_raw = f"{output_dir_raw}/{category}_{recipe_count + 1}.txt"
            with open(filename_raw, "w", encoding="utf-8") as file:
                file.write(recipe_text)

            processed_text = clean_and_trim_text(recipe_text)
            filename_processed = f"{output_dir_processed}/{category}_{recipe_count + 1}.txt"
            with open(filename_processed, "w", encoding="utf-8") as file:
                file.write(processed_text)

            recipe_count += 1
            print(f"{category.capitalize()} {recipe_count}: {title} téléchargée et traitée")

        page += 1


def scrape_wikipedia_history(category, max_articles=1000):
    output_dir_raw = f"{BASE_DIR_RAW}/{category}"
    output_dir_processed = f"{BASE_DIR_PROCESSED}/{category}"

    os.makedirs(output_dir_raw, exist_ok=True)
    os.makedirs(output_dir_processed, exist_ok=True)

    wikipedia.set_lang("fr")
    articles_downloaded = 0

    while articles_downloaded < max_articles:
        try:
            random_page = requests.get(CATEGORIES["histoire"], headers=HEADERS).url
            title = random_page.split("/wiki/")[-1]
            title = title.replace('_', ' ')

            content = wikipedia.page(title).content

            filename_raw = f"{output_dir_raw}/{category}_{articles_downloaded + 1}.txt"
            with open(filename_raw, "w", encoding="utf-8") as file:
                file.write(content)

            processed_text = clean_and_trim_text(content)
            filename_processed = f"{output_dir_processed}/{category}_{articles_downloaded + 1}.txt"
            with open(filename_processed, "w", encoding="utf-8") as file:
                file.write(processed_text)

            articles_downloaded += 1
            print(f"{category.capitalize()} {articles_downloaded}: {title} téléchargé et traité")

        except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError) as e:
            print(f"Erreur ou ambiguïté pour la page {title}, page ignorée.")
            continue


if __name__ == "__main__":
    scrape_recipes("recette", CATEGORIES["recette"], max_recipes=1000)
    scrape_wikipedia_history("histoire", max_articles=1000)