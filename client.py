#!/usr/bin/env python3

from MAList import Story, Profile
from MARecommendations import Recommendations

user1 = "amykyst"
user2 = "winstonmanatee"
user3 = "lanzer001"
user4 = "frosty114"


def main():
	profile = Profile(user4)
	make_user(profile)
	make_recommendations(profile)

def make_user(p):
	p.set_list("anime")
	p.export_list("anime")

def make_recommendations(p):
	r = Recommendations(p)
	r.recommend("anime")


if __name__ == '__main__':
    main()
