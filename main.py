import requests
from time import sleep

PUSH_URL = "https://api.pushshift.io/reddit/search/submission/"
PUSH_SUBMISSIONS = "?author={}&size=100"
PUSH_SUBREDDIT = "?subreddit={}&size=5"


def is_naughty(post_history):
    return any([post['over_18'] == True for post in post_history])


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


def get_history(user):
    r = requests.get(PUSH_URL + PUSH_SUBMISSIONS.format(user))
    return r.json()['data']

def get_new(sub="kikpals"):
    r = requests.get(PUSH_URL + PUSH_SUBREDDIT.format(sub))
    return r.json()['data']


def parse_title(title):
    # \d\d\s?\[(M|G|F|R)4(M|G|F|R)\]
    pass


def main():
    posts = get_new(sub='kikpals')
    naughty = find_naughty(posts)
    if len(naughty) > 0:
        for post in naughty:
            print(post['title'] + ' || ' + post['author'])
    
        

if __name__ == "__main__":
    main()