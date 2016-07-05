#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Andy Airey'
SITENAME = u'aairey.github.io'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Brussels'

DEFAULT_LANG = u'en'

THEME = "/home/andy/pelican-themes/flex"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Utopit', 'http://www.utopit.be/'),)

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/a_airey'),
          ('linkedin', 'https://be.linkedin.com/in/andyairey'),
          ('google', 'https://plus.google.com/u/0/+AndyAire'),
          ('github', 'https://github.com/aairey'),
	  ('rss', 'http://aairey.github.io/feeds/all.atom.xml'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True


# Flex theme settings
SITETITLE = AUTHOR
SITESUBTITLE = u'System Engineer'
SITEDESCRIPTION = u'%s\'s Thoughts and Writings' % AUTHOR
SITELOGO = u'//en.gravatar.com/userimage/33572940/d1226e18865ebdb31edc84661c5abaa3.jpeg'
FAVICON = SITEURL + '/images/favicon.ico'
BROWSER_COLOR = '#333333'
PYGMENTS_STYLE = 'monokai'

USE_FOLDER_AS_CATEGORY = True
MAIN_MENU = True

MENUITEMS = (('Archives', '/archives.html'),
	     ('Categories', '/categories.html'),
             ('Tags', '/tags.html'),)

COPYRIGHT_YEAR = 2016

# plugins
PLUGIN_PATHS = ['/home/andy/pelican-plugins']
PLUGINS = ['gravatar', 'sitemap']

AUTHOR_EMAIL = 'airey.andy@gmail.com'

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
