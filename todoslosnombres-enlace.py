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
    req = urllib.request.Request(url, headers={ 'User-Agent': '' })
    try:
        raw = urllib.request.urlopen(req).read().strip().decode('utf-8')
    except:
        pass
    return raw

def main():
    site = pywikibot.Site('15mpedia', '15mpedia')
    catnames = [
        'Categoría:Personas fusiladas por el franquismo', 
        'Categoría:Víctimas del nazismo', 
    ]
    start = ''
    skip = 'Herminio García Rodríguez'
    
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
            if not re.search(r'{{Infobox Persona', wtext):
                continue
            print('\n== %s ==' % (wtitle))
            if re.search(r'(?im){{todos[ -]los[ -]nombres\|', wtext):
                print('Ya tiene el ID')
                continue
            
            try:
                nombre = re.findall(r'(?im)\|nombre=([^\|]*)', wtext)[0].strip()
                primerapellido = re.findall(r'(?im)\|primer apellido=([^\|]*)', wtext)[0].strip()
                segundoapellido = re.findall(r'(?im)\|segundo apellido=([^\|]*)', wtext)[0].strip()
                apellidos = '%s %s' % (primerapellido, segundoapellido)
                apellidos = apellidos.strip()
                nombre_ = re.sub(r' ', r'-', nombre)
                apellidos_ = re.sub(r' ', r'-', apellidos)
                nombrecompleto = '%s-%s' % (nombre_, apellidos_)
                nombrecompleto_ = removeaccute(nombrecompleto.lower())
                fechafallecimiento = re.findall(r'(?im)\|fecha de fallecimiento=(\d\d\d\d/\d\d/\d\d)', wtext)[0].strip()
                fechafallecimiento2 = '%s/%s/%s' % (fechafallecimiento.split('/')[2], fechafallecimiento.split('/')[1], fechafallecimiento.split('/')[0])
            except:
                continue
            
            #print nombre, apellidos
            url = 'http://www.todoslosnombres.org/content/personas/%s' % (nombrecompleto_)
            archiveurl = 'https://web.archive.org/web/2020/http://www.todoslosnombres.org/content/personas/%s' % (nombrecompleto_)
            url = archiveurl #mientras el server no carga, tiramos de archive
            
            print(url)
            raw = getURL(url=url)
            
            if raw and (not re.search(r'Página no encontrada', raw) and not re.search(r'This page is not available on the web', raw)):
                if re.search(r'%s' % (fechafallecimiento2), raw):
                    print('La fecha coincide, debe ser la misma persona')
                    tlnid = nombrecompleto_
                    #print(tlnid)
                    print('Añadiendo ID %s al artículo' % tlnid)
                    newtext = wtext.replace("""<!--
* {{""", """* {{todos los nombres|%s}}
<!--
* {{""" % (tlnid))
                    if wtext != newtext:
                        pywikibot.showDiff(wtext, newtext)
                        page.text = newtext
                        page.save('BOT - Añadiendo enlace a [[Todos los nombres]]', botflag=True)
                else:
                    print('ERROR: La fecha no coincide, saltando')
                    f = open('todoslosnombres.error', 'a')
                    msg = '\n* [[%s]] no coincide su fecha en todoslosnombres' % (wtitle)
                    f.write(msg)
                    f.close()
            else:
                print('ERROR: No hay ficha para esta persona, saltando')
                f = open('todoslosnombres.error', 'a')
                msg = '\n* [[%s]] no tiene ficha en todoslosnombres' % (wtitle)
                f.write(msg)
                f.close()
            
            #print(raw)
            time.sleep(1)
    
if __name__ == '__main__':
    main()
