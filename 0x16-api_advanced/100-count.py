#!/usr/bin/python3
""" Count it! """
from requests import get
import requests

def count_words(subreddit, word_list, counts=None):
    if not counts:
        counts = {}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Invalid subreddit or no posts match.")
        return
    data = response.json()
    for post in data['data']['children']:
        title = post['data']['title'].lower()
        for word in word_list:
            if word.lower() in title:
                if word in counts:
                    counts[word] += 1
                elif word.title() in counts:
                    counts[word.title()] += 1
                elif word.upper() in counts:
                    counts[word.upper()] += 1
                else:
                    counts[word] = 1
    if data['data']['after']:
        return count_words(subreddit, word_list, counts)
    sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    for word, count in sorted_counts:
        print(f"{word}: {count}")

