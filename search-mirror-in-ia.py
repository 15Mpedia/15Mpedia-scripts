#!/usr/bin/env python
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

#This script generates redirects for wiki articles
#removing uppercase, accents and other symbols

import re
import sys
import urllib

import pywikibot
import pywikibot.pagegenerators as pagegenerators

def main():
    skip = ''
    site = pywikibot.Site('15mpedia', '15mpedia')
    cat = pywikibot.Category(site, u'Category:CC BY 3.0')
    files = cat.articles(namespaces=6)
    pre = pagegenerators.PreloadingGenerator(files, 100)
    
    skip = 'Archivo:YouTube - BarrioCanino - LVMh92Y4vOk.jpg'
    for page in pre:
        if skip:
            if page.title() == skip:
                skip = False
            else:
                continue
        
        if not page.exists():
            continue
        if not page.title().startswith('Archivo:YouTube - '):
            continue
        
        print page.title()
        videoid = re.findall(ur'(?im)embebido id=([^\n]+)', page.text)[0]
        print videoid
        
        if re.search(ur'(?im)\|mirrors=.+\n', page.text):
            print 'Ya tiene mirror puesto'
            continue
        
        f = urllib.urlopen('https://archive.org/search.php?query=%s%%20subject%%3A"spanishrevolution"' % (videoid))
        raw = f.read()
        if re.search(ur'Your search did not match any items in the Archive', raw):
            print u'No esta en Internet Archive'
        else:
            items = re.findall(ur'<div class="item-ia" data-id="([^>]+?)">', raw)
            if len(items) == 1:
                if not items[0].startswith('spanishrevolution'):
                    continue
                print 'Encontrado un item'
                print items[0]
                newtext = page.text
                newtext = re.sub(ur'(?im)(\|licencia=)', ur'|mirrors={{internet archive|id=%s}}\n\1' % (items[0]), newtext)
                page.text = newtext
                page.save(u'BOT - Añadiendo mirror: https://archive.org/details/%s' % (items[0]))
            elif len(items) > 1:
                print 'Hay mas de un item coincidente'
                print items
            else:
                print 'No se ha podido parsear el item'
    
if __name__ == '__main__':
    main()
