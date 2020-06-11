class Recommendations():

	# Recommends stories base on profile's story lists
	def __init__(self, profile):
		self.profile = profile
		self.anime_recmd = []
		self.manga_recmd = []

	def recommend(self, category, threshold):
		good_ones = self.profile.set_stories(category, threshold)

		for story in good_ones:
			print(str(story))

		# TODO: Great, we got a bunch of stories with "good" ratings.
		# Now we need to fish the recommendation section from the story
		# page and add the first few stories to the list of recommendations.
