from datasets import load_dataset
import os
import logging
import re
from textwrap import wrap
import time

# === CONFIGURATION ===
DATASET_NAME = "Nadav/historical_texts"
OUTPUT_DIR = "../Data/Raw/histoire"
os.makedirs(OUTPUT_DIR, exist_ok=True)

MAX_FILES = 1000
CHUNK_SIZE = 500

# === LOGGING ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("📚 Début de l'extraction du dataset historique")

# === REGEX : texte occidental seulement
latin_regex = re.compile(r'^[\x20-\x7EÀ-ÿ\s\n\r.,!?;:()\[\]\"\'%€$£@#&*+=<>/-]+$')

def is_latin_only(text: str) -> bool:
    return bool(latin_regex.match(text))

# === Dictionnaire vieil anglais -> moderne ===
archaic_to_modern = {
    "thou": "you", "thee": "you", "thy": "your", "thine": "yours", "hath": "has",
    "doth": "does", "art": "are", "shalt": "shall", "wilt": "will", "ye": "you",
    "nay": "no", "aye": "yes", "whence": "from where", "wherefore": "why", "thither": "there",
    "hither": "here", "betwixt": "between", "nigh": "near", "aught": "anything",
    "naught": "nothing", "anon": "soon", "oft": "often", "unto": "to", "imployment": "employment",
    "governour": "governor", "governours": "governors", "aforesaid": "previously mentioned",
    "inhabitants": "residents", "abode": "residence", "dispose": "arrange", "thereof": "of that",
    "hereby": "by this", "forthwith": "immediately", "divers": "various", "especial": "special",
    "whereas": "considering that", "doe": "do", "maketh": "makes", "giveth": "gives",
    "beginneth": "begins", "settleth": "settles", "requireth": "requires",
    "leeve": "believe", "majestie": "majesty", "saith": "says", "parliamenti": "parliament",
    "banish": "expel", "meddle": "interfere", "obedience": "compliance", "councel": "council"
}

def translate_archaic(text: str) -> str:
    words = text.split()
    translated = [archaic_to_modern.get(word.lower(), word) for word in words]
    return ' '.join(translated)

# === Chargement en streaming
try:
    dataset = load_dataset(DATASET_NAME, split="train", streaming=True)
    logging.info(f"📦 Dataset '{DATASET_NAME}' chargé en mode streaming.")
except Exception as e:
    logging.error(f"❌ Échec du chargement du dataset : {e}")
    exit(1)

# === Traitement avec découpage par mot (sans couper de mot)
count = 0
for row in dataset:
    if count >= MAX_FILES:
        break

    try:
        text = row.get("text", "").strip()
        if not text or not is_latin_only(text):
            continue

        text = translate_archaic(text)
        words = text.split()
        chunk = []
        chunk_len = 0

        for word in words:
            if chunk_len + len(word) + 1 > CHUNK_SIZE:
                with open(os.path.join(OUTPUT_DIR, f"histoire_{count + 1}.txt"), "w", encoding="utf-8") as f:
                    f.write(' '.join(chunk))
                logging.info(f"✅ Chunk sauvegardé : histoire_{count + 1}.txt")
                count += 1
                if count >= MAX_FILES:
                    break
                chunk = [word]
                chunk_len = len(word) + 1
            else:
                chunk.append(word)
                chunk_len += len(word) + 1

        if chunk and count < MAX_FILES:
            with open(os.path.join(OUTPUT_DIR, f"histoire_{count + 1}.txt"), "w", encoding="utf-8") as f:
                f.write(' '.join(chunk))
            logging.info(f"✅ Chunk sauvegardé : histoire_{count + 1}.txt")
            count += 1

    except KeyboardInterrupt:
        logging.warning("⛔️ Interruption manuelle détectée. Sauvegarde des fichiers déjà traités…")
        break
    except Exception as e:
        logging.warning(f"⚠️ Une erreur est survenue lors du traitement d'une ligne : {e}")
        time.sleep(1)
        continue

logging.info(f"🏁 Terminé : {count} fichiers sauvegardés dans '{OUTPUT_DIR}'")