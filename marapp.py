import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.dropdown import DropDown
kivy.require("1.11.1")

from MAList import Story, Profile
from MARecommendations import Recommendations

min_thres = 10
min_score = 8
max_recom = 5

class RecommendationsPage(GridLayout):
	query_name = ObjectProperty(None)
	query_category = ObjectProperty(None)

	# For now we just look for a recommendation list for the query's name
	# and if they don't have a receommendations list, generate one.
	def search_for_user(self):
		# So name_query is now our username (i.e "amykyst")
		filename = "rec_" + self.query_category.text + "_" + self.query_name.text + ".txt"
		with open("./recommendation_lists/" + filename, "r") as storage:
			if storage.readline() != "":
				lines = storage.readlines()
				for line in lines:
					if "Link" in line:
						link = line.split("Link: ")[1].strip()
						print("Anime:", link)
			else:
				storage.close()
				self.make_recommendations()

		storage.close()


	# Processes a list of recommendations if the user doesn't have any
	def make_recommendations(self):
		profile = Profile(self.query_name.text)
		r = Recommendations(profile)
		r.recommend(self.query_category.text, min_thres, min_score, max_recom)
		r.export_recommendations(self.query_category.text)

	def app_exit(self):
		exit(1)



class MarApp(App):
	def build(self):
		return RecommendationsPage()

if __name__ == '__main__':
	MarApp().run()
