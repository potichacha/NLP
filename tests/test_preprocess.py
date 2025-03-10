import unittest
from src.preprocess import preprocess_text

class TestPreprocess(unittest.TestCase):
    def test_preprocess(self):
        self.assertEqual(preprocess_text("Bonjour, NLP 123!"), "bonjour nlp")

if __name__ == '__main__':
    unittest.main()
