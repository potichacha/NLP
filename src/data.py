import os

def load_data(data_dir):
    texts, labels = [], []
    for category in os.listdir(data_dir):
        category_path = os.path.join(data_dir, category)
        if os.path.isdir(category_path):
            for filename in os.listdir(category_path):
                filepath = os.path.join(category_path, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    texts.append(file.read())
                    labels.append(category)
    return texts, labels
