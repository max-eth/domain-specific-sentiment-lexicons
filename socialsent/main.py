from socialsent.reddit import subreddit_run, subredditgen
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser("Compute Polarities")
    parser.add_argument("subreddits", nargs="+", help="the subreddits to compute the polarities for")
    args = parser.parse_args()
    for subreddit in args.subreddits:
        print('\n \n Working on subreddit {}'.format(subreddit))
        subredditgen.main(subreddit)
        subreddit_run.main(subreddit)
