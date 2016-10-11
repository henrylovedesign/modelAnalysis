import argparse
import os 
import sys
import report


parser = argparse.ArgumentParser()
parser.add_argument('-p',"--photos",default="",help="the path to the model result file")
parser.add_argument('-s',"--save",default=os.path.abspath(os.curdir),help="the path to save the analysis results")
args = parser.parse_args()


if args.photos =="":
	sys.exit("result file address needed")


if args.photos != "":
	if not os.path.isfile(args.photos):
		sys.exit( "can not find file:"+args.photos)
	
	else:
		photos = args.photos
		print photos


if not os.path.isdir(args.save):
	sys.exit("no such directory: " + args.save)


else:
	classifyRoot = args.save

viewer(photos,classifyRoot)

