# translate png-image into pov-file: each line is one column (one moment in time),
# containing the raw-data for the strip

import Image

def makePOV(inFile, outFile, output=False):

	# Load image in RGB format and get dimensions:
	if output:
		print "Opening image..."
	img       = Image.open(inFile).convert("RGB")
	pixels    = img.load()
	width     = img.size[0]
	height    = img.size[1]
	if output:
			print "%dx%d pixels" % img.size

	if output:
			print "Processing image for dotstar-strip... Please wait."
	if height>60: # check if image is too high
		if output:
			print "ERROR: image is higher than 60 pixels. visible part will be reduced to 60 pixels..."
		height=60

	# create copy of image as lists-in-list with bigger dimension
	nwidth = width
	nheight=60
	if width%60!=0:
		nwidth=(1+width/60)*60

	# create empty image:
	nPixels=[0 for i in range(nwidth)]
	for col in range(nwidth):
		nPixels[col]=[(0,0,0) for line in range(60)] 
	pixels_temp=nPixels # copy for work...

	# re-combine lines in order to use second part of strip correctly
	for cLine in range(height/2): # copy image and reorder lines
		for col in range(width):
			pixels_temp[col][29-cLine] = pixels[col, 2*cLine] # even lines
			pixels_temp[col][30+cLine] = pixels[col, 2*cLine+1]	# odd lines
	if height%2==1:
		for col in range(width):
			pixels_temp[col][29-(height/2)] = pixels[col, 2*(height/2)] # last line

	for parts in range(nwidth/60): # reorder odd lines: shift by half cycle! do these for each part of 60 columns
		for col in range(30):
			for cLine in range(30):
				cCol=col+parts*60 # current column

				nPixels[cCol][cLine]=pixels_temp[cCol][cLine] # just copy even lines
				nPixels[cCol+30][cLine] = pixels_temp[cCol+30][cLine]

				temppix=pixels_temp[cCol][cLine+30] # shift odd lines: it is crucially neccessary to do it this way with temppix!
				nPixels[cCol][cLine+30] = pixels_temp[cCol+30][cLine+30]
				nPixels[cCol+30][cLine+30] = temppix

	# update width & height
	width= nwidth
	height= nheight

	# Calculate gamma correction table, makes mid-range colors look 'right':
	gamma = bytearray(256)
	for i in range(256):
		gamma[i] = int(pow(float(i) / 255.0, 2.7) * 255.0 + 0.5)







###### NOT NEEDED ANYMORE?!


	# Allocate list of bytearrays, one for each column of image.
	# Each pixel REQUIRES 4 bytes (0xFF, B, G, R).
#	print "Allocating..."
#	column = [0 for x in range(width)]
#	for x in range(width):
#		column[x] = bytearray(height * 4)

	# Convert entire RGB image into column-wise BGR bytearray list.
	# The image-paint.py example proceeds in R/G/B order because it's counting
	# on the library to do any necessary conversion.  Because we're preparing
	# data directly for the strip, it's necessary to work in its native order.
#	print "Converting..."


###### NOT NEEDED ANYMORE?!









	f = open(outFile, 'w')
	f.write(str(width) + "," + str(height)+"\n")

	for x in range(width):          # For each column of image...

		if output:
			if width%6000==0:
				print "saving image: " + str((100*x)/width) + "%"

		for y in range(height): # For each pixel in column...
			value             = nPixels[x][y]    # Read pixel in image
			f.write(str(0xFF)+","+str(gamma[value[2]])+","+str(gamma[value[1]])+","+str(gamma[value[0]]))
			if y<height-1:
				f.write(",")
		if x<width-1:
			f.write("\n")

	f.close()

# makePOV("images/worldmap_scan1.png", "pov/worldmap_scan1.pov") # example-call
