from socialsent.reddit import subreddit_run, subredditgen
from socialsent import constants
from argparse import ArgumentParser


def compute_polarities(subreddit, interval=None, intervals=None, stem=True):

    if interval is not None and intervals is None:
        raise ValueError("specify all intervals")

    constants.set_constants(stem, interval, intervals, False)

    #subredditgen.main(subreddit)
    subreddit_run.main(subreddit)


if __name__ == "__main__":
    parser = ArgumentParser("Compute Polarities")
    parser.add_argument("subreddits", nargs="+", help="the subreddits to compute the polarities for")
    args = parser.parse_args()
    for subreddit in args.subreddits:
        print('\n \n Working on subreddit {}'.format(subreddit))
        compute_polarities(subreddit)
