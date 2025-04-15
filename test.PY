# ca c'est pour chopper les recettes sur marmiton le reuf

from bs4 import BeautifulSoup
import rillette
import unicodedata
import re

def clean(text):
    # Remove accents
    text = ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )
    # Encode to ASCII with placeholder, decode back
    text = text.encode('ascii', 'replace').decode()
    # Collapse all whitespace into a single space
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Clean and parse HTML
texte = clean(rillette.marmiton)
soup = BeautifulSoup(texte, 'html.parser')

# Find the step list container
step_div = soup.find('div', class_='recipe-step-list')

if step_div:
    # Remove empty tags
    for tag in step_div.find_all():
        if not tag.get_text(strip=True):
            tag.decompose()

    # Get the cleaned text with custom separator
    result = step_div.get_text(separator=' ', strip=True)
    print(result)
else:
    print("No .recipe-step-list div found.")
