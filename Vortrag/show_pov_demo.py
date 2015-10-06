import time
import os
from os import listdir
from os.path import isfile, join
from dotstar import Adafruit_DotStar
import get_freq

FreqAverage=5
povPath="pov/"
freq = get_freq.freqThread(NAverage=FreqAverage) # initialize frequency-thread

if os.path.isdir(povPath)==False:
	message= "Pov Path (" + str(povPath) + ") does not exist!"
else:

	all_files = [ f for f in listdir(povPath) if (isfile(join(povPath,f)) and f[len(f)-4:]=='.pov')] # find all pov-files in imagePath

	if len(all_files)==0:
		message= "No pov-files in pov Path (" + str(povPath) + ") available!"

	else:

		all_sizes=[0 for i in range(len(all_files))]
		for i in range(len(all_files)):
			f=open(povPath+all_files[i],'r')
			all_sizes[i]=f.readline()
			f.close

		convMess=""
		fileNumber=""
		times=1

		while fileNumber=="":

			inv = False

			os.system('clear')
			maxN = 10*times
			minN = 10*(times-1) +1
			if maxN>len(all_files):
				maxN = len(all_files)

			print "Available pov-files [" + str(minN) + " to " + str(maxN) + " of " + str(len(all_files)) +"]:\n"

			n=10
			if len(all_files)<10*times:
				n=len(all_files)-10*(times-1)

			for i in range(n):
				siz=all_sizes[i+(times-1)*10]
				print str(i+1+(times-1)*10)+"\t"+ str(int((siz)[0:len(siz)-4])/60) + "\t" +all_files[i+(times-1)*10]
			if n<10:
				for i in range(10-n):
					print ""

			print "\ne\texit"
			print "\nPress enter to continue\n"
			print convMess
			convMess=""

			fileNumber=raw_input("\nChoose pov-file to display: ")

			if fileNumber=="":
				times = times +1
				if len(all_files)<=10*(times-1):
					times = 1

			elif fileNumber != "e":

				try:
					if int(fileNumber)<=len(all_files) and int(fileNumber)>0:
						okay=True
					else:
						okay=False
				except:
					okay=False

				if okay==False:
					fileNumber=""
					convMess="Invalid input! Choose e or integer from 1 to "+str(len(all_files))+"!"

				else:

					m=int(fileNumber)
					fN=all_files[m-1]

					f=open(povPath+fN,'r')
					size=map(int,(f.readline().rstrip("\n")).split(','))
					width=size[0]

					print "\nLoading "+povPath+fN + " into buffer; size: "+str(size[0])+"x"+str(size[1])
					lines = f.read().splitlines()
					array=[0 for i in range(width)]
					for i in range(width):
						array[i]=map(int,lines[i].split(','))
						if i%900==0:
							print "\r"+str(100*i/width)+"% loaded."
					print "\r100% loaded."

					print "\nwaiting for valid frequency-values..."
					while (freq.period>2.0) or (freq.period<0.05):
						pass
					print "Displaying... period="+ str(freq.period) + "\t frequency=" + str(freq.frequency)


# initialize values
pos=0
timeB=time.time()
timeDiff=0
timeDiff_new=0

while True: # Loop until KeyInterrupt

	period=freq.period
	pixel_time=(period-timeDiff)/60.

	for x in range(60):         		# For each column of image...
		strip.show(array[x+pos*60])  	# Write raw data to strip
		time.sleep(pixel_time)

	pos=(pos+1)%(width/60) 			# next slice/rotation
	actPeriod=time.time()-timeB
	timeDiff_new=actPeriod-period
	timeDiff=(timeDiff+timeDiff_new)%period
	timeB=time.time()

						print "pos " + str(pos+1) + " of " + str(width/60) + "\tmeasured/calc period: "+ str(period) +"\t"+str(actPeriod)+"\tdifference: "+str(timeDiff)
