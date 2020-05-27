import requests
from bs4 import BeautifulSoup

class Story():

    # Given URL, retrieve story page soup
    def __init__(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Any errors in gathering story data will make story invalid
        try:
            self.title = soup.find_all(class_='spaceit_pad')[0].get_text().split('English: ')[1].split('\n')[0]
            self.score = float(soup.find(class_='score-label score-8').get_text())
            self.rank = int(soup.find('span', attrs={'class':'numbers ranked'}).find('strong').get_text().split('#')[1])
            self.episodes = int(soup.find_all(class_='spaceit')[3].get_text().split('/')[1])
        except Exception as e:
            print('Something wrong with story..\t', url)
            print('Exception: ', e,'\n')
            self.title, self.score, self.rank, self.episodes = 'error', 0, 0, 0

    def get_title(self):
        return self.title

    def get_score(self):
        return self.score

    def get_rank(self):
        return self.rank

    def get_episodes(self):
        return self.episodes

    def __str__(self):
        s = '\nTitle: ' + self.title
        s += '\nScore: ' + str(format(self.score, '.2f'))
        s += '\nRank: #' + str(self.rank)
        s += '\nEpisodes: ' + str(self.episodes)
        return s


class Profile():

    # Find user's favourite anime or manga
    def favourite_stories(self, category):
        stories = []
        # Try if user has a list of favourites in this category
        try:
            for entry in category.find_all(class_='di-tc va-t pl8 data'):
                for link in entry.find_all('a', href=True):
                    # got the link!
                    story = Story(str(link['href']))
                    stories.append(story)
        # If not, return an empty list
        except:
            return []

        return stories

    # Find user's favourite characters or people
    def favourite_beings(self):
        pass

    # Given URL, retrieve user profile data
    def __init__(self, url):
        # Get soup and categories
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        category = ['anime', 'manga', 'characters', 'people']

        # Set favourite anime and manga
        anime = soup.find('ul', attrs={'class':'favorites-list '+category[0]})
        manga = soup.find('ul', attrs={'class':'favorites-list '+category[1]})
        self.favourite_anime = self.favourite_stories(anime)
        self.favourite_manga = self.favourite_stories(manga)

    def get_fave_anime(self):
        for story in self.favourite_anime:
            if story.get_title() != 'error':
                print(story)

    def get_fave_manga(self):
        for story in self.favourite_manga:
            if story.get_title() != 'error':
                print(story)
