from bs4 import BeautifulSoup as beauty
import cloudscraper

scraper = cloudscraper.create_scraper(delay=10, browser='chrome') 
url = "https://www.g2.com/categories"

info = scraper.get(url).text
soup = beauty(info, "html.parser")
print('yes......................')
print(soup.contents)


