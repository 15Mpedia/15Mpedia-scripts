#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2023 emijrp <emijrp@gmail.com>
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
import unicodedata

def removeaccute(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def getURL(url=''):
    raw = ''
    req = urllib.request.Request(url, headers={ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0' })
    try:
        raw = urllib.request.urlopen(req).read().strip().decode('utf-8')
    except:
        try:
            raw = urllib.request.urlopen(req).read().strip().decode('latin-1')
        except:
            sleep = 10 # seconds
            maxsleep = 0
            while sleep <= maxsleep:
                print('Error while retrieving: %s' % (url))
                print('Retry in %s seconds...' % (sleep))
                time.sleep(sleep)
                try:
                    raw = urllib.request.urlopen(req).read().strip().decode('utf-8')
                except:
                    pass
                sleep = sleep * 2
    return raw

def main():
    site = pywikibot.Site('15mpedia', '15mpedia')
    catnames = [
        #'Categoría:Personas fusiladas por el franquismo', #cuidado, diferenciar con fechas si es la persona
        #'Categoría:Personas deportadas al Campo de concentración de Mauthausen', 
        'Categoría:Personas deportadas por el nazismo', 
    ]
    f = open('duckduckgo.error', 'r')
    log = f.read()
    f.close()
    start = '!'
    start = 'Almoza'
    delay = 3
    cache = {}
    for catname in catnames:
        category = pywikibot.Category(site, catname)
        gen = pagegenerators.CategorizedPageGenerator(category=category, start=start, namespaces=[0])
        pre = pagegenerators.PreloadingGenerator(gen, pageNumber=250)
        
        for page in pre:
            if not page.exists() or page.isRedirectPage():
                continue
            wtext = page.text
            newtext = wtext
            wtitle = page.title()
            if not re.search(r'{{Infobox Persona', wtext):
                continue
            print('\n== %s ==' % (wtitle))
            """
            if wtitle in log:
                print('Ya en el log')
                continue"""
            
            nombre = ""
            primerapellido = ""
            segundoapellido = ""
            try:
                nombre = re.findall(r'(?im)\|nombre=([^\|]*)', wtext)[0].strip()
                primerapellido = re.findall(r'(?im)\|primer apellido=([^\|]*)', wtext)[0].strip()
                segundoapellido = re.findall(r'(?im)\|segundo apellido=([^\|]*)', wtext)[0].strip()
                apellidos = '%s %s' % (primerapellido, segundoapellido)
                apellidos = apellidos.strip()
                nombreapellidos = nombre + " " + apellidos
                apellidosnombre = apellidos + " " + nombre
                apellidoscomanombre = apellidos + ", " + nombre
                apellidoscomanombreentrecomillas = '"' + apellidos + ", " + nombre + '"'
            except:
                print("Error al parsear nombre o apellidos")
                continue
            
            bbdd = [
                #de momento solo editamos deportados, buscando en bbdd de deportados
                
                ["banc de la memoria id", "banc.memoria.gencat.cat", r'(?im)https?://banc\.memoria\.gencat\.cat/(?:ca|es)?/?results/deportats/(\d+)'], 
                ["barcelonins deportats id", "barceloninsdeportats.org", r'(?im)https?://barceloninsdeportats\.org/(?:ca|es)?/?(\d+/[^\.]+?)\.html'], 
                #["censo de represaliados de la ugt id", "censorepresaliadosugt.es", r'(?im)https?://censorepresaliadosugt\.es/s/public/item/(\d+)'], 
                ["fallecidos en los campos nazis id", "fallecidosenloscamposnazis.org", r'(?im)https?://fallecidosenloscamposnazis\.org/(?:ca|es)?/?(\d+/[^\.]+?)\.html'], 
                #Maria Alonso Alonso no es la misma["ihrworld id", "scwd.ihr.world", r'(?im)https?://scwd\.ihr\.world/es/document/(\d+)'], 
            ]
            
            for wikiid, bd, linkregexp in bbdd:
                if re.search(r'(?im)%s' % (wikiid), wtext):
                    print('Ya tiene el ID', wikiid)
                    continue
                
                busqueda = apellidoscomanombreentrecomillas
                #busqueda = apellidoscomanombreentrecomillas + " site:" + bd
                url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote_plus(busqueda)
                raw = ""
                cached = False
                if url in cache.keys():
                    print("Cached url...", url)
                    raw = cache[url]
                    cached = True
                else:
                    print("Retrieving url...", url)
                    raw = getURL(url=url)
                    cache[url] = raw
                if '<div class="no-results">' in raw:
                    print("Sin resultados")
                    time.sleep(cached and 0.1 or delay)
                    continue
                
                splits = raw.split('<h2 class="result__title">')[1:]
                for split in splits:
                    #print(split)
                    wtext = page.text
                    newtext = wtext
                    if re.search(r'(?im)%s' % (wikiid), newtext): #necesario comprobar en cada bucle split por si lo añadio antes
                        #print('Ya tiene el ID', wikiid)
                        continue
                    m = re.findall(r'(?im)<a rel="nofollow" class="result__a" href="([^"]+?)">[^<>]*?</a>', split)
                    if m and len(m) == 1:
                        munquote = urllib.parse.unquote_plus(m[0]).split('uddg=')[1].split('&amp;rut=')[0]
                        m = re.findall(linkregexp, munquote)
                        if m and len(m) == 1:
                            bdid = m[0]
                            print(munquote)
                            n1 = re.findall(r"(?im)%s" % (nombreapellidos), split)
                            n2 = re.findall(r"(?im)%s" % (apellidoscomanombre), split)
                            if (n1 and len(n1) >= 1) or (n2 and len(n2) >= 1):
                                print(m)
                                print(n1)
                                print(n2)
                                print('Añadiendo ID %s %s al artículo' % (wikiid, bdid))
                                newtext = re.sub(r"(?im)({{Infobox Persona)", r"\1\n|%s=%s" % (wikiid, bdid), newtext)
                                
                                if wtext != newtext:
                                    pywikibot.showDiff(wtext, newtext)
                                    page.text = newtext
                                    page.save('BOT - Añadiendo enlace a [[%s]]' % (bd), botflag=True)
                time.sleep(cached and 0.1 or delay)
            #print(raw)
            time.sleep(1)
    
if __name__ == '__main__':
    main()

