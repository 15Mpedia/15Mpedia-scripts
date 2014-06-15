#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2014 emijrp
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

import catlib
import re
import pagegenerators
import wikipedia

def main():
    eswiki = wikipedia.Site('es', 'wikipedia')
    site = wikipedia.Site('15mpedia', '15mpedia')
    cat = catlib.Category(site, u"Category:Municipios de España")
    gen = pagegenerators.CategorizedPageGenerator(cat,start="Motril")
    pre = pagegenerators.PreloadingGenerator(gen, pageNumber=60)
    
    for page in pre:
        wtitle = page.title()
        wtext = page.get()
        
        print '\n===', wtitle, '==='
        if not re.search(ur"(?im)\{\{\s*Infobox Municipio", wtext):
            print u"Le falta la infobox"
            continue
        
        #capturar {{wikipedia}} si existe, sino mismo nombre
        eswikititle = wtitle
        search = re.findall(ur"(?im)\{\{\s*wikipedia\s*\|\s*es\s*\|\s*([^\}]+?)\s*\}\}", wtext)
        if search:
            eswikititle = search[0].strip()
            if eswikititle.endswith("PAGENAME"):
                eswikititle = wtitle
            print "Capturada plantilla {{wikipedia}} con valor", eswikititle
        else:
            search = re.findall(ur"(?im)\{\{\s*wikipedia\s*\}\}", wtext)
            if search:
                eswikititle = wtitle
                print "Capturada plantilla {{wikipedia}}"
            else:
                print "Usando mismo titulo"
        
        #comprobando si existe en wikipedia
        eswikipage = wikipedia.Page(eswiki, eswikititle)
        if eswikipage.exists():
            print "Existe en Wikipedia"
        else:
            print "No existe en Wikipedia"
            continue
        
        #resolviendo redirect si lo fuera
        if eswikipage.isRedirectPage():
            eswikipage = eswikipage.getRedirectTarget()
            if eswikipage.isRedirectPage():
                continue
        
        if page.isDisambig():
            print "Es una desambiguación, saltamos"
            continue
        
        eswikitext = eswikipage.get()
        eswikititle = eswikipage.title()
        if not re.search(ur"\{\{\s*Ficha de localidad", eswikitext):
            continue
        wikipediatemplate = u'* {{wikipedia|es|%s}}' % (eswikititle)
        
        resumen = []
        parametros = []
        #capturar comarca
        if not re.search(ur"(?im)\|\s*comarca", wtext):
            comarca = re.findall(ur"(?im)\|\s*comarca\s*=\s*(?:\[\[\s*(?:Archivo|File|Imagen?)\s*:\s*[^\[\]\r\n]*?\s*\]\])?\s*\[\[([^\[\]\r\n]+?)(?:\|[^\[\]\r\n]*?)?\]\]", eswikitext)
            if comarca:
                comarca = comarca[0]
                parametros.append(u"|comarca=%s" % (comarca))
                resumen.append(u"comarca")
        
        print '\n'.join(parametros)
        print ', '.join(resumen)
        
        newtext = wtext
        if parametros:
            newtext = re.sub(ur"(?im)(\{\{\s*Infobox Municipio)", ur"\1\n%s" % ('\n'.join(parametros)), newtext)
        if not re.search(ur"(?im)\{\{\s*enlaces externos\s*\}\}", newtext):
            if re.search(ur"(?im)\|\s*enlaces externos\s*=", newtext):
                newtext = re.sub(ur"(?im)(\|\s*enlaces externos\s*=)", ur"\1{{enlaces externos}}\n", newtext)
            else:
                newtext = re.sub(ur"(?im)(\{\{\s*Infobox Municipio)", ur"\1\n|enlaces externos={{enlaces externos}}", newtext)
        if wikipediatemplate and not re.search(ur"(?im)\{\{\s*wikipedia", newtext):
            newtext = re.sub(ur"(?im)({{enlaces externos}})", ur"\1\n%s" % (wikipediatemplate), newtext)
        if wtext != newtext:
            wikipedia.showDiff(wtext, newtext)
            if resumen:
                page.put(newtext, u"BOT - Añadiendo datos de [[:wikipedia:es:%s]]: %s" % (eswikititle, ', '.join(resumen)), botflag=True)
            else:
                page.put(newtext, u"BOT - Añadiendo plantillas de enlaces externos", botflag=True)
        #break
        
if __name__ == '__main__':
    main()
