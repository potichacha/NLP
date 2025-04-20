from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
import joblib

# ✅ Ajout de l'import de MODEL_PATH
from config import DATA_DIR, TEST_SIZE, RANDOM_STATE, MAX_FEATURES, STOP_WORDS, MODEL_PATH

from data import load_data
from preprocess import preprocess_text

def train_calibrated_svm():
    texts, labels = load_data(DATA_DIR)
    texts = [preprocess_text(text) for text in texts]

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    vectorizer = TfidfVectorizer(max_features=MAX_FEATURES, stop_words=STOP_WORDS)
    base_svm = LinearSVC(random_state=RANDOM_STATE)
    calibrated_svm = CalibratedClassifierCV(base_svm)

    model = Pipeline([
        ('vectorizer', vectorizer),
        ('classifier', calibrated_svm)
    ])

    print("Entraînement du modèle SVM calibré...")
    model.fit(X_train, y_train)

    joblib.dump(model, MODEL_PATH)
    print(f"Modèle calibré sauvegardé dans : {MODEL_PATH}")

if __name__ == "__main__":
    train_calibrated_svm()