#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests

from AmyList import Story, Profile

user = 'amykyst'

show = Story('https://myanimelist.net/anime/205/Samurai_Champloo')
print(show)

user_profile = Profile('https://myanimelist.net/profile/' + user)

print(user_profile.get_faves())