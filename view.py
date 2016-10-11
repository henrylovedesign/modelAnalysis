import cv2
import numpy as np
import os
from matplotlib import pyplot as plt


def nextindex(current,size):
	nextindex = (current+1)%size
	return nextindex

def lastindex(current,size):
	sign = 1
	if current==0:
		sign = -1
	lastindex = sign * abs(current-1)%size
	return lastindex

def next(imgList,current):
	next = (current+1)%len(imgList)
	return imgList[next]

def last(imgList,current):
	
	sign = 1
	if current==0:
		sign = -1
	last = sign * abs(current-1)%len(imgList)
	return imgList[last]

def viewer(address,classifyroot):
	#images = os.listdir(address)
	paths = [line.strip().split(",")[0] for line in open(address)]
	images=[os.path.basename(line.strip().split(",")[0]) for line in open(address)]
	scores=[line.strip().split(",")[1] for line in open (address)]
	current = 0
	size = len(images)
	
	title = images[current]+"_score:"+str(scores[current])
	image = images[current]
	
	path = paths[current]
	image =  cv2.resize(cv2.imread(path),(650,650))
	
	
	cv2.imshow(title,image)
	
	#if key == 27:
	key = cv2.waitKey(0)
	while(key!= ord('e')):
		
		
		if key==ord('n'):
			cv2.destroyAllWindows()
			title = next(images,current)+"_score"+str(next(scores,current))
			#image = next(images,current)
			#path = address + image
			path = next(paths,current)
			image = cv2.resize(cv2.imread(path),(650,650))
			cv2.imshow(title,image)
			

			current = nextindex(current,size)
			key = cv2.waitKey(0)
		if key==ord('l'):
			cv2.destroyAllWindows()

			title = last(images,current)+"_score"+str(last(scores,current))
			#image = last(images,current)

			#path = address + image
			path = paths[current]
			image = cv2.resize(cv2.imread(path),(650,650))

			cv2.imshow(title,image)
			
			current = lastindex(current,size)
			key = cv2.waitKey(0)
		if key== ord("s"):
			title = images[current]
			#image = last(images,current)

			#path = address + image
			path = paths[current]
			image = cv2.imread(path)
			cv2.imwrite(classifyroot+title,image)
			print "successfully save"
    		key = cv2.waitKey(0)

if __name__ == '__main__':
	
	address="/home/henry/projects/sphere_detection/modelAnalysis/error/fpSphere/357_3544.772705.csv"
	classifyroot="/home/henry/projects/sphere_detection/algoopt/Filter/CNN/errortype/fpShere/"

	viewer(address,classifyroot)
	

