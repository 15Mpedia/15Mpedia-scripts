#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2015-2023 emijrp <emijrp@gmail.com>
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

import datetime
import pywikibot

def main():
    overwrite = False
    currentyear = datetime.datetime.now().year
    #for year in range(1780, currentyear+1):
    #for year in range(2020, 2029+1):
    for year in range(1, 2100):
        #[[1950]]
        infobox = u"""{{Infobox Año
|año=%s
}}""" % (year)
        page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), u'%s' % (year))
        if not page.exists():
            page.text = infobox
            page.save(u'BOT - Creando año', botflag=True)
        redirects = [
            u'%s (año)' % (year), 
            u'Año %s' % (year), 
        ]
        redoutput = u"#REDIRECT [[%s]]" % (year)
        for red in redirects:
            redp = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), red)
            if not redp.exists():
                redp.text = redoutput
                redp.save(u"BOT - Creando redirección")
        
        #number disambig
        page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), u'%s (desambiguación)' % (year))
        if not page.exists():
            page.text = u"{{desambiguación número}}"
            page.save(u'BOT - Creando página de desambiguación', botflag=True)
        
        """
        #[[Categoría:1950]]
        infobox = u'{{navegación por año categoría|año=%s}}' % (year)
        page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), u'Categoría:%s' % (year))
        if not page.exists():
            page.text = infobox
            page.save(u'BOT - Creando categoría de año', botflag=True)
        
        if year >= currentyear:
            continue
        
        if year < 1800:
            continue
        
        #[[Categoría:Crímenes del capitalismo en 1950]]
        infobox = u'{{Categoría crímenes del capitalismo por año|año=%s}}' % (year)
        page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), u'Categoría:Crímenes del capitalismo en %s' % (year))
        if not page.exists():
            page.text = infobox
            page.save(u'BOT - Creando categoría de año', botflag=True)
        
        
        
        #[[Categoría:Personas fallecidas en 1950]]
        infobox = u'{{Categoría personas fallecidas por año|año=%s}}' % (year)
        page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), u'Categoría:Personas fallecidas en %s' % (year))
        if not page.exists() or overwrite:
            page.text = infobox
            page.save(u'BOT - Creando categoría de fallecimientos por año', botflag=True)
        
        if year >= 2000:
            continue
        
        #[[Categoría:Personas nacidas en 1950]]
        infobox = u'{{Categoría personas nacidas por año|año=%s}}' % (year)
        page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), u'Categoría:Personas nacidas en %s' % (year))
        if not page.exists() or overwrite:
            page.text = infobox
            page.save(u'BOT - Creando categoría de nacimientos por año', botflag=True)
        """

if __name__ == '__main__':
    main()

