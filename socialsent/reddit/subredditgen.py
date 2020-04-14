from gensim.utils import simple_preprocess
from gensim.corpora import Dictionary

from socialsent import util

from argparse import ArgumentParser
from socialsent.representations import ppmigen, cooccurgen, makelowdim
import json

COMMENTS = "data/small_output.json"
DICTS = "data/{}-dict.pkl"
OUT = "data/{}"


def word_gen(filename, gensim_dict, subreddit):

    for i, line in enumerate(open(filename)):
        comment = json.loads(line)
        if comment["score"] <= 0 or comment["subreddit"] != subreddit:
            continue

        for word in simple_preprocess(comment["body"]):
            word = word.lower()
            if word in gensim_dict.token2id:
                yield word
        if i % 10000 == 0:
            print("Processed line", i)


def main(filename, subreddit):
    out_path = OUT.format(subreddit)
    util.mkdir(out_path)

    print("Getting and writing dictionary...")

    with open(filename, "r") as f:
        dicts = (json.loads(comment) for comment in f)
        gdict = Dictionary(
            simple_preprocess(comment["body"])
            for comment in dicts
            if comment["score"] > 0 and comment["subreddit"] == subreddit
        )

    gdict.filter_extremes(no_above=0.5, no_below=100)
    gdict.compactify()
    util.write_pickle(gdict.token2id, out_path + "-index.pkl")

    print("Generating word co-occurrences...")
    cooccurgen.run(
        word_gen(filename, gdict, subreddit),
        gdict.token2id,
        4,
        out_path + "counts.bin",
    )
    print("Generating PPMI vectors...")
    ppmigen.run(out_path +"-index.pkl", out_path + "counts.bin", out_path + "ppmi", cds=True)
    print("Generating SVD vectors...")
    makelowdim.run(out_path +"-index.pkl", out_path + "ppmi.bin", out_path + "vecs")


if __name__ == "__main__":
    parser = ArgumentParser("Make subreddit word vectors")
    parser.add_argument("filename")
    parser.add_argument("subreddit")
    args = parser.parse_args()
    main(args.filename, args.subreddit)
