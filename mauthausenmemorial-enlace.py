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
        'Categoría:Personas deportadas al Campo de concentración de Mauthausen', 
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
            newtext = wtext
            wtitle = page.title()
            if not re.search(r'{{Infobox Persona', wtext):
                continue
            print('\n== %s ==' % (wtitle))
            if re.search(r'(?im)mauthausen memorial id', wtext):
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
                fechafallecimiento3 = '%d.%d.%d' % (int(fechafallecimiento.split('/')[2]), int(fechafallecimiento.split('/')[1]), int(fechafallecimiento.split('/')[0]))
            except:
                continue
            
            #print nombre, apellidos
            url = 'https://raumdernamen.mauthausen-memorial.org/index.php?txtSearch=%s+%s&id=5&L=6' % (removeaccute(nombre_), removeaccute(apellidos_))
            raw = getURL(url=url)
            splits = raw.split('<div class="column-main">')
            if splits:
                splits = splits[1:]
            
            for split in splits:
                nombrecompleto = '%s %s' % (nombre, apellidos)
                nombrecompleto_ = removeaccute(nombrecompleto)
                if re.search(r'(?im)%s' % (nombrecompleto), split) or re.search(r'(?im)%s' % (nombrecompleto_), split):
                    if re.search(r'(?im)Muert', split):
                        if re.search(r'(?im)Muert[oa]:?\s*%s' % (fechafallecimiento3), split):
                            print('La fecha coincide, debe ser la misma persona')
                            bbddid = re.findall(r'&p=(\d+)&L[^<>]*?">\s*Seguir leyendo', split)[0]
                            #print(bbddid)
                            print('Añadiendo ID %s al artículo' % bbddid)
                            newtext = re.sub(r"(?im)({{Infobox Persona)", r"\1\n|mauthausen memorial id=%s" % (bbddid), newtext)
                            
                            if wtext != newtext:
                                pywikibot.showDiff(wtext, newtext)
                                page.text = newtext
                                page.save('BOT - Añadiendo enlace a [[Mauthausen Memorial]]', botflag=True)
                        else:
                            print('ERROR: La fecha no coincide, saltando')
                            f = open('mauthausenmemorial.error', 'a')
                            msg = '\n* [[%s]] no coincide su fecha en mauthausenmemorial' % (wtitle)
                            f.write(msg)
                            f.close()
                    else:
                        print('ERROR: No hay ficha para esta persona, saltando')
                        f = open('mauthausenmemorial.error', 'a')
                        msg = '\n* [[%s]] no tiene ficha en mauthausenmemorial' % (wtitle)
                        f.write(msg)
                        f.close()
            
            #print(raw)
            time.sleep(10)
    
if __name__ == '__main__':
    main()
