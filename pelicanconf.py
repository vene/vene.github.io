#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

from defusedxml import ElementTree
import markdown

AUTHOR = 'Vlad'
SITENAME = 'Vlad Niculae'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = 'en'
DATE_FORMATS = {'en': ('en_US.utf8', '%a, %d %b %Y')}
LOCALE=('en_US.utf8', 'en', 'usa')

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = None

# Social widget
#  SOCIAL = (('You can add links in your config file', '#'),
          #  ('Another social link', '#'),)

DEFAULT_PAGINATION = 3

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

TYPOGRIFY = True
TYPOGRIFY_IGNORE_TAGS = [".mathskip"]

THEME = 'themes/vene-tufte'

# Jupyter Notebook plugin
MARKUP = ('md', 'ipynb', 'rst')
from pelican_jupyter import markup as nb_markup
PLUGINS = [nb_markup, "plugins.wrap_math", "plugins.tufte_footnote"]
IPYNB_IGNORE_CSS = True
IPYNB_SKIP_CSS = True

AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
ARTICLE_PATHS = ['blog']
ARTICLE_URL = 'blog/{slug}.html'
ARTICLE_SAVE_AS = ARTICLE_URL
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = PAGE_URL
INDEX_SAVE_AS = 'blog/index.html'
DISPLAY_CATEGORIES_ON_MENU = False
MENUITEMS = (('Papers', 'papers.html'),
             ('Blog', 'blog/'),
             ('Teaching', 'teaching.html'))

STATIC_PATHS = ['papers',
                'talks',
                'figurative-comparisons',
                'betrayal',
                'constructive',
                'images',
                'extras/favicon.ico',
                'extras/vlad-niculae.jpg',
                'extras/README.rst',
                'extras/CNAME']

EXTRA_PATH_METADATA = {
    'extras/favicon.ico': {'path': 'favicon.ico'},
    'extras/README.rst': {'path': 'README.rst'},
    'extras/vlad-niculae.jpg': {'path': 'vlad-niculae.jpg'},
    'extras/CNAME': {'path': 'CNAME'}}
