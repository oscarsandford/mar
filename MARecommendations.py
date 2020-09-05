import requests
import random
import time # for performance testing
from bs4 import BeautifulSoup

class Recommendations():

	# Globals
	# title_index = 0
	# link_index = 1
	# score_index = 2

	# Create Recommendations for some given Profile.
	# Set up blank list. This instance will handle only a single category: anime or manga.
	def __init__(self, profile, category):
		self.profile = profile
		self.category = category
		self.recommendations = []


	def get_link_code(self, link):
		return link.split("/")[4]

	# Given an existing list and parameters from the client, choose random stories
	# from which to draw recommendations from. Add these stories to the main list.
	# (TODO: min_score currently not used, but will likely be!)
	def recommend(self, user_list, min_score, result_count):

		# I think that this algorithm would only benefit if we export lists a certain
		# way such that they have already been sorted in the way we want before we access them.

		start = time.time()

		user_list = self.sort_user_list(user_list)
		populated_sections_indices = [i for i in range(len(user_list)) if len(user_list[i]) != 0]
		tmp = []
		used_links = []

		while len(tmp) < result_count:
			
			rand_section_index = random.choice(populated_sections_indices)
			rand_story_index = random.randint(0,len(user_list[rand_section_index])-1)
			rand_link = user_list[rand_section_index][rand_story_index][1]

			if rand_link not in used_links:
				used_links.append(rand_link)
				page_recs = self.get_page_recommendation_info(rand_link)
				
				for suggestion in page_recs:
					leading_code_digit = int(self.get_link_code(suggestion[1])[0])

					if leading_code_digit not in populated_sections_indices and len(tmp) < result_count:
						tmp.append(suggestion)
					else:
						links = [el[1] for el in user_list[leading_code_digit]]
						if suggestion[1] not in links and len(tmp) < result_count:
							tmp.append(suggestion)	

		self.set_recommendations(tmp)

		end = time.time()
		print("{~} Execution time for recommendations was " + str(format(end - start, "0.4f")) + " seconds.")
	
	# Return an array of collections (arrays) of links with leading 
	# code digit corresponding to the index of collection in array.
	def sort_user_list(self, li_i):
		li_f = [[] for _ in range(10)]
		for story in li_i:
			leading_code_digit = int(self.get_link_code(story[1])[0])
			li_f[leading_code_digit].append(story)
		return li_f

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

				link_code = self.get_link_code(link).split("-")[0]

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
		self.recommendations = li


	# Returns the list of recommendations
	def get_recommendations(self):
		return self.recommendations


	# Export existing recommendations list for this category to plaintext file
	def export_recommendations(self):
		filepath = "./recommendation_lists/" + "rec_" + self.category + "_" + self.profile.username + ".txt"
		with open(filepath, "w", errors="replace") as storage:
			for story in self.get_recommendations():
				# Format: [title, link]
				s = str(story[0]) + "\n" + str(story[1]) + "\n\n"
				storage.write(s)
		storage.close()
