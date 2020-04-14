import numpy as np
import os
from socialsent import util
import pyximport

pyximport.install(setup_args={"include_dirs": np.get_include()})
from socialsent.representations import sparse_io


def load_matrix(f):
    if not f.endswith(".bin"):
        f += ".bin"
    return sparse_io.retrieve_mat_as_coo(f.encode()).tocsr()


def save_vocabulary(path, vocab):
    with open(path, "w") as f:
        for w in vocab:
            print >> f, w


def load_vocabulary(mat, path):
    index = util.load_pickle(path)
    vocab = sorted(index, key=lambda word: index[word])
    iw = vocab[: mat.shape[0]]
    ic = vocab[: mat.shape[1]]
    return iw, ic
