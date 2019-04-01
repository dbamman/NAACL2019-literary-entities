for i in `ls /data/dbamman/naacl2019/gutenberg/transformed`; do basen=`basename $i`; echo $basen; echo $i; python3 predict.py lit.lit.test.config /data/dbamman/naacl2019/gutenberg/transformed/$basen /data/dbamman/naacl2019/gutenberg/lit_predict/$basen; done >> lit.predict.log

