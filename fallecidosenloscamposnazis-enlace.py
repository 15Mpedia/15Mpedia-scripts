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
    req = urllib.request.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
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
        #'Categoría:Personas fusiladas por el franquismo', 
        'Categoría:Víctimas del nazismo', 
    ]
    start = 'Alcubierre'
    for catname in catnames:
        category = pywikibot.Category(site, catname)
        gen = pagegenerators.CategorizedPageGenerator(category=category, start=start, namespaces=[0])
        pre = pagegenerators.PreloadingGenerator(gen, pageNumber=50)
        """templatepage = pywikibot.Page(site, template)
        gen = pagegenerators.ReferringPageGenerator(templatepage, followRedirects=True, withTemplateInclusion=True)
        pre = pagegenerators.PreloadingGenerator(gen, pageNumber=50)"""
        
        for page in pre:
            if not page.exists() or page.isRedirectPage():
                continue
            wtext = page.text
            wtitle = page.title()
            if not re.search(r'{{Infobox Persona', wtext):
                continue
            print('\n== %s ==' % (wtitle))
            if re.search(r'(?im)fallecidos en los campos nazis id', wtext):
                print('Ya tiene el ID')
                continue
            
            try:
                nombre = re.findall(r'(?im)\|nombre=([^\|]*)', wtext)[0].strip()
                primerapellido = re.findall(r'(?im)\|primer apellido=([^\|]*)', wtext)[0].strip()
                segundoapellido = re.findall(r'(?im)\|segundo apellido=([^\|]*)', wtext)[0].strip()
                apellidos = '%s %s' % (primerapellido, segundoapellido)
                apellidos = apellidos.strip()
                nombre_ = re.sub(r' ', r'+', nombre)
                apellidos_ = re.sub(r' ', r'+', apellidos)
                fechafallecimiento = re.findall(r'(?im)\|fecha de fallecimiento=(\d\d\d\d/\d\d/\d\d)', wtext)[0].strip()
                fechafallecimiento2 = '%s/%s/%s' % (fechafallecimiento.split('/')[2], fechafallecimiento.split('/')[1], fechafallecimiento.split('/')[0])
            except:
                continue
            
            #print nombre, apellidos
            url = 'https://html.duckduckgo.com/html/?q=%s+%s+%%20site:fallecidosenloscamposnazis.org' % (nombre_, apellidos_)
            raw = getURL(url=url)
            splits = raw.split('<div class="result results_links results_links_deep web-result ">')
            
            for split in splits:
                nombrecompleto = '%s, %s' % (apellidos, nombre)
                nombrecompleto = removeaccute(nombrecompleto)
                if re.search(r'(?im)%s' % (nombrecompleto), split):
                    if re.search(r'(?im)Fecha de la muerte:', split):
                        if re.search(r'(?im)Fecha de la muerte: %s' % (fechafallecimiento2), split):
                            print('La fecha coincide, debe ser la misma persona')
                            bbddid = re.findall(r'<a rel="nofollow" class="result__a" href="//duckduckgo.com/l/\?uddg=[^ ]+fallecidosenloscamposnazis\.org%2Fes%2F(\d+[^ ]+\.html', split)[0]
                            bbddid = bbddid.replace('%2F', '/')
                            bbddid = bbddid.replace('%2D', '-')
                            #print(bbddid)
                            print('Añadiendo ID %s al artículo' % bbddid)
                            newtext = wtext.replace("", "" % (mempubid))
                            
                            if wtext != newtext:
                                pywikibot.showDiff(wtext, newtext)
                                page.text = newtext
                                #page.save('BOT - Añadiendo enlace a [[Fallecidos en los campos nazis (sitio web)]]', botflag=True)
                        else:
                            print('ERROR: La fecha no coincide, saltando')
                            f = open('fallecidosenloscamposnazis.error', 'a')
                            msg = '\n* [[%s]] no coincide su fecha en Fallecidos en los campos nazis' % (wtitle)
                            f.write(msg)
                            f.close()
                    else:
                        print('ERROR: No hay ficha para esta persona, saltando')
                        f = open('fallecidosenloscamposnazis.error', 'a')
                        msg = '\n* [[%s]] no tiene ficha en Fallecidos en los campos nazis' % (wtitle)
                        f.write(msg)
                        f.close()
            
            #print(raw)
            time.sleep(5)
    
if __name__ == '__main__':
    main()
