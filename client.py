#!/usr/bin/env python3

from MAList import Story, Profile

user1 = "amykyst"
user2 = "winstonmanatee"
user3 = "lanzer001"
user4 = "frosty114"

def main():
	profile = make_user(user4)

def make_user(user):
	p = Profile(user)
	p.set_list("anime")
	p.export_list("anime")
	return p

if __name__ == '__main__':
    main()
