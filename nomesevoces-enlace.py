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
        pass
    return raw

def number2month(n=0):
    months = {1:"xaneiro", 2:"febreiro", 3:"marzo", 4:"abril", 5:"maio", 6:"xuño", 7:"xullo", 8:"agosto",
    9:"setembro", 10:"outubro", 11:"novembro", 12:"decembro", }
    return months[n]

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
        
        for page in pre:
            if not page.exists() or page.isRedirectPage():
                continue
            wtext = page.text
            wtitle = page.title()
            if not re.search(r'{{Infobox Persona', wtext):
                continue
            print('\n== %s ==' % (wtitle))
            if re.search(r'(?im){{(nomesevoces|nomes[ -]e[ -]voces)\|', wtext):
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
                nombrecompleto = '%s, %s' % (apellidos, nombre)
                nombrecompleto_ = '%s+%s' % (apellidos_, nombre_)
                fechafallecimiento = re.findall(r'(?im)\|fecha de fallecimiento=(\d\d\d\d/\d\d/\d\d)', wtext)[0].strip()
                fechafallecimiento2 = '%s/%s/%s' % (fechafallecimiento.split('/')[2], fechafallecimiento.split('/')[1], fechafallecimiento.split('/')[0])
                fechafallecimiento3 = '%s de %s de %s' % (fechafallecimiento.split('/')[2], number2month(int(fechafallecimiento.split('/')[1])), fechafallecimiento.split('/')[0])
            except:
                continue
            
            url = 'http://vitimas.nomesevoces.net/gl/buscar/?orde=nome&buscar=%s' % (removeaccute(nombrecompleto_))
            print(url)
            raw = getURL(url=url)
            if not raw:
                print("ERROR retrieving page")
                continue
            
            if not re.search(r'(?im)Atopamos 0 resultados', raw):
                m = re.findall(r'(?im)<a href="/gl/ficha/(\d+)/">%s</a>' % (nombrecompleto), raw)
                for n in m:
                    url2 = 'http://vitimas.nomesevoces.net/gl/ficha/%s/' % (n)
                    print(url2)
                    raw2 = getURL(url=url2)
                    if re.search(r'(?im)%s' % (fechafallecimiento3), raw2):
                        print('La fecha coincide, debe ser la misma persona')
                        nevid = n
                        #print(nevid)
                        print('Añadiendo ID %s al artículo' % nevid)
                        newtext = wtext.replace("""<!--
* {{""", """* {{nomes e voces|%s}}
<!--
* {{""" % (nevid))
                        if wtext != newtext:
                            pywikibot.showDiff(wtext, newtext)
                            page.text = newtext
                            page.save('BOT - Añadiendo enlace a [[Nomes e Voces]]', botflag=True)
                    else:
                        print('ERROR: La fecha no coincide, saltando')
            else:
                print('ERROR: No hay ficha para esta persona, saltando')
                f = open('nomesevoces.error', 'a')
                msg = '\n* [[%s]] no tiene ficha en nomesevoces' % (wtitle)
                f.write(msg)
                f.close()
            
            #print(raw)
            time.sleep(10)
    
if __name__ == '__main__':
    main()
