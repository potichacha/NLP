import joblib
import sys
from preprocess import preprocess_text
from config import MODEL_PATH

def predict_category(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    content = preprocess_text(content)
    model = joblib.load(MODEL_PATH)
    prediction = model.predict([content])[0]
    return prediction

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python predict.py <chemin_fichier>")
        sys.exit(1)

    filepath = sys.argv[1]
    print(f"La catégorie prédite est : {predict_category(filepath)}")
