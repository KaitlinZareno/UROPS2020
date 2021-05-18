import Tkinter as tk
import time
import sys
import os
import multiprocessing
from threading import Thread

class pacmanGui(tk.Frame):
	#path to state video
	global PATH
	PATH = "/home/kaitlinzareno/Desktop/UROPS2021/"

	def __init__(self, parent):
		self.parent = parent
		self.frame = tk.Frame(self.parent)
		canvas = tk.Canvas(parent, width = 650, height = 750)
		canvas.pack()

		self.key_dict = {}
		self.game_over = False
		#keep track of keypress
		self.c=0

		self.input_box(parent,canvas)

		#button to start processes
		B= tk.Button(parent,text="playback states",command= self.start)
		B.pack()

	#create input box
	def input_box(self,parent,canvas):
		self.response = tk.Entry(parent) 
		canvas.create_window(325, 550, window=self.response)

	#start threads
	def start(self):
		try:
			pac = Thread(self.playback())
			inp = Thread(self.get_inp, args = (1,))

			#start threads and wait for execution
			pac.start()
			inp.start()
			pac.join()
			inp.join()

			#write to csv/merge with pacman data 
			to_csv = Thread(self.make_csv())
			to_csv.start()
			to_csv.join()

		except: 
			print("Error: unable to start thread")


	def get_inp(self, delay):
		#while pacman states are still being replayed
		while not self.game_over:
			#wait one second for state to change --> time.sleep good??
			time.sleep(delay)
			#obtain response
			res = self.response.get()
			print(res)
			#add keypress to dictionary
			self.key_dict[self.c] = res
			self.c+=1
			#refreshes/clears inp box at the end of every second
			self.response.delete(0,"end")

		print("game over inp")


	def playback(self):
		os.system('python pacman.py --replay recorded-game-0')
		#game has finished executing, do not get any more keypresses
		self.game_over = True
		print("game over")

	def make_csv(self):
		#write user inp to csv files 
		with open('state_action.csv') as r, open('merged.csv', 'w') as file:
			reader = csv.reader(r)
			writer = csv.writer(file)

	        for row in reader:
	        	#for every row, append user inp (make new column)
	            writer.writerow(row + [key_dict[x]])

	


if __name__ == "__main__":
    root = tk.Tk()
    #root.geometry("650x750")
    pacmanGui(root)
    root.mainloop()