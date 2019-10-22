try:
    import requests

    HAS_REQUESTS = True
except ModuleNotFoundError:
    HAS_REQUESTS = False


class Tip:
    def __init__(self, text=None, url=None):
        self.text = text
        self.url = url

    def get_url(self):
        self.html = requests.get(self.url).content.decode("utf-8")

    def _repr_html_(self):
        return self.html

class TextTip(Tip):
    pass

class TwitterTip(Tip):
        def __init__(self, tweet_id):
            super().__init__()
            self.tweet_id  = tweet_id
        def get_html(self):
            url = f'https://publish.twitter.com/?query=https%3A%2F%2Ftwitter.com%2Fdovpanda%2Fstatus%2F{self.tweet_id}&widget=Tweet'
            self.html = requests.get(url).content.decode("utf-8")


Tip('abc','https://twitter.com/justmarkham/status/1168930165658914816')
TwitterTip('1168930165658914816')