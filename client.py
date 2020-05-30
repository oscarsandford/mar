#!/usr/bin/env python3

from AmyList import Story, Profile

user1 = 'amykyst'
user2 = 'winstonmanatee'
user3 = 'lanzer001'
user4 = 'frosty114'

def main():
    user_profile = Profile(user4)

    li = user_profile.get_anime_list()
    print(li)

    # Put this info in a txt file
    user_profile.export_anime_list()


if __name__ == '__main__':
    main()
