#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import random
import threading

tasterBluePressed = False
tasterRedPressed = False
winner = 0
winnerTaster = 0

def setButtonBlue(channel):
	global tasterBluePressed
	tasterBluePressed = True
	GPIO.output(18, 1)
def setButtonRed(channel):
	global tasterRedPressed
	tasterRedPressed = True
	GPIO.output(25, 1)
def hitButtonBlue(channel):
	global winner
	global winnerTaster
	if winner == 0:
		winner = 18
		winnerTaster = channel
def hitButtonRed(channel):
	global winner
	global winnerTaster
	if winner == 0:
		winner = 25
		winnerTaster = channel


print "Start programm"

GPIO.setmode(GPIO.BCM)

blau = 0; gruen = 1; gelb = 2; rot = 3; tasterb = 4; tasterr = 5
pin=[18,23,24,25,4,17]
GPIO.setup(pin[rot], GPIO.OUT, initial=False)
GPIO.setup(pin[gelb], GPIO.OUT, initial=False)
GPIO.setup(pin[gruen], GPIO.OUT, initial=False)
GPIO.setup(pin[blau], GPIO.OUT, initial=False)
GPIO.setup(pin[tasterb], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pin[tasterr], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


print "GPIO setup finished"

print "Press Ctrl+C to close the programm"

try:
	while True:
		print "start new game"
		winner = 0
		winnerTaster = 0


		for i in range(5):
			GPIO.output(pin[gelb], 1)
			GPIO.output(pin[gruen], 1)
			time.sleep(0.05)
			GPIO.output(pin[gelb], 0)
			GPIO.output(pin[gruen], 0)
			time.sleep(0.05)
		GPIO.output(pin[gelb], 1)
		GPIO.output(pin[gruen], 1)
		print "wait"
		
		tasterBluePressed = False
		tasterRedPressed = False
		GPIO.add_event_detect(pin[tasterb], GPIO.RISING, callback = setButtonBlue)
		GPIO.add_event_detect(pin[tasterr], GPIO.RISING, callback = setButtonRed)
		
		while not (tasterBluePressed and tasterRedPressed):		
			hallo = 1	

		print "Players are ready"

		
		GPIO.output(pin[gelb], 0)
		GPIO.output(pin[gruen], 0)
		time.sleep(2)
		GPIO.output(pin[blau], 0)
		GPIO.output(pin[rot], 0)
		time.sleep(1)
		
		tasterBluePressed = False
		tasterRedPressed = False
		GPIO.output(pin[gelb], 1)
		randomSleep = random.randrange(1000, 5000)
		time.sleep(randomSleep/1000)
		GPIO.remove_event_detect(pin[tasterb])
		GPIO.remove_event_detect(pin[tasterr])
		if not tasterBluePressed:
			GPIO.add_event_detect(pin[tasterb], GPIO.RISING, callback = hitButtonBlue)
		if not tasterRedPressed:
			GPIO.add_event_detect(pin[tasterr], GPIO.RISING, callback = hitButtonRed)
		GPIO.output(pin[blau], 0)
		GPIO.output(pin[rot], 0)
		if not (tasterBluePressed and tasterRedPressed):
			GPIO.output(pin[gruen], 1)
			start = time.time()
			while winner==0:
				hallo = 1
			GPIO.remove_event_detect(pin[tasterb])
			GPIO.remove_event_detect(pin[tasterr])
			GPIO.output(winner, 1)
			end = time.time()
			elapsed = end - start
			print "Time: ", elapsed, " seconds"
			time.sleep(2)
			for i in range(100):
				GPIO.output(winner, i%2)
				time.sleep(0.1)
				if GPIO.input(winnerTaster):
					break
			GPIO.output(winner, 0)
			
		else:
			print "No winner"
			time.sleep(2)
except KeyboardInterrupt:
	GPIO.cleanup()
