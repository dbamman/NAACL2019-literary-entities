import argparse, os

def process_file(filename, outfile):
	out=open(outfile, "w", encoding="utf-8")

	with open(filename) as file:
		lines=file.readlines()

		for i in range(0,len(lines), 3):
			text=lines[i].rstrip()
			entitiesStr=lines[i+1].rstrip()

			entities=entitiesStr.split("|")
			new_entities=[]

			for entity in entities:
				if len(entity) < 2:
					continue
				parts=entity.split(" ")
				e_type=parts[0]
				e_subtype=parts[1]
				e_class=parts[2]
				e_start=int(parts[3])
				e_end=int(parts[4])
				e_head_start=int(parts[5])
				e_head_end=int(parts[6])
				if e_class == "PRO" or e_class == "WHQ":
					continue
				if e_type == "WEA":
					continue
					
				new_entities.append("%s,%s,%s,%s %s" % (e_start, e_end, e_head_start, e_head_end, e_type))

			out.write ("%s\n\n" % text)
			out.write  ("%s\n\n"%  "|".join(new_entities))
	
	out.close()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('-i','--input', help='directory containing train.data, dev.data, test.data', required=True)

	args = vars(parser.parse_args())
	inputDir=args["input"]


	for split in "train", "dev", "test":
		inputPath=os.path.join(inputDir, "%s.txt" % split)
		outputPath=os.path.join(inputDir, "%s.txt.no_PRO_WHQ_WEA" % split)
		process_file(inputPath, outputPath)

