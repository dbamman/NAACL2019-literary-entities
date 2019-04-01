# Run with path to ACE 2005 data (LDC2006T06) as command-line argument
# ./create_ace_data.sh /path/to/LDC2006T06

ACE2005=$1

curDir=`pwd`

# copy dtd to all subdirectories that need it
cd $ACE2005
find . -type d -exec cp dtd/apf.v5.1.1.dtd {} \;

cd $curDir

ACE_OUTPUT_DIR=../data/ace

cd ../ACEReader/

./runjava Reader $ACE2005/data/English/bc/adj/ $ACE_OUTPUT_DIR/txt/bc/
./runjava Reader $ACE2005/data/English/bn/adj/ $ACE_OUTPUT_DIR/txt/bn/
./runjava Reader $ACE2005/data/English/nw/adj/ $ACE_OUTPUT_DIR/txt/nw/
./runjava Reader $ACE2005/data/English/wl/adj/ $ACE_OUTPUT_DIR/txt/wl/

cd ../scripts/

# Fill in splits; creates {train, dev, test}.txt files
python3 create_ace_splits.py -i $ACE_OUTPUT_DIR -o $ACE_OUTPUT_DIR -t $ACE_OUTPUT_DIR/txt

# Filter out PRO/WHQ mentions and WEA labels; creates {train, dev, test}.txt.no_PRO_WHQ_WEA files
python3 filter_ace_no_PRO_WHQ_WEA.py -i $ACE_OUTPUT_DIR

# Convert to nested NER format; create {train, dev, test}.txt.no_PRO_WHQ_WEA.tsv files
python3 convert_txt_to_tsv.py -i $ACE_OUTPUT_DIR

# Pad each sentence to have same level of nesting; creates {train, dev, test}.data files
python3 postACE.py -i $ACE_OUTPUT_DIR

cd $ACE_OUTPUT_DIR 
rm train.txt dev.txt test.txt train.txt.no_PRO_WHQ_WEA dev.txt.no_PRO_WHQ_WEA test.txt.no_PRO_WHQ_WEA train.txt.no_PRO_WHQ_WEA.tsv dev.txt.no_PRO_WHQ_WEA.tsv test.txt.no_PRO_WHQ_WEA.tsv
