#getch adapted from https://www.jonwitts.co.uk/archives/896

import sys,termios, tty, os, time
import multiprocessing as mp
from multiprocessing import Process, Queue
import threading
from threading import Thread
from keypressTester import KBHit

global key_dict 
key_dict = {}
game_over = False
end = False

def start():
	print("starting in 1 second")
	time.sleep(1)

	keyThread = threading.Thread(target = keypress)
	#playThread = threading.Thread(target = playback)

	keyThread.start()
	#playThread.start()


def playback():
	os.system('python pacman.py --replay recorded-game-0')

	if end:
		sys.exit()
	#game has finished executing, do not get any more keypresses
	game_over = True
	print("game over")

def keypress():

    kb = KBHit()
    start = time.clock()
    available = True
    c = 0

    #print('Hit any key, or ESC to exit')

    while True:
    	current = time.clock()
    	key_dict[c] = ""

    	if current - start >= 1:
    		if kb.kbhit() and available:
			    char = kb.getch()
			    key_dict[c] = char
			    available = False

			    if ord(char) == 27: # ESC
			        break
    		#print(c, key_dict[c])

        else:
			c+=1
			start = time.clock()
			available = True



    kb.set_normal_term()



def get_keypress():
	print("obtain keypress")
	start = time.time()
	available = True
	c = 0

	while True:
		#if it's been within 1 second
		current = time.time()

		if current - start <= 1:

			# if no input within a certain time frame run again
			if time.time()-current > 0.49:
				continue

			char = getch()

			#add 1 char to dictionary
			if char:
				if available:
					if char == "-":
						end = True
						print("ending")
						sys.exit()

					available = False
					key_dict[c] = char

		else:
			key_dict[c] = " "
			print("end state")
			print(c, key_dict[c])
			c+=1
			start = time.time()
			available = True



def getch():
	fd = sys.stdin.fileno()
	old = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd,termios.TCSADRAIN,old)
	return ch




if __name__ == "__main__":
	start()