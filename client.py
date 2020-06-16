#!/usr/bin/env python3

from MAList import Story, Profile
from MARecommendations import Recommendations
import sys

users = [
	"amykyst",
	"winstonmanatee",
	"lanzer001",
	"frosty114",
	"smokezone"
]

min_consider = 10
min_score = 8
max_recommendations = 5


def main():
	user = sys.argv[1]
	parse_args(Profile(user))

# Do things with given profile based on args
def parse_args(p):
	for i in range(len(sys.argv)):
		if sys.argv[i] == "-m":
			make_user(p)
		elif sys.argv[i] == "-r":
			make_recommendations(p)

# Defines a user's complete anime list and exports it
def make_user(p):
	p.set_all_stories("anime")
	p.export_list("anime")

# Defines a user's recommendations
def make_recommendations(p):
	r = Recommendations(p)
	r.recommend("anime", min_consider, min_score)
	r.export_recommendations("anime")

if __name__ == '__main__':
    main()
