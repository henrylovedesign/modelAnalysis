import os
import math
import numpy as np
import sys
sys.path.insert(0,"/home/henry/projects/sphere_detection/algoopt")
import ROC.roc_curve as roc


def combineIntoCsv(imgAdr,labelAdr,scoreAdr,csvFile):
	imgs = []
	labels = []
	scores= []
	imgnumber = len(os.listdir(imgAdr))
	print(imgnumber)
	for i in xrange(imgnumber):

		imgPath = imgAdr+str(i+1)+".png"
		imgs.append(imgPath)

	for i in xrange(imgnumber):

		labelPath = labelAdr +str(i+1)+".txt"
		label = open(labelPath,'r').read()
		label = label.strip().split(" ")[1]	
		labels.append(label)


	for i in xrange(imgnumber):
		scorePath = scoreAdr + str(i+1)+".txt"
		score =float(open(scorePath,'r').read().strip())
		scores.append(score)

	#maxscore = max(np.asarray(scores))
	#print(maxscore)
	#scores = [str(score) for score in list(np.asarray(scores)/maxscore)]


	with open(csvFile,"w") as f:
		f.write("name,label,predict")
		f.write("\n")
		for i in xrange(len(imgs)):
			f.write(imgs[i]+","+labels[i]+","+str(scores[i]))
			if i != len(imgs)-1:
				f.write("\n")
		f.close()


if __name__ == '__main__':
	imgAdr="/home/henry/projects/sphere_detection/algoopt/testData/ResultCNNBoosting/Image/"
	labelAdr="/home/henry/projects/sphere_detection/algoopt/testData/ResultCNNBoosting/GT/"
	
	scoreAdr="/home/henry/projects/sphere_detection/algoopt/testData/ResultCNNBoosting/CNNResultPatchCPP/"
	csvFile="/home/henry/projects/sphere_detection/algoopt/testData/CNNResultPatchCPP.csv"
	
	scoreAdr2="/home/henry/projects/sphere_detection/algoopt/testData/ResultCNNBoosting/ResultBoosting/"
	csvFile2="/home/henry/projects/sphere_detection/algoopt/testData/ResultBoosting.csv"

	saveAddress = "/home/henry/projects/sphere_detection/algoopt/ROC/curves"
	name=["CNN","ResultBoosting"]
	
	#combineIntoCsv(imgAdr,labelAdr,scoreAdr,csvFile)
	#roc.draw_roc_fromFile2(csvFile,saveAddress,method="CNN")
	
	#combineIntoCsv(imgAdr,labelAdr,scoreAdr2,csvFile2)
	#roc.draw_roc_fromFile2(csvFile2,saveAddress,method="ResultBoosting" )
	
	roc.draw_multi_roc(csvFile,csvFile2,name,saveAddress)
