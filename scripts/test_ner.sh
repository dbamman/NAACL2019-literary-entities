cd ../layered-bilstm-crf/src/

# After training and before testing, manually add the last saved model in ../lit_model/ to lit.lit.test.config (the "path_model" variable)
python3 test.py lit.lit.test.config > lit_lit_test.log 2>&1
python3 ../../scripts/bootstrapF.py ../../results/lit_lit.preds.txt > ../../results/lit_lit.bootstrap.results.txt

# After training and before testing, manually add the last saved model in ../ace_model/ to ace.ace.test.config (the "path_model" variable)
python3 test.py ace.ace.test.config > ace_ace_test.log 2>&1
python3 ../../scripts/bootstrapF.py ../../results/ace_ace.preds.txt > ../../results/ace_ace.bootstrap.results.txt


# After training and before testing, manually add the last saved model in ../ace_model/ to ace.lit.test.config (the "path_model" variable)
python3 test.py ace.lit.test.config > ace_lit_test.log 2>&1
python3 ../../scripts/bootstrapF.py ../../results/ace_lit.preds.txt > ../../results/ace_lit.bootstrap.results.txt
