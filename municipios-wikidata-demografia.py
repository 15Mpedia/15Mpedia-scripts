#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2020-2023 emijrp <emijrp@gmail.com>
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

import json
import urllib2 
import pywikibot
import pywikibot.pagegenerators as pagegenerators
import re
import sys

def logerror(errorline):
    error = open('demografia-municipios.errores', 'a')
    error.write(errorline.encode('utf-8'))
    error.close()

def getURL(url=''):
    raw = ''
    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    try:
        raw = urllib2.urlopen(req).read().strip().decode('utf-8')
    except:
        pass
    return raw

def main():
    site = pywikibot.Site('15mpedia', '15mpedia')
    catnames = [
        u'Categoría:Municipios de España', 
    ]
    start = ''
    skip = ''
    if len(sys.argv) > 1:
        skip = sys.argv[1]
        start = sys.argv[1]
    
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
            
            print(u'\n== %s ==' % (wtitle))
            if not re.search(r'{{Infobox Municipio', wtext):
                print("No tiene infobox municipio")
                continue
            
            """if re.search(r'demografía=', wtext):
                print("Ya tiene demografia")
                continue"""
            
            m = re.findall(r"(?im){{wikidata\|(Q\d+)\}\}", wtext)
            if not m:
                print("No tiene Wikidata")
                continue
            wikidataid = m[0]
            url = "https://www.wikidata.org/wiki/Special:EntityData/%s.json" % (wikidataid)
            wdjson = json.loads(getURL(url=url))
            if "entities" in wdjson and wikidataid in wdjson["entities"] and "claims" in wdjson["entities"][wikidataid]:
                if "P1082" in wdjson["entities"][wikidataid]["claims"]:
                    #print(wdjson["entities"][wikidataid]["claims"]["P1082"])
                    demografia = []
                    demoerror = False
                    for pobdata in wdjson["entities"][wikidataid]["claims"]["P1082"]:
                        if not "datavalue" in pobdata["mainsnak"]: #sin valor Q1606686
                            continue
                        if not "qualifiers" in pobdata:
                            continue
                        pobnum = int(pobdata["mainsnak"]["datavalue"]["value"]["amount"])
                        pobdate = ''
                        if "P585" in pobdata["qualifiers"]:
                            pobdate = pobdata["qualifiers"]["P585"][0]["datavalue"]["value"]["time"]
                            pobdate = pobdate.split('T')[0][1:5]
                        if pobdate in [x for x, y in demografia]:
                            msg = u'\n[[%s]] (%s) tiene poblacion duplicada en %s' % (wtitle, wikidataid, pobdate)
                            print(msg)
                            logerror(msg)
                            demoerror = True
                            continue #saltamos este dato y nos quedamos con el que ya cogimos
                        demografia.append([pobdate, pobnum])
                    demografia.sort()
                    if False and demoerror: #guardar demografia aunque haya duplicados (ya los descartamos con el continue), sino quedan 50 munis sin demografia...
                        continue
                    #print('\n'.join(["%s, %s" % (str(x), str(y)) for x, y in demografia]))
                    demografiaplain = ''.join([u"{{población|total=%s|año=%s}}" % (str(y), str(x)) for x, y in demografia])
                    newtext = wtext
                    if re.search(ur'(?im)demografía=', newtext):
                        newtext = re.sub(ur"(?im){{Población\s*\|\s*total\s*=\s*(\d+)\s*\|\s*año\s*=\s*(\d+)\s*}}", ur"{{Población|total=\1|año=\2}}", newtext)
                        newtext = re.sub(ur"(?im)(demografía=)([^\n\s]+)(\n\|)", ur"\1%s\3" % (demografiaplain), newtext)
                    else:
                        newtext = newtext.replace(u"{{Infobox Municipio", u"{{Infobox Municipio\n|demografía=%s" % (demografiaplain))
                    if wtext != newtext:
                        pywikibot.showDiff(wtext, newtext)
                        page.text = newtext
                        page.save("BOT - Añadiendo datos de población, fuente INE/Wikidata", botflag=True)
                        page.save() #purge atributos
                        #break
            else:
                print("Error leyendo wikidata")

if __name__ == '__main__':
    main()
