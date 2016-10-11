import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from time import gmtime, strftime
from sklearn import metrics

def get_TPR(test_result,threshold):
	
	test_result = pd.DataFrame.from_csv(test_result)
	fnn = float(len(test_result['name'][test_result['predict']<threshold & test_result['lable'] == 1]))
	tpn = float(len(test_result['name'][test_result['predict']>threshold & test_result['lable'] == 1]))

	tpr = tpn/(fnn + tpn)
	
	return tpr

def get_FPR(test_result,threshold):
	
	test_result = pd.DataFrame.from_csv(test_result)
	tnn = float(len(test_result['name'][test_result['predict']<threshold & test_result['lable'] == 0]))
	fpn = float(len(test_result['name'][test_result['predict']>threshold & test_result['lable'] == 0]))
	
	fpr = fpn/(tnn+fpn)
	
	return fpr

def get_tpr_fpr_pair(test_result,resolt):
	#number of points
	if resolt > 0.5:
		print "resolution must between 0 and 0.5"
		import sys
		sys.exit()
	
	nop = int(float(1)/resolt)
	
	tprs = []
	fprs = []

	for i in xrange(nop):
		threshold = (i+1)*resolt
		
		tpr = get_TPR(test_result,threshold)
		fpr = get_FPR(test_result,threshold)
		
		tprs.append(tpr)
		fprs.append(fpr)
	
	return fprs,tprs
	
	

def draw_roc_fromFile(test_result,resolt,saveAddress):
	fprs,tprs = get_tpr_fpr_pair(test_result,resolt)
	fprs = np.asarray(fprs)
	tprs = np.asarray(tprs)

	plt.xlabel("FPR")
	plt.ylabel("TPR")

	auc_score = get_roc_auc_score_fromFile(test_result)

	plt.title("roc with auc score "+str(auc_score))
	
	plt.plot(fprs,tprs,'yo-')
	rocfig = plt.gcf()
	
	time = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
	figname = 'roc'+"_"+time+".jpg"
	rocfig.savefig(saveAddress+"/"+figname)

def draw_roc_fromFile2(test_result,saveAddress,method):

	test_result = pd.DataFrame.from_csv(test_result)
	y = np.asarray(test_result['label'])
	scores = np.asarray(test_result['predict'])

	fpr, tpr, thresholds = metrics.roc_curve(y, scores)

	auc_score =  metrics.roc_auc_score(y, scores)

	plt.xlabel("FPR")
	plt.ylabel("TPR")
	plt.title(method +" roc with auc score "+str(auc_score))
	plt.plot(fpr,tpr,'yo-')
	rocfig = plt.gcf()
	
	time = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
	figname = method+'_roc'+"_"+time+".jpg"
	rocfig.savefig(saveAddress+"/"+figname)
	plt.close()

def get_curve_and_index(test_result):
	test_result = pd.DataFrame.from_csv(test_result)
	y = np.asarray(test_result['label'])
	scores = np.asarray(test_result['predict'])

	fpr, tpr, thresholds = metrics.roc_curve(y, scores)

	auc_score =  metrics.roc_auc_score(y, scores)

	return fpr,tpr,thresholds,auc_score

def draw_multi_roc(test_result1,test_result2,name,saveAddress):
	
	fpr1,tpr1,thresholds1,auc_score1 = get_curve_and_index(test_result1)
	fpr2,tpr2,thresholds2,auc_score2 = get_curve_and_index(test_result2)

	plt.xlabel("FPR")
	plt.ylabel("TPR")
	plt.title( name[0]+" and "+name[1] +" ROC ")
	
	plt.plot(fpr1,tpr1,'yo-',label=name[0] +" roc with auc score "+str(auc_score1))
	plt.plot()

	plt.plot(fpr2,tpr2,label=name[1] +" roc with auc score "+str(auc_score2))
	
	plt.legend(loc=2,prop={'size':6})
	rocfig = plt.gcf()
	time = strftime("%Y-%m-%d-%H-%M-%S", gmtime())
	figname = name[0]+" and "+name[1]+'_roc'+"_"+time+".jpg"
	rocfig.savefig(saveAddress+"/"+figname)


def get_roc_auc_score_fromFile(test_result):
	
	test_result = pd.DataFrame.from_csv(test_result)
	y = np.asarray(test_result['lable'])
	probs = np.asarray(test_result['predict'])

	auc_score = metrics.roc_auc_score(y,probs)
	
	return auc_score

if __name__ == '__main__':
	test_result=""
	resolt = 0.05
	saveAddress = "/home/henry/projects/algoopt/ROC/curves"

	draw_roc_fromFile(test_result,resolt,saveAddress)
	#draw_roc_fromFile2(test_result,saveAddress)
	
