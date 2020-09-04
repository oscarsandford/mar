import os.path
import requests
from bs4 import BeautifulSoup

class Story():

	# A Story is an anime or manga with a title, userbase score, rank, episode count, and personal rating.
	# This initializer takes a Story url and scrapes info from it to define the class.
	def __init__(self, url):
		response = requests.get(url)

		self.soup = BeautifulSoup(response.text, "html.parser")
		self.link = url
		self.title, self.score, self.rank, self.episodes, self.my_rating = " N/A", 0.0, 0, 0, 0

		try:
			# Define title
			t_div = self.soup.find("div", {"class":"h1-title"})
			self.title = t_div.find("h1", {"class":"title-name"}).get_text()

			print("\tAppending . . . ", self.title)

			# Define userbase average score
			s_div = self.soup.find("div", {"class":"fl-l score"}).get_text()
			if s_div != "N/A":
				self.score = float(s_div)

			# Define userbase rank on MAL
			r_div = self.soup.find("span", {"class":"numbers ranked"}).find("strong").get_text()
			if r_div != "N/A":
				self.rank = int(r_div.split("#")[1])

			# Define the number of episodes in the story
			# (Could be causing issues with manga! Might have to remove or figure a workaround.)
			# self.episodes = int(self.soup.find_all(class_="spaceit")[3].get_text().split("/")[1])

		except Exception as e:
			print("[Story] Error : Story page has an irregularity. ("+url+")\nException:",e,"\n")


	# Returns list of recommendations from a story page
	def get_page_recommendation_links(self):
		try:
			links = []
			page_link_code = self.get_link().split("/")[4]

			rec_section = self.soup.find("ul", {"class":"anime-slide js-anime-slide"})
			for r in rec_section.find_all("a", {"class":"link bg-center"}):
				link = r.get("href")

				# Edge case where recommendations is in the url for some reason
				if "recommendations" in link:
					link = link.replace("recommendations/", "")

				link_code = link.split("/")[4].split("-")[0]

				# Compare page code against potential links
				if page_link_code != link_code:
					links.append(link.split("-")[0])

				# Just take the top 3 recommendations before moving on
				if len(links) >= 3:
					break
		except Exception as e:
			print("[Story] Error : Page recommendations not working. ("+self.get_link()+")\nException:",e,"\n")

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

	# Note that this format is relied on by read/write functionality between
	# plaintext story lists. Take care when editing this!
	def __str__(self):
		s = "Title: " + self.title
		s += "\nLink: " + str(self.link)
		s += "\nUser Rating: " + str(self.my_rating) + "\n\n"
		return s



class Profile():

	# Create a Profile for some given user with a username.
	# Keep everything lowercase so "frosty" and "Frosty" are the same.
	# Set up blank lists for anime and manga.
	def __init__(self, username):
		self.username = username.lower()
		self.anime_list = []
		self.manga_list = []


	# Set list of every Story the user has recorded on MAL for a given category
	def set_all_stories(self, category):
		print("[Profile] Setting "+category+" stories!")
		url = "https://myanimelist.net/"+category+"list/"+self.username
		response = requests.get(url)
		soup = BeautifulSoup(response.text, "html.parser")
		stories = []

		try:
			contents = soup.find("table", {"class":"list-table"})
			for t in contents("tbody"):
				t.decompose()
			data = contents["data-items"]

			links = data.split(category + "_url\":\"")
			scores = data.split("\"score\":")
			assert len(links) == len(scores)

			for i in range(1, len(links)):
				link = links[i].split("\"")[0].replace("\\", "")
				link_code = link.split("/")[2]

				score = int(scores[i].split("\"")[0].replace(",", ""))
				story = Story("https://myanimelist.net/"+category+"/"+ link_code)

				story.set_my_rating(score)
				stories.append(story)

		except Exception:
			print("[Profile] Error : User does not exist! (set_all_stories)")

		if category == "manga":
			self.manga_list = stories
		else:
			self.anime_list = stories


	# Returns a given list, defaulting to anime
	def get_list(self, category):
		if category == "manga":
			return self.manga_list
		else:
			return self.anime_list


	# Export stories to plaintext file. Don't do this if
	# the list is empty to prevent created garbage empty lists.
	def export_list(self, category):
		if len(self.get_list(category)) == 0:
			return

		filename = "mal_" + category + "_" + self.username + ".txt"
		storage = open("./story_lists/" + filename, "w", errors="replace")
		for story in self.get_list(category):
			storage.write(str(story))
		storage.close()


	# Returns a list of stories with score >= min_score from this Profile's 
	# list in the given category, if it exists. If not, we make such a list
	# and export it to plaintext to be reread by the same function.
	def import_links(self, category, min_score):
		filename = "mal_" + category + "_" + self.username + ".txt"
		links = []

		if not os.path.isfile("./story_lists/" + filename):
			print("[Profile] "+self.username+"'s list does not exist. Creating list...")
			self.set_all_stories(category)
			self.export_list(category)

		try:
			with open("./story_lists/" + filename, "r") as storage:
					lines = storage.readlines()
					for i in range(len(lines)):
						if "Link" in lines[i] and "User Rating" in lines[i+1]:
							score = int(lines[i+1].split("User Rating: ")[1])
							if score >= min_score:
								links.append(lines[i].split("Link: ")[1].strip())
			storage.close()
		except Exception:
			print("[Profile] Error : User does not exist! (import_links)")

		return links
