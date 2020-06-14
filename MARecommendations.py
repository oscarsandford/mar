from MAList import Story

class Recommendations():

	# Recommends stories base on profile's story lists
	def __init__(self, profile):
		self.profile = profile
		self.anime_recmd = []
		self.manga_recmd = []

	def recommend(self, category, threshold):
		good_links = self.profile.import_good_links(category, threshold)
		for link in good_links:
			good_story = Story(link)
			self.get_recommendations(category).append(good_story)


	# Returns a given set of recommendations, defaulting to anime
	def get_recommendations(self, category):
		if category == "manga":
			return self.manga_recmd
		else:
			return self.anime_recmd


	# Export recommendations to plaintext file
	def export_recommendations(self, category):
		filename = "rec_" + category + "_" + self.profile.username + ".txt"
		storage = open(filename, "w", errors="replace")
		storage.write(self.profile.username + "\'s " + category + " recommendations:\n")

		for story in self.get_recommendations(category):
			storage.write(str(story))
		storage.close()
