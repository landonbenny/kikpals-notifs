#!/usr/bin/python3
import re
import requests
from time import sleep

PUSH_URL = "https://api.pushshift.io/reddit/search/submission/"
PUSH_SUBMISSIONS = "?author={}&size=100"
PUSH_SUBREDDIT = "?subreddit={}&size=5"

#
# Return true if the user has made any NSFW posts 
#
def is_naughty(post_history):
    return any([post['over_18'] == True for post in post_history])

#
# Filter for only NSFW posts
#
def find_naughty(posts_lst):
    naughty = []
    for post in posts_lst:
        author = post['author']
        history = get_history(author)
        if is_naughty(history):
            naughty.append(post)
    return naughty

def get_ids(posts_lst):
    return [post['id'] for post in posts_lst]

#
# Get the post history of a user
#
def get_history(user):
    r = requests.get(PUSH_URL + PUSH_SUBMISSIONS.format(user))
    return r.json()['data']

#
# Get new posts from a subreddit
#
def get_new(sub="kikpals"):
    r = requests.get(PUSH_URL + PUSH_SUBREDDIT.format(sub))
    return r.json()['data']

#
# Parse a post's title to find age, location, M4F/F4M, etc.
#
def parse_title(title):
    # \d\d\s?\[(M|G|F|R)4(M|G|F|R)\]
    expr = '(\d+) ?\[(\w)4(\w)\] ?(.*)'
    age, gen_poster, gen_seeked, title = re.search(expr, title).groups()
    return {'age': age, 'gen_poster': gen_poster, 'gen_seeked': gen_seeked, 'title': title}


def main():
    posts = get_new(sub='kikpals')
    naughty = find_naughty(posts)
    if len(naughty) > 0:
        for post in naughty:
            data = parse_title(post['title'])
            print(data)
    
        

if __name__ == "__main__":
    main()
