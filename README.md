# Many Anime Recommendations (MAR)

## Overview
This project uses Python and various libraries to extract page data from profiles on [MyAnimeList](https://myanimelist.net/profile/amykyst). The harvested data is then used to create personalized recommendations for anime to watch or manga to read. This information is accessible through a desktop application. Plans are in place to make a version for Android devices.

## Table of Contents
1. Installation
2. Usage
3. Authors
4. Acknowledgements

<hr/>

## Installation
The release package includes the latest build with resources to run the Kivy app as is. For development purposes, clone the source code and install the requirements.
```
git clone https://github.com/oscarsandford/Many-Anime-Recommendations.git
```
In its current state, this project requires installation of the following:
- [Python 3](https://www.python.org/download/releases/3.0/) (naturally)
- [Kivy 1.11.1](https://kivy.org/#home) (for the application itself)
- [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/) (for reading HTML)
- [Requests](https://3.python-requests.org/) (to ask nicely)
- [Colorama](https://github.com/tartley/colorama) (makes terminal output more colourful!)

Once cloned, dependency installation can be swiftly accomplished with `pip install -r requirements.txt`.

Python 3.7 is recommended to work smoothly with Kivy 1.11.1. If Python 3.8 is installed, and you are having issues with Kivy, try installing Kivy master with:
```
pip install kivy[base] kivy_examples --pre --extra-index-url https://kivy.org/downloads/simple
```


## Usage

### Command Line
Execute `python marapp.py` in a terminal to launch the Kivy app.

### Kivy Application
The Kivy executable in the latest release build can be started via the included shortcut. Same effect as starting the program from the terminal.

## Authors
Created by Oscar Sandford.

## Acknowledgements
The Anime Recommendations project would be impossible without the documentation and technical effort behind [myanimelist.net](https://myanimelist.net/). My work is meant to complement this service and provide more information to users about anime and manga. Thanks is also due to the developers who create and maintain this project's dependencies.
