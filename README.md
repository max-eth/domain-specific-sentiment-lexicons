# domain-specific-sentiment-lexicons
Updated implementation of SocialSent, a method for generating domain specific sentiment scores proposed in ["Inducing Domain-Specific Sentiment Lexicons from Unlabeled Corpora"](https://arxiv.org/abs/1606.02820) by Hamilton et al. Code adapted from [https://github.com/williamleif/socialsent](https://github.com/williamleif/socialsent) (Ported to Python 3 and simplified). 

## Run SocialSent on Reddit Comments

1. Download comment data from http://files.pushshift.io/reddit/comments/ in zst format and save under 	 `filename.zst`
2. Extract only the posts of the subreddits of interest by running
	```
    python filter.py filenmame.zst subreddit1 subreddit2 ...
    ```
3. run 	
	```
	python -m subreddit1 subreddit2 ...
	```
	The polarity scores will be saved under `data/subreddit_name/stemmed-polarities.pkl`
## Analysis
In this [notebook]() we apply the method on data from various subreddits and perform some analysis that is beyond the scope of the paper.  
