from gensim.utils import simple_preprocess
from gensim.corpora import Dictionary
from socialsent import util
from argparse import ArgumentParser
from socialsent.representations import ppmigen, cooccurgen, makelowdim
import json
from tqdm import tqdm
import os

from socialsent.constants import DATA_DIR, DICTS, OUTPUTS, NO_ABOVE_1, NO_BELOW, INDICES, COUNTS, PPMI, VECS, filter_comments, CORPUS, stemming

from string import punctuation
translator = str.maketrans('','',punctuation) 
from nltk.corpus import stopwords
stoplist = set(stopwords.words('english'))
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer('english')

def normalize_text(doc):
    "Input doc and return clean list of tokens"
    doc = doc.replace('\r', ' ').replace('\n', ' ')
    lower = doc.lower() # all lower case
    nopunc = lower.translate(translator) # remove punctuation
    words = nopunc.split() # split into tokens
    nostop = [w for w in words if w not in stoplist and not w.isdigit()] # remove stopwords
    if stemming:
        stemmed = [stemmer.stem(w) for w in nostop] # stem each word
        return stemmed
    else:
        return nostop


def word_gen(corpus, gensim_dict, subreddit, num_lines):
    for i, comment in tqdm(enumerate(corpus), total=num_lines):
        for word in comment:
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
    file_corpus = os.path.join(dir_path, CORPUS)

    print("Getting and writing dictionary...")

    with open(file_comments, "r") as f:
       num_lines = sum(1 for line in f)


    with open(file_comments, "r") as f:
       dicts = (json.loads(comment) for comment in tqdm(f, total=num_lines))
       
       corpus = list(
           normalize_text(comment["body"])
           for comment in dicts
           if filter_comments(comment)
       )

       gdict = Dictionary(
           corpus
       )

    gdict.filter_extremes(no_above=NO_ABOVE_1, no_below=NO_BELOW)
    gdict.compactify()


    util.write_pickle(gdict.token2id, file_indices)
    util.write_pickle(gdict, file_dicts)
    util.write_pickle(corpus, file_corpus)

    corpus = util.load_pickle(file_corpus)

    print("Generating word co-occurrences...")
    cooccurgen.run(
       word_gen(corpus, gdict, subreddit, num_lines),
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
    parser.add_argument("subreddit")
    args = parser.parse_args()
    main(args.subreddit)
