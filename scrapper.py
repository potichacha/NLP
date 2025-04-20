from bs4 import BeautifulSoup
import unicodedata
import requests
import json
import symbols
from unidecode import unidecode
import re
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36"
}


def load_variable():
    try:
        with open("state.json", "r") as f:
            return json.load(f)["my_global_variable"]
    except FileNotFoundError:
        return 10  # Default value

def save_variable(value):
    with open("state.json", "w") as f:
        json.dump({"my_global_variable": value}, f)

my_global_variable = load_variable()


def clean(text):
    # Remove accents
    # Encode to ASCII with placeholder, decode back
    text1 = text.replace("â€™","'").encode('latin1').decode('utf-8').replace("?", "").replace(' ndeg '," numero ").replace('deg','e')
    text2 = unidecode(text1)
    # Collapse all whitespace into a single space
    return re.sub(r'\s+', ' ', text2).strip()

def download_html(url, output_filename):
    try:
        # Send a GET request to the URL
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Write the HTML content to a file
            with open(output_filename, 'w', encoding='utf-8') as file:
                file.write(response.text)
        else:
            print(f"Failed to retrieve the URL. HTTP Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Clean and parse HTML
def scrap_text(url):
    output = f"Data/Processed/SciencesEtAvenir/{load_variable()}.txt"
    download_html(url, "currentfile.txt")

    with open("currentfile.txt", "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Find the step list container
    step_div = soup.find('div',attrs={"itemprop":"articleBody"} )

    if step_div:
        # Remove empty tags
        for tag in step_div.find_all():
            if not tag.get_text(strip=True):
                tag.decompose()

        # Get the cleaned text with custom separator
        result = step_div.get_text(separator=' ', strip=True)

    else:
        print("No .recipe-step-list div found.")

    with open(output, "w", encoding="utf-8") as file:
        file.write(clean(result))
        print(f"{load_variable()} file scrapped : {output}")
        save_variable(load_variable() + 1)

