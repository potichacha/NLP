import joblib
import sys
import os
from preprocess import preprocess_text

# ✅ Chemin corrigé
MODEL_PATH = "../Models/classifier_linear_svm_calibrated.joblib"

def predict_category_with_proba(filepath):
    if not os.path.exists(filepath):
        print(f"❌ Fichier non trouvé : {filepath}")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read().strip()

    if not content:
        print(f"⚠️ Le fichier est vide : {filepath}")
        sys.exit(1)

    content = preprocess_text(content)

    try:
        model = joblib.load(MODEL_PATH)
    except Exception as e:
        print(f"❌ Erreur lors du chargement du modèle : {e}")
        sys.exit(1)

    try:
        probabilities = model.predict_proba([content])[0]
        categories = model.classes_
        results = sorted(zip(categories, probabilities), key=lambda x: x[1], reverse=True)
        return results
    except Exception as e:
        print(f"❌ Erreur pendant la prédiction : {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python predict.py <chemin_fichier>")
        sys.exit(1)

    filepath = sys.argv[1]
    results = predict_category_with_proba(filepath)
    print(f"\n📄 Résultats de la classification pour : {filepath}\n")
    for label, score in results:
        print(f"{label} : {score:.2%}")