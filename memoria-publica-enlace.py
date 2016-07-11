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
import urllib2
import pywikibot
import pywikibot.pagegenerators as pagegenerators

def main():
    site = pywikibot.Site('15mpedia', '15mpedia')
    category = pywikibot.Category(site, u'Categoría:Personas fusiladas por el franquismo')
    gen = pagegenerators.CategorizedPageGenerator(category=category, start='', namespaces=[0])
    pre = pagegenerators.PreloadingGenerator(gen, pageNumber=250)
    
    for page in pre:
        if not page.exists() or page.isRedirectPage():
            continue
        wtext = page.text
        wtitle = page.title()
        if not re.search(ur'{{Infobox Persona', wtext):
            continue
        print('\n== %s ==' % (wtitle))
        if re.search(ur'{{memoria pública\|[\d]+\}\}', wtext):
            print(u'Ya tiene el ID')
            continue
        
        nombre = re.findall(ur'(?im)\|nombre=([^\|]*)', wtext)[0].strip()
        primerapellido = re.findall(ur'(?im)\|primer apellido=([^\|]*)', wtext)[0].strip()
        segundoapellido = re.findall(ur'(?im)\|segundo apellido=([^\|]*)', wtext)[0].strip()
        apellidos = u'%s %s' % (primerapellido, segundoapellido)
        nombre_ = re.sub(ur' ', ur'+', nombre)
        apellidos_ = re.sub(ur' ', ur'+', apellidos)
        fechafallecimiento = re.findall(ur'(?im)\|fecha de fallecimiento=(\d\d\d\d/\d\d/\d\d)', wtext)[0].strip()
        fechafallecimiento2 = u'%s/%s/%s' % (fechafallecimiento.split('/')[2], fechafallecimiento.split('/')[1], fechafallecimiento.split('/')[0])
        
        #print nombre, apellidos
        url = 'http://especiales.publico.es/es/memoria-publica/buscar?nombre=%s&apellidos=%s' % (nombre_.encode('utf-8'), apellidos_.encode('utf-8'))
        req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
        raw = urllib2.urlopen(req).read()
        raw = unicode(raw, 'utf-8')
        
        if re.search(ur'Fecha de muerte: <span>%s</span>' % (fechafallecimiento2), raw):
            print(u'La fecha coincide, debe ser la misma persona')
            mempubid = re.findall(ur'<meta property="og:url" content="http://especiales.publico.es/es/memoria-publica/ficha/(\d+)/', raw)[0]
            #print(mempubid)
            print(u'Añadiendo ID %s al artículo' % mempubid)
            newtext = wtext.replace(u"""<!--
* {{memoria pública|}}
* {{mcu represión|}}
-->""", u"""* {{memoria pública|%s}}
<!--
* {{mcu represión|}}
-->""" % (mempubid))
            if wtext != newtext:
                pywikibot.showDiff(wtext, newtext)
                page.text = newtext
                page.save(u'BOT - Añadiendo enlace a [[Memoria Pública]]', botflag=True)
        else:
            print(u'ERROR: La fecha no coincide, saltando')
            f = open('memoria-publica.error', 'a')
            msg = u'\n* [[%s]] no coincide su nombre en Memoria Pública' % (wtitle)
            f.write(msg.encode('utf-8'))
            f.close()
        
        #print(raw)
        time.sleep(10)
    
if __name__ == '__main__':
    main()
