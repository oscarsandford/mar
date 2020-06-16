import requests
from bs4 import BeautifulSoup

class Story():

	# Given URL, retrieve story info
	def __init__(self, url):
		response = requests.get(url)
		self.soup = BeautifulSoup(response.text, "html.parser")
		self.link = url
		self.title, self.score, self.rank, self.episodes, self.my_rating = " error", 0.0, 0, 0, 0
		try:
			t_div = self.soup.find("span", {"class":"h1-title"})
			try:
				self.title = t_div.find("span", {"class":"title-english"}).get_text()
			except Exception as e:
				self.title = t_div.find("span", {"itemprop":"name"}).get_text()

			print("Appending . . . ", self.title)

			s_div = self.soup.find("div", {"class":"fl-l score"}).get_text()
			if s_div != "N/A":
				self.score = float(s_div)

			r_div = self.soup.find("span", {"class":"numbers ranked"}).find("strong").get_text()
			if r_div != "N/A":
				self.rank = int(r_div.split("#")[1])

			self.episodes = int(self.soup.find_all(class_="spaceit")[3].get_text().split("/")[1])

		except Exception as e:
			print("Something wrong with story..\t", url)
			print("Exception: ", e,"\n")


	# Returns list of recommendations from story page, up to length given by max
	def get_recommendation_links(self, max):
		links = []
		response = requests.get(self.get_link() + "/userrecs")
		r_soup = BeautifulSoup(response.text, "html.parser")
		lst = r_soup.find("div", {"class":"js-scrollfix-bottom-rel"})
		for r in lst.find_all("div", {"class":"picSurround"}):
			lk = r.find("a").get("href")
			links.append(lk)
			if len(links) >= max:
				break
		return links


	def get_link(self):
		return self.link

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

	def __str__(self):
		s = "\nTitle: " + self.title
		s += "\nLink: " + str(self.link)
		s += "\nUser Rating: " + str(self.my_rating) + "\n"
		return s



class Profile():

	# Given MAL username, retrieve, import/export their story lists
	def __init__(self, username):
		self.username = username
		self.anime_list = []
		self.manga_list = []


	# Return list of Story objects with the user's scores >= threshold
	def set_stories(self, category, threshold):
		print("\n\t<> Setting "+category+" stories! <>\n")
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
			score = int(scores[i].split("\"")[0].replace(",", ""))
			if score >= threshold:
				link = links[i].split("\"")[0].replace("\\", "")
				story = Story("https://myanimelist.net" + link)
				story.set_my_rating(score)
				stories.append(story)

		return stories


	# Set all stories of a category, of any score
	def set_all_stories(self, category):
		if category == "manga":
			self.manga_list = self.set_stories("manga", 0)
		else:
			self.anime_list = self.set_stories("anime", 0)


	# Returns a given list, defaulting to anime
	def get_list(self, category):
		if category == "manga":
			return self.manga_list
		else:
			return self.anime_list


	# Export stories to plaintext file
	def export_list(self, category):
		filename = "mal_" + category + "_" + self.username + ".txt"
		storage = open("./story_lists/" + filename, "w", errors="replace")
		storage.write(self.username + "\'s " + category + " list:\n")
		for story in self.get_list(category):
			storage.write(str(story))
		storage.close()


	# Import list of story links with score >= threshold from existing user's storage file
	def import_links(self, category, threshold):
		filename = "mal_" + category + "_" + self.username + ".txt"
		links = []
		try:
			with open("./story_lists/" + filename, "r") as storage:
				lines = storage.readlines()
				for i in range(len(lines)):
					if "Link" in lines[i] and "User Rating" in lines[i+1]:
						score = int(lines[i+1].split("User Rating: ")[1])
						if score >= threshold:
							links.append(lines[i].split("Link: ")[1].strip())
			storage.close()
		except Exception as e:
			print("Oh noes! This user's "+category+" list does not exist.\nExiting..")
			exit(0)

		return links
