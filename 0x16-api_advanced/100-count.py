import requests

def count_words(subreddit, word_list, after=None, word_count={}):
    """Query the Reddit API, parse titles of hot articles, and count given keywords."""
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {
        "User-Agent": "esw1229/0.0.1 (by /u/hayweezybaby)"
    }
    params = {"limit": 100, "after": after}
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)
    
    if response.status_code == 200:
        data = response.json().get("data", {})
        children = data.get("children", [])
        
        for child in children:
            title = child["data"]["title"].lower()
            for word in word_list:
                if title.count(f" {word.lower()} ") > 0:  # Check for exact word match with spaces
                    word_count[word.lower()] = word_count.get(word.lower(), 0) + title.count(f" {word.lower()} ")
        
        after = data.get("after")
        if after:
            count_words(subreddit, word_list, after, word_count)
        else:
            sorted_counts = sorted(word_count.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_counts:
                print(f"{word}: {count}")
