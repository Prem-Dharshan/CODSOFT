#!/usr/bin/env python

__author__ = "Saulius Bartkus"
__copyright__ = "Copyright 2017"

__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Saulius Bartkus"
__email__ = "saulius181@yahoo.com"
__status__ = "Production"


import tkinter as tk
import random
from PIL import Image, ImageTk

class Game(tk.Frame):

	def ai(self):
		return random.choice(["Scissors", "Rock", "Paper"])
		
	def new_game(self):
		if self.canvas.data["play"] is None:
			self.canvas.data["play"] = True
			self.l1.configure(text="Select your hand")
		elif self.canvas.data["play"] is True:
			pass
		else:
			self.canvas.itemconfigure(7, state=tk.HIDDEN, image="")
			self.canvas.itemconfigure(8, state=tk.HIDDEN, image="")

			self.canvas.itemconfigure(2, state=tk.NORMAL)
			self.canvas.itemconfigure(4, state=tk.NORMAL)
			self.canvas.itemconfigure(6, state=tk.NORMAL)			
			
			self.canvas.data["play"] = True
			self.l1.configure(text="Select your hand")			
			
	def quit_game(self):
		pass
		
	def load_images(self):
		
		self.canvas.data["Player"] = {}
		self.canvas.data["AI"] = {}
		
		self.rock1 = Image.open("rock1.png")
		self.rock2 = Image.open("rock2.png")
		self.scissors1 = Image.open("scissors1.png")
		self.scissors2 = Image.open("scissors2.png")
		self.paper1 = Image.open("paper1.png")
		self.paper2 = Image.open("paper2.png")

		self.canvas.data["Player"]["Rock"] = ImageTk.PhotoImage(self.rock1)
		self.canvas.data["AI"]["Rock"] = ImageTk.PhotoImage(self.rock2)
		self.canvas.data["Player"]["Scissors"] = ImageTk.PhotoImage(self.scissors1)
		self.canvas.data["AI"]["Scissors"] = ImageTk.PhotoImage(self.scissors2)
		self.canvas.data["Player"]["Paper"] = ImageTk.PhotoImage(self.paper1)
		self.canvas.data["AI"]["Paper"] = ImageTk.PhotoImage(self.paper2)		
		
		self.canvas_scissors_back = self.canvas.create_rectangle(31, 171, 169, 309, fill="#000055", dash=200, width=5, stipple='gray25', state=tk.HIDDEN)
		self.canvas_scissors1 = self.canvas.create_image(100, 240, image=self.canvas.data["Player"]["Scissors"], tag="Scissors")
		
		self.canvas_rock_back = self.canvas.create_rectangle(206, 171, 344, 309, fill="#000055", dash=200, width=5, stipple='gray25', state=tk.HIDDEN)
		self.canvas_rock1 = self.canvas.create_image(275, 240, image=self.canvas.data["Player"]["Rock"], tag="Rock")
		
		self.canvas_paper_back = self.canvas.create_rectangle(381, 171, 519, 309, fill="#000055", dash=200, width=5, stipple='gray25', state=tk.HIDDEN)
		self.canvas_paper1 = self.canvas.create_image(450, 240, image=self.canvas.data["Player"]["Paper"], tag="Paper")
		
		self.canvas_player_pick = self.canvas.create_image(180, 130, image="", tag="Player Pick", state=tk.HIDDEN)
		self.canvas_ai_pick = self.canvas.create_image(380, 130, image="", tag="AI Pick", state=tk.HIDDEN)
		
	def bind_images(self):
		self.canvas.tag_bind(self.canvas_scissors1, "<Enter>", self.on_enter)
		self.canvas.tag_bind(self.canvas_scissors1, "<Leave>", self.on_leave)
		self.canvas.tag_bind(self.canvas_rock1, "<Enter>", self.on_enter)
		self.canvas.tag_bind(self.canvas_rock1, "<Leave>", self.on_leave)
		self.canvas.tag_bind(self.canvas_paper1, "<Enter>", self.on_enter)
		self.canvas.tag_bind(self.canvas_paper1, "<Leave>", self.on_leave)		

		self.canvas.tag_bind(self.canvas_scissors1, "<Button-1>", self.on_click)
		self.canvas.tag_bind(self.canvas_rock1, "<Button-1>", self.on_click)
		self.canvas.tag_bind(self.canvas_paper1, "<Button-1>", self.on_click)
		
	def __init__(self, *args, **kwargs):
		tk.Frame.__init__(self, *args, **kwargs)
		self.canvas = tk.Canvas(root, width=565, height=310)
		self.canvas.pack()
		
		self.button1 = tk.Button(self.canvas, text = "New game", anchor = tk.W, command = self.new_game)
		self.button1.place(x=460,y=25)
		self.button2 = tk.Button(self.canvas, text = "Quit", anchor = tk.W, command = self.quit)
		self.button2.place(x=530,y=25)

		self.canvas.data = { }
		self.canvas.data["play"] = None
		
		self.load_images()
		self.bind_images()
		
		self.l1 = tk.Label(self, text="Rock-Paper-Scissors Tk")
		self.l2 = tk.Label(self, text="", width=40)
		self.l1.pack(side="top")
		self.l2.pack(side="top", fill="x")
	
	def on_click(self, event):
		self.aiPick = self.ai()
		
		self.canvas.itemconfigure(1, state=tk.HIDDEN)
		self.canvas.itemconfigure(3, state=tk.HIDDEN)
		self.canvas.itemconfigure(5, state=tk.HIDDEN)
		
		self.canvas.itemconfigure(2, state=tk.HIDDEN)
		self.canvas.itemconfigure(4, state=tk.HIDDEN)
		self.canvas.itemconfigure(6, state=tk.HIDDEN)
		
		self.canvas.itemconfigure(7, state=tk.NORMAL, image=self.canvas.data["Player"][self.playerPick])
		self.canvas.itemconfigure(8, state=tk.NORMAL, image=self.canvas.data["AI"][self.aiPick])
		
		self.l2.configure(text="")
		
		if self.aiPick == self.playerPick:
			self.l1.configure(text="It's a draw")
		elif self.aiPick == "Rock":
			if self.playerPick == "Scissors":
				self.l1.configure(text="Rock beats scissors: Player lose")
			else:
				self.l1.configure(text="Paper beats rock: Player win")
		elif self.aiPick == "Paper":
			if self.playerPick == "Rock":
				self.l1.configure(text="Paper beats rock: Player lose")
			else:
				self.l1.configure(text="Scissors beats paper: Player win")
		else:
			if self.playerPick == "Paper":
				self.l1.configure(text="Scissors beats paper: Player lose")
			else:
				self.l1.configure(text="Rock beats scissors: Player win")
		
		self.canvas.data["play"] = False
		
	def on_enter(self, event):
		if self.canvas.data["play"]:		
			self.currentID = self.canvas.find_withtag(tk.CURRENT)[0]
			self.playerPick = self.canvas.gettags(self.currentID)[0]
			self.l2.configure(text="Pick {}".format(self.playerPick))
			self.canvas.itemconfigure(self.currentID-1, state=tk.NORMAL)
		
	def on_leave(self, enter):
		if self.canvas.data["play"]:
			self.l2.configure(text="")
			self.canvas.itemconfigure(self.currentID-1, state=tk.HIDDEN)
		
if __name__ == "__main__":
	root = tk.Tk()
	Game(root).pack(side="top", fill="both", expand="true")
	root.mainloop()