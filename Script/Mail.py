from datasets import load_dataset
import os
import logging

# === CONFIGURATION ===
DATASET_NAME = "rtweera/customer_care_emails"
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Data/Processed/Mail"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

MAX_FILES = 1000
MAX_CHARS = 3000

# === LOGGING ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("📬 Début de l'extraction des mails")

# === Chargement du dataset en streaming
dataset = load_dataset(DATASET_NAME, split="train", streaming=True)
logging.info(f"📦 Dataset '{DATASET_NAME}' chargé en mode streaming.")

# === Traitement
count = 0
for row in dataset:
    text = row.get("message_body", "")
    if not isinstance(text, str) or len(text.strip()) < 200:
        continue

    trimmed = text[:MAX_CHARS].strip()
    file_path = os.path.join(OUTPUT_DIR, f"mail_{count + 1}.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(trimmed)

    logging.info(f"✅ Mail {count + 1} sauvegardé")
    count += 1
    if count >= MAX_FILES:
        break

logging.info(f"🏁 Extraction terminée : {count} mails sauvegardés dans '{OUTPUT_DIR}'")