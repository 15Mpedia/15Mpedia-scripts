#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 emijrp <emijrp@gmail.com>
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

import csv
import os
import re
import sys
import pywikibot

def main():
    codsccaa = {'01': u'Andalucía', }
    codsprov = {'04': u'Provincia de Almería', }
    csvfile = open('deuda-municipios.csv', 'r')
    deuda = csv.reader(csvfile, delimiter=',', quotechar='"')
    
    pais = u'España'
    c = 0
    for row in deuda:
        if c == 0:
            c += 1
            continue
        
        ejercicio = int(row[0])
        codccaa = row[1]
        ccaa = unicode(row[2], 'utf-8').strip()
        codprov = row[3]
        provincia = unicode(row[4], 'utf-8').strip()
        codmuni = row[5]
        municipio = unicode(row[6], 'utf-8').strip()
        deuda2010 = int(row[7].replace('.', ''))*1000
        
        nombre = re.sub(ur'(?im)([^\(\)]+?) \(([^\(\)]+?)\)', ur'\2 \1', municipio)
        print '\n', '#'*40, '\n', nombre, '\n', '#'*40, '\n'
        
        #coger info de wikipedia
        eswikititle = nombre
        eswiki = pywikibot.Page(pywikibot.Site('es', 'wikipedia'), u'%s' % (eswikititle))
        if eswiki.exists() and eswiki.isRedirectPage():
            eswiki = eswiki.getRedirectTarget()
            eswikititle = eswiki.title()
        
        if not eswiki.exists() or \
            (eswiki.exists() and eswiki.isDisambig()) or \
            (eswiki.exists() and not re.search(ur'(?im)\{\{\s*Ficha de localidad de España', eswiki.text)):
            print u'Municipio %s no encontrado en eswiki' % eswikititle
            eswikititle = u'%s (España)' % (eswikititle)
            print u'Probando con %s' % (eswikititle)
            eswiki = pywikibot.Page(pywikibot.Site('es', 'wikipedia'), u'%s' % (eswikititle))
            
            if eswiki.exists() and eswiki.isRedirectPage():
                eswiki = eswiki.getRedirectTarget()
                eswikititle = eswiki.title()
            
            if not eswiki.exists() or \
                (eswiki.exists() and eswiki.isDisambig()) or \
                (eswiki.exists() and not re.search(ur'(?im)\{\{\s*Ficha de localidad de España', eswiki.text)):
                print u'Municipio %s no encontrado en eswiki' % eswikititle
                
                eswikititle = u'%s (%s)' % (eswikititle.split(' (')[0], codsprov[codprov].split('Provincia de ')[1])
                print u'Probando con %s' % (eswikititle)
                eswiki = pywikibot.Page(pywikibot.Site('es', 'wikipedia'), u'%s' % (eswikititle))
                
                if eswiki.exists() and eswiki.isRedirectPage():
                    eswiki = eswiki.getRedirectTarget()
                    eswikititle = eswiki.title()
                
                if not eswiki.exists() or \
                    (eswiki.exists() and eswiki.isDisambig()) or \
                    (eswiki.exists() and not re.search(ur'(?im)\{\{\s*Ficha de localidad de España', eswiki.text)):
                    print u'Municipio %s no encontrado en eswiki. Escribiendo al log de errores' % eswikititle
                
                    error = open('crear-municipios.errores', 'a')
                    errorline = u'%s\n' % (municipio)
                    error.write(errorline.encode('utf-8'))
                    error.close()
                    continue

        if eswiki.exists() and not eswiki.isRedirectPage() and not eswiki.isDisambig():
            if re.search(ur'(?im)\{\{\s*Ficha de localidad de España', eswiki.text):
                escudo = u''
                if re.search(ur'(?im)escudo\s*=', eswiki.text):
                    escudo = re.findall(ur'escudo\s*=\s*([^\n\r\|\[\]]+)', eswiki.text)[0].strip()
                    if escudo == 'no':
                        escudo = u''
                bandera = u''
                if re.search(ur'(?im)bandera\s*=', eswiki.text):
                    bandera = re.findall(ur'bandera\s*=\s*([^\n\r\|\[\]]+)', eswiki.text)[0].strip()
                    if bandera == 'no':
                        bandera = u''
                comarca = u''
                if re.search(ur'(?im)comarca\s*=\s*\[\[', eswiki.text):
                    comarca = re.findall(ur'(?im)comarca\s*=\s*\[\[([^\n\r\|\[\]]+?)(?:\|[^\n\r\[\]]+?)?\]\]', eswiki.text)[0].strip()
                web = u''
                if re.search(ur'(?im)web\s*=\s*\[?http', eswiki.text):
                    web = re.findall(ur'web\s*=\s*\[?(https?://[^\s]+)', eswiki.text)[0].strip()  
            else:
                print u'Municipio no encontrado en eswiki'
                continue
        else:
            print u'Municipio no encontrado en eswiki'
            continue
        
        infobox = u"""{{Infobox Municipio
|nombre=%s
|país=%s
|comunidad autónoma=%s
|comunidad autónoma código=%s
|provincia=%s
|provincia código=%s
|comarca=%s
|municipio código=%s
|escudo=%s
|bandera=%s
|deuda viva={{deuda viva|año=2010|euros=%s}}
|sitio web=%s
|enlaces externos={{enlaces externos}}
* {{wikipedia|es|%s}}
}}""" % (nombre, pais, codsccaa[codccaa], codccaa, codsprov[codprov], codprov, comarca, codmuni, escudo, bandera, deuda2010, web, eswikititle)
        
        print infobox
        
        """page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), u'%s' % (nombre))
        if page.exists():
            print 'La pagina ya existe'
            continue
        else:
            page.text = infobox
            page.save(u'BOT - Creando municipio', botflag=False)"""
        
        c += 1

    csvfile.close()

if __name__ == '__main__':
    main()
