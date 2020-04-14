from collections import Counter
import os
import numpy as np
from socialsent import util
import pyximport
pyximport.install(setup_args={"include_dirs": np.get_include()})

from socialsent.representations import sparse_io

def run(word_gen, index, window_size, out_file):
    context = []
    pair_counts = Counter()
    for word in word_gen:
        context.append(index[word])
        if len(context) > window_size * 2 + 1:
            context.pop(0)
        pair_counts = _process_context(context, pair_counts, window_size)

    sparse_io.export_mat_from_dict(pair_counts, out_file.encode())

def _process_context(context, pair_counts, window_size):
    if len(context) < window_size + 1:
        return pair_counts
    target = context[window_size]
    indices = list(range(0, window_size))
    indices.extend(range(window_size + 1, 2 * window_size + 1))
    for i in indices:
        if i >= len(context):
            break
        pair_counts[(target, context[i])] += 1
    return pair_counts
