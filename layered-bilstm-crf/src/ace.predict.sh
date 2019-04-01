for i in `ls /data/dbamman/naacl2019/gutenberg/transformed`; do basen=`basename $i`; echo $basen; echo $i; python3 predict.py ace.lit.test.config /data/dbamman/naacl2019/gutenberg/transformed/$basen /data/dbamman/naacl2019/gutenberg/ace_predict/$basen; done >> ace.predict.log 2>&1

