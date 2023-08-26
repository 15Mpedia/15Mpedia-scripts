#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2014-2023 emijrp
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
import sys
import pywikibot
import pywikibot.pagegenerators as pagegenerators

"""
Bot para importar datos de Wikipedia para los municipios.
De momento solo la comarca y poco más.
"""

def main():
    eswiki = pywikibot.Site('es', 'wikipedia')
    site = pywikibot.Site('15mpedia', '15mpedia')
    cat = pywikibot.Category(site, u"Category:Municipios de España")
    gen = pagegenerators.CategorizedPageGenerator(cat,start=sys.argv[1])
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
        eswikipage = pywikibot.Page(eswiki, eswikititle)
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
                if not ':' in comarca:
                    parametros.append(u"|comarca=%s" % (comarca))
                    resumen.append(u"comarca")
        #capturar gentilicio
        if not re.search(ur"(?im)\|\s*gentilicio", wtext):
            gentilicios = re.findall(ur"(?im)\|\s*gentilicio\s*=\s*([a-záéíóúñ]+o, ?-?[rnñ]?a)[\n\r\s<]", eswikitext)
            if gentilicios:
                gentilicioms = gentilicios[0].split(',')[0].strip()
                gentiliciofs = gentilicioms[:-1] + 'a'
                gentiliciomp = gentilicioms + 's'
                gentiliciofp = gentiliciofs + 's'
                parametros.append(u"|gentilicio fs=%s" % (gentiliciofs))
                parametros.append(u"|gentilicio ms=%s" % (gentilicioms))
                parametros.append(u"|gentilicio fp=%s" % (gentiliciofp))
                parametros.append(u"|gentilicio mp=%s" % (gentiliciomp))
                resumen.append(u"gentilicio [fs=%s,ms=%s,fp=%s,mp=%s]" % (gentiliciofs, gentilicioms, gentiliciofp, gentiliciomp))
            else:
                gentilicios = re.findall(ur"(?im)\|\s*gentilicio\s*=\s*([a-záéíóúñ]+és, ?-?a)[\n\r\s<]", eswikitext)
                if gentilicios:
                    gentilicioms = gentilicios[0].split(',')[0].strip()
                    gentiliciofs = gentilicioms[:-2] + 'esa'
                    gentiliciomp = gentilicioms[:-2] + 'eses'
                    gentiliciofp = gentiliciofs + 's'
                    parametros.append(u"|gentilicio fs=%s" % (gentiliciofs))
                    parametros.append(u"|gentilicio ms=%s" % (gentilicioms))
                    parametros.append(u"|gentilicio fp=%s" % (gentiliciofp))
                    parametros.append(u"|gentilicio mp=%s" % (gentiliciomp))
                    resumen.append(u"gentilicio [fs=%s,ms=%s,fp=%s,mp=%s]" % (gentiliciofs, gentilicioms, gentiliciofp, gentiliciomp))
                else:
                    gentilicios = re.findall(ur"(?im)\|\s*gentilicio\s*=\s*([a-záéíóúñ]+nse)[\n\r\s<]", eswikitext)
                    if gentilicios:
                        gentilicioms = gentilicios[0].strip()
                        gentiliciofs = gentilicioms
                        gentiliciomp = gentilicioms + 's'
                        gentiliciofp = gentiliciofs + 's'
                        parametros.append(u"|gentilicio fs=%s" % (gentiliciofs))
                        parametros.append(u"|gentilicio ms=%s" % (gentilicioms))
                        parametros.append(u"|gentilicio fp=%s" % (gentiliciofp))
                        parametros.append(u"|gentilicio mp=%s" % (gentiliciomp))
                        resumen.append(u"gentilicio [fs=%s,ms=%s,fp=%s,mp=%s]" % (gentiliciofs, gentilicioms, gentiliciofp, gentiliciomp))
                    else:
                        print re.findall(ur"(?im)\|\s*gentilicio\s*=\s*[^\n\r]+", eswikitext)
        
        print '\n'.join(parametros)
        print ', '.join(resumen)
        
        newtext = wtext
        if parametros:
            newtext = re.sub(ur"(?im)(\{\{\s*Infobox Municipio)", ur"\1\n%s" % ('\n'.join(parametros)), newtext)
        if wtext != newtext:
            pywikibot.showDiff(wtext, newtext)
            if resumen:
                pass
                page.put(newtext, u"BOT - Añadiendo datos de [[:wikipedia:es:%s]]: %s" % (eswikititle, ', '.join(resumen)), botflag=True)
        #break
        
if __name__ == '__main__':
    main()
