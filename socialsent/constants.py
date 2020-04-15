import os
import socialsent.main as main

BASE_DIR = ""
DATA_DIR = os.path.join(BASE_DIR, "data")


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


def get_interval_idx(x):
    all_intervals = ALL_INTERVALS

    index = 0
    for low, high in all_intervals[:-1]:
        if x < high:
            return index

        index += 1

    return len(all_intervals) - 1


def set_constants(stemming, scores_interval, all_intervals=None):

    global STEMMING
    STEMMING = stemming
    global SCORES_INTERVAL
    SCORES_INTERVAL = scores_interval

    global ALL_INTERVALS
    ALL_INTERVALS = all_intervals


def get_interval_name(scores_interval):
    return "scores-{}-{}-".format(
        scores_interval[0] if scores_interval[0] is not None else "nolim",
        scores_interval[1] if scores_interval[1] is not None else "nolim",
    )


def get_interval_fname(subreddit, scores_interval):
    return os.path.join(
        DATA_DIR,
        subreddit,
        ("stemmed-" if STEMMING else "") + 
        get_interval_name(scores_interval)
        + "corpus.pkl",
    )


def get_constants(subreddit):

    stemming = STEMMING
    scores_interval = SCORES_INTERVAL

    prefix = "" if scores_interval is None else get_interval_name(scores_interval)

    if stemming:
        prefix = "stemmed-" + prefix

    constants = dict()
    constants["OUTPUTS"] = "outputs.json"
    constants["DICTS"] = prefix + "dict.pkl"
    constants["INDICES"] = prefix + "index.pkl"
    constants["COUNTS"] = prefix + "counts.bin"
    constants["PPMI"] = prefix + "ppmi.bin"
    constants["PPMI_INDEX"] = prefix + "ppmi-index.pkl"
    constants["VECS"] = prefix + "vecs"
    constants["POLARITIES"] = prefix + "polarities.pkl"
    constants = {k: os.path.join(DATA_DIR, subreddit, v) for k, v in constants.items()}

    constants["CORPUS"] = get_interval_fname(subreddit, scores_interval)
    constants["NO_ABOVE_1"] = 0.5
    constants["NO_ABOVE_2"] = 0.1
    constants["NO_BELOW"] = 100
    constants["STEMMING"] = stemming
    constants["INTERVAL"] = SCORES_INTERVAL
    constants["ALL_INTERVALS"] = ALL_INTERVALS
    constants["DATADIR"] = DATA_DIR
    return constants
