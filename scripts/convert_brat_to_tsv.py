"""
Script to convert a directory of brat files (*.ann, *.txt) to tsv, one column for each level of nesting

"""

import glob, argparse, os
from itertools import groupby
from operator import itemgetter
import bisect
import random

class NestedNERGenerator:
	def __init__(self, content, closed=True):
		self.closed = closed
		self.sorted = False
		self.intervals = []
		self.nestedIntervals = []
		self.content = [" ".join([c.split()[1], c.split()[2], c.split()[3]])
						for c in content if c[0] == 'T']
		self.original = self.content

	def insert(self, label, begin, end):
		diff = str(int(end) - int(begin))
		self.intervals.append(begin)
		self.intervals.append(end + " " + label + " " + diff)
		self.sorted = False

	def sort(self):
		if not self.sorted:
			self.intervals.sort(key=lambda x: (int(x.split()[0]), int(x.split()[-1])))
			self.sorted = True

	def findNested(self):
		self.intervals = []
		content = [x.split() for x in self.content]
		for c in content:
			self.insert(c[0], c[1], c[2])
		self.sort()
		numIntervals = 0
		beginIdxStack = []
		levelIntervals = []
		for i in self.intervals:
			# When beginning index entry
			if len(i.split()) == 1:
				beginIdxStack.append(i)
				numIntervals += 1
				continue
			# When ending index entry
			else:
				numIntervals -= 1
				beginIdx = beginIdxStack.pop()
				if numIntervals == 0:
					continue
			# Join label + begin + end
			levelIntervals.append(" ".join([i.split()[1], beginIdx, i.split()[0]]))
		self.nestedIntervals.append(self.content)
		self.content = levelIntervals

	def nestedNum(self):
		return len(self.nestedIntervals)

	def findAllNested(self):
		while len(self.content) > 0:
			self.findNested()
		return self.nestedIntervals

	def getLayers(self):
		allLayers = []
		for i in range(self.nestedNum())[::-1]:
			allLayers.append(set(self.nestedIntervals[i]))
		for i in range(len(allLayers)-1, 0, -1):
			allLayers[i].difference_update(allLayers[i-1])

		for i in range(len(allLayers)):
			for j in range(i+1, len(allLayers)):
				adders = []
				for big in allLayers[j]:
					flag = True
					bStart, bEnd = int(big.split()[1]), int(big.split()[2])
					for small in allLayers[i]:
						sStart, sEnd = int(small.split()[1]), int(small.split()[2])
						if not (bStart > sEnd or bEnd < sStart):
							flag = False
					if flag:
						adders.append(big)
				for a in adders:
					allLayers[i].add(a)
					allLayers[j].remove(a)
		return allLayers

def splitWithIndices(text):
	p = 0
	idx = 0
	for k, g in groupby(text, lambda x: x==' ' or x=='\n'):
		q = p + sum(1 for i in g)
		if not k:
			yield p, q, idx
			idx += 1
		p = q

def splitSentences(text):
	p = 0
	idx = 0
	for k, g in groupby(text, lambda x: x=='\n'):
		q = p + sum(1 for i in g)
		if not k:
			yield q
			idx += 1
		p = q

def lookup(id, lower_bounds, sorted_data):
    index = bisect.bisect(lower_bounds, id) - 1
    if index < 0:
        return None
    _, upper, country = sorted_data[index]
    return country if id <= upper else None

# python scripts/convert_brat_to_tsv.py -i data/brat/ -o data/tsv
if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-i','--input', help='input directory containing brat files', required=True)
	parser.add_argument('-o','--output', help='output directory to write new tsv files to', required=True)

	args = vars(parser.parse_args())
	inputDir=args["input"]
	outputDir=args["output"]

	for filename in glob.glob(os.path.join(inputDir, '*.ann')):
		with open(filename) as f:
			content = f.readlines()
		with open(filename[:-3]+"txt") as f:
			text = f.read()
		print(filename)
		gen = NestedNERGenerator(content)
		gen.findAllNested()
		layers = gen.getLayers()

		textSplit = tuple(splitWithIndices(text))
		endSet = set(splitSentences(text))
		sentenceEnds = set([x[2] for x in textSplit if x[1] in endSet])
		textSplit = sorted(textSplit, key=itemgetter(0))
		lower_bounds = [lower for lower,_,_ in textSplit]
		formatingList = []
		formatingList.append(text.split())

		for l in layers:
			labelList = ['O' for i in range(len(textSplit))]
			for elem in l:
				label, begin, end = elem.split()[0], int(elem.split()[1]), int(elem.split()[2])
				textBeginIdx = lookup(begin, lower_bounds, textSplit)
				textEndIdx = lookup(end, lower_bounds, textSplit)
				labelList[textBeginIdx] = "B-" + label
				if textEndIdx > textBeginIdx:
					labelList[textBeginIdx+1: textEndIdx+1] = ["I-"+label] * (textEndIdx - textBeginIdx)
			formatingList.append(labelList)
		if len(layers) == 2:
			formatingList.append(['O' for i in range(len(textSplit))])
		formatingList.append(['O' for i in range(len(textSplit))])

		with open(os.path.join(outputDir, os.path.basename(filename)[:-3]+"tsv"),'w', encoding='utf8') as f:
			for j in range(len(formatingList[0])):
				line = ''
				for i in range(len(formatingList)):
					line = line + formatingList[i][j] + '\t'
				line = line + '\n'
				if j in sentenceEnds:
					line = line + '\n'
				f.write(line)
