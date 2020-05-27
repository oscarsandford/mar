#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests

from AmyList import Story

show = Story('https://myanimelist.net/anime/205/Samurai_Champloo')
print(show)