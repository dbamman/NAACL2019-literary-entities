import sys, os
from collections import Counter

def proc(inputDir):

	counts=Counter()
	for split in "train", "dev", "test":
		inputPath=os.path.join(inputDir, "%s.data" % split)
		with open(inputPath) as file:
			for line in file:
				cols=line.rstrip().split("\t")
				for layer in cols[1:]:
					if layer.startswith("B-"):
						cat=layer.split("-")[1]
						counts[cat]+=1
	return counts

# python scripts/fig1_data.py data/ace/ data/litbank/ > results/fig1.dists.txt

if __name__ == "__main__":
	ace_counts=proc(sys.argv[1])
	lit_counts=proc(sys.argv[2])

	ace_total=sum(ace_counts.values())
	lit_total=sum(lit_counts.values())

	print ("type\tACE\tLiterature")

	for label in lit_counts:
		print ("%s\t%.3f\t%.3f" % (label, float(ace_counts[label])/ace_total, float(lit_counts[label])/lit_total))