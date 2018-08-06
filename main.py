#!/usr/bin/env python

import sys
import time
from multiprocessing import Manager

import botconfig
import botuser
import bot

# ChatBot account login
# A 2FA prompt will be shown if it's enabled on Facebook.
facebookUsername = botConfig["username"]
facebookPassword = botConfig["password"]

# Might want to use this without a Scroll pHAT HD)
useRobot = True
try:
	import scrollphathd as sphd
except:
	useRobot = False

if __name__ == '__main__':
	with Manager() as manager:
		
		# Time keeping thread
		dateTime = manager.dict()
		dateTime['time'] = time.strftime("%H:%M")
		dateTime['datetime'] = time.strftime("%H:%M")
		dateTime['date'] = time.strftime("%H:%M")
		clockProcess = startProcess(updateClock, [dateTime])

		# Initial screen clear
		if useRobot:
			#The screen is installed upside down on my robot case.
			sphd.rotate(180)
			sphd.set_brightness(1.0)
			clearText()
		
		# ChatBot client
		try:
			client = DeskBot(facebookUsername, facebookPassword, dateTime, useRobot)
			client.listen()
		except (KeyboardInterrupt, SystemExit):
			print("Going to sleep")
			stopProcess(clockProcess)
			stopProcess(client.scrollProcess)
			sys.exit()
