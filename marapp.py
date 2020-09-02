import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.config import Config

kivy.require("1.11.1")

from MAList import Story, Profile
from MARecommendations import Recommendations
import webbrowser

Config.set("graphics", "width", "400")
Config.set("graphics", "height", "700")
Config.set("graphics", "resizable", False)


class RecommendationsPage(GridLayout):
	query_name = ObjectProperty(None)
	query_category = ObjectProperty(None)
	results_list = ObjectProperty(None)
	results_count = ObjectProperty(None)
	results_min_score = ObjectProperty(None)
	recommendations = []

	def search_for_user(self):
		self.results_list.clear_widgets()
		filename = "rec_" + self.query_category.text + "_" + self.query_name.text + ".txt"
		try:
			storage = open("./recommendation_lists/" + filename, "r")
			lines = storage.readlines()
			for i in range(len(lines)):
				if "Title" in lines[i]:
					title = lines[i].split("Title: ")[1].strip()
					link = lines[i+1].split("Link: ")[1].strip()
					self.add_result_label(title, link)
					self.recommendations.append(link)
			storage.close()

		except FileNotFoundError:
			print("[Search] No recommendations found. Creating recommendations...")
			self.make_recommendations()


	def add_result_label(self, label_title, label_link):
		label = Button(
			text=label_title,
			on_press=self.open_link,
			size_hint_y=None,
			height="40dp",
			background_color=[1,30,150,0.5]
		)
		self.results_list.add_widget(label)

	def open_link(self, instance):
		print("TODO: implement opening links with browser")

	# Processes a list of recommendations if the user doesn't have any, or
	# if the client decides to generate new recommendations for a user
	def make_recommendations(self):
		print("\n(1/3) Collecting "+self.query_name.text+"'s "+self.query_category.text+"...")
		p = Profile(self.query_name.text)
		story_links = p.import_links(self.query_category.text, int(self.results_min_score.value))

		print("(2/3) Creating "+self.query_category.text+" recommendations...")
		r = Recommendations(p)
		r.recommend(story_links, self.query_category.text, int(self.results_min_score.value), int(self.results_count.value))

		print("(3/3) Exporting...")
		r.export_recommendations(self.query_category.text)


	def exit_app(self, instance):
		exit(1)


class MarApp(App):
	def build(self):
		return RecommendationsPage()

if __name__ == '__main__':
	MarApp().run()
