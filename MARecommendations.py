from MAList import Story
from random import shuffle

class Recommendations():

	# Create Recommendations for some given Profile.
	# Set up blank lists for anime and manga recommendation lists.
	# (This class could end up obsolete, as Profile might handle its functionality.)
	def __init__(self, profile):
		self.profile = profile
		self.anime_r_list = []
		self.manga_r_list = []


	# Get a collection of stories, look at each story page and grab its recommendation
	# links. Add any of these links to the list of recommendations, if not already seen.
	def recommend(self, user_links, category, min_score, result_count):
		recommended_links = []
		
		print("[Recommendations] (1/2) Collecting some user stories...")

		shuffle(user_links)
		i = 0

		for page in user_links:
			story = Story(page)
			page_links = story.get_page_recommendation_links()
			i = 0

			while len(recommended_links) < result_count and i < len(page_links):
				link = page_links[i]
				if link not in user_links + recommended_links:
					recommended_links.append(link)
				i += 1

			if len(recommended_links) >= result_count:
				break

		print("[Recommendations] (2/2) Creating recommendations...")

		for link in recommended_links:
			story = Story(link)
			self.get_recommendations(category).append(story)


	# Returns the appropriate list of recommendations, defaulting to anime
	def get_recommendations(self, category):
		if category == "manga":
			return self.manga_r_list
		else:
			return self.anime_r_list


	# Export existing recommendations list of a given category to plaintext file
	def export_recommendations(self, category):
		filename = "rec_" + category + "_" + self.profile.username + ".txt"
		storage = open("./recommendation_lists/" + filename, "w", errors="replace")

		for story in self.get_recommendations(category):
			storage.write(str(story))
		storage.close()
