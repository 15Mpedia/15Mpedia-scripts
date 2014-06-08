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
import pagegenerators
import re
import wikipedia

def main():
    site = wikipedia.Site('15mpedia', '15mpedia')
    cat = catlib.Category(site, u"Category:Círculos de Podemos")
    gen = pagegenerators.CategorizedPageGenerator(cat)
    pre = pagegenerators.PreloadingGenerator(gen, pageNumber=60)
    
    for page in pre:
        wtitle = page.title()
        wtext = page.get()
        
        if not re.search(ur"(?im)\{\{\s*Infobox Nodo", wtext):
            continue
        
        print '\n===', wtitle, '==='
        newtext = wtext
        suffix = ' '.join(wtitle.split(' ')[1:])
        
        if re.search(ur"(?im)\{\{\s*nodos\s*\}\}", newtext) and not re.search(ur"(?im)\{\{\s*podemos\s*\}\}", newtext):
            newtext = re.sub(ur"(?im)\{\{\s*nodos\s*\}\}", ur"{{podemos}}", newtext)
        
        if re.search(ur"(?im)^'''([^\']+)''' es un \[\[nodo\]\] de \[\[Podemos\]\]\.", newtext):
            newtext = re.sub(ur"(?im)^'''([^\']+)''' es un \[\[nodo\]\] de \[\[Podemos\]\]\.", ur"'''\1''' es un [[Lista de círculos de Podemos|círculo]] de [[Podemos]] de [[%s]]." % (suffix), newtext)
        
        if re.search(ur"(?im)== Enlaces externos ==\s*\*[^\r\n]+\r\n", newtext):
            newtext = re.sub(ur"(?im)== Enlaces externos ==\s*\*[^\r\n]+\r\n", ur"== Enlaces externos ==\n{{enlaces externos}}\n", newtext)
        
        newtext = re.sub(ur"(?im)\[\[Categoría:Podemos\]\]", ur"", newtext)
        newtext = re.sub(ur"(?im)\[\[Categoría:Nodos\]\]", ur"[[Categoría:Círculos de Podemos|%s]]" % (suffix), newtext)
        newtext = re.sub(ur"(?im)\[\[Categoría:Círculos de Podemos\]\]", ur"[[Categoría:Círculos de Podemos|%s]]" % (suffix), newtext)
        
        newtext = re.sub(ur"(?im)== Véase también ==\r\n\* \[\[Lista de nodos de Podemos\]\]\r\n\r\n", ur"== Véase también ==\n* [[Podemos]]\n* [[Lista de círculos de Podemos]]\n\n", newtext)

        if wtext != newtext:
            wikipedia.showDiff(wtext, newtext)
            page.put(newtext, u"BOT - Unificando círculos")
        
if __name__ == '__main__':
    main()
