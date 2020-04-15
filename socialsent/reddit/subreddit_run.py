from argparse import ArgumentParser
from socialsent import seeds
from socialsent import util
from socialsent import polarity_induction_methods
from socialsent.reddit import subredditgen

from socialsent.constants import get_constants

from socialsent.representations.representation_factory import create_representation


def main(subreddit):
    const = get_constants(subreddit)

    word_dict = util.load_pickle(const['DICTS'])
    word_dict.filter_extremes(no_above=const['NO_ABOVE_2'], no_below=const['NO_BELOW'])
    to_keep = sorted(word_dict.dfs, key=lambda w: word_dict.dfs[w], reverse=True)[:5000]
    word_dict.filter_tokens(good_ids=to_keep)

    print("Create representation...")
    sub_vecs = create_representation(
        'SVD', const['VECS']
    )
    pos_seeds, neg_seeds = seeds.twitter_seeds()

    pos_seeds = list(set(subredditgen.normalize_text(' '.join(pos_seeds), const['STEMMING'])))
    neg_seeds = list(set(subredditgen.normalize_text(' '.join(neg_seeds), const['STEMMING'])))


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

    util.write_pickle(pols, const['POLARITIES'])


if __name__ == "__main__":
    parser = ArgumentParser("Generate polarities")
    parser.add_argument("subreddit")
    args = parser.parse_args()
    main(args.subreddit)
