#!/usr/bin/env python
 
import time
from dotstar import Adafruit_DotStar
import get_freq
import threading


class povThread(threading.Thread):
	def __init__(self, FreqAverage=5, Path="pov/", start=""):
		threading.Thread.__init__(self)

		self.datapin   = 2	# GPIO-Numbering!
		self.clockpin  = 3 	# GPIO-Numbering!
		self.strip     = Adafruit_DotStar(0, self.datapin, self.clockpin)
			# Notice the number of LEDs is set to 0.  This is on purpose...we're asking
			# the DotStar module to NOT allocate any memory for this strip...we'll handle
			# our own allocation and conversion and will feed it 'raw' data.
		self.strip.begin()	# Initialize pins for output

		self.empty_array=bytearray(60*4) # prepare empty-flash
		for x in range(60):
			self.empty_array[x*4]=0xFF
			self.empty_array[x*4+1]=0x00
			self.empty_array[x*4+2]=0x00
			self.empty_array[x*4+3]=0x00

		self.povPath=Path
		self.povFile = start
		self.size=[0,0]

		self.FAverage=FreqAverage
		self.actPeriod=0
		self.freq = get_freq.freqThread(NAverage=self.FAverage) # initialize frequency-thread

		self.running=False # is Thread displaying a pov-File?
		self.NEWrunning=False # want to stop and start new?
		self.active=True # is Thread active? (& playing OR waiting to play) -> only False if quitting main.
		self.pause=False
		self.pos=0
		self.loading=False # loading? --> main waits for finishing loading-process

		if start!="":
			self.running=True
		else:
			self.off()

		self.start()

		####status data / show status function

	def off(self):
		self.running=False
		self.pause=False
		self.strip.show(self.empty_array)
		self.size=[0,0]
		self.pos=0

	def doPause(self):
		if self.running==True:
			if self.pause:
				self.pause=False
			else:
				self.pause=True

	def stop(self): # only to quit!! else: use self.off()
		self.off()
		self.freq.running=False
		self.active=False

#	def restart(self):
#		self.off()
#		self.running=True

	def showPOV(self, File=""):
		self.off()
		if File!="":
			self.povFile=File
		self.NEWrunning=True
		self.loading=True

	def run(self):

		while self.active:

			if self.NEWrunning==True:
				self.running=True
				self.NEWrunning=False

			if self.running == True:
				if self.povFile == "":
					print "Error: No pov-file specified!"
					self.off()
					self.loading=False

				else:
					f=open(self.povPath+self.povFile,'r')
					self.size=map(int,(f.readline().rstrip("\n")).split(','))
					width=self.size[0]

					print "\nLoading "+self.povPath+self.povFile + " into buffer; size: "+str(self.size[0])+"x"+str(self.size[1])
					lines = f.read().splitlines()
					array=[0 for i in range(width)]
					for i in range(width):
						array[i]=bytearray(60*4)
						j=0
						for LED in lines[i].split(','):
							array[i][j]=int(LED)
							j=j+1
						if i%900==0:
							print "\r"+str(100*i/width)+"% loaded."
					print "\r100% loaded."

					print "\nwaiting for valid frequency-values..."
					while (self.freq.period>2.0) or (self.freq.period<0.05):
						pass
					print "Displaying... period="+ str(self.freq.period) + "\t frequency=" + str(self.freq.frequency)


					self.pos=0 # start at beginning; first rotation

					# for calculating needed time for one period
					timeB=time.time()
					timeDiff=0
					timeDiff_new=0

					self.loading=False

					period=.16

					while self.running: # Loop

						period=self.freq.period
						pixel_time=(period-timeDiff)/60.
			
						if self.pause==False: # pause?
							for x in range(60):         # For each column of image...
								self.strip.show(array[x+self.pos*60])  # Write raw data to strip
								time.sleep(pixel_time)
							self.pos=(self.pos+1)%(width/60) # next slice/rotation; modulo(%)=>endless loop

						else:
							time.sleep(period)

						self.actPeriod=time.time()-timeB
						timeDiff_new=self.actPeriod-period
						timeDiff=(timeDiff+timeDiff_new)%period
						timeB=time.time()

			self.off()
			time.sleep(0.1)

