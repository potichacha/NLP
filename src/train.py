from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib
from config import DATA_DIR, MODEL_PATH, TEST_SIZE, RANDOM_STATE, MAX_FEATURES, STOP_WORDS
from data import load_data
from preprocess import preprocess_text

def train_and_evaluate_models():
    texts, labels = load_data(DATA_DIR)
    texts = [preprocess_text(text) for text in texts]

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    models = {
        'naive_bayes': MultinomialNB(),
        'random_forest': RandomForestClassifier(random_state=RANDOM_STATE),
        'linear_svm': LinearSVC(random_state=RANDOM_STATE)
    }

    for name, classifier in models.items():
        print(f"\nEntraînement et évaluation : {name}")
        model = Pipeline([
            ('vectorizer', TfidfVectorizer(max_features=MAX_FEATURES, stop_words=STOP_WORDS)),
            ('classifier', classifier)
        ])

        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        print(classification_report(y_test, predictions))

        model_path = f"{MODEL_PATH}_{name}.joblib"
        joblib.dump(model, model_path)
        print(f"Modèle sauvegardé dans {model_path}")

if __name__ == "__main__":
    train_and_evaluate_models()