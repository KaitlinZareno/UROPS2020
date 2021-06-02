
import sys,termios, tty, os, time
import threading
from threading import Thread
from keypressTester import KBHit
import csv 

global key_dict 
key_dict = {}
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


def playback():
	global game_over

	if not game_over:
		os.system('python pacman.py --replay recorded-game-0')

		#game has finished executing, do not get any more keypresses
		game_over = True
		print("game over") 


def keypress():
	#Initialize variables
	global game_over
	start = time.clock()
	available = True
	initialized_current = False
	c = 0
	kb = KBHit()

	#start code
	time.sleep(0.05)

	while True:
		if not game_over:		 

			#initialize cuurrent for timer
			if not initialized_current:
				current = time.clock()
				initializedCurrent = True

			#if press key within time limit
			if current - start <= 1.2:
				#if a key hasn't been obtained for the current time interval/state -- not working?
				if available:
					
					#if a key is pressed, obtain key 
					if kb.kbhit():
						char = kb.getch()

						#print("pressed: ", char, available)

						if ord(char) == 27: # ESC
							print(key_dict)
							break

						#update dictionary, block keypresses for the rest of time period
						key_dict[c] = char
						available = False

			#time limit is up, move to next state
			else:
				#if no key was pressed during the time period, set equal to null
				if not c in key_dict:
					key_dict[c] = "-"

				print(c,key_dict[c])
				# print("CHANGE", c)

				#reset counter and timer
				c+=1
				available = True
				start = time.clock()
				initialized_current = False
				kb = KBHit()

		#if game over make csv
		else:
			print(key_dict)
			make_csv()
			break

	kb.set_normal_term()

def make_csv():
		print("creating csv")

		writer = csv.writer(open('merged.csv', 'w'))
		x = 0

		for row in  csv.reader(open('state_action.csv', 'r')):
        	#for every row, append user inp (make new column)
			writer.writerow(row + [key_dict[x]])
			x+=1




if __name__ == "__main__":
	start()