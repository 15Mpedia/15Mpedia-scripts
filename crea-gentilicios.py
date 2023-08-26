#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2023 emijrp
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
import sys
import pywikibot
import pywikibot.pagegenerators as pagegenerators

def main():
    eswiki = pywikibot.Site('es', 'wikipedia')
    site = pywikibot.Site('15mpedia', '15mpedia')
    cat = pywikibot.Category(site, u"Category:Municipios de España")
    gen = pagegenerators.CategorizedPageGenerator(cat,start=sys.argv[1])
    pre = pagegenerators.PreloadingGenerator(gen, pageNumber=60)
    
    for page in pre:
        wtitle = page.title()
        wtext = page.get()
        
        print '\n===', wtitle, '==='
        if not re.search(ur"(?im)\{\{\s*Infobox Municipio", wtext):
            print u"Le falta la infobox"
            continue
        
        fs = u""
        ms = u""
        fp = u""
        mp = u""
        try:
            fs = re.findall(ur"(?im)\|gentilicio fs=([^\s]+?)[\n\r]", wtext)[0]
            ms = re.findall(ur"(?im)\|gentilicio ms=([^\s]+?)[\n\r]", wtext)[0]
            fp = re.findall(ur"(?im)\|gentilicio fp=([^\s]+?)[\n\r]", wtext)[0]
            mp = re.findall(ur"(?im)\|gentilicio mp=([^\s]+?)[\n\r]", wtext)[0]
        except:
            continue
        
        output = u"{{desambiguación gentilicio}}"
        redtitle = u""
        reds = []
        if fs == ms:
            redtitle = fs
            reds.append(fp)
            reds.append(mp)
        else:
            redtitle = u"%s, %s" % (fs, ms)
            reds.append(fs)
            reds.append(ms)
            reds.append(fp)
            reds.append(mp)
        
        redpage = pywikibot.Page(site, redtitle)
        if not redpage.exists():
            redpage.text = output
            redpage.save(u"BOT - Creando página")
        
        reds = list(set(reds))
        outputred = u"{{rg|%s}}" % (redtitle)
        for red in reds:
            redpage = pywikibot.Page(site, red)
            if not redpage.exists():
                redpage.text = outputred
                redpage.save(u"BOT - Creando redirección")

if __name__ == '__main__':
    main()
