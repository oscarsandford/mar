import os.path
import requests, random, time
import colorama
from bs4 import BeautifulSoup

colorama.init()
TITLE_INDEX = 0
LINK_INDEX = 1
SCORE_INDEX = 2


class Recommendations():

	# Create Recommendations for some given Profile.
	# Set up blank list. This instance will handle only a single category: anime or manga.
	def __init__(self, profile, category):
		self.profile = profile
		self.category = category
		self.recommendations = []


	# Given an existing list and parameters from the client, choose random stories
	# from which to draw recommendations from. Add these stories to the class's list.
	# (TODO: min_score currently not used, but will likely be!)
	def recommend(self, user_list, min_score, result_count):

		start = time.time()
		tmp = []
		used_links = [[]]

		while len(tmp) < result_count:

			rand_index = random.randint(0,len(user_list)-1)
			rand_link = user_list[rand_index][LINK_INDEX]

			if rand_link not in used_links:
				used_links.append(rand_link)
				page_recs = self.get_page_recommendation_info(rand_link)
				
				# Although we iterate through the use list a lot here, I have tried to
				# sort the list by link code leading digit, and only look at leading digit
				# sections to cut down on runtime. I concluded that noticeable improvement
				# would require rewriting the export format. Maybe one day! 
				for suggestion in page_recs:
					already_exists = False
					for existing_item in user_list:
						# Check: if links are the same, reject
						if suggestion[LINK_INDEX] == existing_item[LINK_INDEX]:
							already_exists = True
							break
					if not already_exists and len(tmp) < result_count and suggestion not in tmp:
						tmp.append(suggestion)
						print("\t. . . "+suggestion[TITLE_INDEX])

		self.set_recommendations(tmp)

		end = time.time()
		print("\t(\033[92m@\033[0m) Recommendations compiled in \033[96m" + str(format(end-start, "0.4f")) + "\033[0m seconds.")
		

	# Given a story URL, grab the recommendations list data.
	# Return a list of [title, link] pairs.
	def get_page_recommendation_info(self, url):
		response = requests.get(url)
		soup = BeautifulSoup(response.text, "html.parser")
		recs = []

		try:
			section = soup.find("ul", {"class":""+self.category+"-slide js-"+self.category+"-slide"})
			all_recommended = section.find_all("a", {"class":"link bg-center"})
			tries = 0

			# Counting the number of tries prevents infinite loop, checking length
			# of all recommendations here prevents negative in randint function call.
			while len(recs) <= 3 and len(all_recommended) != 0 and tries < 10:
				rand_index = random.randint(0, len(all_recommended)-1)
				r = all_recommended[rand_index]
				link = r.get("href")

				# Edge case where recommendations is in the url for some reason
				if "recommendations" in link:
					link = link.replace("recommendations/", "")

				link_code = link.split("/")[4].split("-")[0]

				# Compare page code against potential links
				if url.split("/")[4] != link_code:
					title = r.find("span", {"class":"title fs10"}).get_text()
					link = "https://myanimelist.net/"+self.category+"/"+link_code
					recs.append([title, link])

				tries += 1

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
		directory = "./recommendation_lists/"
		if not os.path.exists(directory):
			os.makedirs(directory)
		filepath = directory + "rec_" + self.category + "_" + self.profile.username + ".txt"
		
		with open(filepath, "w", errors="replace") as storage:
			for story in self.get_recommendations():
				# Format: [title, link]
				s = str(story[TITLE_INDEX]) + "\n" + str(story[LINK_INDEX]) + "\n\n"
				storage.write(s)
		storage.close()
