import logging
from datetime import datetime
from time import mktime

from dateutil.parser import parse

import feedparser


class FeedValidator(object):

    def __init__(self,
                 url,
                 min_article_count=None,
                 max_day_interval=None,
                 exclude_keywords=None):
        self.url = url
        self.min_article_count = min_article_count
        self.max_day_interval = max_day_interval
        self.exclude_keywords = exclude_keywords

    @property
    def is_valid(self):
        return self.check_feed_is_valid()

    def check_feed_is_valid(self):
        if self.exclude_keywords and \
                self.keywords_in_str(self.url, self.exclude_keywords):
            return False
        parsed_feed = feedparser.parse(self.url)
        if self.max_day_interval:
            feed_updated_at = self.get_feed_last_updated(parsed_feed)
            updated_delta = (datetime.now() - feed_updated_at).days
            if updated_delta > self.max_day_interval:
                logging.warning(
                    'Last feed item is older than max_day_interval.'
                    ' Filtered: {0}'
                    .format(self.url)
                )
                return False

        if self.min_article_count is not None:
            if len(parsed_feed.items()) < self.min_article_count:
                logging.warning(
                    'Feed contains less than {0} articles. Filtered: {1}'
                    .format(self.min_article_count, self.url)
                )
                return False
        return True

    def keywords_in_str(self, test_string, keywords):
        return any(keyword for keyword in keywords if keyword in test_string)

    def get_feed_last_updated(self, feed):

        def feed_datetime(dt):
            return datetime.fromtimestamp(mktime(dt))

        if getattr(feed, 'updated_parsed', None):
            updated = feed.updated_parsed
        elif feed.get('feed') and feed.feed.get('updated_parsed'):
            updated = feed.feed.updated_parsed
        elif feed.entries and getattr(feed.entries[0], 'published_parsed', None):
            updated = feed.entries[0].published_parsed
        elif feed.entries and getattr(feed.entries[0], 'published', None):
            try:
                updated = parse(feed.entries[0].published)
            except:
                updated = parse(feed.entries[0].published.split(',', 1)[1])
        else:
            return
        return feed_datetime(updated)
