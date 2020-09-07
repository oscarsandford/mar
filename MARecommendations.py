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
	def recommend(self, user_list, target_count, max_attempts):
		start = time.time()
		tmp = []
		used_links = [[]]
		attempt_count = 0

		while len(tmp) < target_count and attempt_count < max_attempts:

			rand_index = random.randint(0,len(user_list)-1)
			rand_link = user_list[rand_index][LINK_INDEX]

			if rand_link not in used_links:
				used_links.append(rand_link)
				page_recs = self.get_page_recommendations(rand_link, max_attempts)
				
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
					if not already_exists and len(tmp) < target_count and suggestion not in tmp:
						tmp.append(suggestion)
						print("\t\033[2m. . . \033[0m"+suggestion[TITLE_INDEX])

			attempt_count += 1

		self.set_recommendations(tmp)
		end = time.time()
		print("\t(\033[92m@\033[0m) Recommendations compiled in \033[96m" + str(format(end-start, "0.4f")) + "\033[0m seconds.")
		

	# Given a story URL, grab the recommendations list data.
	# Return a list of [title, link] pairs.
	def get_page_recommendations(self, url, max_attempts):
		response = requests.get(url)
		soup = BeautifulSoup(response.text, "html.parser")
		recs = []

		try:
			section = soup.find("ul", {"class":"anime-slide js-anime-slide"})
			all_recommended = section.find_all("a", {"class":"link bg-center"})
			page_code = url.split("/")[4]
			attempt_count = 0

			# Counting the number of tries prevents infinite loop, checking length
			# of all recommendations here prevents negative in randint function call.
			while len(recs) <= 3 and len(all_recommended) != 0 and attempt_count < max_attempts:
				rand_index = random.randint(0, len(all_recommended)-1)
				r = all_recommended[rand_index]
				link = r.get("href")

				# Dummy example link: "https://myanimelist.net/recommendations/anime/1-2"
				# is referenced in these comments

				# Common case where recommendations is in the url for some reason
				if "recommendations" in link:
					link = link.replace("recommendations/", "")
				
				# Either the recommended story has its code on 
				# the left or right side of the hyphen
				codes = link.split("/")[4].split("-")
				link_code_0 = link_code_1 = link.split("/")[4].split("-")[0]

				# Only reassign if the dummy link case is present. Sometimes
				# we have "https://myanimelist.net/recommendations/anime/1" only.
				# In this case, we don't reassign.
				if len(codes) > 1:
					link_code_1 = link.split("/")[4].split("-")[1]

				title = r.find("span", {"class":"title fs10"}).get_text()
				link = "https://myanimelist.net/"+self.category+"/"

				# Compare the page's code against the possible codes. So if 
				# the page's code was 1, we take the elif case since 2 is 
				# on the right side and 1 is on the left, and 1==1.
				if page_code != link_code_0:
					recs.append([title, link+link_code_0])
				elif page_code != link_code_1:
					recs.append([title, link+link_code_1])
				
				attempt_count += 1

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
