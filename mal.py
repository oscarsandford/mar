#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

response = requests.get("https://myanimelist.net/profile/amykyst")
soup = BeautifulSoup(response.text, "html.parser")

user_faves = soup.find(class_="user-favorites js-truncate-inner di-t mb24")

fave_anime = user_faves.find_all(class_="di-tc")[0]
fave_manga = user_faves.find_all(class_="di-tc")[1]
fave_chars = user_faves.find_all(class_="di-tc")[2]
fave_peopl = user_faves.find_all(class_="di-tc")[3]

# print out titles off amykyst's favourite anime
for series in fave_anime.find_all(class_="list di-t mb8"):
    title = series.find(class_="di-tc va-t pl8 data").get_text()
    title = title.replace("  ", "")
    title = title.replace("\n", "")
    print(title)
