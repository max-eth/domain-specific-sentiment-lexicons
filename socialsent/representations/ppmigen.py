import numpy as np
from socialsent import util
from scipy.sparse import coo_matrix
from socialsent.representations.representation_factory import create_representation

import pyximport
pyximport.install(setup_args={"include_dirs": np.get_include()})

from socialsent.representations import sparse_io
from socialsent.constants import get_constants



def make_ppmi_mat(old_mat, row_probs, col_probs, smooth, neg=1, normalize=False):
    prob_norm = old_mat.sum() + (old_mat.shape[0] * old_mat.shape[1]) * smooth
    old_mat = old_mat.tocoo()
    row_d = old_mat.row
    col_d = old_mat.col
    data_d = old_mat.data
    neg = np.log(neg)

    for i in range(len(old_mat.data)):
        if data_d[i] == 0.0:
            continue
        joint_prob = (data_d[i] + smooth) / prob_norm
        denom = row_probs[row_d[i], 0] * col_probs[0, col_d[i]]
        if denom == 0.0:
            data_d[i] = 0
            continue
        data_d[i] = np.log(joint_prob / denom)
        data_d[i] = max(data_d[i] - neg, 0)
        if normalize:
            data_d[i] /= -1 * np.log(joint_prob)
    return coo_matrix((data_d, (row_d, col_d)))


def run(subreddit, smooth=0, cds=True, normalize=False, neg=1):
    const = get_constants(subreddit)
    file_indices = const['INDICES']
    file_counts = const['COUNTS']
    file_ppmi = const['PPMI']
    file_ppmi_index = const['PPMI_INDEX']

    counts = create_representation('Explicit', file_counts, file_indices, normalize=False)
    old_mat = counts.m
    index = counts.wi
    smooth = old_mat.sum() * smooth

    # getting marginal probs
    row_probs = old_mat.sum(1) + smooth
    col_probs = old_mat.sum(0) + smooth
    if cds:
        col_probs = np.power(col_probs, 0.75)
    row_probs = row_probs / row_probs.sum()
    col_probs = col_probs / col_probs.sum()

    # building PPMI matrix
    ppmi_mat = make_ppmi_mat(
        old_mat, row_probs, col_probs, smooth, neg=neg, normalize=normalize
    )

    sparse_io.export_mat_eff(
        ppmi_mat.row, ppmi_mat.col, ppmi_mat.data, file_ppmi.encode()
    )
    util.write_pickle(index, file_ppmi_index)

