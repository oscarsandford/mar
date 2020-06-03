#!/usr/bin/env python3

from AmyList import Story, Profile

user1 = "amykyst"
user2 = "winstonmanatee"
user3 = "lanzer001"
user4 = "frosty114"

def main():
	user = Profile(user4)
	user.export_list("anime")
	user.export_list("manga")

if __name__ == '__main__':
    main()
