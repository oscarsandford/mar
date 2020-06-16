# Anime Recommendations

### Overview
This project uses Python and the Beautiful Soup library to extract page data from profiles on [MyAnimeList](https://myanimelist.net/profile/amykyst). The harvested data is then to create personalized recommendations for anime to watch or manga to read.

### Table of Contents
1. Installation
2. Usage
3. Acknowledgements

<hr/>

### Installation
There are currently no convenient ways to install a polished version of this project besides downloading the repository and running usage commands via the command line. Eventually, I hope to make a functioning app that can be simply installed to desktop.

### Usage
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

### Acknowledgements
The Anime Recommendations project would be impossible without the documentation and technical effort behind [myanimelist.net](https://myanimelist.net/). My work is meant to complement this service and provide more information to users about anime and manga.
