#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2024 emijrp <emijrp@gmail.com>
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

import json
import urllib2 
import pywikibot
import pywikibot.pagegenerators as pagegenerators
import re
import sys

def main():
    site = pywikibot.Site('15mpedia', '15mpedia')
    catnames = [
        u'Categoría:Municipios de España', 
    ]
    start = ''
    skip = ''
    if len(sys.argv) > 1:
        skip = sys.argv[1]
        start = sys.argv[1]
    
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
            
            if "(" in wtitle or "/" in wtitle:
                #print("Nombre con caracteres raros")
                continue
            
            print(u'\n== %s ==' % (wtitle))
            if not re.search(r'{{Infobox Municipio', wtext):
                print("No tiene infobox municipio")
                continue
            
            if not re.search(r'(?im)total=\d{4,}', wtext):
                print("Municipio pequeno")
                continue
            
            m = re.findall(r"(?im)\|\s*comunidad autónoma\s*=\s*([^\s*]+)", wtext)
            ccaa = m and m[0] or ""
            m = re.findall(r"(?im)\|\s*provincia\s*=\s*([^\s*]+)", wtext)
            prov = m and m[0] or ""
            
            if not ccaa or not prov:
                print("Sin datos de ccaa o prov")
                continue
            
            mhtitle = "Memoria Histórica en %s" % (wtitle)
            mhpage = pywikibot.Page(site, mhtitle)
            if not mhpage.exists():
                mhpage.text = """{{Infobox Memoria Histórica por lugar
|país=España
|comunidad autónoma=%s
|provincia=%s
|municipio=%s
|introducción=
}}""" % (ccaa, prov, wtitle)
                mhpage.save("BOT - Creando página", botflag=True)
            redirects = [
                "Memoria histórica en %s" % (wtitle), 
                "Memoria Historica en %s" % (wtitle), 
                "Memoria historica en %s" % (wtitle), 
                
                "Memoria Histórica de %s" % (wtitle), 
                "Memoria histórica de %s" % (wtitle), 
                "Memoria Historica de %s" % (wtitle), 
                "Memoria historica de %s" % (wtitle), 
                
                "MH en %s" % (wtitle), 
                "MH de %s" % (wtitle), 
                "mh en %s" % (wtitle), 
                "mh de %s" % (wtitle), 
                
            ]
            for redirect in redirects:
                mhredpage = pywikibot.Page(site, redirect)
                if not mhredpage.exists():
                    mhredpage.text = "#REDIRECT [[%s]]" % (mhtitle)
                    mhredpage.save("BOT - Creando redirección a [[%s]]" % (mhtitle), botflag=True)
            
if __name__ == '__main__':
    main()
