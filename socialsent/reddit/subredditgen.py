from gensim.utils import simple_preprocess
from gensim.corpora import Dictionary
from socialsent import util
from argparse import ArgumentParser
from socialsent.representations import ppmigen, cooccurgen, makelowdim
import json
from tqdm import tqdm
import os

from socialsent.constants import get_constants, filter_comments, get_interval_idx, get_interval_fname

from string import punctuation
translator = str.maketrans('','',punctuation) 
from nltk.corpus import stopwords
stoplist = set(stopwords.words('english'))
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer('english')

def normalize_text(doc, stemming):
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
    const = get_constants(subreddit)

    if os.path.exists(const['CORPUS']):
        print("Loading preexisting corpus...")
        corpus = util.load_pickle(const['CORPUS'])
    else:
        print("Getting and writing dictionary...")

        with open(const['OUTPUTS'], "r") as f:
            num_lines = sum(1 for line in f)


        with open(const['OUTPUTS'], "r") as f:
            dicts = (json.loads(comment) for comment in tqdm(f, total=num_lines))

            if const["INTERVAL"] is not None:
                corpuses = [[] for interval in const["ALL_INTERVALS"]]

                for comment in dicts:
                    i = get_interval_idx(comment["score"])
                    corpuses[i].append(normalize_text(comment["body"], const['STEMMING']))

                for i, interval in enumerate(const["ALL_INTERVALS"]):
                    util.write_pickle(corpuses[i], get_interval_fname(subreddit, interval))

                corpus = corpuses[0]
                
    gdict = Dictionary(
        corpus
    )

    gdict.filter_extremes(no_above=const['NO_ABOVE_1'], no_below=const['NO_BELOW'])
    gdict.compactify()


    util.write_pickle(gdict.token2id, const['INDICES'])
    util.write_pickle(gdict, const['DICTS'])


    print("Generating word co-occurrences...")
    cooccurgen.run(
       word_gen(corpus, gdict, subreddit, len(corpus)),
       gdict.token2id,
       4,
       const['COUNTS']
    )
    print("Generating PPMI vectors...")
    ppmigen.run(subreddit, cds=True)
    print("Generating SVD vectors...")
    makelowdim.run(const['INDICES'], const['PPMI'], const['VECS'])


if __name__ == "__main__":
    parser = ArgumentParser("Make subreddit word vectors")
    parser.add_argument("subreddit")
    args = parser.parse_args()
    main(args.subreddit)
