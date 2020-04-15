from socialsent.reddit import subreddit_run, subredditgen
from socialsent import constants
from argparse import ArgumentParser

def compute_polarities(subreddit, scores_interval=None):
    constants.scores_interval = scores_interval
    subredditgen.main(subreddit)
    subreddit_run.main(subreddit)


if __name__ == "__main__":
    parser = ArgumentParser("Compute Polarities")
    parser.add_argument("subreddits", nargs="+", help="the subreddits to compute the polarities for")
    args = parser.parse_args()
    for subreddit in args.subreddits:
        print('\n \n Working on subreddit {}'.format(subreddit))
        compute_polarities(subreddit)
