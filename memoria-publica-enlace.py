#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016 emijrp <emijrp@gmail.com>
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
        'Categoría:Personas fusiladas por el franquismo', 
        'Categoría:Víctimas del nazismo', 
    ]
    start = ''
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
            if re.search(r'(?im){{memoria p[úu]blica\|[\d]+\}\}', wtext):
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
            url = 'https://especiales.publico.es/es/memoria-publica/buscar?nombre=%s&apellidos=%s' % (nombre_, apellidos_)
            raw = getURL(url=url)
            
            if re.search(r'Fecha de muerte:', raw):
                if re.search(r'Fecha de muerte: <span>%s</span>' % (fechafallecimiento2), raw):
                    print('La fecha coincide, debe ser la misma persona')
                    mempubid = re.findall(r'<meta property="og:url" content="http://especiales.publico.es/es/memoria-publica/ficha/(\d+)/', raw)[0]
                    #print(mempubid)
                    print('Añadiendo ID %s al artículo' % mempubid)
                    if '<!--\n* {{memoria pública|}}' in wtext:
                        newtext = wtext.replace("""<!--
* {{memoria pública|}}
* {{mcu represión|}}
-->""", """* {{memoria pública|%s}}
<!--
* {{mcu represión|}}
-->""" % (mempubid))
                    elif '<!--\n* {{PARES deportados|id=}}' in wtext:
                        newtext = wtext.replace("""<!--
* {{PARES deportados|id=}}
-->""", """* {{memoria pública|%s}}
<!--
* {{PARES deportados|id=}}
-->""" % (mempubid))
                    else:
                        newtext = wtext.replace("""<!--""", """* {{memoria pública|%s}}
<!--""" % (mempubid))
                    if wtext != newtext:
                        pywikibot.showDiff(wtext, newtext)
                        page.text = newtext
                        page.save('BOT - Añadiendo enlace a [[Memoria Pública]]', botflag=True)
                else:
                    print('ERROR: La fecha no coincide, saltando')
                    f = open('memoria-publica.error', 'a')
                    msg = '\n* [[%s]] no coincide su fecha en Memoria Pública' % (wtitle)
                    f.write(msg)
                    f.close()
            else:
                print('ERROR: No hay ficha para esta persona, saltando')
                f = open('memoria-publica.error', 'a')
                msg = '\n* [[%s]] no tiene ficha en Memoria Pública' % (wtitle)
                f.write(msg)
                f.close()
            
            #print(raw)
            time.sleep(20)
    
if __name__ == '__main__':
    main()
