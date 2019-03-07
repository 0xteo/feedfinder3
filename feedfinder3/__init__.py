#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

__version__ = "0.0.8"

try:
    __FEEDFINDER2_SETUP__
except NameError:
    __FEEDFINDER2_SETUP__ = False

if not __FEEDFINDER2_SETUP__:
    __all__ = ["find_feeds"]
    from feedfinder3.components import FeedFinder, FeedValidator


def find_feeds(url,
               check_all=False,
               user_agent=None,
               timeout=None,
               validate_options=None):
    finder = FeedFinder(user_agent=user_agent, timeout=timeout)
    feeds = finder.find_feeds(url, check_all)
    if validate_options:
        feeds = [
            feed for feed in feeds
            if FeedValidator(feed, **validate_options).is_valid
        ]
    return feeds


if __name__ == "__main__":
    print(find_feeds("www.preposterousuniverse.com/blog/", timeout=1))
    print(find_feeds("www.preposterousuniverse.com/blog/"))
    print(find_feeds("http://xkcd.com",
                     validate_options={
                         'max_day_interval': 1
                     }
                     )
          )
    print(find_feeds("dan.iel.fm/atom.xml"))
    print(find_feeds("dan.iel.fm", check_all=True))
    print(find_feeds("kapadia.github.io"))
    print(find_feeds("blog.jonathansick.ca"))
    print(find_feeds("asdasd"))
