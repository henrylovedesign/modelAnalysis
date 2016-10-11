import os
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from sklearn import metrics
from time import gmtime, strftime




def modelinfor(test_result):
	
	method = os.path.basename(test_result).split(".")[0]
	test_result = pd.DataFrame.from_csv(test_result,header=0,sep=",",index_col=None)
	
	y = np.asarray(test_result['label'])
	scores = np.asarray(test_result['predict'])
	fpr, tpr, thresholds = metrics.roc_curve(y, scores)
	auc_score = metrics.roc_auc_score(y,scores)
	fpNumbers = []
	fnNumbers = []
	for i in xrange(len(thresholds)):
		#name the doc by index and threshold
		fp_sphereList = np.asarray(test_result['name'][(test_result['predict'] > thresholds[i]) & (test_result['label'] == 0)]  )
		fn_sphereList = np.asarray(test_result['name'][(test_result['predict'] < thresholds[i]) & (test_result['label'] == 1)]  )
		
		fpNumbers.append(len(fp_sphereList))
		fnNumbers.append(len(fn_sphereList))

	return test_result,method,fpr,tpr,thresholds,auc_score,fpNumbers,fnNumbers


def errorreport(test_result,fpr, tpr, thresholds,errorAddress):

	for i in xrange(len(thresholds)):
		#name the doc by index and threshold
		pwriteTo = errorAddress+"/fpSphere/"+str(i)+"_"+str(thresholds[i])+".csv"
		nwriteTo = errorAddress+"/fnSphere/"+str(i)+"_"+str(thresholds[i])+".csv"
		fp_sphereList = np.asarray(test_result['name'][(test_result['predict'] > thresholds[i]) & (test_result['label'] == 0)]  )
		fn_sphereList = np.asarray(test_result['name'][(test_result['predict'] < thresholds[i]) & (test_result['label'] == 1)]  )
		if len(fp_sphereList)>0:
			os.mkdir("/home/henry/hello")
			with open(pwriteTo,"w") as fpSphere:
				for fpsphere in fp_sphereList:
					score = np.asarray(test_result['predict'][test_result['name']==fpsphere])[0]
					fpSphere.write(fpsphere+","+str(score))
					if fpsphere!=fp_sphereList[-1]:
						fpSphere.write("\n")
			fpSphere.close()
		
		if len(fn_sphereList)>0:
			with open(nwriteTo,"w") as fnSphere:
				for fnsphere in fn_sphereList:
					score = np.asarray(test_result['predict'][test_result['name']==fnsphere])[0]
					fnSphere.write(fnsphere+","+str(score))
					if fnsphere!=fn_sphereList[-1]:
						fnSphere.write("\n")
			fnSphere.close()


def stareport(method,fpr,tpr,thresholds,auc_score,fpNumbers,fnNumbers,saveStaData):
	
	precisionname = method+"_precision.csv"
	rocname = method+"_roc.csv"
	fpnumbername=method+"_fpnumbers.csv"
	fnnumbername=method+"+fnnumbers.csv"

	maxscore = max(thresholds)
	minscore = min(thresholds)
	meanscore = np.mean(thresholds)

	size = len(fpr)
	#precision file
	with open(saveStaData+"/"+precisionname,"w") as stafile:
		stafile.write("threshold,precision"+"\n")
		for i in xrange(size):
			stafile.write(str(thresholds[i])+","+str(tpr))
			if i!= size-1:
				stafile.write("\n")
		stafile.close()

	#roc
	with open(saveStaData+"/"+rocname,"w") as rocfile:
		rocfile.write("roc curve data with auc: "+str(auc_score)+"\n")
		rocfile.write("fpr,tpr"+"\n")
		for i in xrange(size):
			rocfile.write(str(fpr[i])+","+str(tpr[i]))
			if i!= size-1:
				rocfile.write("\n")
		rocfile.close()

	#fpnumbers
	with open(saveStaData+"/"+fpnumbername,"w") as fpnfile:
		fpnfile.write("maxscore: "+str(maxscore)+" minscore: "+str(minscore)+" meanscore:"+str(meanscore)+"\n")
		fpnfile.write("threshold,fpNumber"+"\n")
		revthresholds = thresholds[::-1]
		for i in xrange(size):
			if fpNumbers[i]!=0:
				fpnfile.write(str(revthresholds[i])+","+str(fpNumbers[i]))
				if i != size-1:
					fpnfile.write("\n")
		fpnfile.close()

	#fnnumbers
	with open(saveStaData+"/"+fnnumbername,"w") as fnnfile:
		fnnfile.write("maxscore: "+str(maxscore)+" minscore: "+str(minscore)+" meanscore:"+str(meanscore)+"\n")

		fnnfile.write("threshold,fpNumber"+"\n")
		revthresholds = thresholds[::-1]
		for i in xrange(size):
			if fnNumbers[i]!=0:
				fnnfile.write(str(revthresholds[i])+","+str(fnNumbers[i]))
				if i != size-1:
					fnnfile.write("\n")
		fnnfile.close()


def graphreport(test_result,method,fpr,tpr,thresholds,auc_score,fpNumbers,fnNumbers,saveGraph):
	
	
	maxscore = max(thresholds)
	minscore = min(thresholds)
	meanscore = np.mean(thresholds)
	
	y = np.asarray(test_result['label'])
	scores = np.asarray(test_result['predict'])
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
	pngname = "/"+method+	"_histogram.png"
	scoreHistogram.savefig(saveGraph+pngname)
	plt.close()
	
	pngname2 = "/"+method + "_fpnumbers"
	plt.title("thresholds VS fpnum")
	plt.xlabel("threshold")
	plt.ylabel("fasle positive number")
	plt.plot(thresholds,fpNumbers,'yo-')
	thresholdsVSfpnum = plt.gcf()
	thresholdsVSfpnum.savefig(saveGraph+pngname2)
	plt.close()


	pngname2_ = "/"+method + "_fnnumbers"
	plt.title("thresholds VS fnnum")
	plt.xlabel("threshold")
	plt.ylabel("fasle negative number")
	plt.plot(thresholds,fnNumbers,'yo-')
	thresholdsVSfnnum = plt.gcf()
	thresholdsVSfnnum.savefig(saveGraph+pngname2_)
	plt.close()

	pngname3 = "/"+method + "precison.png"
	plt.title("precision")
	plt.xlabel("threshold")
	plt.ylabel("precision")
	plt.plot(thresholds[::-1],tpr)
	precision = plt.gcf()
	precision.savefig(saveGraph+pngname3)
	plt.close()

	time = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
	pngname4 = "/"+method+'_roc'+"_"+time+".jpg"
	auc_score =  metrics.roc_auc_score(y, scores)
	plt.xlabel("FPR")
	plt.ylabel("TPR")
	plt.title(method +" roc with auc score "+str(auc_score))
	plt.plot(fpr,tpr,'yo-')
	rocfig = plt.gcf()
	rocfig.savefig(saveGraph+"/"+pngname4)
	plt.close()


def analysis(test_result,saveGraph,saveStaData,errorAddress):

	test_result,method,fpr,tpr,thresholds,auc_score,fpNumbers,fnNumbers = modelinfor(test_result)
	graphreport(test_result,method,fpr,tpr,thresholds,auc_score,fpNumbers,fnNumbers,saveGraph)
	stareport(method,fpr,tpr,thresholds,auc_score,fpNumbers,fnNumbers,saveStaData)
	errorreport(test_result,fpr, tpr, thresholds,errorAddress)


def modelCompare():
	pass


if __name__ == '__main__':
	csvname = "ResultBoosting.csv" #"CNNResultPatchCPP.csv"
	docname = "ResultBoosting"	#"CNN"
	figname = "fpNumber.png"
	test_result ="/home/henry/projects/sphere_detection/algoopt/testData/"+csvname
	saveAddress ="/home/henry/projects/sphere_detection/algoopt/Filter/"+docname+"/fpSphere/"
	saveGraph = "/home/henry/projects/sphere_detection/algoopt/Filter/"+docname+"/graphreport/"
	

	test_result,method,fpr,tpr,thresholds,auc_score,fpNumbers,fnNumbers = modelinfor(test_result)
	#get_fp_sphere(test_result,saveAddress)
	graphreport(method,fpr,tpr,thresholds,auc_score,fpNumbers,fnNumbers,saveGraph)
