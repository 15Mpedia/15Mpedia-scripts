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

import HTMLParser
import os
import re

def main():
    l = []
    h = HTMLParser.HTMLParser()
    for root, dirs, files in os.walk("."):
        for filename in files:
            filepath = os.path.join(root, filename)
            #print filepath
            f = open(filepath, 'r')
            raw = unicode(f.read(), 'iso-8859-1')
            #raw = f.read()
            f.close()
            
            m = re.findall(ur'(?im)<span class="titulo">([^<>]+?)</span>', raw)
            title = m and m[0] or ''
            title = h.unescape(title)
            m = re.findall(ur'(?im)<a href=\'(http://www\.mundoobrero\.es/pl\.php\?id=\d+)\' name=\'fb_share\'', raw)
            url = m and m[0] or ''
            m = re.findall(ur'(?im)<span class="fecha">(\d\d/\d\d/\d\d\d\d)</span>', raw)
            fecha = m and m[0] or ''
            if fecha:
                fecha = fecha.split('/')[2] + '-' + fecha.split('/')[1] + '-' + fecha.split('/')[0]
            
            if title and url and fecha:
                output = "* {{noticia|titular=%s|enlace=%s|fuente=Mundo Obrero|fecha=%s}}" % (title, url, fecha)
                c = int(url.split('?id=')[1])
                l.append([c, output])
    
    l.sort()
    c = 0
    for ll in l:
        if c % 10 == 0:
            print u'\n== %d-%d ==' % (c+1, c+10)
        print ll[1].encode('iso-8859-1')
        c += 1

if __name__ == '__main__':
    main()
