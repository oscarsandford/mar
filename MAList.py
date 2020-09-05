import os.path
import requests
from bs4 import BeautifulSoup

class Profile():

	# Create a Profile for some given user with a username.
	# Keep everything lowercase so "frosty" and "Frosty" are the same.
	# Set up blank lists for anime and manga.
	def __init__(self, username):
		self.username = username.lower()
		self.anime_list = []
		self.manga_list = []


	# Set list of every Story the user has recorded on MAL for a given category
	# record: TITLE -> LINK -> SCORE
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
			titles = data.split(category + "_title\":\"")

			for i in range(1, len(links)):
				link_code = links[i].split("\"")[0].replace("\\", "").split("/")[2]

				title = titles[i].split("\"")[0]
				link = "https://myanimelist.net/"+category+"/"+ link_code
				my_score = int(scores[i].split("\"")[0].replace(",", ""))
				
				# Format: [title, link, score]
				print("["+str(i-1)+"]\tAppending . . . "+title)
				stories.append([title, link, my_score])

		except Exception as e:
			print("[Profile - set_all_stores]\nException: ",e)

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
				s = str(story[0]) + "\n" + str(story[1]) + "\n" + str(story[2]) + "\n\n"
				storage.write(s)

		storage.close()


	# Import a list from filepath with stories' score >= min_score. If this Profile's instance list doesn't
	# exist, get their stories from MAL and export them, then reimport. Create directory if needed.
	def import_list(self, category, min_score):
		directory = "./story_lists/"
		filepath = directory + "mal_" + category + "_" + self.username + ".txt"
		li = []

		if not os.path.isfile(filepath):
			if not os.path.exists(directory):
				os.makedirs(directory)
			print("[Profile] "+self.username+"'s list does not exist. Creating list...")
			self.set_all_stories(category)
			self.export_list(category)

		try:
			with open(filepath, "r") as storage:
				lines = storage.readlines()
				for i in range(len(lines)-1):
					if "https://myanimelist.net/" in lines[i+1]:
						if int(lines[i+2].strip()) >= min_score:
							li.append([lines[i].strip(), lines[i+1].strip(), lines[i+2]])
			storage.close()
		except Exception as e:
			print(print("[Profile - import_list]\nException: ",e))

		# Format: [title, link, score]
		return li
