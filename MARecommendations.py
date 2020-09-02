from MAList import Story
from random import shuffle

class Recommendations():

	# Recommends stories base on profile's story lists
	def __init__(self, profile):
		self.profile = profile
		self.anime_recmd = []
		self.manga_recmd = []

	# Makes list of story recommendations that user has not viewed
	# with score >= min_score based on their stories with score >= min_score
	def recommend(self, user_links, category, min_score, result_count):
		recommended_links, i = [], 0
		shuffle(user_links)

		while len(recommended_links) < result_count and i < len(user_links):
			u_link = user_links[i]
			story = Story(u_link)
			i += 1

			page_links = story.get_page_recommendation_links()
			for link in page_links:
				if link not in user_links:
					recommended_links.append(link)

		list(set(recommended_links))

		for link in recommended_links:
			story = Story(link)
			self.get_recommendations(category).append(story)


	# Returns a given set of recommendations, defaulting to anime
	def get_recommendations(self, category):
		if category == "manga":
			return self.manga_recmd
		else:
			return self.anime_recmd


	# Export recommendations to plaintext file
	def export_recommendations(self, category):
		filename = "rec_" + category + "_" + self.profile.username + ".txt"
		storage = open("./recommendation_lists/" + filename, "w", errors="replace")

		for story in self.get_recommendations(category):
			storage.write(str(story))
		storage.close()
