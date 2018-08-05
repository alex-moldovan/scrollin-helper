#!/usr/bin/env python

import sys
import time
import scrollphathd as sphd
from multiprocessing import Process

#The screen is rotated on my robot case.
sphd.rotate(180)
sphd.set_brightness(1.0)

if len(sys.argv) != 2:
	print("\nusage: python simple-text-scroll-rotated.py \"message\" \npress CTRL-C to exit\n")
	sys.exit(0)

def scrollText(text):
	sphd.clear()
	sphd.write_string(text, 11)
	while True:
		sphd.show()
		sphd.scroll(1)
		time.sleep(0.05)

if __name__ == '__main__':
	#Start scroll process
	text = sys.argv[1]
	print("%s" % text)
	scrollProcess = Process(target=scrollText, args=text)
	scrollProcess.start()

	sleep(5)

	scrollProcess.terminate()
	scrollProcess.join()