import logging
import requests
from bs4 import BeautifulSoup
from six.moves.urllib import parse as urlparse

from components.utils import coerce_url


class FeedFinder(object):

    def __init__(self, user_agent=None, timeout=None):
        if user_agent is None:
            user_agent = "feedfinder2"
        self.user_agent = user_agent
        self.timeout = timeout

    def get_feed(self, url):
        try:
            r = requests.get(url, headers={"User-Agent": self.user_agent}, timeout=self.timeout)
        except Exception as e:
            logging.warning("Error while getting '{0}'".format(url))
            logging.warning("{0}".format(e))
            return None
        return r.text

    def is_feed_data(self, text):
        data = text.lower()
        if data.count("<html"):
            return False
        return data.count("<rss")+data.count("<rdf")+data.count("<feed")

    def is_feed(self, url):
        text = self.get_feed(url)
        if text is None:
            return False
        return self.is_feed_data(text)

    def is_feed_url(self, url):
        return any(
            map(
                url.lower().endswith,
                [".rss", ".rdf", ".xml", ".atom"]
            )
        )

    def is_feedlike_url(self, url):
        return any(
            map(
                url.lower().count,
                ["rss", "rdf", "xml", "atom", "feed"]
            )
        )

    def sort_urls(self, feeds):
        return sorted(list(set(feeds)), key=self.url_feed_prob, reverse=True)

    def url_feed_prob(self, url):
        if "comments" in url:
            return -2
        if "georss" in url:
            return -1
        keywords = ["atom", "rss", "rdf", ".xml", "feed"]
        for p, t in zip(range(len(keywords), 0, -1), keywords):
            if t in url:
                return p
        return 0

    def find_feeds(self, url, check_all=False):
        # Format the URL properly.
        url = coerce_url(url)

        # Download the requested URL.
        text = self.get_feed(url)
        if text is None:
            return []

        # Check if it is already a feed.
        if self.is_feed_data(text):
            return [url]

        # Look for <link> tags.
        logging.info("Looking for <link> tags.")
        tree = BeautifulSoup(text, "html.parser")
        links = []
        for link in tree.find_all("link"):
            if link.get("type") in ["application/rss+xml",
                                    "text/xml",
                                    "application/atom+xml",
                                    "application/x.atom+xml",
                                    "application/x-atom+xml"]:
                links.append(urlparse.urljoin(url, link.get("href", "")))

        # Check the detected links.
        urls = list(filter(self.is_feed, links))
        logging.info("Found {0} feed <link> tags.".format(len(urls)))
        if urls and not check_all:
            return self.sort_urls(urls)

        # Look for <a> tags.
        logging.info("Looking for <a> tags.")
        local, remote = [], []
        for a in tree.find_all("a"):
            href = a.get("href", None)
            if href is None:
                continue
            if "://" not in href and self.is_feed_url(href):
                local.append(href)
            if self.is_feedlike_url(href):
                remote.append(href)

        # Check the local URLs.
        local = [urlparse.urljoin(url, l) for l in local]
        urls += list(filter(self.is_feed, local))
        logging.info("Found {0} local <a> links to feeds.".format(len(urls)))
        if urls and not check_all:
            return self.sort_urls(urls)

        # Check the remote URLs.
        remote = [urlparse.urljoin(url, l) for l in remote]
        urls += list(filter(self.is_feed, remote))
        logging.info("Found {0} remote <a> links to feeds.".format(len(urls)))
        if urls and not check_all:
            return self.sort_urls(urls)

        # Guessing potential URLs.
        fns = ["atom.xml", "index.atom", "index.rdf", "rss.xml", "index.xml",
               "index.rss"]
        urls += list(
            filter(
                self.is_feed,
                [urlparse.urljoin(url, f) for f in fns]
            )
        )
        return self.sort_urls(urls)
