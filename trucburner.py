from bs4 import BeautifulSoup

with open("test.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Now you can use soup to parse and extract data
print(soup.title.string)  # Just an example