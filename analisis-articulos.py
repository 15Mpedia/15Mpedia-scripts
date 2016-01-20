#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016 emijrp
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
import urllib
import pywikibot
import pywikibot.pagegenerators

def main():
    site = pywikibot.Site('15mpedia', '15mpedia')
    catsinfobox = [
        [u"Category:Acampadas", u"Acampada"],
        #[u"Category:Asambleas", u"Asamblea"],
        #[u"Category:Asociaciones", u"Asociación"],
        #[u"Category:Bancos de tiempo", u"Banco de tiempo"],
        [u"Category:Centros sociales", u"Centro social"],
        #[u"Category:Comisiones", u"Comisión"],
        #[u"Category:Cooperativas", u"Cooperativa"],
        #[u"Category:Grupos de trabajo", u"Grupo de trabajo"],
        #[u"Category:Nodos", u"Nodo"],
        #[u"Category:Partidos políticos", u"Partido político"],
        [u"Category:Plataformas", u"Plataforma"],
        #[u"Category:Realojos", u"Realojo"],
    ]
    output = """'''Análisis de artículos''' por tema.

* '''Leyenda:''' Bytes (tamaño), Ref (referencias), N (noticias), I (imágenes), V (vídeos)

{|"""
    for catname, infoboxname in catsinfobox:
        cat = pywikibot.Category(site, catname)
        gen = pywikibot.pagegenerators.CategorizedPageGenerator(cat)
        pre = pywikibot.pagegenerators.PreloadingGenerator(gen, pageNumber=250)
        
        rows = []
        for page in pre:
            if page.isRedirectPage():
                continue
            
            wtitle = page.title()
            wtext = page.text
            if not '{{Infobox %s' % (infoboxname) in wtext:
                continue
            noticias = len(re.findall(r'(?im)\{\{\s*noticia\s*\|', wtext))
            referencias = len(re.findall(r'(?im)</ref>', wtext))
            images = len(re.findall(r'(?im)\.jpe?g', wtext))
            videos = len(re.findall(r'(?im)\{\{\s*(bambuser|youtube|vimeo)( v[íi]deo)?\s*\|', wtext))
            rows.append('| [[%s]] || %s || %s || %s || %s || %s\n|-\n' % (wtitle, len(wtext), referencias, noticias, images, videos))
        rows.sort()
        output += """\n| valign=top |\n=== [[Plantilla:Infobox %s|%s]] ===
{| class="wikitable sortable"\n
! width=180px | Nombre !! Bytes !! Ref !! N !! I !! V\n|-\n
%s
|}""" % (infoboxname, infoboxname, ''.join(rows))
    output += '\n|}'
    
    analisis = pywikibot.Page(site, 'Usuario:Emijrp/Análisis de artículos')
    analisis.text = output
    analisis.save('BOT - Actualizando análisis')
   
if __name__ == '__main__':
    main()

