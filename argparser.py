import argparse
import os 
import sys
import report


parser = argparse.ArgumentParser()
parser.add_argument('-rf',"--resultfile",default="",help="the path to the model result file")
parser.add_argument('-s',"--save",default=os.path.abspath(os.curdir),help="the path to save the analysis results")
args = parser.parse_args()

if args.resultfile =="":
	sys.exit("result file address needed")


if args.resultfile != "":
	if not os.path.isfile(args.resultfile):
		sys.exit( "can not find file:"+args.resultfile)
	
	else:
		resultfile = args.resultfile
		print resultfile


if not os.path.isdir(args.save):
	sys.exit("no such directory: " + args.save)


else:
	reportRoot = args.save


saveGraph = reportRoot +"/graph"
saveStaData = reportRoot + "/stadata"
errorAddress = reportRoot + "/error"
fpsphere = errorAddress+"/fpSphere"
fnsphere = errorAddress+"/fnSphere"

docs = [saveGraph,saveStaData,errorAddress,fpsphere,fnsphere]
for doc in docs:
	if not os.path.isdir(doc):
		os.mkdir(doc)

report.analysis(resultfile,saveGraph,saveStaData,errorAddress)





