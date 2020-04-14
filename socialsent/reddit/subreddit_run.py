from argparse import ArgumentParser
import sys
import os
import time
import random

from socialsent import seeds
from socialsent import constants
from socialsent import util
from socialsent import polarity_induction_methods

from socialsent.representations.representation_factory import create_representation


DICTS = "data/{}-dict.pkl"
POLARITIES = "data/polarities/"


def main(subreddit_name):
    # subredditgen.main(subreddit_name)
    word_dict = util.load_pickle(DICTS.format(subreddit_name))
    word_dict.filter_extremes(no_above=0.1, no_below=100)

    to_keep = sorted(word_dict.dfs, key=lambda w: word_dict.dfs[w], reverse=True)[:5000]
    word_dict.filter_tokens(good_ids=to_keep)

    print("create representation")
    sub_vecs = create_representation(
        "SVD", constants.SUBREDDIT_EMBEDDINGS.format(subreddit_name)
    )
    pos_seeds, neg_seeds = seeds.twitter_seeds()

    print("get sub embedding")
    sub_vecs = sub_vecs.get_subembed(
        set(word_dict.token2id.keys()).union(pos_seeds).union(neg_seeds)
    )

    print("bootstrap")
    pols = polarity_induction_methods.bootstrap(
        sub_vecs,
        pos_seeds,
        neg_seeds,
        return_all=True,
        nn=25,
        beta=0.9,
        num_boots=50,
        n_procs=10,
    )

    util.write_pickle(pols, POLARITIES + subreddit_name + ".pkl")


if __name__ == "__main__":
    parser = ArgumentParser("Generate polarities")
    parser.add_argument("subreddit")
    args = parser.parse_args()
    main(args.subreddit)
