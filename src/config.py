import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

DATA_DIR = "../data/Processed"
MODEL_PATH = "../Models/classifier_linear_svm_calibrated.joblib"
TEST_SIZE = 0.2
RANDOM_STATE = 42
MAX_FEATURES = 5000

# ✅ Liste de stop words français de NLTK
STOP_WORDS = stopwords.words('french')