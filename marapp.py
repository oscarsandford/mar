import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

kivy.require("1.11.1")

from MAList import Story, Profile
from MARecommendations import Recommendations

min_thres = 10
min_score = 8
max_recom = 5

class RecommendationsPage(GridLayout):
	query_name = ObjectProperty(None)
	query_category = ObjectProperty(None)
	query_results = ObjectProperty(None)
	recommendations = []

	def search_for_user(self):
		self.query_results.clear_widgets()
		filename = "rec_" + self.query_category.text + "_" + self.query_name.text + ".txt"
		try:
			storage = open("./recommendation_lists/" + filename, "r")
			lines = storage.readlines()
			for i in range(len(lines)):
				if "Title" in lines[i]:
					title = lines[i].split("Title: ")[1].strip()
					link = lines[i+1].split("Link: ")[1].strip()
					# TODO: these lines are temp, add title instead
					self.add_result_label(title)
					self.recommendations.append(link)
					print("Story:", link)
			storage.close()

		except FileNotFoundError:
			self.make_recommendations()


	def add_result_label(self, st):
		label = Label(text=st)
		self.query_results.add_widget(label)


	# Processes a list of recommendations if the user doesn't have any
	def make_recommendations(self):
		profile = Profile(self.query_name.text)
		r = Recommendations(profile)
		r.recommend(self.query_category.text, min_thres, min_score, max_recom)
		r.export_recommendations(self.query_category.text)


class MarApp(App):
	def build(self):
		return RecommendationsPage()

if __name__ == '__main__':
	MarApp().run()
