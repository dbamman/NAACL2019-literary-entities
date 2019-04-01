python fig1_data.py ../data/ace/ ../data/litbank/ > ../results/fig1.dists.txt

# code for generating figure from that data is in fig1.r

python fig2_data.py ../results/ace_lit.bootstrap.results.txt ../results/lit_lit.bootstrap.results.txt > ../results/fig2.labeldist.txt

# code for generating figure from that data is in fig2.r
