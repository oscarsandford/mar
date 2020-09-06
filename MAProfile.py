import os.path
import requests
import colorama
from bs4 import BeautifulSoup

colorama.init()
TITLE_INDEX = 0
LINK_INDEX = 1
SCORE_INDEX = 2


class Profile():

	# Create a Profile for some given user with a username.
	# Keep everything lowercase so "frosty" and "Frosty" are the same.
	# Set up blank lists for anime and manga.
	def __init__(self, username):
		self.username = username.lower()
		self.anime_list = []
		self.manga_list = []


	# Set list of stories that the user has recorded 
	# on their list page for a category. 
	def set_list(self, category):
		print("[\033[33mProfile\033[0m] Setting stories for "+category+".")
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
			titles = data.split(category + "_title\":\"")

			for i in range(1, len(links)):
				link_code = links[i].split("\"")[0].replace("\\", "").split("/")[2]

				title = titles[i].split("\"")[0]
				link = "https://myanimelist.net/"+category+"/"+ link_code
				my_score = int(scores[i].split("\"")[0].replace(",", ""))
				
				# Format: [title, link, score]
				print("["+str(i-1)+"]\t\033[2mAppending . . . \033[0m"+title)
				stories.append([title, link, my_score])

		except Exception as e:
			print(" [\033[33mProfile\033[0m] set_list\n Exception: ",e)

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
	# Exporting guarantees we have proper existing directory.
	def export_list(self, category):
		li = self.get_list(category)
		if len(li) == 0:
			return

		filepath = "./story_lists/" + "mal_" + category + "_" + self.username + ".txt"
		with open(filepath, "w", errors="replace") as storage:
			for story in li:
				# Format: [title, link, score]
				s = str(story[TITLE_INDEX]) + "\n" + str(story[LINK_INDEX]) + "\n" + str(story[SCORE_INDEX]) + "\n\n"
				storage.write(s)

		storage.close()


	# Import a list from filepath with stories' score >= min_score. If this Profile's instance list doesn't
	# exist, get their stories from MAL and export them, then reimport. Create directory if needed.
	def import_list(self, category, min_score):
		directory = "./story_lists/"
		filepath = directory + "mal_" + category + "_" + self.username + ".txt"
		imported = []

		if not os.path.isfile(filepath):
			if not os.path.exists(directory):
				os.makedirs(directory)
			print("[\033[33mProfile\033[0m] "+self.username+"'s list does not exist. Creating list...")
			self.set_list(category)
			self.export_list(category)

		try:
			with open(filepath, "r") as storage:
				lines = storage.readlines()
				for i in range(len(lines)-1):
					if "https://myanimelist.net/" in lines[i+LINK_INDEX]:
						if int(lines[i+SCORE_INDEX].strip()) >= min_score:
							imported.append([lines[i+TITLE_INDEX].strip(), lines[i+LINK_INDEX].strip(), lines[i+SCORE_INDEX]])
			storage.close()
		except Exception as e:
			print(" [\033[33mProfile\033[0m] import_list\n Exception: ",e)

		# Format: [title, link, score]
		return imported
