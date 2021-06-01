#getch adapted from https://www.jonwitts.co.uk/archives/896

import sys,termios, tty, os, time
import multiprocessing as mp
from multiprocessing import Process, Queue
import threading
from threading import Thread
from keypressTester import KBHit

global key_dict 
key_dict = {}
condition = threading.Condition()
game_over = False
global PATH
PATH = "/home/kaitlinzareno/Desktop/UROPS2021/"

def start():
	global game_over 
	print("starting in 1 second")
	time.sleep(1)

	keyThread = threading.Thread(target = keypress)
	playThread = threading.Thread(target = playback)

	keyThread.start()
	playThread.start()

	if game_over:
		make_csv()
		sys.exit()


def playback():
	global game_over

	if not game_over:
		os.system('python pacman.py --replay recorded-game-0')

		#game has finished executing, do not get any more keypresses
		game_over = True
		print("game over") 


def keypress():
	global game_over
	start = time.clock()
	available = True
	c = 0
	initialized_current = False
	kb = KBHit()
	time.sleep(0.05)
	onePressed = False
	key_inp = ""

	while True:
		if not game_over:		 

			#initialize cuurrent for timer
			if not initialized_current:
				current = time.clock()
				initializedCurrent = True

			#if press key within time limit
			if current - start <= 2.2:
				if available:
					#timeout if user doesn't input button -- tries to unblock getch process
					if kb.kbhit():

						char = kb.getch()

						print("pressed: ", char, available)

						if ord(char) == 27: # ESC
							print(key_dict)
							break

						#update dictionary, block keypresses for the rest of time period
						key_dict[c] = char
						available = False
			else:
				#if no key was pressed during the time period, set equal to null
				if not key_inp:
					key_dict[c] = ""
				else:
					key_dict[c] = key_inp

				print(c,key_dict[c])
				print("CHANGE", c)

				#reset counter and timer
				c+=1
				available = True
				start = time.clock()
				initialized_current = False
				kb.reset()

		else:
			#print(key_dict)
			break

	kb.set_normal_term()

def make_csv():
		print("creating csv")
		#write user inp to csv files 
		with open('state_action.csv') as r, open('merged.csv', 'w') as file:
			reader = csv.reader(r)
			writer = csv.writer(file)
			x = 0

	        for row in reader:
	        	#for every row, append user inp (make new column)
	            writer.writerow(row + [key_dict[x]])
	            x+=1




if __name__ == "__main__":
	start()