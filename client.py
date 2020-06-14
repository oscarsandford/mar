#!/usr/bin/env python3

from MAList import Story, Profile
from MARecommendations import Recommendations

user1 = "amykyst"
user2 = "winstonmanatee"
user3 = "lanzer001"
user4 = "frosty114"

min_score = 10


def main():
	profile = Profile(user4)
	make_recommendations(profile)
	#make_user(profile)

# Defines a user's complete anime list and exports it
def make_user(p):
	p.set_all_stories("anime")
	p.export_list("anime")

# Defines a user's recommendations
def make_recommendations(p):
	r = Recommendations(p)
	r.recommend("anime", min_score)
	r.export_recommendations("anime")

if __name__ == '__main__':
    main()
