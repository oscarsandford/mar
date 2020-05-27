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

    def get_title(self):
        return self.title

    def __str__(self):
        s = 'Title: ' + self.title
        s += '\nScore: ' + str(format(self.score, '.2f'))
        s += '\nRank: #' + str(self.rank)
        s += '\nEpisodes: ' + str(self.episodes)
        return s


class Profile():

    def favourite_stories(self, category):
        stories = []
        for entry in category.find_all(class_='di-tc va-t pl8 data'):
            for link in entry.find_all('a', href=True):
                # got the link!
                #print(link['href'])
                story = Story(str(link['href']))
                stories.append(story)

        return stories

    def favourite_beings(self):
        pass

    def __init__(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        category = ['anime', 'manga', 'characters', 'people']

        anime = soup.find('ul', attrs={'class':'favorites-list '+category[0]})
        self.favourite_anime = self.favourite_stories(anime)

        

    def get_faves(self):
        for anime in self.favourite_anime:
            print(anime.get_title())