from bs4 import BeautifulSoup
from sitemap import liens_recettes
from bs4 import XMLParsedAsHTMLWarning
import warnings
import scrapper

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

soup = BeautifulSoup(liens_recettes, 'html.parser')
# Find the step list container
step_div = soup.find_all('loc')
x = scrapper.load_variable()

if step_div:
    while x < len(step_div) and x < 1000 :
        x = scrapper.load_variable()
        link = step_div[x].text
        scrapper.scrap_text(link)
