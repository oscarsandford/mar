#!/usr/bin/env python3

from MAList import Story, Profile
from MARecommendations import Recommendations

user1 = "amykyst"
user2 = "winstonmanatee"
user3 = "lanzer001"
user4 = "frosty114"

def main():
	profile = make_user(user4)
	make_recommendations(profile)

def make_user(u):
	p = Profile(u)
	p.set_list("anime")
	p.export_list("anime")
	return p

def make_recommendations(p):
	r = Recommendations(p)
	r.recommend("anime")


if __name__ == '__main__':
    main()
