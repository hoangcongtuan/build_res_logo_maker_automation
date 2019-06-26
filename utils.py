# import the necessary packages
import numpy as np
import cv2
from colormap import rgb2hex

white_color = np.array([255, 255, 255])

def centroid_histogram(clt):
	# grab the number of different clusters and create a histogram
	# based on the number of pixels assigned to each cluster
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)

	# normalize the histogram, such that it sums to one
	hist = hist.astype("float")
	hist /= hist.sum()
	# return the histogram
	return hist

def findPri_Sec(hist, centroids):
	hist, centroids = zip(*sorted(zip(hist, centroids), reverse = True))
	dist2white = np.array([])
	hexColor = np.array([])

	for (percent, color) in zip(hist, centroids):
		# plot the relative percentage of each cluster
		int_color_np = color.astype("uint8")
		hex_color = rgb2hex(int_color_np[0], int_color_np[1], int_color_np[2])
		hexColor = np.append(hexColor, hex_color)
		dist = np.linalg.norm(white_color - int_color_np)
		dist2white = np.append(dist2white, dist.astype('uint32'))

	dist2white, hist, hexColor = zip(*sorted(zip(dist2white, hist, hexColor), reverse = True))

	colorCount = len(centroids)

	if colorCount == 0:
		primaryColor = secondaryColor = '#000000'
	else:
		if colorCount == 2:
			primaryColor = secondaryColor = hexColor[0]
		else:
			dist2white =  np.delete(dist2white, colorCount - 1)
			hist = np.delete(hist, colorCount - 1)
			hexColor = np.delete(hexColor, colorCount - 1)
			hist, hexColor = zip(*sorted(zip(hist, hexColor), reverse = True))

			primaryColor = hexColor[0]
			secondaryColor = hexColor[1]

	return primaryColor, secondaryColor

def plot_colors(hist, centroids):
	# initialize the bar chart representing the relative frequency
	# of each of the colors
	bar = np.zeros((50, 300, 3), dtype = "uint8")
	startX = 0
	hist, centroids = zip(*sorted(zip(hist, centroids)))

	# loop over the percentage of each cluster and the color of
	# each cluster
	for (percent, color) in zip(hist, centroids):
		# plot the relative percentage of each cluster
		endX = startX + (percent * 300)
		cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
			color.astype("uint8").tolist(), -1)
		startX = endX
	# return the bar chart
	return bar