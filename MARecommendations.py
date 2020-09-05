import requests
import random
from bs4 import BeautifulSoup

class Recommendations():

	# Create Recommendations for some given Profile.
	# Set up blank list. This instance will handle only a single category: anime or manga.
	def __init__(self, profile, category):
		self.profile = profile
		self.category = category
		self.r_list = []


	# Given an existing list and parameters from the client, choose random stories
	# from which to draw recommendations from. Add these stories to the main list.
	# (TODO: min_score currently not used, but will likely be!)
	# ( !!! TODO: duplicate issue is abound!)
	def recommend(self, user_list, min_score, result_count):
		tmp_r_list = []
		used_links = []
		print(" [Recommendations] (1/2) Collecting some user stories...")

		while len(tmp_r_list) < result_count:

			rand_index = random.randint(0,len(user_list)-1)
			rand_link = user_list[rand_index][1]

			if rand_link not in used_links:
				used_links.append(rand_link)
				page_recs = self.get_page_recommendation_info(rand_link)
				tmp_r_list += [tl for tl in page_recs if tl[1] not in user_list + tmp_r_list]

		print(" [Recommendations] (2/2) Creating recommendations...")
		self.set_recommendations([page_recs for page_recs in tmp_r_list if len(page_recs) != 0])
		

	# Given a story URL, grab the recommendations list data.
	# Return a list of [title, link] pairs.
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
					title_and_link = [title, "https://myanimelist.net/"+self.category+"/"+link_code]
					recs.append(title_and_link)

				# Just take the top 3 recommendations before moving on
				# (TODO: make this more random to inject some variety!)
				if len(recs) >= 3:
					break
		except Exception as e:
			print("Page recommendation went wrong! ("+url+")\n Exception: ", e)

		return recs


	# Overwrites the list of recommendations
	def set_recommendations(self, li):
		self.r_list = li


	# Returns the list of recommendations
	def get_recommendations(self):
		return self.r_list


	# Export existing recommendations list for this category to plaintext file
	def export_recommendations(self):
		filepath = "./recommendation_lists/" + "rec_" + self.category + "_" + self.profile.username + ".txt"
		with open(filepath, "w", errors="replace") as storage:
			for story in self.r_list:
				# Format: [title, link]
				s = str(story[0]) + "\n" + str(story[1]) + "\n\n"
				storage.write(s)
		storage.close()
