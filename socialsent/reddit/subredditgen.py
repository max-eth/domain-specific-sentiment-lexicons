from gensim.utils import simple_preprocess
from gensim.corpora import Dictionary
from socialsent import util
from argparse import ArgumentParser
from socialsent.representations import ppmigen, cooccurgen, makelowdim
import json
from tqdm import tqdm
import os


from socialsent.constants import DATA_DIR, DICTS, OUTPUTS, NO_ABOVE, NO_BELOW, INDICES, COUNTS, PPMI, VECS


def word_gen(filename, gensim_dict, subreddit, num_lines):

    for i, line in tqdm(enumerate(open(filename)), total=num_lines):
        comment = json.loads(line)
        if comment["score"] <= 0 or comment["subreddit"] != subreddit:
            continue

        for word in simple_preprocess(comment["body"]):
            word = word.lower()
            if word in gensim_dict.token2id:
                yield word

def main(subreddit):
    dir_path = os.path.join(DATA_DIR, subreddit)
    util.mkdir(dir_path)
    file_comments = os.path.join(dir_path, OUTPUTS)
    file_indices = os.path.join(dir_path, INDICES)
    file_dicts = os.path.join(dir_path, DICTS)
    file_counts = os.path.join(dir_path, COUNTS)
    file_ppmi = os.path.join(dir_path, PPMI)
    file_vecs = os.path.join(dir_path, VECS)

    print("Getting and writing dictionary...")

    with open(file_comments, "r") as f:
       num_lines = sum(1 for line in f)

    with open(file_comments, "r") as f:
       dicts = (json.loads(comment) for comment in tqdm(f, total=num_lines))
       gdict = Dictionary(
           simple_preprocess(comment["body"])
           for comment in dicts
           if comment["score"] > 0 and comment["subreddit"] == subreddit
       )

    gdict.filter_extremes(no_above=NO_ABOVE, no_below=NO_BELOW)
    gdict.compactify()
    util.write_pickle(gdict.token2id, file_indices)
    util.write_pickle(gdict, file_dicts)

    print("Generating word co-occurrences...")
    cooccurgen.run(
       word_gen(file_comments, gdict, subreddit, num_lines),
       gdict.token2id,
       4,
       file_counts
    )
    print("Generating PPMI vectors...")
    ppmigen.run(subreddit, cds=True)
    print("Generating SVD vectors...")
    makelowdim.run(file_indices, file_ppmi, file_vecs)


if __name__ == "__main__":
    parser = ArgumentParser("Make subreddit word vectors")
    parser.add_argument("filename")
    parser.add_argument("subreddit")
    args = parser.parse_args()
    main(args.filename, args.subreddit)
