#!/usr/bin/env python3

from MAList import Story, Profile
from MARecommendations import Recommendations
import sys

min_thres = 10
min_score = 8
max_recom = 5


def main():
	user = sys.argv[1]
	parse_args(Profile(user))

# Do things with given profile based on args
def parse_args(p):
	category = "anime"
	for i in range(len(sys.argv)):
		# TODO: revise this if chain
		if sys.argv[i] == "!a":
			category = "anime"
		elif sys.argv[i] == "!m":
			category = "manga"
		elif sys.argv[i] == "-c":
				make_user(p, category)
		elif sys.argv[i] == "-r":
				make_recommendations(p, category)

# Defines a user's complete anime list and exports it
def make_user(p, c):
	p.set_all_stories(c)
	p.export_list(c)

# Defines a user's recommendations
def make_recommendations(p, c):
	r = Recommendations(p)
	r.recommend(c, min_thres, min_score, max_recom)
	r.export_recommendations(c)

if __name__ == '__main__':
    main()
