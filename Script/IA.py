from datasets import load_dataset
import os
import logging

# === CONFIGURATION ===
DATASET_NAME = "P1ayer-1/chatgpt-conversations-chatlogs.net"
OUTPUT_DIR = "IA"
os.makedirs(OUTPUT_DIR, exist_ok=True)

MAX_FILES = 1000
MAX_CHARS = 3000

# === LOGGING ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("🚀 Début de l'extraction du dataset IA")

# === Chargement en streaming
dataset = load_dataset(DATASET_NAME, split="train", streaming=True)
logging.info(f"📦 Dataset '{DATASET_NAME}' chargé en mode streaming.")

# === Traitement et sauvegarde
count = 0
for row in dataset:
    # On cible explicitement le champ "conversation"
    conv = row.get("conversation")
    if isinstance(conv, list):
        content = "\n".join([str(msg).strip() for msg in conv if msg])
    else:
        # fallback si "conversation" pas là
        content = row.get("text", "")

    trimmed = content[:MAX_CHARS].strip()
    if not trimmed:
        continue

    with open(os.path.join(OUTPUT_DIR, f"ia_{count + 1}.txt"), "w", encoding="utf-8") as f:
        f.write(trimmed)

    logging.info(f"✅ Fichier IA {count + 1} sauvegardé")
    count += 1
    if count >= MAX_FILES:
        break

logging.info(f"🏁 Terminé : {count} fichiers sauvegardés dans '{OUTPUT_DIR}'")