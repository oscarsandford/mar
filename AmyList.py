import requests
from bs4 import BeautifulSoup

class Story():

	# Given URL, retrieve story page soup
	def __init__(self, url):
		response = requests.get(url)
		soup = BeautifulSoup(response.text, "html.parser")
		self.title, self.score, self.rank, self.episodes, self.my_rating = " error", 0.0, 0, 0, 0
		try:
			# TODO: find a better way to get the title from h1-title
			t_div = soup.find(class_="spaceit_pad")
			self.title = t_div.get_text().split(t_div.find("span", {"class":"dark_text"}).get_text())[1].replace("\n", "")
			print("Appending . . . ", self.title)

			s_div = soup.find("div", {"class":"fl-l score"}).get_text()
			if s_div != "N/A":
				self.score = float(s_div)

			r_div = soup.find("span", {"class":"numbers ranked"}).find("strong").get_text()
			if r_div != "N/A":
				self.rank = int(r_div.split("#")[1])

			self.episodes = int(soup.find_all(class_="spaceit")[3].get_text().split("/")[1])

		except Exception as e:
			print("Something wrong with story..\t", url)
			print("Exception: ", e,"\n")


	def get_title(self):
		return self.title

	def get_score(self):
		return self.score

	def get_rank(self):
		return self.rank

	def get_episodes(self):
		return self.episodes

	def set_my_rating(self, num):
		self.my_rating = num

	def get_my_rating(self):
		return self.my_rating

	def format_story(self):
		return "\nTitle:" + self.title + "\nUser Rating: " + str(self.my_rating) + "\n"

	def __str__(self):
		s = "\nTitle:" + self.title
		s += "\nScore: " + str(format(self.score, ".2f"))
		s += "\nRank: #" + str(self.rank)
		s += "\nEpisodes: " + str(self.episodes)
		return s


class Profile():

	# Given MAL username, retrieve user profile page data
	def __init__(self, username):
		self.username = username
		self.anime_list = self.all_stories("anime")
		self.manga_list = self.all_stories("manga")


	def all_stories(self, category):
		url = "https://myanimelist.net/"+category+"list/"+self.username
		response = requests.get(url)
		soup = BeautifulSoup(response.text, "html.parser")
		stories = []

		contents = soup.find("table", {"class":"list-table"})
		for t in contents("tbody"):
			t.decompose()
		data = contents["data-items"]

		links = data.split(category + "_url\":\"")
		scores = data.split("\"score\":")
		assert len(links) == len(scores)

		for i in range(1, len(links)):
			link = links[i].split("\"")[0].replace("\\", "")
			score = int(scores[i].split("\"")[0].replace(",", ""))
			story = Story("https://myanimelist.net" + link)
			story.set_my_rating(score)
			stories.append(story)

		return stories


	def get_list(self, category):
		if category == "manga":
			return self.manga_list
		else:
			return self.anime_list


	def build_list(list):
		for story in list:
			s += story.format_story()
		return s


	def get_list_string(self, category):
		if category == "manga":
			return build_list(self.manga_list)
		else:
			return build_list(self.anime_list)


	def export_list(self, category):
		filename = "mal_" + category + "_" + self.username + ".txt"
		txt_file = open(filename, "w", errors="replace")
		txt_file.write(self.username + "\'s " + category + " list:\n")
		for story in self.get_list(category):
			txt_file.write(story.format_story())
		txt_file.close()
