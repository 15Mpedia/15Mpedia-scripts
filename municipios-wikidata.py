#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2018 emijrp <emijrp@gmail.com>
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

import urllib.parse
import urllib.request
import pywikibot
import pywikibot.pagegenerators as pagegenerators
import re

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
    skip = 'Cerezal de Peñahorcada'
    
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
            if re.search(r"(?im){{wikidata", wtext):
                print("Ya tiene Wikidata")
                continue
            
            m = re.findall(r"(?im){{wikipedia\|es\|([^{}]+?)}}", wtext)
            if m:
                munititle = m[0]
                url = 'https://es.wikipedia.org/w/index.php?title=%s&redirect=yes' % (urllib.parse.quote(munititle))
                raw = getURL(url=url)
                n = re.findall(r'(?im)<li id="t-wikibase"><a href="https://www.wikidata.org/wiki/Special:EntityPage/(Q\d+)"', raw)
                if n:
                    wikidataid = n[0]
                    newtext = wtext
                    newtext = newtext.replace("{{wikipedia|es|%s}}" % (munititle), """{{wikipedia|es|%s}}
* {{wikidata|%s}}""" % (munititle, wikidataid))
                    if wtext != newtext:
                        pywikibot.showDiff(wtext, newtext)
                        page.text = newtext
                        page.save("BOT - Añadiendo enlace a Wikidata", botflag=True)
                else:
                    print("No se encontro Wikidata ID")
            else:
                print("Plantilla {{wikipedia}} no encontrada")

if __name__ == '__main__':
    main()
