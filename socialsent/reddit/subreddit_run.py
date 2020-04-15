from argparse import ArgumentParser
import os
from socialsent import seeds
from socialsent import util
from socialsent import polarity_induction_methods
from socialsent.reddit import subredditgen

from socialsent.representations.embedding import SVDEmbedding
from socialsent.constants import DATA_DIR, VECS, DICTS, POLARITIES, NO_ABOVE_2, NO_BELOW

from socialsent.representations.representation_factory import create_representation


def main(subreddit):
    dir_path = os.path.join(DATA_DIR, subreddit)
    file_dicts = os.path.join(dir_path, DICTS)
    file_vecs = os.path.join(dir_path, VECS)
    file_polarities = os.path.join(dir_path, POLARITIES)

    word_dict = util.load_pickle(file_dicts)
    word_dict.filter_extremes(no_above=NO_ABOVE_2, no_below=NO_BELOW)
    to_keep = sorted(word_dict.dfs, key=lambda w: word_dict.dfs[w], reverse=True)[:5000]
    word_dict.filter_tokens(good_ids=to_keep)

    print("Create representation...")
    sub_vecs = create_representation(
        'SVD', file_vecs
    )
    pos_seeds, neg_seeds = seeds.twitter_seeds()

    pos_seeds = list(set(subredditgen.normalize_text(' '.join(pos_seeds))))
    neg_seeds = list(set(subredditgen.normalize_text(' '.join(neg_seeds))))


    print("Get sub embedding...")
    sub_vecs = sub_vecs.get_subembed(
        set(word_dict.token2id.keys()).union(pos_seeds).union(neg_seeds)
    )

    print("Bootstrapping...")
    print ("using seeds {} {}".format(pos_seeds, neg_seeds))
    pols = polarity_induction_methods.bootstrap(
        sub_vecs,
        pos_seeds,
        neg_seeds,
        return_all=True,
        nn=25,
        beta=0.9,
        boot_size=len(pos_seeds) - 2,
        num_boots=30,
        n_procs=10,
    )

    util.write_pickle(pols, file_polarities)


if __name__ == "__main__":
    parser = ArgumentParser("Generate polarities")
    parser.add_argument("subreddit")
    args = parser.parse_args()
    main(args.subreddit)
