import pandas as pd
import numpy as np
from sklearn import metrics
import os
import shutil
import matplotlib.pyplot as plt

threshold = 0.5

def get_fn_sphere(test_result,saveAddress):
	
	test_result = pd.DataFrame.from_csv(test_result,header=0,sep=",",index_col=None)
	
	y = np.asarray(test_result['label'])
	scores = np.asarray(test_result['predict'])

	fpr, tpr, thresholds = metrics.roc_curve(y, scores)
	
	for i in xrange(len(thresholds)):
		#name the doc by index and threshold
		saveTo = saveAddress+str(i)+"_"+str(thresholds[i])
		
		fn_sphereList = np.asarray(test_result['name'][(test_result['predict'] < thresholds[i]) & (test_result['label'] == 1)]  )
		

		if (not os.path.exists(saveTo)) &(len(fn_sphereList)!=0):
			os.mkdir(saveTo)

		for name in fn_sphereList:
			
			imgName = os.path.basename(name)
			score = np.asarray(test_result['predict'][test_result['name']==name])[0]
			newname = imgName.split(".")[0]+"_"+str(score)+".png"
			shutil.copy(name,saveTo+"/"+ newname)
	
	


def report(test_result,saveReport):
	method = os.path.basename(test_result).split(".")[0]
	test_result = pd.DataFrame.from_csv(test_result,header=0,sep=",",index_col=None)
	
	y = np.asarray(test_result['label'])
	scores = np.asarray(test_result['predict'])

	fpr, tpr, thresholds = metrics.roc_curve(y, scores)

	fnNumbers = []
	for i in xrange(len(thresholds)):
		#name the doc by index and threshold
		fn_sphereList = np.asarray(test_result['name'][(test_result['predict'] < thresholds[i]) & (test_result['label'] == 1)]  )
		fnNumbers.append(len(fn_sphereList))

	maxscore = max(thresholds)
	minscore = min(thresholds)
	meanscore = np.mean(thresholds)
	
	#scoreHistogram = 
	plt.xlabel("threshold")
	plt.ylabel("number")
	plt.hist(np.asarray(test_result['predict']), bins='auto')
	title = method+	"_histogram.png "+"\n"+ \
						"maxscore: "+str(maxscore) +"\n"+ \
						"minscore: "+str(minscore)+"\n"+\
						"meanscore: "+str(meanscore)
	plt.title(title)
	scoreHistogram = plt.gcf()
	pngname = method+	"_histogram.png"
	scoreHistogram.savefig(saveReport+pngname)
	plt.close()

	pngname2 = method + "_fnnumbers"
	plt.title("thresholds VS fnnum")
	plt.xlabel("threshold")
	plt.ylabel("fasle negative number")
	plt.plot(thresholds,fnNumbers,'yo-')
	thresholdsVSfnnum = plt.gcf()
	thresholdsVSfnnum.savefig(saveReport+pngname2)
	plt.close()

	pngname3 = method + "precison.png"
	plt.title("precision")
	plt.xlabel("threshold")
	plt.ylabel("precision")
	plt.plot(thresholds[::-1],tpr)
	precision = plt.gcf()
	precision.savefig(saveReport+pngname3)
	plt.close()



if __name__ == '__main__':
	csvname = "CNNResultPatchCPP.csv" #"CNNResultPatchCPP.csv"  "ResultBoosting.csv"
	docname = "CNN" #"CNN" "ResultBoosting"
	figname = "fnNumber.png"
	test_result ="/home/henry/projects/sphere_detection/algoopt/testData/"+csvname
	saveAddress ="/home/henry/projects/sphere_detection/algoopt/Filter/"+docname+"/fnSphere/"
	saveReport = "/home/henry/projects/sphere_detection/algoopt/Filter/"+docname+"/report/"
	
	#get_fn_sphere(test_result,saveAddress)
	report(test_result,saveReport)