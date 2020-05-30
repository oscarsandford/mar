import requests
from bs4 import BeautifulSoup

class Story():

    # Given URL, retrieve story page soup
    def __init__(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.title, self.score, self.rank, self.episodes, self.my_rating = 'error', 0.0, 0, 0, 0
        # Any errors in gathering story data will make story invalid
        try:
            # TODO: find a better way to get the title from h1-title
            t_div = soup.find(class_='spaceit_pad')
            self.title = t_div.get_text().split(t_div.find('span', {'class':'dark_text'}).get_text())[1].replace('\n', '')
            print("Appending . . . ", self.title)

            s_div = soup.find('div', {'class':'fl-l score'}).get_text()
            if s_div != 'N/A':
                self.score = float(s_div)

            r_div = soup.find('span', {'class':'numbers ranked'}).find('strong').get_text()
            if r_div != 'N/A':
                self.rank = int(r_div.split('#')[1])

            self.episodes = int(soup.find_all(class_='spaceit')[3].get_text().split('/')[1])

        except Exception as e:
            print('Something wrong with story..\t', url)
            print('Exception: ', e,'\n')


    def get_title(self):
        return self.title

    def get_score(self):
        return self.score

    def get_rank(self):
        return self.rank

    def get_episodes(self):
        return self.episodes

    def set_my_rating(self, score):
        self.my_rating = score

    def get_my_rating(self):
        return self.my_rating

    def __str__(self):
        s = '\nTitle:' + self.title
        s += '\nScore: ' + str(format(self.score, '.2f'))
        s += '\nRank: #' + str(self.rank)
        s += '\nEpisodes: ' + str(self.episodes)
        return s


class Profile():

    # Given MAL username, retrieve user profile page data
    def __init__(self, username):
        self.username = username

        # Set lists (watching, completed, ptw, etc.)
        self.anime_list = self.all_stories('anime')

    # Find user's favourite anime or manga
    # TODO: deprecate this at some point
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
        except Exception as e:
            print(e + ': user does not have a favourite '+category +' list!')

        return stories


    # Find all anime from user list
    def all_stories(self, category):
        url = 'https://myanimelist.net/'+category+'list/'+self.username
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        stories = []
        # This try is for avoiding random 403's
        try:
            # Get rid of the other table contents, isolate data
            contents = soup.find('table', {'class':'list-table'})
            for t in contents('tbody'):
                t.decompose()
            data = contents['data-items']
            # Sort out and make stories with the urls

            links = data.split(category + '_url\":\"')
            scores = data.split('\"score\":')
            assert len(links) == len(scores)

            for i in range(1, len(links)):
                # Split on last " and remove redundant backslashes
                link = links[i].split('\"')[0].replace('\\', '')
                score = int(scores[i].split('\"')[0].replace(',', ''))
                story = Story('https://myanimelist.net' + link)
                story.set_my_rating(score)
                stories.append(story)

        except Exception as e:
            print(e + ': myanimelist.net is down again!')

        return stories

    def get_fave_anime(self):
        return self.favourite_anime

    def get_fave_manga(self):
        return self.favourite_manga

    # TODO: add an arg to change for different display options
    def get_anime_list(self):
        s = ''
        for anime in self.anime_list:
            s += str(anime) + '\n(User Score: ' + str(anime.get_my_rating()) + ')\n'
        return s

    def export_anime_list(self):
        filename = 'mal_' + self.username + '.txt'
        txt_file = open(filename, 'w', errors='replace')
        s = ''
        for anime in self.anime_list:
            s = str(anime) + '\n(User Score: ' + str(anime.get_my_rating()) + ')\n'
            txt_file.write(s)
        txt_file.close()
