from datasets import load_dataset
import os
import logging
from scrapper import clean
# === CONFIGURATION ===
DATASET_NAME = "harvard-lil/cold-french-law"
OUTPUT_DIR = "Data/Processed/Juridique"
os.makedirs(OUTPUT_DIR, exist_ok=True)

MAX_FILES = 1000
MAX_CHARS = 3000

# === LOGGING ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("Début de l'extraction du dataset juridique")

# === Chargement en streaming
dataset = load_dataset(DATASET_NAME, split="train", streaming=True)
logging.info(f"Dataset '{DATASET_NAME}' chargé en mode streaming.")

# === Chargement des textes existants pour comparaison
existing_texts = set()
for filename in os.listdir(OUTPUT_DIR):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.isfile(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            existing_texts.add(f.read().strip())

# === Traitement
count = 0
new = 0
for row in dataset:
    if new==4: break
    
    texte = row.get("article_contenu_text")
    
    if isinstance(texte, list):
        texte = " ".join(texte)
    if not texte or len(texte) < 200:
        logging.debug("Texte trop court ou vide, ignoré")
        continue

    trimmed = texte[:MAX_CHARS].strip()

    if trimmed in existing_texts:
        logging.debug("Texte déjà existant, ignoré")
        continue

    try:
        with open(os.path.join(f"src/TestData/test_juridique{count + 1}.txt"), "w", encoding="utf-8") as f:
            f.write(clean(trimmed))
            new+=1
        logging.info(f"Article {count + 1} sauvegardé")
        count += 1
    except Exception as e:
        logging.warning(f"Erreur sauvegarde fichier {count + 1}: {e}")
        continue

    if count >= MAX_FILES:
        break

logging.info(f"Extraction terminée : {count} fichiers juridiques sauvegardés dans '{OUTPUT_DIR}'")