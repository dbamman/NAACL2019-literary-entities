import os
import sys
os.environ['CHAINER_SEED'] = '0'
import random
random.seed(0)
import numpy as np
np.random.seed(0)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pickle

import chainer.functions as F
from chainer import iterators
from chainer import cuda
from chainer import serializers

from src.model.layered_model import Model, Evaluator, Updater
from src.model.loader import load_sentences, update_tag_scheme, parse_config
from src.model.loader import prepare_dataset
from src.model.utils import evaluate


def predict(data_iter, model, mode):
    """
    Iterate data with well - trained model
    """
    for batch in data_iter:
        raw_words = [x['str_words'] for x in batch]
        words = [model.xp.array(x['words']).astype('i') for x in batch]
        chars = [model.xp.array(y).astype('i') for x in batch for y in x['chars']]
        tags = model.xp.vstack([model.xp.array(x['tags']).astype('i') for x in batch])

        # Init index to keep track of words
        index_start = model.xp.arange(F.hstack(words).shape[0])
        index_end = index_start + 1
        index = model.xp.column_stack((index_start, index_end))

        # Maximum number of hidden layers = maximum nested level + 1
        max_depth = len(batch[0]['tags'][0])
        sentence_len = np.array([x.shape[0] for x in words])
        section = np.cumsum(sentence_len[:-1])
        predicts_depths = model.xp.empty((0, int(model.xp.sum(sentence_len)))).astype('i')

        for depth in range(max_depth):
            next, index, extend_predicts, words, chars = model.predict(chars, words, tags[:, depth], index, mode)
            predicts_depths = model.xp.vstack((predicts_depths, extend_predicts))
            if not next:
                break

        predicts_depths = model.xp.split(predicts_depths, section, axis=1)
        ts_depths = model.xp.split(model.xp.transpose(tags), section, axis=1)
        yield ts_depths, predicts_depths, raw_words


def load_mappings(mappings_path):
    """
    Load mappings of:
      + id_to_word
      + id_to_tag
      + id_to_char
    """
    with open(mappings_path, 'rb') as f:
        mappings = pickle.load(f)
        id_to_word = mappings['id_to_word']
        id_to_char = mappings['id_to_char']
        id_to_tag = mappings['id_to_tag']

    return id_to_word, id_to_char, id_to_tag


def get_entities(xs, ys, id_to_tag):

    all_entities={}

    # for i in range(len(xs)):

    for k in range(int(len(ys))):

        start=None
        this_type=None

        for j in range(len(xs)):
            tag0=id_to_tag[int(ys[k][j])]
            parts=tag0.split("-")
            p_type=None
            p_position=tag0
            if len(parts) == 2:
                p_type=parts[1]
                p_position=parts[0]

            if p_position == "B" or p_position == "O" or (p_position == "I" and p_type != last_p_type):
                # end previous tag
                if start != None:
                    end=j
                    ent=(0,start, end, this_type)
                    all_entities[ent]=1
                start=None
                this_type=None

            if p_position == "B":
                start=j
                this_type=p_type

            last_p_type=p_type

        if start != None:
            ent=(0,start, len(xs), this_type)
            all_entities[ent]=1

    return all_entities

def calc_f(all_pred, all_true):
    cor=0.
    for ent in all_pred:
        if ent in all_true:
            cor+=1

    precision=cor/len(all_pred)
    recall=cor/len(all_true)
    F=2*precision*recall/(precision+recall)

    print ("Precision: %.3f, Recall: %.3f, F: %.3f %s %s"  % (precision, recall, F, len(all_pred), len(all_true)))
    
def main(config_path):
    args = parse_config(config_path)

    # Load sentences
    test_sentences = load_sentences(args["path_test"], args["replace_digit"])

    # Update tagging scheme (IOB/IOBES)
    update_tag_scheme(test_sentences, args["tag_scheme"])

    # Load mappings from disk
    id_to_word, id_to_char, id_to_tag = load_mappings(args["mappings_path"])
    word_to_id = {v: k for k, v in id_to_word.items()}
    char_to_id = {v: k for k, v in id_to_char.items()}
    tag_to_id  = {v: k for k, v in id_to_tag.items()}

    # Index data
    test_data = prepare_dataset(test_sentences, word_to_id, char_to_id, tag_to_id, None, args["lowercase"])
    test_iter = iterators.SerialIterator(test_data, args["batch_size"], repeat=False, shuffle=False)

    model = Model(len(word_to_id), len(char_to_id), len(tag_to_id), args)

    serializers.load_npz(args['path_model'], model)

    model.id_to_tag = id_to_tag
    model.parameters = args

    device = args['gpus']
    if device['main'] >= 0:
        cuda.get_device_from_id(device['main']).use()
        model.to_gpu()

    pred_tags = []
    gold_tags = []
    words = []

    # Collect predictions
    out=open(args['predictions_path'], "w", encoding="utf-8")

    all_true={}
    all_pred={}
    idx=0
    for ts, ys, xs in predict(test_iter, model, args['mode']):
        gold_tags.extend(ts)
        pred_tags.extend(ys)
        words.extend(xs)
        
        # for sentence in batch size
        for i in range(len(xs)):
            true_entities=get_entities(xs[i], ts[i], id_to_tag)
            pred_entities=get_entities(xs[i], ys[i], id_to_tag)

            out.write("%s\t%s\n" % ("|".join(["%s %s %s" % (v[1], v[2], v[3]) for v in true_entities]), "|".join(["%s %s %s" % (v[1], v[2], v[3]) for v in pred_entities])))
            for sid,start, end,label in true_entities:
                all_true[(idx,sid,start,end,label)]=1
            for sid,start, end,label in pred_entities:
                all_pred[(idx,sid,start,end,label)]=1

            idx+=1

    out.close()

    calc_f(all_pred, all_true)
    evaluate(model, pred_tags, gold_tags, words)


if __name__ == '__main__':
    main(sys.argv[1])
