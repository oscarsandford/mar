#!/usr/bin/env python3

from AmyList import Story, Profile

user1 = 'amykyst'
user2 = 'winstonmanatee'
user3 = 'lanzer001'
user4 = 'frosty114'

def main():
    user_profile = Profile(user4)

    anime = user_profile.get_anime_list()

    for entry in anime:
        if entry.get_title() != 'error':
            print(entry.get_title())

    print('Total Entries:', len(anime))

if __name__ == '__main__':
    main()
# TODO: it seems manga and anime movies are giving me issues
# - movies: Your Name and Silent Voice don't work
# - manga: MF Ghost, SDS, FSN:HF, etc
# I figure index out of range can be fixed by fixing the hard-coded index calls
