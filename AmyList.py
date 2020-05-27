import requests
from bs4 import BeautifulSoup

class Story():

    # Retrieve anime/manga series page soup
    def __init__(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        self.title= soup.find('span', attrs={'itemprop':'name'}).get_text()
        self.score = float(soup.find(class_='score-label score-8').get_text())
        self.rank = int(soup.find('span', attrs={'class':'numbers ranked'}).find('strong').get_text().split('#')[1])
        self.episodes = int(soup.find_all(class_='spaceit')[3].get_text().split('/')[1])


    def __str__(self):
        s = 'Title: ' + self.title
        s += '\nScore: ' + str(format(self.score, '.2f'))
        s += '\nRank: #' + str(self.rank)
        s += '\nEpisodes: ' + str(self.episodes)
        return s


class Profile():

    def __init__(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        