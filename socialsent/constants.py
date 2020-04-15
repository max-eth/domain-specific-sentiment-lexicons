import os

stemming = True
scores_interval = [None, 0]
prefix = '' if scores_interval is None else 'scores-{}-'.format(scores_interval[1] if scores_interval[1] is not None else 'top')

if stemming:
    prefix = "stemmed-" + prefix

BASE_DIR = ""
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUTS = "outputs.json"
DICTS = prefix + "dict.pkl"
INDICES = prefix + "index.pkl"
COUNTS = prefix + "counts.bin"
CORPUS = prefix + "corpus.pkl"
PPMI = prefix + "ppmi.bin"
PPMI_INDEX = prefix + "ppmi-index.pkl"
VECS = prefix + "vecs"
POLARITIES = prefix + "polarities.pkl"


def filter_comments(x):
    if scores_interval is not None:
        if scores_interval[0] is not None:
            if x["score"] < scores_interval[0]:
                return False
        if scores_interval[1] is not None:
            if x["score"] >= scores_interval[1]:
                return False
    return True


NO_ABOVE_1 = 0.5
NO_ABOVE_2 = 0.1
NO_BELOW = 100
