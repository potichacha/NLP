from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib
from config import DATA_DIR, MODEL_PATH, TEST_SIZE, RANDOM_STATE, MAX_FEATURES, STOP_WORDS
from data import load_data
from preprocess import preprocess_text

def train_and_save_model():
    texts, labels = load_data(DATA_DIR)
    texts = [preprocess_text(text) for text in texts]

    X_train, _, y_train, _ = train_test_split(
        texts, labels, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    model = Pipeline([
        ('vectorizer', TfidfVectorizer(max_features=MAX_FEATURES, stop_words=STOP_WORDS)),
        ('classifier', MultinomialNB())
    ])

    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATH)
    print(f"Modèle sauvegardé dans {MODEL_PATH}")

if __name__ == "__main__":
    train_and_save_model()
