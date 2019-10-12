#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2019 emijrp <emijrp@gmail.com>
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
        raw = urllib.request.urlopen(req).read().strip().decode('utf-8')
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
            
            url = 'https://15mpedia.org/wiki/' + page.title(as_url=True)
            print(url)
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
                    page2.save("BOT - Creando lista")
            
            #print(raw)
            time.sleep(1)
    
if __name__ == '__main__':
    main()
