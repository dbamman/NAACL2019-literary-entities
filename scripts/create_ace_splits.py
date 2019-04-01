"""
This script creates {train,dev,test}.data from {train,dev,test}.ids

"""

import argparse, os

def process_file(filename, out):
	with open(filename) as file:
		for line in file:
			out.write(line)

def proc(filename, outfile, tsvDir):

	out=open(outfile, "w", encoding="utf-8")
	with open(filename) as file:
		for line in file:
			filename=line.rstrip()
			path=os.path.join(tsvDir, filename)
			process_file(path, out)
	out.close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i','--input', help='directory containing train.ids, dev.ids, test.ids', required=True)
	parser.add_argument('-o','--output', help='output directory where train.data, dev.data and test.data should be written', required=True)
	parser.add_argument('-t','--tsvDir', help='path to procssed ACE files', required=True)

	args = vars(parser.parse_args())
	inputDir=args["input"]
	outputDir=args["output"]
	tsvDir=args["tsvDir"]


	for split in "train", "dev", "test":
		inputPath=os.path.join(inputDir, "%s.ids" % split)
		outputPath=os.path.join(outputDir, "%s.txt" % split)
		proc(inputPath, outputPath, tsvDir)
