import sys, argparse, glob, os

def get_max(pathToTSV):
	maxCols=0
	for filename in glob.glob(os.path.join(pathToTSV, '*.tsv')):
		print(filename)
		with open(filename) as file:
			for line in file:
				cols=line.rstrip().split("\t")
				if len(cols) > maxCols:
					maxCols=len(cols)
	return maxCols


def make_split(filename, outputFile, pathToTSV, maxCols):

	out=open(outputFile, "w", encoding="utf-8")
	with open(filename) as file:

		for line in file:
			name=line.rstrip()
			path=os.path.join(pathToTSV, name)

			with open(path) as file2:
				for line in file2:
					cols=line.rstrip().split("\t")
					if len(cols) > 1:

						for i in range(len(cols), maxCols):
							cols.append("O")

					out.write("%s\n" % '\t'.join(cols))

	out.close()


# python scripts/create_splits.py -i experiments/literary_splits/ -o experiments/literary_splits/ -t data/tsv/
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i','--input', help='directory containing train.ids, dev.ids, test.ids', required=True)
	parser.add_argument('-o','--output', help='output directory where train.data, dev.data and test.data should be written', required=True)
	parser.add_argument('-t','--tsvDir', help='path to tsv files', required=True)

	args = vars(parser.parse_args())
	inputDir=args["input"]
	outputDir=args["output"]
	tsvDir=args["tsvDir"]

	# ensure train, dev and test have the same number of nested layers
	maxCols=get_max(tsvDir)

	for split in "train", "dev", "test":
		inputPath=os.path.join(inputDir, "%s.ids" % split)
		outputPath=os.path.join(outputDir, "%s.data" % split)

		make_split(inputPath, outputPath, tsvDir, maxCols)

