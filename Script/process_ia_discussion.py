import re
import os

INPUT_DIR = "../Data/Processed/IA"
OUTPUT_DIR = "../Data/Processed/IA"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_messages(text):
    # Extraire seulement les messages textuels (sans user/message JSON)
    messages = re.findall(r"'message':\s*\"(.*?)\"|'message':\s*'(.*?)'", text, re.DOTALL)
    
    # Garder uniquement les messages (choisir la capture non-vide)
    clean_messages = [msg[0] if msg[0] else msg[1] for msg in messages]
    
    # Combiner les messages avec séparation claire
    return "\n\n".join(msg.strip() for msg in clean_messages)

def process_ia_discussions():
    for file_name in os.listdir(INPUT_DIR):
        with open(os.path.join(INPUT_DIR, file_name), 'r', encoding='utf-8') as f:
            raw_text = f.read()

        cleaned_text = extract_messages(raw_text)

        with open(os.path.join(OUTPUT_DIR, file_name), 'w', encoding='utf-8') as f:
            f.write(cleaned_text)

    print("✅ Discussions IA traitées, superflu supprimé avec succès.")

if __name__ == "__main__":
    process_ia_discussions()