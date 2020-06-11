class Recommendations():

	# Recommends stories base on profile's story lists
	def __init__(self, profile):
		self.profile = profile
		self.anime_recmd = []
		self.manga_recmd = []

	def recommend(self, category):
		current_list_links = self.profile.import_list_links(category)
		for l in current_list_links:
			print(l)
		# TODO: turn links into stories and look at their pages.
		# It might be best to just look at the user scores
		# on line 88 of MAList.py and see if it's above the threshold
		# we want to set. Otherwise, there's no need to even add it to a
		# massive list.
		# So yeah, Profile now needs renovations.
