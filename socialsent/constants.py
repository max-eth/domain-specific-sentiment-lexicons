import os
import socialsent.main as main

BASE_DIR = ""
DATA_DIR = os.path.join(BASE_DIR, "data")

#STEMMING = True
#SCORES_INTERVAL = None

def filter_comments(x):
    scores_interval = SCORES_INTERVAL
    if scores_interval is not None:
        if scores_interval[0] is not None:
            if x["score"] < scores_interval[0]:
                return False
        if scores_interval[1] is not None:
            if x["score"] >= scores_interval[1]:
                return False
    return True

def set_constants(stemming, scores_interval):
    global STEMMING
    STEMMING = stemming
    global SCORES_INTERVAL
    SCORES_INTERVAL = scores_interval


def get_constants(subreddit):

    stemming = STEMMING
    scores_interval = SCORES_INTERVAL

    prefix = '' if scores_interval is None else 'scores-{}-{}-'.format(
        scores_interval[0] if scores_interval[0] is not None else 'nolim',
        scores_interval[1] if scores_interval[1] is not None else 'nolim')

    if stemming:
        prefix = "stemmed-" + prefix

    constants = dict()
    constants['OUTPUTS'] = "outputs.json"
    constants['DICTS'] = prefix + "dict.pkl"
    constants['INDICES'] = prefix + "index.pkl"
    constants['COUNTS'] = prefix + "counts.bin"
    constants['CORPUS'] = prefix + "corpus.pkl"
    constants['PPMI'] = prefix + "ppmi.bin"
    constants['PPMI_INDEX'] = prefix + "ppmi-index.pkl"
    constants['VECS'] = prefix + "vecs"
    constants['POLARITIES'] = prefix + "polarities.pkl"
    constants = {k: os.path.join(DATA_DIR, subreddit, v) for k, v in constants.items()}
    constants['NO_ABOVE_1'] = 0.5
    constants['NO_ABOVE_2'] = 0.1
    constants['NO_BELOW'] = 100
    constants['STEMMING'] = stemming
    return constants

