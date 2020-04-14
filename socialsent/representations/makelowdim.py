import numpy as np

from sklearn.utils.extmath import randomized_svd
from socialsent import util
from socialsent.representations.explicit import Explicit


def run(index_path, in_file, out_path, dim=300, keep_words=None):
    base_embed = Explicit.load(in_file, index_path, normalize=False)
    if keep_words != None:
        base_embed = base_embed.get_subembed(keep_words)
    print("Factorising {} with shape {}".format(base_embed.m.nnz, base_embed.m.shape))
    u, s, v = randomized_svd(base_embed.m, n_components=dim, n_iter=5)
    np.save(out_path + "-u.npy", u)
    np.save(out_path + "-v.npy", v)
    np.save(out_path + "-s.npy", s)
    util.write_pickle(base_embed.iw, out_path + "-vocab.pkl")


