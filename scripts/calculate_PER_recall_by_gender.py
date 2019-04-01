import sys, argparse
import numpy as np
import random

def read_gender_labels(filename, exclude_honorifics):

	count=0
	valid=set(["M", "F", "U"])
	labels={}
	with open(filename) as file:
		for idx,line in enumerate(file):
			cols=line.rstrip().split("\t")
			textstart=cols.index("_TEXT_")
			for i in range(0,textstart-1,3):
				target=cols[i]
				text=cols[i+1]

				if exclude_honorifics:
					if text.startswith("Mrs.") or text.startswith("Miss") or text.startswith("Mr."):
						continue 

				gender=cols[i+2]

				if gender not in valid:
					continue

				count+=1
				labels[(idx, target)]=gender

	print("%s entities" % count)
	return labels

def permute(labels):
	targets=list(labels.keys())
	genders=list(labels.values())
	random.shuffle(genders)
	permuted_labels={}
	for idx, target in enumerate(targets):
		permuted_labels[target]=genders[idx]

	# print(permuted_labels)
	return permuted_labels

def evaluate(lit_data, ace_data, gender_labels, do_print=False):
	M_tot=F_tot=U_tot=0.

	M_lit_cor=F_lit_cor=U_lit_cor=0.
	M_ace_cor=F_ace_cor=U_ace_cor=0.
	
	for target in lit_data:
		gender=gender_labels[target]
	
		if gender == "M":
			M_lit_cor+=1
		elif gender == "F":
			F_lit_cor+=1
		else:
			U_lit_cor+=1
	
	for target in ace_data:
		gender=gender_labels[target]

		if gender == "M":
			M_ace_cor+=1
		elif gender == "F":
			F_ace_cor+=1
		else:
			U_ace_cor+=1
			

	for target in gender_labels:
		gender=gender_labels[target]
		if gender == "M":
			M_tot+=1
		elif gender == "F":
			F_tot+=1
		else:
			U_tot+=1

	if do_print:

		print ("ACE Recall (F): %.3f (%s), recall (M): %.3f (%s), recall (U): %.3f (%s)" % (F_ace_cor/F_tot, F_tot, M_ace_cor/M_tot, M_tot,  U_ace_cor/U_tot, U_tot ))
		print ("LIT Recall (F): %.3f (%s), recall (M): %.3f (%s), recall (U): %.3f (%s)" % (F_lit_cor/F_tot, F_tot, M_lit_cor/M_tot, M_tot,  U_lit_cor/U_tot, U_tot ))

	ace_diff=(F_ace_cor/F_tot)-(M_ace_cor/M_tot)
	lit_diff=(F_lit_cor/F_tot)-(M_lit_cor/M_tot)

	return ace_diff, lit_diff


def proc(filename, gender_labels):

	data={}

	with open(filename) as file:
		for idx, line in enumerate(file):
			cols=line.rstrip().split("\t")
			sentence_preds=[]
			if len(cols) == 2:
				preds=cols[1].split("|")
				for pred in preds:

					if (idx,pred) in gender_labels:
						data[idx,pred]=1

	return data

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-l','--lit_file', help='lit test predictions trained on Lit', required=True)
	parser.add_argument('-a','--ace_file', help='lit test predictions trained on ACE', required=True)
	parser.add_argument('-g','--gender_labels', help='labeled gold entity gender for test data', required=True)
	parser.add_argument('-e','--exclude_honorifics', help='exclude entities beginning with Mrs., Miss and Mr.', action='store_true')
	
	args = vars(parser.parse_args())

	ace_file=args["ace_file"]
	lit_file=args["lit_file"]
	exclude_honorifics=args["exclude_honorifics"]

	print ("Excluding honorifics: %s" % exclude_honorifics)

	gender_labels=read_gender_labels(args["gender_labels"], exclude_honorifics)

	lit_data=proc(lit_file, gender_labels)
	ace_data=proc(ace_file, gender_labels)

	true_ace_diff, true_lit_diff=evaluate(lit_data, ace_data, gender_labels, do_print=True)

	print("true ACE diff:\t%s" % true_ace_diff)
	print("true LIT diff:\t%s" % true_lit_diff)

	P=100000
	ace_p_value=0.
	lit_p_value=0.

	for i in range(P):
		permuted_labels=permute(gender_labels)
		ace_diff, lit_diff=evaluate(lit_data, ace_data, permuted_labels, do_print=False)

		if abs(ace_diff) > abs(true_ace_diff):
			ace_p_value+=1./P
		if abs(lit_diff) > abs(true_lit_diff):
			lit_p_value+=1./P


	print("ACE P value: %.10f" % ace_p_value)
	print("LIT P value: %.10f" % lit_p_value)


