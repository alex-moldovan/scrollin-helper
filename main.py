#!/usr/bin/env python

import sys
import time
from multiprocessing import Manager, Process

from fbchat import Client, log
from fbchat.models import *

from botconfig import *
from botuser import *

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

class DeskBot(Client):
	def __init__(self, email, password):
		
		self.scrollProcess = None
		self.users = {}
		
		self.actions = {
			"ohanes" : "say _ _ _ _   _ _ _",
			"time" : "show the current time"
		}

		client = Client.__init__(self, email, password)

	def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
		# Heartbeat
		self.markAsDelivered(thread_id, message_object.uid)
		self.markAsRead(thread_id)

		msg = ("%s".lower()) % message_object.text
		
		user = None
		if author_id in self.users:
			user = self.users[author_id]
		else:
			user = BotUser(author_id, thread_id)
			self.users[author_id] = user

		publishToRobot = True if (useRobot and user.isAdmin) else False

		if publishToRobot:
			print("Should publish")

		if "ohanes" in msg:
			self.send(Message(text="_ _ _ _   _ _ _"), thread_id=thread_id, thread_type=thread_type)
			
			if publishToRobot:
				# Clear what's currently displayed on the screen
				if self.scrollProcess is not None:
					stopProcess(self.scrollProcess)

				self.scrollProcess = startProcess(scrollText, ["_ _ _ _   _ _ _"])

		if "time" in msg:
			self.send(Message(text=dateTime["time"]), thread_id=thread_id, thread_type=thread_type)
				if publishToRobot:
					showClock(dateTime)

# Time-keeper thread, updates clock globally every 5 seconds.
def updateClock(dateTime):
	dateTime['time'] = time.strftime("%H:%M")
	dateTime['datetime'] = time.strftime("%H:%M")
	dateTime['date'] = time.strftime("%H:%M")
	time.sleep(5)
	updateClock(dateTime)

# Basic multi-processing
def startProcess(targetFunction, functionArguments):
	process = Process(target=targetFunction, args=functionArguments)
	process.start()
	return process

def stopProcess(process):
	if process is not None:
		process.terminate()
		process.join()

	if useRobot:
		clearText()

def scrollText(text, dateTime=None):
	if sphd is not None:
		sphd.clear()
		sphd.write_string(text, 10)
		while True:
			sphd.show()
			sphd.scroll(1)
			time.sleep(0.015)
			# Update clock time
			if dateTime is not None and text != dateTime['time']:
				scrollText(dateTime['time'], dateTime)

def clearText():
	if sphd is not None:
		sphd.clear()
		sphd.show()

def showClock(dateTime):
	scrollText(dateTime['time'], dateTime)

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
			client = DeskBot(facebookUsername, facebookPassword)
			client.listen()
		except (KeyboardInterrupt, SystemExit):
			print("Going to sleep")
			stopProcess(clockProcess)
			stopProcess(client.scrollProcess)
			sys.exit()
