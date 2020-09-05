from MAList import Story
import random

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
		used_indices = []
		print("[Recommendations] (1/2) Collecting some user stories...")

		while len(recommended_links) < result_count:
			rand_index = random.randint(0,len(user_links)-1)
			rand_link = user_links[rand_index]

			if rand_index not in used_indices:
				story = Story(rand_link)
				page_links = story.get_page_recommendation_links()
				recommended_links += [link for link in page_links if link not in user_links + recommended_links]
				used_indices.append(rand_index)

		print("[Recommendations] (2/2) Creating recommendations...")
		self.set_recommendations([Story(link) for link in recommended_links], category)


	# Overwrites the appropriate list of recommendations, defaulting to anime
	def set_recommendations(self, li, category):
		if category == "manga":
			self.manga_r_list = li
		else:
			self.anime_r_list = li


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
