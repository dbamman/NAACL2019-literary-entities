
python3 calculate_PER_recall_by_gender.py -l ../results/lit_lit.preds.txt -a ../results/ace_lit.preds.txt -g ../data/gender_labels.txt > ../results/PER_recall_by_gender.txt

python3 calculate_PER_recall_by_gender.py -l ../results/lit_lit.preds.txt -a ../results/ace_lit.preds.txt -g ../data/gender_labels.txt -e > ../results/PER_recall_by_gender_exclude_honorifics.txt