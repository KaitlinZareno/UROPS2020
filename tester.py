import Tkinter as tk
from Tkinter import Tk, Entry


class tester(tk.Frame):

	def __init__(self, parent):
		self.parent = parent
		self.frame = tk.Frame(self.parent)

		self.canvas = tk.Canvas(parent, width = 100, height = 100)
		self.canvas.pack()

		self.key_dict = {}
		self.game_over = False
		#keep track of keypress
		self.c=0

		self.input_box(parent)

		B= tk.Button(parent,text="playback states",command= self.start)
		B.pack()


	def start(self):
		try:
			# Bind entry to any keypress
			self.entry.bind("<Key>", self.click)

			# while self.c<5:
			# 	if time.time()-start >=2:
			#  		print('start thread')
			# 	 	inp = Process(target = self.input_box)
			# 	 	inp.start()
			# 	 	inp.join() #dont make killed process a zombie
			# 	 	inp.terminate()
			# 	 	start = time.time()
			# 	 	self.c+=1

		except:
			print("Error: unable to start thread")



	def input_box(self, parent):
		self.entry = Entry()
		self.entry.focus_set()
		self.entry.pack()


	def click(self,key):
	    # print the key that was pressed
	    print(key.char)
	    self.clear_entry()

	def clear_entry(self):
		self.entry.delete(0,"end")
		root.update()



if __name__ == "__main__":
    root = tk.Tk()
    #root.geometry("650x750")
    tester(root)
  
    root.mainloop()