from datasets import load_dataset
from transformers import pipeline
import os

# === CONFIGURATION ===
OUTPUT_DIR = "TranslatedTexts"
os.makedirs(OUTPUT_DIR, exist_ok=True)
MAX_FILES = 1000
MAX_CHARS = 3000
DATASET_NAME = "wikihow"
LANGUAGE_MODEL = "Helsinki-NLP/opus-mt-en-fr"

# === Load dataset ===
dataset = load_dataset(DATASET_NAME, split="train")

# === Load translation pipeline ===
translator = pipeline("translation", model=LANGUAGE_MODEL)

# === Process and save translated texts ===
count = 0
for item in dataset:
    text = item.get("text", "")
    if not text or len(text) < 200:
        continue

    try:
        translation = translator(text[:1000], max_length=512)[0]['translation_text']
        trimmed = translation[:MAX_CHARS].strip()

        with open(os.path.join(OUTPUT_DIR, f"text_{count+1}.txt"), "w", encoding="utf-8") as f:
            f.write(trimmed)

        count += 1
        print(f"✅ Fichier {count} sauvegardé")
        if count >= MAX_FILES:
            break
    except Exception as e:
        print(f"⚠️ Erreur : {e}")
        continue