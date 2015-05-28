#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 emijrp <emijrp@gmail.com>
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

import pywikibot

def main():
    for year in range(1780, 1996):
        #[[1950]]
        infobox = u"""{{Infobox Año
|año=%s
}}""" % (year)
        page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), u'%s' % (year))
        if not page.exists():
            page.text = infobox
            page.save(u'BOT - Creando año', botflag=True)
        
        #[[Categoría:1950]]
        infobox = u'{{navegación por año categoría|año=%s}}' % (year)
        page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), u'Categoría:%s' % (year))
        if not page.exists():
            page.text = infobox
            page.save(u'BOT - Creando categoría de año', botflag=True)
        
        #[[Categoría:Personas nacidas en 1950]]
        infobox = u"""{{navegación por año y tema categoría|tema=Personas nacidas|año=%s}}
{{main|%s#Nacimientos}}

[[Categoría:Personas por año de nacimiento| %s]]""" % (year, year, year)
        page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), u'Categoría:Personas nacidas en %s' % (year))
        if not page.exists():
            page.text = infobox
            page.save(u'BOT - Creando categoría de nacimientos por año', botflag=True)
        
        #[[Categoría:Personas fallecidas en 1950]]
        infobox = u"""{{navegación por año y tema categoría|tema=Personas fallecidas|año=%s}}
{{main|%s#Fallecimientos}}

[[Categoría:Personas por año de fallecimiento| %s]]""" % (year, year, year)
        page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), u'Categoría:Personas fallecidas en %s' % (year))
        if not page.exists():
            page.text = infobox
            page.save(u'BOT - Creando categoría de fallecimientos por año', botflag=True)
        

if __name__ == '__main__':
    main()

