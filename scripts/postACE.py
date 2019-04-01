import argparse, os


def proc(filename, output):
	out=open(output, "w", encoding="utf-8")
	with open(filename) as file:
		for line in file:
			cols=line.rstrip().split("\t")
			if len(cols) < 2:
				out.write("\n")
			else:
				if len(cols) < 6:
					cols.extend(["O", "O", "O", "O", "O", "O"])
				out.write("%s\n" % '\t'.join(cols[:6]))
	out.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input', help='directory containing train.data, dev.data, test.data', required=True)

    args = vars(parser.parse_args())
    inputDir=args["input"]

    for split in "train", "dev", "test":
    	filename=os.path.join(inputDir, "%s.txt.no_PRO_WHQ_WEA.tsv" % split)
    	outfilename=os.path.join(inputDir, "%s.data" % split)
    	proc(filename, outfilename)