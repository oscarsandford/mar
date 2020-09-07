import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.config import Config

kivy.require("1.11.1")

from MAProfile import Profile
from MARecommendations import Recommendations
import webbrowser
import colorama

colorama.init()
Config.set("graphics", "width", "420")
Config.set("graphics", "height", "720")
Config.set("graphics", "resizable", False)
Config.set("kivy","window_icon","./assets/marapp_icon.png")


class RecommendationsPage(GridLayout):

	name = ObjectProperty(None)
	category = ObjectProperty(None)
	results_list = ObjectProperty(None)
	results_count = ObjectProperty(None)
	results_min_score = ObjectProperty(None)


	# Pull up a list of recommendations based on user input.
	def search_for_user(self):
		self.results_list.clear_widgets()
		filepath = "./recommendation_lists/" + "rec_" + self.category.text + "_" + self.name.text + ".txt"
		try:
			with open(filepath, "r") as storage:
				lines = storage.readlines()
				for i in range(len(lines)-1):
					if "https://myanimelist.net/" in lines[i+1]:
						btn = Button(
							text=lines[i].strip(),
							on_press=self.open_link,
							size_hint_y=None,
							height="40dp",
							color=[0,0,0,1],
							background_color=[1,30,150,0.8]
						)
						self.results_list.add_widget(btn)
			storage.close()

		except FileNotFoundError:
			print("[Search] No recommendations found. Creating recommendations...")
			self.make_recommendations()


	# (TODO: implement opening links with browser)
	def open_link(self, instance):
		print("TODO: implement opening links with browser")


	# Builds a list of recommendations if the user doesn't have any, or
	# if the client decides to generate new recommendations for a user.
	def make_recommendations(self):
		if self.name.text == "":
			print("[\033[36mMAR\033[0m] No input!")
			return

		print("\n\033[1m(1/3)\033[0m Collecting \033[95m"+self.name.text+"\033[0m's "+self.category.text+"...")
		p = Profile(self.name.text)
		all_stories, filtered_stories = p.import_list(self.category.text, int(self.results_min_score.value))

		if len(all_stories) == 0:
			print("[\033[36mMAR\033[0m] No stories!")
			return

		print("(\033[1m2/3)\033[0m Creating "+self.category.text+" recommendations with \033[96m"+str(len(filtered_stories))+"\033[0m stories...")
		r = Recommendations(p, self.category.text)
		r.recommend(all_stories, filtered_stories, int(self.results_count.value), int(self.results_count.max))

		print("\033[1m(3/3)\033[0m Exporting...")
		r.export_recommendations()
		print("(\033[92m@\033[0m) Complete!")


	def exit_app(self, instance):
		exit(1)


class MARApp(App):
	def build(self):
		print("[\033[36mMAR\033[0m] Launching MAR...")
		return RecommendationsPage()


if __name__ == '__main__':
	MARApp().run()
