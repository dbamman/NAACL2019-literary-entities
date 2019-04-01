import argparse, os

class NestedNERGenerator:
    def __init__(self, content, closed=True):
        self.closed = closed
        self.sorted = False
        self.intervals = []
        self.nestedIntervals = []
        self.content = content
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

def filter_label(label):
    labels = []
    if len( label  ) == 0:
        return []
    for label_raw in label.split("|"):
        idx, label_name = label_raw.split()
        begin, end = idx.split(",")[:2]
        labels.append( " ".join( [ label_name, begin, end ] ) )
    return labels

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input', help='directory containing train.data, dev.data, test.data', required=True)

    args = vars(parser.parse_args())
    inputDir=args["input"]

    files = ["train.data", "test.data", "dev.data"]
    for split in "train", "dev", "test":
        filename=os.path.join(inputDir, "%s.txt.no_PRO_WHQ_WEA" % split)
        outfilename=os.path.join(inputDir, "%s.txt.no_PRO_WHQ_WEA.tsv" % split)

        dataset = []
        with open(filename, "r") as stream:
            datas = stream.read().split("\n")
            length = len(datas)
            for data_idx in range(0, length-1, 4): 
                dataset.append( (datas[data_idx], datas[data_idx+2]) )


        outfile = open( outfilename, "w" )
        for text, label in dataset:
            content = filter_label( label )
            gen = NestedNERGenerator(content)
            gen.findAllNested()
            layers = gen.getLayers()
            textSplit = tuple( text.split() )
            formatingList = []
            formatingList.append(text.split())
            for l in layers:
                labelList = ['O' for i in range(len(textSplit))]
                for elem in l:
                    label, textBeginIdx, textEndIdx = elem.split()[0], int(elem.split()[1]), int(elem.split()[2]) - 1 
                    labelList[textBeginIdx] = "B-" + label
                    if textEndIdx > textBeginIdx:
                        labelList[textBeginIdx+1: textEndIdx+1] = ["I-"+label] * (textEndIdx - textBeginIdx)
                formatingList.append(labelList)
            if len(layers) == 2:
                formatingList.append(['O' for i in range(len(textSplit))])
            formatingList.append(['O' for i in range(len(textSplit))])
            for j in range(len(formatingList[0])):
                line = ''
                for i in range(len(formatingList)):
                    line = line + formatingList[i][j] + '\t'
                line = line[:-1] + '\n'
                outfile.write( line )
            outfile.write("\n")
        outfile.close()
