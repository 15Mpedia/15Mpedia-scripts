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
    cat = catlib.Category(site, u"Category:Políticos")
    gen = pagegenerators.CategorizedPageGenerator(cat)
    pre = pagegenerators.PreloadingGenerator(gen, pageNumber=60)
    
    for page in pre:
        wtitle = page.title()
        wtext = page.get()
        
        print '\n===', wtitle, '==='
        if not re.search(ur"(?im)\{\{\s*Infobox Persona", wtext):
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
        wikipediatemplate = u'* {{wikipedia|es|%s}}' % (eswikititle)
        
        #leyendo redirects de wikipedia y creandolas en local
        eswikireds = eswikipage.getReferences(redirectsOnly=True)
        for eswikired in eswikireds:
            if '(' in eswikired.title() or len(eswikititle) == eswikired.title(): #saltar redirecciones sin cambio de longitud (probablemente sea una con acentos intercambiados)
                continue
            print "   ", eswikired.title()
            red = wikipedia.Page(site, eswikired.title())
            if not red.exists():
                red.put(u"#REDIRECT [[%s]]" % (wtitle), u"BOT - Creando redirección hacia [[%s]]" % (wtitle), botflag=True)
        eswikipage = ''
        
        resumen = []
        parametros = []
        #capturar fecha nacimiento
        if not re.search(ur"(?im)\|\s*fecha de nacimiento", wtext):
            fechanacimiento = re.findall(ur"(?im)\|\s*fechanac\s*=[^\{\n]*?\{\{\s*(?:edad|fecha|fecha de inicio)\s*\|\s*([0-9]+)\s*\|\s*([0-9]+)\s*\|\s*([0-9]+)\s*(?:\|\s*edad\s*)?\s*\}\}", eswikitext)
            if fechanacimiento:
                fechanacimiento = fechanacimiento[0]
                parametros.append(u"|fecha de nacimiento=%d/%02d/%02d" % (int(fechanacimiento[2]), int(fechanacimiento[1]), int(fechanacimiento[0])))
                resumen.append(u"fecha de nacimiento")
        #capturar lugar nacimiento
        if not re.search(ur"(?im)\|\s*lugar de nacimiento", wtext):
            lugarnacimiento = re.findall(ur"(?im)\|\s*lugarnac\s*=\s*\[\[\s*([^\]]+?)\s*\]\]", eswikitext)
            if lugarnacimiento:
                lugarnacimiento = lugarnacimiento[0]
                if '|' in lugarnacimiento:
                    lugarnacimiento = lugarnacimiento.split('|')[1]
                parametros.append(u"|lugar de nacimiento=%s" % (lugarnacimiento))
                resumen.append(u"lugar de nacimiento")
        #capturar imagen
        if not re.search(ur"(?im)\|\s*imagen", wtext):
            imagen = re.findall(ur"(?im)\|\s*imagen\s*=\s*([^\|\n]+?)\n", eswikitext)
            if imagen and imagen[0].strip():
                parametros.append(u"|imagen=%s" % (imagen[0].strip()))
                resumen.append(u"imagen")
        
        print '\n'.join(parametros)
        print ', '.join(resumen)
        
        newtext = wtext
        if parametros:
            newtext = re.sub(ur"(?im)(\{\{\s*Infobox Persona)", ur"\1\n%s" % ('\n'.join(parametros)), newtext)
        if not re.search(ur"(?im)\{\{\s*enlaces externos\s*\}\}", newtext):
            newtext = re.sub(ur"(?im)(==\s*Enlaces externos\s*==)", ur"\1\n{{enlaces externos}}", newtext)
        if wikipediatemplate and not re.search(ur"(?im)\{\{\s*wikipedia", newtext):
            newtext = re.sub(ur"(?im)({{enlaces externos}})", ur"\1\n%s" % (wikipediatemplate), newtext)
        if wtext != newtext:
            wikipedia.showDiff(wtext, newtext)
            if resumen:
                page.put(newtext, u"BOT - Añadiendo datos de [[:wikipedia:es:%s]]: %s" % (eswikititle, ', '.join(resumen)), botflag=False)
            else:
                page.put(newtext, u"BOT - Añadiendo plantillas de enlaces externos", botflag=False)
        #break
        
if __name__ == '__main__':
    main()
