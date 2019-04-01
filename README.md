# NAACL2019-literary-entities
Code to support Bamman et al. (2019), "An Annotated Dataset of Literary Entities" (NAACL 2019).

#

* `litbank` is a snapshot of the master [LitBank repo](https://github.com/dbamman/litbank) used for these experiments.
* `layered-bilstm-crf` contains a clone of [the Github repo](https://github.com/meizhiju/layered-bilstm-crf) for the nested NER model of [Ju et al. 2018](http://aclweb.org/anthology/N18-1131).  `train.py` and `test.py` are both updated to take a command-line argument specifying a configuration file; and `test.py` now also writes predictions to file (specified in the configuration as `predictions_path`).
* `ACEReader` wraps code from Stanford CoreNLP for processing the XML files of the ACE 2005 data (LDC2006T06), including tokenization and sentence splitting.
* 80/10/10 train, dev and test splits (by document) for both ACE 2005 and LitBank can be found in `data/ace/{train,dev,test}.ids` and `data/litbank/{train,dev,test}.ids`, respectively.


## pipeline

This pipeline requires access to [ACE 2005](https://catalog.ldc.upenn.edu/LDC2006T06). Download from LDC and specify the path in `ACE2005_PATH` below.

```sh
ACE2005_PATH=/path/to/LDC2006T06
cd scripts
./create_literary_data.sh
./create_ace_data.sh $ACE2005_PATH
./train_ner.sh
./test_ner.sh
./evaluate_gender.sh
./create_figures.sh 
```
