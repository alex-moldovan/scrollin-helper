#!/usr/bin/env python

from botconfig import *

class BotUser():
	def __init__(self, userID, threadID):
		self.userID = userID
		self.threadID = threadID

		self.userStatus = 0
		self.userAwaitedActions = []

		self.isAdmin = True	if (botConfig["adminID"] is not None and userID != botConfig["adminID"]) else False

		print("Created user %d with thread %d" % (userID, threadID))
