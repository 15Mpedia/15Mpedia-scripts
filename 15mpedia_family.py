# -*- coding: utf-8  -*-
"""Family module for 15mpedia wiki."""
from __future__ import unicode_literals

__version__ = '$Id: 8c9856dd7c0af8d400d0d95b00bf406002729008 $'

from pywikibot import family

"""
Este fichero es necesario para correr los bots sobre 15Mpedia 
Hay que guardarlo en el directorio "families" de pywikibot
"""

# The MediaWiki family
# user-config.py: usernames['15mpedia']['15mpedia'] = 'User name'
class Family(family.WikimediaFamily):

    """Family module for 15mpedia wiki."""

    def __init__(self):
        """Constructor."""
        super(Family, self).__init__()
        self.name = '15mpedia'

        self.langs = {
            '15mpedia': 'wiki.15m.cc',
        }

    def protocol(self, code):                                                         
        return 'HTTP'
