import requests
from bs4 import BeautifulSoup

class Story():

    # Given URL, retrieve story page soup
    def __init__(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.validity = True
        # Any errors in gathering story data will make story invalid
        try:
            self.title = soup.find_all(class_='spaceit_pad')[0].get_text().split('English: ')[1].split('\n')[0]
            self.score = float(soup.find(class_='score-label score-8').get_text())
            self.rank = int(soup.find('span', {'class':'numbers ranked'}).find('strong').get_text().split('#')[1])
            self.episodes = int(soup.find_all(class_='spaceit')[3].get_text().split('/')[1])
        except Exception as e:
            print('Something wrong with story..\t', url)
            print('Exception: ', e,'\n')
            self.title, self.score, self.rank, self.episodes = 'error', 0, 0, 0
            self.validity = False

    def get_title(self):
        return self.title

    def get_score(self):
        return self.score

    def get_rank(self):
        return self.rank

    def get_episodes(self):
        return self.episodes

    def is_valid(self):
        return self.validity

    def __str__(self):
        s = '\nTitle: ' + self.title
        s += '\nScore: ' + str(format(self.score, '.2f'))
        s += '\nRank: #' + str(self.rank)
        s += '\nEpisodes: ' + str(self.episodes)
        return s


class Profile():

    # Given MAL username, retrieve user profile page data
    def __init__(self, username):
        # Get soup and categories
        self.username = username

        # Set favourite anime and manga
        #self.favourite_anime = self.favourite_stories('anime')
        #self.favourite_manga = self.favourite_stories('manga')
        # Set user lists (watching, completed, etc)
        self.anime_list = self.all_stories('anime')

    # Find user's favourite anime or manga
    def favourite_stories(self, category):
        url = 'https://myanimelist.net/profile/' + self.username
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        list = soup.find('ul', attrs={'class':'favorites-list '+category})

        stories = []
        # Try if user has a list of favourites in this category
        try:
            for entry in list.find_all(class_='di-tc va-t pl8 data'):
                for link in entry.find_all('a', href=True):
                    # got the link!
                    story = Story(str(link['href']))
                    stories.append(story)
        # If not, return an empty list
        except:
            return []
        return stories

    # Find user's all anime list
    def all_stories(self, category):
        url = 'https://myanimelist.net/' + category +'list/'+ self.username
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        stories = []

        # Get rid of the other table contents
        contents = soup.find('table', {'class':'list-table'})
        for t in contents('tbody'):
            t.decompose()

        data = contents['data-items']
        story_urls = []
        # look for str = category + '_url'
        sections = data.split(category + '_url\":\"')
        for i in range(1, len(sections)):
            link = sections[i].split("\"")[0].replace('\\', '')
            story_urls.append(link)

        count = 0
        for st in story_urls:
            print(st)
            count += 1
        print(count)

        return stories

    def get_fave_anime(self):
        for story in self.favourite_anime:
            if story.is_valid():
                print(story)

    def get_fave_manga(self):
        for story in self.favourite_manga:
            if story.is_valid():
                print(story)
