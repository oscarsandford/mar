from MAList import Story
from random import shuffle

class Recommendations():

	# Recommends stories base on profile's story lists
	def __init__(self, profile):
		self.profile = profile
		self.anime_recmd = []
		self.manga_recmd = []


	# Makes list of story recommendations that user has not viewed
	# with score >= min_score based on their stories with score >= threshold
	def recommend(self, category, threshold, min_score, max_rec):
		print("\n\t<> Creating "+category+" recommendations! <>\n")

		best_user_links = self.profile.import_links(category, threshold)
		shuffle(best_user_links)
		all_user_links = self.profile.import_links(category, 0)
		recommended_links = []

		for link in best_user_links[:max_rec]:
			story = Story(link)
			recommended_links += story.get_recommendation_links(max_rec)

		list(set(recommended_links))

		for link in recommended_links:
			if link not in all_user_links:
				story = Story(link)
				if story.get_score() >= min_score:
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
		storage.write(self.profile.username + "\'s " + category + " recommendations:\n")

		for story in self.get_recommendations(category):
			storage.write(str(story))
		storage.close()
