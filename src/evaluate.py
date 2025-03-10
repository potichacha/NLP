from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import joblib
from config import DATA_DIR, MODEL_PATH, TEST_SIZE, RANDOM_STATE
from data import load_data
from preprocess import preprocess_text

def evaluate():
    texts, labels = load_data(DATA_DIR)
    texts = [preprocess_text(text) for text in texts]

    _, X_test, _, y_test = train_test_split(
        texts, labels, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    model = joblib.load(MODEL_PATH)
    predictions = model.predict(X_test)

    print(classification_report(y_test, predictions))
    print(confusion_matrix(y_test, predictions))

if __name__ == "__main__":
    evaluate()
