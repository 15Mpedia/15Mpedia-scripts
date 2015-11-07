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
    """<meta property="og:title" content="Fidel: Inhabilitación de Córdoba y asesinato de &#039;Mono Jojoy&#039; alejan a Colombia de la paz" />
<meta property="og:url" content="http://www.librered.net/?p=6" />
<meta property="og:description" content="El líder de la revolución cubana, Fidel Castro, aseguró que la noticia de la inhabilitación de la senadora colombiana Piedad Córdoba, ordenada por la Procuraduría General de la República (PGR), y e..." />"""
    
    l = []
    h = HTMLParser.HTMLParser()
    for root, dirs, files in os.walk("."):
        for filename in files:
            filepath = os.path.join(root, filename)
            #print filepath
            f = open(filepath, 'r')
            raw = unicode(f.read(), 'utf-8')
            f.close()
            
            m = re.findall(ur'(?im)<meta property="og:title" content="([^<>]+?)" />', raw)
            title = m and m[0] or ''
            title = h.unescape(title)
            m = re.findall(ur'(?im)<meta property="og:url" content="([^<>]+?)" />', raw)
            url = m and m[0] or ''
            m = re.findall(ur'(?im)<meta property="og:description" content="([^<>]+?)" />', raw)
            desc = m and m[0] or ''
            desc = h.unescape(desc)
            m = re.findall(ur'(?im)<meta property="article:published_time" content="(\d\d\d\d-\d\d-\d\d)T[^<>]+?" />', raw)
            fecha = m and m[0] or ''
            
            if title and url and desc:
                output = u"* {{noticia|titular=%s|enlace=%s|fuente=LibreRed|fecha=%s}}" % (title, url, fecha)
                c = int(url.split('?p=')[1])
                l.append([c, output])
    
    l.sort()
    c = 0
    for ll in l:
        if c % 10 == 0:
            print '\n== %d-%d ==' % (c, c+10)
        print ll[1].encode('utf-8')
        c += 1

if __name__ == '__main__':
    main()
