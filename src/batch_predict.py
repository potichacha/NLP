import os
import joblib
from preprocess import preprocess_text

MODEL_PATH = "Models/classifier_linear_svm_calibrated.joblib"
TEST_FOLDER = "src/TestData"

def predict_category_with_proba(text):
    model = joblib.load(MODEL_PATH)
    content = preprocess_text(text)
    probabilities = model.predict_proba([content])[0]
    categories = model.classes_
    return sorted(zip(categories, probabilities), key=lambda x: x[1], reverse=True)

def run_batch_prediction():
    model = joblib.load(MODEL_PATH)
    print("Prédiction sur les fichiers de test...\n")

    for root, _, files in os.walk(TEST_FOLDER):
        for file in files:
            if file.endswith(".txt"):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                results = predict_category_with_proba(content)

                print(f"\n {file}")
                for label, score in results:
                    print(f"  {label} : {score:.2%}")

if __name__ == "__main__":
    run_batch_prediction()