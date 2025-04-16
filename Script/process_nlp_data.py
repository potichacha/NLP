import os
import re
import nltk
from nltk.tokenize import word_tokenize
from googletrans import Translator

# Télécharger le tokenizer NLTK si besoin
nltk.download('punkt')

# Initialisation du traducteur
translator = Translator()

# Dossiers d'entrée et de sortie
DATA_RAW_DIR = "data/raw"
DATA_PROCESSED_DIR = "data/processed"
MAX_CHARS = 3000

# Créer le dossier de sortie si besoin
os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)

# Nettoyage + Traduction
def clean_and_translate(text):
    try:
        # Traduction automatique EN -> FR
        translated = translator.translate(text, dest='fr').text
    except Exception as e:
        print(f"❌ Erreur de traduction : {e}")
        translated = text  # fallback en cas d’erreur

    # Nettoyage classique
    translated = translated.lower()
    translated = re.sub(r'\d+', '<NUM>', translated)
    translated = re.sub(r'[^\w\s\'.,!?]', ' ', translated)
    translated = re.sub(r'\s+', ' ', translated).strip()

    # Tokenisation
    tokens = word_tokenize(translated, language='french')
    return ' '.join(tokens)[:MAX_CHARS]

# Traitement global
def process_all():
    for category in os.listdir(DATA_RAW_DIR):
        raw_category_path = os.path.join(DATA_RAW_DIR, category)
        processed_category_path = os.path.join(DATA_PROCESSED_DIR, category)
        os.makedirs(processed_category_path, exist_ok=True)

        for file_name in os.listdir(raw_category_path):
            if not file_name.endswith(".txt"):
                continue

            input_path = os.path.join(raw_category_path, file_name)
            output_path = os.path.join(processed_category_path, file_name)

            with open(input_path, "r", encoding="utf-8") as f:
                text = f.read()

            print(f"🔄 Traitement de {category}/{file_name} ...")
            cleaned_text = clean_and_translate(text)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(cleaned_text)

            print(f"✅ {category}/{file_name} traduit et nettoyé")

    print("\n🎯 Toutes les données ont été traitées et traduites.")

# Point d’entrée
if __name__ == "__main__":
    process_all()