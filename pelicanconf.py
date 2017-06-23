#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'vene'
SITENAME = u"Vlad Niculae (~vene)"
SITEURL = 'http://vene.ro'

TIMEZONE = 'Europe/Paris'
LOCALE = ('en_GB',)
DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_RSS = 'feed/all.rss.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = None

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


# Evil tracking
GOOGLE_ANALYTICS = None  # 'UA-47024389-1'
DISQUS_SITENAME = 'vene'

# IPython Notebook plugin
MARKUP = ('md', 'ipynb')
PLUGIN_PATH = './plugins'
PLUGINS = ['pelican-ipynb']
