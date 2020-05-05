#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2020 emijrp <emijrp@gmail.com>
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
import pywikibot
import pywikibot.pagegenerators as pagegenerators
import re
import time
import sys

def main():
    site = pywikibot.Site('15mpedia', '15mpedia')
    catnames = [
        'Categoría:Municipios de España', 
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
            
            #print('\n== %s ==' % (wtitle))
            if not re.search(r'{{Infobox Municipio', wtext):
                #print("No tiene infobox municipio")
                continue
            
            provcod = re.findall(r"(?m)\|provincia código=([^\n\|]+)", wtext)
            provcod = provcod and provcod[0] or ''
            municod = re.findall(r"(?m)\|municipio código=([^\n\|]+)", wtext)
            municod = municod and municod[0] or ''
            cod = str(int(provcod+municod))
            if not cod:
                print(wtitle)
                break
            print(cod)
            with open('municipios.codigos', 'a') as f:
                f.write(cod+'\n')

if __name__ == '__main__':
    main()
      
