cd ../layered-bilstm-crf/src/

# Get Wikipedia embeddings used in Ju et al. 2018
wget "http://tti-coin.jp/data/wikipedia200.bin"

# Convert embeddings to .txt
python3 ../../scripts/convert_embeddings_bin_to_txt.py wikipedia200.bin wikipedia200.txt

mkdir ../lit_model
mkdir ../ace_model

python3 train.py lit.train.config > lit_train.log 2>&1
python3 train.py ace.train.config > ace_train.log 2>&1


