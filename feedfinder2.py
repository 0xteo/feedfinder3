#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

try:
    __FEEDFINDER2_SETUP__
except NameError:
    __FEEDFINDER2_SETUP__ = False

if not __FEEDFINDER2_SETUP__:
    __all__ = ["find_feeds"]

    from components.finders import (
        FeedFinder,
    )



def find_feeds(url, check_all=False, user_agent=None, timeout=None):
    finder = FeedFinder(user_agent=user_agent, timeout=timeout)
    return finder.find_feeds(url, check_all)


if __name__ == "__main__":
    print(find_feeds("www.preposterousuniverse.com/blog/", timeout=1))
    print(find_feeds("www.preposterousuniverse.com/blog/"))
    print(find_feeds("http://xkcd.com"))
    print(find_feeds("dan.iel.fm/atom.xml"))
    print(find_feeds("dan.iel.fm", check_all=True))
    print(find_feeds("kapadia.github.io"))
    print(find_feeds("blog.jonathansick.ca"))
    print(find_feeds("asdasd"))
