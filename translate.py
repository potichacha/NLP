import asyncio
from googletrans import Translator
import sys
import os
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import scrapper


archaic_to_modern = {
    "thou": "you",
    "thee": "you",
    "thy": "your",
    "thine": "yours",
    "hath": "has",
    "dost": "do",
    "art": "are",
    "wilt": "will",
    "shalt": "shall",
    "wouldst": "would",
    "couldst": "could",
    "methinks": "I think",
    "anon": "soon",
    "wherefore": "why",
    "’tis": "it is",
    "generall": "general",
    "kingdome": "kingdom",
    "moneth": "month",
    "VVe": "we",
    "VVHen": "when",
    "Our Consent unto it": "our agreement to it",
    "duely": "duly",
    "fit to be exercised": "appropriate to practice",
    "publicke": "public",
    "pretence of Religion": "pretense of religion",
    "Lecturers": "preachers",
    "reliefe": "relief",
    "Meanes": "means",
    "Hypocriticall": "hypocritical",
    "slaunder of true Religion": "slander of true religion",
    "Traiterous": "treasonous",
    "Humiliation": "spiritual humbling",
    "owne": "own",
    "thereof": "of that",
    "ought to doe without": "should not do without",
    "expresly Charge and Command": "formally order",
    "solemne": "solemn",
    "powre out": "pour out",
    "avoyding": "avoiding",
    "Malitious": "malicious",
    "setling": "settling",
}

def preprocess():
    filename = "tempo.txt"
    output =  f"Data/Processed/Histoire/histoire_{scrapper.load_variable()+1}.txt"
    good = True
    print(filename)
    with open(filename,'r') as f:
        fichier = scrapper.clean(f.read())
        texte = ""
        #if (len(fichier)<1500):
            #good = False
    if good:
        for line in fichier.splitlines():
            if line == "\n":
                continue
            else:
                line = scrapper.clean(line)
                texte+=" "+(line)
            #if line.endswith("}") or line.endswith("}\n"):
                #texte += re.sub(r"\{ *'user': *'(Chat GPT|Anonymous)', 'message': (\"|\')", ' ', line)
                #texte = re.sub(r"(\'|\")}", '', texte)
                #texte = texte.replace("\n", " ")
            
    
        with open(output, "w", encoding="utf-8") as file:
            file.write(texte)
            print(f"{scrapper.load_variable()+1} ")
    else:
        print(f"{scrapper.load_variable()+1} deleted!")

async def translate_file(file_path):
    # Step 1: Read the file content
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
        text = scrapper.clean(text)
        sentences = re.split(r'(?<=[.!?]) +', text)

    # Step 2: Create the translator and translate the text
    translator = Translator()
    translation=''

    # Step 3: Print or return the translated text
    for sentence in sentences:
        temp = await translator.translate(sentence, dest='fr')
        translation+=" "+temp.text

    with open("tempo.txt", "w", encoding='utf-8') as t:
        t.write(clean_to_last_punctuation(translation))

def clean_to_last_punctuation(text):
    match = re.search(r'^(.*?[.!?,;])[^.!?,;]*$', text.strip())
    return match.group(1) if match else text

# Run the async function
compteur = 0
while scrapper.load_variable() < 1000:
    asyncio.run(translate_file(f'Data/Raw/Histoire/histoire_{scrapper.load_variable()+1}.txt'))
    try:
        preprocess()
    except:
        print(f'erreur avec histoire_{scrapper.load_variable()+1}.txt')
    scrapper.save_variable(scrapper.load_variable()+1)

if compteur!=0:
    print(f"{compteur} erreurs ont eu lieu sur 1000 fichiers")

