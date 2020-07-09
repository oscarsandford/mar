# Many Anime Recommendations (MAR)

## Overview
This project uses Python and various libraries to extract page data from profiles on [MyAnimeList](https://myanimelist.net/profile/amykyst). The harvested data is then used to create personalized recommendations for anime to watch or manga to read. This information is accessible through a work in progress desktop application.

## Table of Contents
1. Installation
2. Usage
3. Acknowledgements

<hr/>

## Installation
As of now, there is no convenient way to install a polished version of this project besides downloading the repository and running it through a terminal.
A desktop application is in development to remedy this.

In its current state, this project requires installation of the following:
- [Python 3](https://www.python.org/download/releases/3.0/)
- [Kivy](https://kivy.org/#home)
- [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](https://3.python-requests.org/)

## Usage

### Command Line
This program can be run by navigating to the repository folder. The file `client.py` can be run in a terminal with the following command.
```
client.py <MAL username> <list arguments>
```
List arguments can be chosen from the following list. Multiple arguments are allowed and the order does not matter, but take care (i.e. you cannot create manga recommendations for a user before defining their manga list). If a category is not specified, the default will be anime.

- `!a` Specifies anime category
- `!m` Specifies manga category
- `-c` Create complete list for specified category
- `-r` Create recommendations list for specified category based on existing user list

Please note that the first argument **must** be the username of the target.

### Kivy Application
The work in progress Kivy app can be launched using Python. Execute `marapp.py` in a terminal to launch.

## Authors
Created by Oscar Sandford.

## Acknowledgements
The Anime Recommendations project would be impossible without the documentation and technical effort behind [myanimelist.net](https://myanimelist.net/). My work is meant to complement this service and provide more information to users about anime and manga.

In addition to standard Python libraries, this project makes use of [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/) and [Kivy](https://kivy.org/#home) for its web scraping and application support, respectively.
