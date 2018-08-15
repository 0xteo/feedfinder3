import os
import sys

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

# Hackishly inject a constant into builtins to enable importing of the
# package before the library is built.
if sys.version_info[0] < 3:
    import __builtin__ as builtins
else:
    import builtins
builtins.__FEEDFINDER2_SETUP__ = True
import feedfinder3
from setuptools import setup

setup(
    name="feedfinder3",
    version=feedfinder3.__version__,
    url="https://github.com/TeodorIvanov/feedfinder3",
    license="MIT",
    author="Teodor Ivanov",
    author_email="tdrivanov@gmail.com",
    install_requires=[
        "six",
        "requests",
        "beautifulsoup4",
        "python-dateutil",
        "feedparser",
    ],
    description="Find the feed URLs for a website.",
    long_description=open("README.rst").read(),
    py_modules=["feedfinder3"],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
