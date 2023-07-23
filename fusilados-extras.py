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

import pywikibot
import pywikibot.pagegenerators as pagegenerators
import re

def main():
    site = pywikibot.Site('15mpedia', '15mpedia')
    catnames = [
        u'Categoría:Personas fusiladas por el franquismo', 
        #u'Categoría:Víctimas del nazismo', 
    ]
    start = ''
    for catname in catnames:
        category = pywikibot.Category(site, catname)
        gen = pagegenerators.CategorizedPageGenerator(category=category, start=start, namespaces=[0])
        pre = pagegenerators.PreloadingGenerator(gen, pageNumber=250)
        
        comments = []
        for page in pre:
            if not page.exists() or page.isRedirectPage():
                continue
            wtext = page.text
            wtitle = page.title()
            if not re.search(ur'{{Infobox Persona', wtext):
                continue
            print('\n== %s ==' % (wtitle))
            newtext = wtext
            
            #elimina plantillas vacias
            newtext2 = newtext
            newtext = re.sub(ur"(?im)\n<!--(\s*\*\s*{{mcu represión\|\s*(id\s*=)?\s*}}|\s*\*\s*{{memoria pública\|\s*(id\s*=)?\s*}}|\s*\*\s*{{nomes e voces\|\s*(id\s*=)?\s*}}|\s*\*\s*{{pares deportados\|\s*(id\s*=)?\s*}}|\s*\*\s*{{todos los nombres\|\s*(id\s*=)?\s*}})+\s*-->", ur"", newtext)
            if newtext != newtext2:
                comments.append(u"eliminando plantillas vacías")
            
            #bbdd id
            newtext2 = newtext
            replaces = [
                #plantilla, atributo id
                [u"mcu represión", u"pares represaliados id"], 
                [u"memoria pública", u"memoria pública id"], 
                [u"nomes e voces", u"nomes e voces id"], 
                [u"todos los nombres", u"todos los nombres id"], 
                [u"víctimas de la dictadura en clm", u"víctimas de la dictadura en clm id"], 
            ]
            for x, y in replaces:
                if re.search(ur"(?im)\*\s*{{\s*%s\s*\|" % (x), newtext):
                    m = re.findall(ur"(?im)\*\s*{{\s*%s\s*\|\s*(?!id\s*=)?\s*([^\{\}]+)\s*\}\}\n" % (x), newtext)
                    if m:
                        newtext = re.sub(ur"(?im)\*\s*{{\s*%s\s*\|\s*(?!id\s*=)?\s*([^\{\}]+)\s*\}\}\n" % (x), ur"", newtext)
                        newtext = re.sub(ur"(?im)({{Infobox Persona)", ur"\1\n|%s=%s" % (y, m[0]), newtext)
            
            if newtext != newtext2:
                comments.append(u"moviendo ids a infobox persona")
            
            #homenajes
            if re.search(ur'(?im){{\s*homenajes', newtext):
                print(u'Ya tiene plantilla homenajes')
            else:
                if re.search(ur'(?im)==\s*Memoria\s*==', newtext):
                    newtext2 = newtext
                    m = re.findall(ur"(?im)(\{\{homenaje-[^\{\}]+\}\}\n)", newtext)
                    if m:
                        homenajes = []
                        for n in m:
                            newtext = newtext.replace(n, "")
                            homenajes.append(n)
                        homenajes_ = ""
                        c = 1
                        for homenaje in homenajes:
                            homenajes_ += "|%d=%s" % (c, homenaje)
                            c += 1
                        newtext = re.sub(ur'(?im)(==\s*Memoria\s*==)\n', ur"\1\n{{Homenajes\n%s}}" % (homenajes_), newtext)
                    if newtext != newtext2:
                        comments.append(u"modificando sección memoria")
                else:
                    newtext2 = newtext
                    newtext = re.sub(ur"(?im)(==\s*Véase también\s*==)", ur"== Memoria ==\n{{Homenajes}}\n\n\1", newtext)
                    if newtext != newtext2:
                        comments.append(u"añadiendo sección memoria")
            
            #fallecimiento=Sí para fusilados
            if re.search(ur"(?im){{Infobox Persona", newtext) and len(re.findall(ur"(?im)\|represión={{Persona represaliada", newtext)) == 1 and re.search(ur"(?im)\|represión=Fusilamiento", newtext) and not re.search(ur"(?im)\|fallecimiento=", newtext):
                newtext = re.sub(ur"(?im)(\|represión={{Persona represaliada)", ur"\1\n|fallecimiento=Sí", newtext)
                comments.append(u"añadiendo parámetro a plantilla")
            
            if wtext != newtext:
                pywikibot.showDiff(wtext, newtext)
                page.text = newtext
                comments = list(set(comments))
                comments.sort()
                comment = u'BOT - %s' % (', '.join(comments))
                page.save(comment, botflag=True)

if __name__ == '__main__':
    main()
