# testen:
#	- einlesen der dateien & weitergeben an strip
#	- geschwindigkeitsregelung (Verbessern?)
#
# moegliche zus. Features:
#	- mehr Bilder
#	- Laufschrift



import time
import Image
import sys
import pov_control
import os
from os import listdir
from os.path import isfile, join
from pngTOpov import makePOV


# Image & Pov - Path:
imagePath="images/"
povPath="pov/"

pov=pov_control.povThread(Path=povPath)

opt = ""
run=True
message=""
Status="No pov-file playing."

while run==True:

	try:
		while opt!="1" and opt!="2" and opt!="3" and opt!="4" and opt!="5" and opt!="q" and opt!="6":

			os.system('clear')	
			print "POV  -- Persistence of Vision\n"
			print "Choose:"
			print "1 - Convert png-file(s) to pov-file(s)"
			print "2 - Show pov-file"
			print "3 - Pause/Play current pov-file"
			print "4 - Stop current pov-file"
			print "5 - Show status of current pov-file"
			print "q - Quit\n"

			print message + "\n"
			message=""

			opt=raw_input("")





		if opt == "q": # exit
			pov.stop
			run=False







		elif opt == "1": # convert png-files

			if os.path.isdir(imagePath)==False:
				message= "Image Path (" + str(imagePath) + ") does not exist!"
			else:

				all_files = [ f for f in listdir(imagePath) if (isfile(join(imagePath,f)) and f[len(f)-4:]=='.png')] # find all png-files in imagePath

				if len(all_files)==0:
					message= "No png-files in image Path (" + str(imagePath) + ") available!"

				else:

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

						print "Available png-files [" + str(minN) + " to " + str(maxN) + " of " + str(len(all_files)) +"]:\n"
						print "0\tconvert all files\n"

						n=10
						if len(all_files)<10*times:
							n=len(all_files)-10*(times-1)

						for i in range(n):
							print str(i+1+(times-1)*10)+"\t"+ all_files[i+(times-1)*10]
						if n<10:
							for i in range(10-n):
								print ""

						print "\ne\texit"
						print "\nPress enter to continue\n"
						print convMess
						convMess=""

						fileNumber=raw_input("\nChoose png-file to convert: ")

						if fileNumber=="":
							times = times +1
							if len(all_files)<=10*(times-1):
								times = 1

						elif fileNumber != "e":

							try:
								if int(fileNumber)<=len(all_files) and int(fileNumber)>=0:
									okay=True
								else:
									okay=False
							except:
								okay=False

							if okay==False:
								fileNumber=""
								convMess="Invalid input! Choose e or integer from 0 to "+str(len(all_files))+"!"

							else:

								m=int(fileNumber)

								if m>0:
									fN=(all_files[m-1])[0:len(all_files[m-1])-4]
									makePOV(imagePath+fN+".png",povPath+fN+".pov")
									message=imagePath + fN + ".png converted to " + povPath + fN + ".pov"
								else:
									print "\n"
									for m in range(len(all_files)):
										fN=(all_files[m-1])[0:len(all_files[m-1])-4]
										print "converting file \t" + str(m+1) + " of " + str(len(all_files)) + ": \t" + fN
										makePOV(imagePath+fN+".png",povPath+fN+".pov")
									message= "All " + str(len(all_files)) + " png-files from " + imagePath + " converted to pov-files in " + povPath + "."



		elif opt == "2": # show pov-files

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
								pov.showPOV(File=fN)
								while pov.loading:
									time.sleep(0.1)
								Status=povPath+fN + " loaded and playing."
								message=povPath + fN + " loaded."
								raw_input("OK")

		elif opt=="3":
			if pov.pause==False and pov.running==True:
				message="Pov paused."
				Status=pov.povPath+pov.povFile + " loaded and paused."
			elif pov.pause==True and pov.running==True:
				message="Pov continued."
				Status=pov.povPath+pov.povFile + " loaded and playing."
			elif pov.running==False:
				message = "No pov-file playing."
				Status="No pov-file playing."
			pov.doPause()


		elif opt=="4":
			Status="No pov-file playing."
			if pov.running==True:
				message="Pov stopped."
			else:
				message= "No pov-file playing."

			pov.off()


		elif opt=="5":
			if pov.running==False:
				message = "No pov-file playing."

			else:

				try:
					while True:
						os.system('clear')
						print "System displaying file " + pov.povPath + pov.povFile + "."
						print "\nDisplaying-Information:\n"
						print "Displaying is paused:        \t" + str(pov.pause)
						print "Current slice:               \t" + str(pov.pos+1)+" of "+str(pov.size[0]/60)
						p=.16
						p = pov.freq.period
						sp = pov.actPeriod
						av = pov.FAverage
						print "Measured rotating frequency: \t" + str(1./p)
						print "Measured rotating period:    \t" + str(p)
						print "Updating-time per period:    \t" + str(sp)
						print "Diference:                   \t" + str(sp-p)
						print "Number of averaged periods:  \t" + str(av)
						print "\nPress Ctrl + C for main menu."
						time.sleep(0.1)

				except KeyboardInterrupt:
					pass

				message= Status




		if opt!="q":
			opt=""

	except KeyboardInterrupt:
		opt=""


pov.stop()
print "\nGoodbye\n"
