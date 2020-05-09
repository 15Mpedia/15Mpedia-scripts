#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2019-2020 emijrp <emijrp@gmail.com>
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
import time
import sys
import urllib.parse
import urllib.request
import pywikibot
import pywikibot.pagegenerators as pagegenerators

def getURL(url=''):
    raw = ''
    req = urllib.request.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    try:
        raw = urllib.request.urlopen(req, timeout=15).read().strip().decode('utf-8')
    except:
        pass
    return raw

def main():
    site = pywikibot.Site('15mpedia', '15mpedia')
    catnames = [
        'Categoría:Municipios de España', 
    ]
    start = ''
    skip = ''
    
    for catname in catnames:
        category = pywikibot.Category(site, catname)
        gen = pagegenerators.CategorizedPageGenerator(category=category, start=start, namespaces=[0])
        pre = pagegenerators.PreloadingGenerator(gen, pageNumber=50)
        
        for page in pre:
            if not page.exists() or page.isRedirectPage():
                continue
            wtext = page.text
            wtitle = page.title()
            
            if skip:
                if skip == wtitle:
                    skip = ''
                else:
                    print("Skiping", wtitle)
                    continue
            
            if not re.search(r'{{Infobox Municipio', wtext):
                continue
            print('\n== %s ==' % (wtitle))
            if '(' in wtitle or '/' in wtitle or ',' in wtitle:
                print("Skip title")
                continue
            
            url = 'https://15mpedia.org/wiki/' + page.title(as_url=True)
            raw = ''
            print(url)
            try:
                raw = getURL(url=url)
            except:
                time.sleep(30)
                raw = getURL(url=url)
            if not raw:
                print("ERROR retrieving page")
                continue
            
            represaliadosnum = len(re.findall(r'(?im)Represaliad[oa] por el franquismo, fusilad[oa]', raw))
            print(represaliadosnum, 'represaliados')
            if represaliadosnum >= 5:
                page2 = pywikibot.Page(site, "Lista de personas fusiladas por el franquismo en %s" % (wtitle))
                if not page2.exists():
                    page2.text = "{{Lista de personas fusiladas por el franquismo por lugar de fallecimiento|lugar de fallecimiento=%s}}" % (wtitle)
                    print(page2.title())
                    print(page2.text)
                    page2.save("BOT - Creando lista", botflag=True)
                page3 = pywikibot.Page(site, "Lista de personas de %s fusiladas por el franquismo" % (wtitle))
                if not page3.exists():
                    page3.text = "{{Lista de personas fusiladas por el franquismo por lugar de nacimiento|municipio=%s}}" % (wtitle)
                    print(page3.title())
                    print(page3.text)
                    page3.save("BOT - Creando lista", botflag=True)
                    page3red = pywikibot.Page(site, "Fusilados de %s" % (wtitle))
                    if not page3red.exists():
                        page3red.text = "#REDIRECT [[%s]]" % (page3.title())
                        page3red.save("BOT - Creando redirección hacia [[%s]]" % (page3.title()), botflag=True)
            
            #print(raw)
            time.sleep(1)
    
if __name__ == '__main__':
    main()
