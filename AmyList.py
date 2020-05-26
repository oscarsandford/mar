import requests
from bs4 import BeautifulSoup

class Series():

    # Retrieve anime/manga series page soup
    def __init__(self, url):
        response = requests.get(url)
        self.soup = BeautifulSoup(response.text, "html.parser")


    def __str__(self):
        return self.soup.find(class_="spaceit_pad").get_text()
