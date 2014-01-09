#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Vlad Niculae'
SITENAME = u"Vlad Niculae (~vene)"
SITEURL = ''

TIMEZONE = 'Europe/Paris'
LOCALE = ('en_GB',)
DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = None

# Social widget
#SOCIAL = (('You can add links in your config file', '#'),
#          ('Another social link', '#'),)

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
DIRECT_TEMPLATES = ('blog',)
PAGINATED_DIRECT_TEMPLATES = ('index', 'blog')
TYPOGRIFY = True
ARTICLE_DIR = 'blog'
ARTICLE_URL = 'blog/{slug}.html'
ARTICLE_SAVE_AS = ARTICLE_URL
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = PAGE_URL
CATEGORY_URL = 'blog/category/{slug}.html'
CATEGORY_SAVE_AS = 'blog/category/{slug}.html'
TAG_URL = 'blog/tag/{slug}.html'
TAG_SAVE_AS = 'blog/tag/{slug}.html'
AUTHOR_URL = 'blog/author/{slug}.html'
AUTHOR_SAVE_AS = 'blog/author/{slug}.html'
BLOG_SAVE_AS = 'blog/index.html'

DISPLAY_CATEGORIES_ON_MENU = False
MENUITEMS = (('Publications', '/publications.html'),
             ('Blog', SITEURL + '/blog/'))

THEME = 'themes/vene'

STATIC_PATHS = ['papers',
                'talks',
                'extras/favicon.ico',
                'extras/README.rst',
                'extras/CNAME']

EXTRA_PATH_METADATA = {'extras/favicon.ico': {'path': 'favicon.ico'},
                       'extras/README.rst': {'path': 'README.rst'},
                       'extras/CNAME': {'path': 'CNAME'}}
