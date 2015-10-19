#!/usr/bin/env python
 
from time import time, sleep
import RPi.GPIO as GPIO
import threading


class freqThread(threading.Thread):
	def __init__(self, start=True, NAverage=5):
		threading.Thread.__init__(self)
		self.SENSOR = 7 # GPIO.BOARD-Numbering: PIN-Numbering!; Sensor connected to GPIO 4 = PIN 7
		GPIO.setwarnings(False)
 
		self.num_average=NAverage
		self.frequency=0 # averaged frequency calculated by on-signals
		self.period=0 # averaged period-time calculated by on-signals
		self.running=False

		if (start):
			self.start()

	def restart(self):
		self.running=False
		self.start()

	def run(self):
		GPIO.setmode (GPIO.BOARD)
 		GPIO.setup (self.SENSOR, GPIO.IN) # Setup the GPIO pin connected to the Sensor to read as input

		Active = GPIO.input(self.SENSOR) # State of Sensor
		num_on=0
		timeDiff=0
		timeStamp_on=0
		timeDiff_Av=-1
		timeDiff_on_average=[0 for x in range(self.num_average)]

		#print "start frequency-detector. takes at least "+str(self.num_average+5)+" rounds to detect correct frequency...\n\n"
		self.running = True
		while self.running:

			# Main program loop
			try:

				if GPIO.input(self.SENSOR)!=Active:
					Active=GPIO.input(self.SENSOR)

					if( Active == False ):
						timeDiff=time()-timeStamp_on
						timeStamp_on=time()
						num_on = num_on +1
						timeDiff_on_average[(num_on-1)%self.num_average]=timeDiff
						if num_on>self.num_average+5:
							timeDiff_Av=0
							for i in range(self.num_average):
								timeDiff_Av=timeDiff_Av+timeDiff_on_average[i]
							timeDiff_Av=timeDiff_Av/self.num_average
							self.period=timeDiff_Av
							self.frequency=1/timeDiff_Av

			except KeyboardInterrupt:
				GPIO.cleanup() # Clean up GPIO on CTRL+C exit
 
		# End of main program loop 
		# Clean up on normal exit
		GPIO.cleanup()
