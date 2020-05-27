#!/usr/bin/env python3

from AmyList import Story, Profile

user1 = 'amykyst'
user2 = 'winstonmanatee'
user3 = 'lanzer001'

user_profile = Profile('https://myanimelist.net/profile/' + user1)

print(user_profile.get_fave_anime())
print('------------------------------')
print(user_profile.get_fave_manga())

# TODO: it seems manga and anime movies are giving me issues
# - movies: Your Name and Silent Voice don't work
# - manga: MF Ghost, SDS, FSN:HF, etc
