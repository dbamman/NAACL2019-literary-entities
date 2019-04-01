# From brat originals, convert to nested TSV format
python3 convert_brat_to_tsv.py -i ../litbank/entities/brat/ -o ../data/litbank/tsv

# Fill in splits
python3 create_splits.py -i ../data/litbank/ -o ../data/litbank/ -t ../data/litbank/tsv
