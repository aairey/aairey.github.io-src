#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = u'Andy Airey'
SITENAME = u'blog.airey.be'
SITEURL = 'http://localhost:8000'
RELATIVE_URLS = True

PATH = 'content'

TIMEZONE = 'Europe/Brussels'

DEFAULT_LANG = u'en'

THEME = "./pelican-themes/Flex"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('TowerLAN', 'http://www.towerlan.be/'),)

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/a_airey'),
          ('linkedin', 'https://be.linkedin.com/in/andyairey'),
          ('google', 'https://plus.google.com/u/0/+AndyAirey'),
          ('github', 'https://github.com/aairey'),
	  ('rss', 'https://blog.airey.be/feeds/all.atom.xml'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True


# Flex theme settings
SITETITLE = AUTHOR
SITESUBTITLE = u'sysadmin'
SITEDESCRIPTION = u'%s\'s Thoughts and Writings' % AUTHOR
SITELOGO = u'//en.gravatar.com/userimage/33572940/d1226e18865ebdb31edc84661c5abaa3.jpeg'
FAVICON = SITEURL + '/images/favicon.ico'
BROWSER_COLOR = '#333333'
PYGMENTS_STYLE = 'native'

USE_FOLDER_AS_CATEGORY = True
MAIN_MENU = True

MENUITEMS = (('Archives', '/archives.html'),
	     ('Categories', '/categories.html'),
             ('Tags', '/tags.html'),)

COPYRIGHT_YEAR = 2018

# plugins
PLUGIN_PATHS = ['./pelican-plugins']
PLUGINS = ['sitemap', 'disqus_static']

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.6,
        'indexes': 0.6,
        'pages': 0.5,
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly',
    }
}

TYPOGRIFY = True

DISQUS_SITENAME = u'aaireygithubio'
DISQUS_SECRET_KEY = os.environ.get('DISQUS_SECRET_KEY')
DISQUS_PUBLIC_KEY = os.environ.get('DISQUS_PUBLIC_KEY')

# custom solarized CSS
# tell pelican where your solarized-dark.css file is in your content folder
STATIC_PATHS = ['images', 'extras/solarized-dark.css', 'extras/CNAME']

# tell pelican where it should copy that file to in your output folder
EXTRA_PATH_METADATA = {
'extras/solarized-dark.css': {'path': 'static/solarized-dark.css'},
'extras/CNAME': {'path': 'CNAME'},
}

# tell the pelican-bootstrap-3 theme where to find the solarized-dark.css file in your output folder
CUSTOM_CSS = 'static/solarized-dark.css'

