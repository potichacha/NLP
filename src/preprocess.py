import re
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text, language='french')
    cleaned_text = ' '.join(tokens)
    return cleaned_text
