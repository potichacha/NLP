from datasets import load_dataset
import os
import logging
import re

# === CONFIGURATION ===
DATASET_NAME = "P1ayer-1/chatgpt-conversations-chatlogs.net"
OUTPUT_DIR = "IA"
os.makedirs(OUTPUT_DIR, exist_ok=True)

MAX_FILES = 1500
MAX_CHARS = 3000

# === LOGGING ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("🚀 Début de l'extraction du dataset IA")

# === REGEX : accepte seulement alphabet latin + ponctuation “clean”
latin_regex = re.compile(r'^[\x20-\x7EÀ-ÿ\s\n\r.,!?;:()\[\]\'\"%€$£@#&*+=<>/-]+$')

def is_latin_only(text: str) -> bool:
    return bool(latin_regex.match(text))

# === Chargement en streaming
dataset = load_dataset(DATASET_NAME, split="train", streaming=True)
logging.info(f"📦 Dataset '{DATASET_NAME}' chargé en mode streaming.")

# === Traitement et sauvegarde
count = 0
for row in dataset:
    conv = row.get("conversation")
    if isinstance(conv, list):
        content = "\n".join([str(msg).strip() for msg in conv if msg])
    else:
        content = row.get("text", "")

    trimmed = content[:MAX_CHARS].strip()

    # ✅ Skip si texte vide ou contient autre chose que du latin
    if not trimmed or not is_latin_only(trimmed):
        continue

    with open(os.path.join(OUTPUT_DIR, f"ia_{count + 1}.txt"), "w", encoding="utf-8") as f:
        f.write(trimmed)

    logging.info(f"✅ Fichier IA {count + 1} sauvegardé")
    count += 1
    if count >= MAX_FILES:
        break

logging.info(f"🏁 Terminé : {count} fichiers sauvegardés dans '{OUTPUT_DIR}'")