import requests
import random
from bs4 import BeautifulSoup

class Recommendations():

	# Create Recommendations for some given Profile.
	# Set up blank lists for anime and manga recommendation lists.
	# (This class could end up obsolete, as Profile might handle its functionality.)
	def __init__(self, profile, category):
		self.profile = profile
		self.category = category
		self.r_list = []


	# Get a collection of stories, look at each story page and grab its recommendation
	# links. Add any of these links to the list of recommendations, if not already seen.
	def recommend(self, user_list, min_score, result_count):
		tmp_r_list = []
		used_links = []
		print("[Recommendations] (1/2) Collecting some user stories...")

		while len(tmp_r_list) < result_count:

			rand_index = random.randint(0,len(user_list)-1)
			rand_link = user_list[rand_index][1]

			if rand_link not in used_links:
				used_links.append(rand_link)
				page_recs = self.get_page_recommendation_info(rand_link)
				tmp_r_list += [tl for tl in page_recs if tl[1] not in user_list + tmp_r_list and len(tmp_r_list) < result_count]


		print("[Recommendations] (2/2) Creating recommendations...")
		self.r_list = [page_recs for page_recs in tmp_r_list if len(page_recs) != 0]
		print(self.r_list)
		

	def get_page_recommendation_info(self, url):
		response = requests.get(url)
		soup = BeautifulSoup(response.text, "html.parser")
		recs = []

		try:
			rec_section = soup.find("ul", {"class":""+self.category+"-slide js-"+self.category+"-slide"})
			for r in rec_section.find_all("a", {"class":"link bg-center"}):
				title = r.find("span", {"class":"title fs10"}).get_text()
				link = r.get("href")

				# Edge case where recommendations is in the url for some reason
				if "recommendations" in link:
					link = link.replace("recommendations/", "")

				link_code = link.split("/")[4].split("-")[0]

				# Compare page code against potential links
				if url.split("/")[4] != link_code:
					pair = [title, "https://myanimelist.net/"+self.category+"/"+link_code]
					recs.append(pair)

					print(pair)

				# Just take the top 3 recommendations before moving on
				if len(recs) >= 3:
					break
		except Exception as e:
			print("Page recommendation went wrong! ("+url+")\n Exception: ", e)

		return recs


	# Overwrites the appropriate list of recommendations, defaulting to anime
	def set_recommendations(self, li):
		self.r_list = li


	# Returns the appropriate list of recommendations, defaulting to anime
	def get_recommendations(self):
		return self.r_list


	# Export existing recommendations list of a given category to plaintext file
	def export_recommendations(self):
		filepath = "./recommendation_lists/" + "rec_" + self.category + "_" + self.profile.username + ".txt"
		with open(filepath, "w", errors="replace") as storage:
			for story in self.r_list:
				# Format: [title, link]
				s = str(story[0]) + "\n" + str(story[1]) + "\n\n"
				storage.write(s)
		storage.close()
