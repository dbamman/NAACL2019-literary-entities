import sys
import numpy as np
from collections import Counter

def calcFByCategory(gold, pred):
	cat_correct=Counter()
	cat_true_n=Counter()
	cat_pred_n=Counter()

	cor=0.
	for g in gold:
		if g in pred:
			cor+=1.

	for gbig in gold:
		sentence_idx, g=gbig
		parts=g.split(" ")
		lab=parts[2]
		cat_true_n[lab]+=1.

		if gbig in pred:
			cat_correct[lab]+=1

	for sentence_idx, p in pred:
		parts=p.split(" ")
		lab=parts[2]
		
		cat_pred_n[lab]+=1.
		


	precision=cor/len(pred)
	recall=cor/len(gold)
	F=(2*precision*recall)/(precision+recall)

	Fs={}
	Ps={}
	Rs={}

	for lab in cat_true_n:
		lab_P=0
		lab_R=0
		if cat_pred_n[lab] > 0:
			lab_P=cat_correct[lab]/cat_pred_n[lab]

		if cat_true_n[lab] > 0:
			lab_R=cat_correct[lab]/cat_true_n[lab]

		lab_F=0
		if (lab_P+lab_R) > 0:
			lab_F=(2*lab_P*lab_R)/(lab_P+lab_R)
		Fs[lab]=lab_F
		Ps[lab]=lab_P
		Rs[lab]=lab_R



	return precision, recall, F, Ps, Rs, Fs

def calcF(gold, pred):

	cor=0.
	for g in gold:
		if g in pred:
			cor+=1

	precision=cor/len(pred)
	recall=cor/len(gold)
	F=(2*precision*recall)/(precision+recall)

	return precision, recall, F

def resample(lines):

	golds={}
	preds={}

	for sentence_idx,line in enumerate(lines):
		cols=line.rstrip().split("\t")
		if len(cols) > 1:
			gold=cols[0].split("|")
			if len(gold) > 0:
				for g in gold:
					if len(g) > 0:
						golds[(sentence_idx,g)]=1

			if len(cols) > 1:
				pred=cols[1].split("|")

				if len(pred) > 0:
					for p in pred:
						if len(p) > 0:
							preds[(sentence_idx,p)]=1

	return golds, preds


def proc(filename):

	with open(filename) as file:
		lines=file.readlines()

		precs=[]
		recs=[]
		fs=[]

		fs_lab={}
		ps_lab={}
		rs_lab={}

		for i in range(10000):
			sample=np.random.choice(lines, len(lines))
			golds, preds=resample(sample)
			precision, recall, F, Ps, Rs, Fs=calcFByCategory(golds, preds)
			for lab in Fs:
				if lab not in fs_lab:
					fs_lab[lab]=[]
					ps_lab[lab]=[]
					rs_lab[lab]=[]

				fs_lab[lab].append(Fs[lab])
				ps_lab[lab].append(Ps[lab])
				rs_lab[lab].append(Rs[lab])

			precs.append(precision)
			recs.append(recall)
			fs.append(F)

		print ("Precision: %s" % ' '.join(["%.1f" % (x*100) for x in np.percentile(precs, [2.5, 50, 97.5])]))
		print ("Recall: %s" % ' '.join(["%.1f" % (x*100) for x in np.percentile(recs, [2.5, 50, 97.5])]))
		print ("F: %s" % ' '.join(["%.1f" % (x*100) for x in np.percentile(fs, [2.5, 50, 97.5])]))

		for lab in fs_lab:
			print ("%s Precision: %s" % (lab,' '.join(["%.1f" % (x*100) for x in np.percentile(ps_lab[lab], [2.5, 50, 97.5])])))
			print ("%s Recall: %s" % (lab,' '.join(["%.1f" % (x*100) for x in np.percentile(rs_lab[lab], [2.5, 50, 97.5])])))
			print ("%s F: %s" % (lab, ' '.join(["%.1f" % (x*100) for x in np.percentile(fs_lab[lab], [2.5, 50, 97.5])])))

proc(sys.argv[1])