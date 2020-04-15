import os

scores_interval = [None,0]
scores = '' if scores_interval is None else 'scores-{}-'.format(scores_interval[1] if scores_interval[1] is not None else 'top')
BASE_DIR = ''
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUTS = 'outputs.json'
DICTS = scores + 'dict.pkl'
INDICES = scores + 'index.pkl'
COUNTS = scores + 'counts.bin'
PPMI = scores + 'ppmi.bin'
PPMI_INDEX = scores + 'ppmi-index.pkl'
VECS = scores + 'vecs'
POLARITIES = scores + 'polarities.pkl'

def filter_comments(x):
    if scores_interval is not None:
        if scores_interval[0] is not None:
            if x['score'] <= scores_interval:
                return False
        if scores_interval[1] is not None:
            if x['score'] > scores_interval:
                return False
    return True



NO_ABOVE = 0.4
NO_BELOW = 100
