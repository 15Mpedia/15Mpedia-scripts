#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2020 emijrp <emijrp@gmail.com>
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
import urllib.parse
import urllib.request
import pywikibot
import pywikibot.pagegenerators as pagegenerators
import re
import sys

def logerror(errorline):
    error = open('otrosdatos-municipios.errores', 'a')
    error.write(errorline)
    error.close()

def getURL(url=''):
    raw = ''
    req = urllib.request.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    try:
        raw = urllib.request.urlopen(req).read().strip().decode('utf-8')
    except:
        pass
    return raw

def float2str(d):
    d = str(d)
    d = d.replace('.', '-')
    d = d.replace(',', '.')
    d = d.replace('-', ',')
    d = re.sub(r',0+$', '', d) # remove ,0 & ,00
    d = re.sub(r'(,\d\d)\d+$', r'\1', d) #round 2
    return d

def main():
    site = pywikibot.Site('15mpedia', '15mpedia')
    catnames = [
        'Categoría:Municipios de España', 
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
            
            print('\n== %s ==' % (wtitle))
            if not re.search(r'{{Infobox Municipio', wtext):
                print("No tiene infobox municipio")
                continue
            
            """comentado para lanzarlo una vez y comprobar que todos son municipios de españa o subcategorias
            if re.search(r'\|altitud=\d+', wtext) and re.search(r'\|superficie=\d+', wtext) and re.search(r'\|coordenadas=\d+', wtext):
                print("Ya tiene todos los datos")
                continue
            """
            
            m = re.findall(r"(?im){{wikidata\|(Q\d+)\}\}", wtext)
            if not m:
                print("No tiene Wikidata")
                continue
            wikidataid = m[0]
            url = "https://www.wikidata.org/wiki/Special:EntityData/%s.json" % (wikidataid)
            wdjson = json.loads(getURL(url=url))
            newtext = wtext
            if "entities" in wdjson and wikidataid in wdjson["entities"] and "claims" in wdjson["entities"][wikidataid]:
                esmunicipioespana = False
                if "P31" in wdjson["entities"][wikidataid]["claims"]:
                    for p31 in wdjson["entities"][wikidataid]["claims"]["P31"]:
                        if p31["mainsnak"]["datavalue"]["value"]["id"] in ["Q2074737", "Q2276925", "Q3284867", "Q5055981", "Q33146843", "Q55863584", "Q61763947"]:
                            esmunicipioespana = True
                if not esmunicipioespana:
                    msg = '[[%s]] (%s) no es municipio Espana\n' % (wtitle, wikidataid)
                    print(msg)
                    logerror(msg)
                    continue
                #altitud
                if not re.search(r'\|altitud=\d+', wtext):
                    if "P2044" in wdjson["entities"][wikidataid]["claims"]:
                        p2044 = wdjson["entities"][wikidataid]["claims"]["P2044"]
                        #print(p2044)
                        altitud = ''
                        if len(p2044) != 1:
                            msg = '[[%s]] (%s) error en altitud\n' % (wtitle, wikidataid)
                            print(msg)
                            logerror(msg)
                        else:
                            altitud_ = p2044[0]["mainsnak"]["datavalue"]["value"]["amount"]
                            print(altitud_)
                            altitud = '.' in altitud_ and float2str(float(altitud_)) or int(altitud_)
                            altitudunit = p2044[0]["mainsnak"]["datavalue"]["value"]["unit"]
                            if altitudunit == 'http://www.wikidata.org/entity/Q11573': #metros
                                newtext = newtext.replace("{{Infobox Municipio", """{{Infobox Municipio\n|altitud=%s""" % (altitud))
                            else:
                                msg = '[[%s]] (%s) error en unidad de altitud\n' % (wtitle, wikidataid)
                                print(msg)
                                logerror(msg)
                
                #superficie
                if not re.search(r'\|superficie=\d+', wtext):
                    if "P2046" in wdjson["entities"][wikidataid]["claims"]:
                        p2046 = wdjson["entities"][wikidataid]["claims"]["P2046"]
                        #print(p2046)
                        superficie = ''
                        if len(p2046) != 1:
                            msg = '[[%s]] (%s) error en superficie\n' % (wtitle, wikidataid)
                            print(msg)
                            logerror(msg)
                        else:
                            superficie_ = p2046[0]["mainsnak"]["datavalue"]["value"]["amount"]
                            print(superficie_)
                            superficie = '.' in superficie_ and float2str(float(superficie_)) or int(superficie_)
                            superficieunit = p2046[0]["mainsnak"]["datavalue"]["value"]["unit"]
                            if superficieunit == 'http://www.wikidata.org/entity/Q712226': #km2
                                newtext = newtext.replace("{{Infobox Municipio", """{{Infobox Municipio\n|superficie=%s""" % (superficie))
                            else:
                                msg = '[[%s]] (%s) error en unidad de superficie\n' % (wtitle, wikidataid)
                                print(msg)
                                logerror(msg)
                
                #coordenadas
                if not re.search(r'\|coordenadas=\d+', wtext):
                    if "P625" in wdjson["entities"][wikidataid]["claims"]:
                        p625 = wdjson["entities"][wikidataid]["claims"]["P625"]
                        #print(p625)
                        coordenadas = ''
                        if len(p625) != 1:
                            msg = '[[%s]] (%s) error en coordenadas\n' % (wtitle, wikidataid)
                            print(msg)
                            logerror(msg)
                        else:
                            lat = p625[0]["mainsnak"]["datavalue"]["value"]["latitude"]
                            lon = p625[0]["mainsnak"]["datavalue"]["value"]["longitude"]
                            coordenadas = "%s, %s" % (lat, lon)
                            print(coordenadas)
                            globe = p625[0]["mainsnak"]["datavalue"]["value"]["globe"]
                            if globe == 'http://www.wikidata.org/entity/Q2': #earth
                                newtext = newtext.replace("{{Infobox Municipio", """{{Infobox Municipio\n|coordenadas=%s""" % (coordenadas))
                            else:
                                msg = '[[%s]] (%s) error en globo de coordenadas\n' % (wtitle, wikidataid)
                                print(msg)
                                logerror(msg)
                
                if wtext != newtext and len(newtext) > len(wtext):
                    pywikibot.showDiff(wtext, newtext)
                    page.text = newtext
                    page.save("BOT - Añadiendo datos desde Wikidata", botflag=True)
            else:
                print("Error leyendo wikidata")

if __name__ == '__main__':
    main()
