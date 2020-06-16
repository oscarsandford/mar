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
	def recommend(self, category, threshold, min_score, max_recommend):
		print("\n\t<> Creating "+category+" recommendations! <>\n")
		good_links = self.profile.import_links(category, threshold)
		shuffle(good_links)
		all_links = self.profile.import_links(category, 0)

		for link in good_links[:5]:
			good_story = Story(link)
			r_links = good_story.get_recommendation_links(10)

			for r_link in r_links:
				if r_link not in all_links:
					r_story = Story(r_link)
					if r_story.get_score() >= min_score:
						self.get_recommendations(category).append(r_story)


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
