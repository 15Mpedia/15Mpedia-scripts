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
    print 'Leyendo videos que aun no tienen parametro mirror'
    queryurl = 'http://15mpedia.org/w/index.php?title=Especial%3AAsk&q=[[Categor%C3%ADa%3AArchivos+en+YouTube]][[Categor%C3%ADa%3ACC+BY+3.0]][[Categor%C3%ADa%3AArchivos+sin+mirror]]&po=&eq=yes&p[format]=broadtable&sort_num=&order_num=ASC&p[limit]=5000&p[offset]=&p[link]=all&p[sort]=&p[headers]=show&p[mainlabel]=&p[intro]=&p[outro]=&p[searchlabel]=%26hellip%3B+siguientes+resultados&p[default]=&p[class]=sortable+wikitable+smwtable&eq=yes'
    f = urllib.urlopen(queryurl)
    html = unicode(f.read(), 'utf-8')
    #print html
    m = re.findall(ur'(?im)title="(Archivo:[^>]+?)">', html)
    
    for archivo in m:
        page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), archivo)
        if not page.exists():
            continue
        if not page.title().startswith('Archivo:YouTube - '):
            continue
        
        print '\n', '#'*40, '\n', page.title(), '\n', '#'*40, '\n'
        videoid = re.findall(ur'(?im)embebido id=([^\n]+)', page.text)[0]
        print videoid
        
        if re.search(ur'(?im)\|mirrors=.+\n', page.text):
            print 'Ya tiene mirror puesto'
            continue
        
        f = urllib.urlopen('https://archive.org/search.php?query=originalurl%%3A%%22https%%3A%%2F%%2Fwww.youtube.com%%2Fwatch%%3Fv%%3D%s%%22' % (videoid))
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
