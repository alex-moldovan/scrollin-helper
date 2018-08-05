#!/usr/bin/env python

import sys
import time
from multiprocessing import Process, Manager
import logging
from fbchat import Client, log
from fbchat.models import *

useRobot = True
try:
    import scrollphathd as sphd
except:
    useRobot = False

if useRobot:
    #The screen is installed upside down on my robot case.
    sphd.rotate(180)
    sphd.set_brightness(1.0)

    scrollProcess = None

class DeskBot(Client):
    def __init__(self, email, password, dateTime):
        if useRobot:
            scrollProcess = None

        self.dateTime = dateTime
        
        client = Client.__init__(self, email, password)

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)
        msg = "%s" % message_object.text
        msg = msg.lower()
        #log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))

        print(message_object)

        if author_id != self.uid:
            if "ohanes" in msg:
                self.send(Message(text="_ _ _ _   _ _ _"), thread_id=thread_id, thread_type=thread_type)
                try:
                    if scrollProcess is not None:
                        stopProcess(self.scrollProcess)
                except:
                    pass
                
                scrollProcess = createProcess(scrollText, ["Muie PSD"])

            if "time" in msg:
                self.send(Message(text=dateTime["time"]), thread_id=thread_id, thread_type=thread_type)

def updateClock(dateTime):
    dateTime['time'] = time.strftime("%H:%M")
    dateTime['datetime'] = time.strftime("%H:%M")
    dateTime['date'] = time.strftime("%H:%M")
    time.sleep(2)
    updateClock(dateTime)

def scrollText(text, dateTime=None):
    sphd.clear()
    sphd.write_string(text, 10)
    while True:
	sphd.show()
	sphd.scroll(1)
	time.sleep(0.02)
        if dateTime is not None and text != dateTime['time']:
            scrollText(dateTime['time'], dateTime)

def clearText():
    sphd.clear()
    sphd.show()

def showClock(dateTime):
    scrollText(dateTime['time'], dateTime)   

def createProcess(targetFunction, functionArguments):
    scrollProcess = Process(target=targetFunction, args=functionArguments)
    scrollProcess.start()
    
    return scrollProcess

def stopProcess(process):
    process.terminate()
    process.join()
    clearText()

if __name__ == '__main__':

        with Manager() as manager:
            # Time keeping thread
            dateTime = manager.dict()
            clockProcess = createProcess(updateClock, [dateTime])

            # Initial clear
            if useRobot:
                clearText()

            client = DeskBot("<user>", "<password>", dateTime)
            client.listen()

        sys.exit()
