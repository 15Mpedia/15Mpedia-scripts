#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 emijrp
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import pywikibot

def main():
    monthname = {1:'enero', 2:'febrero', 3:'marzo', 4:'abril', 5:'mayo', 6:'junio', 7:'julio', 8:'agosto', 9:'septiembre', 10:'octubre', 11:'noviembre', 12:'diciembre'}
    
    site = pywikibot.Site('15mpedia', '15mpedia')
    for year in range(2010, 2016):
        for month in range(1, 13):
            page = pywikibot.Page(site, u'Lista de manifestaciones en %s de %d' % (monthname[month], year))
            page.text = u'{{Lista de manifestaciones por mes|mes=%d-%02d}}' % (year, month)
            page.save(u'BOT - Creando lista de manifestaciones por mes')
            
            cat = pywikibot.Page(site, u'Categoría:Manifestaciones en %s de %d' % (monthname[month], year))
            cat.text = u"""{{navegación por mes y tema categoría|tema=Manifestaciones|mes=%d-%02d}}
{{main|Lista de manifestaciones en %s de %d}}

[[Categoría:Manifestaciones en %d| %d-%02d]]""" % (year, month, monthname[month], year, year, year, month)
            cat.save(u'BOT - Creando categoría de manifestaciones por mes')

if __name__ == '__main__':
    main()
