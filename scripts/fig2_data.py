import sys, re

def proc(filename):
	label_F={}
	with open(filename) as file:
		for line in file:
			match=re.match("^(\w{3}) F: (\d+\.\d) (\d+\.\d) (\d+\.\d)$", line.rstrip())
			if match != None:
				label=match.group(1)
				lower=match.group(2)
				median=match.group(3)
				upper=match.group(4)
				label_F[label]=(lower, median, upper)
	return label_F


# python fig2_data.py ../results/ace_lit.bootstrap.results.txt ../results/lit_lit.bootstrap.results.txt > ../results/fig2.labeldist.txt
if __name__ == "__main__":
	ace_lit_file=sys.argv[1]
	lit_lit_file=sys.argv[2]

	ace_lit_F=proc(ace_lit_file)
	lit_lit_F=proc(lit_lit_file)


	print('\t'.join(["type", "Data", "ymin", "value", "ymax"]))
	for label in ace_lit_F:
		print('\t'.join([label, "ACE", ace_lit_F[label][0], ace_lit_F[label][1], ace_lit_F[label][2]]))

	for label in lit_lit_F:
		print('\t'.join([label, "Literature", lit_lit_F[label][0], lit_lit_F[label][1], lit_lit_F[label][2]]))
