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
            raw = unicode(f.read(), 'utf-8')
            f.close()
            
            news = {}
            m = re.findall(ur'(?im)<h2><a href="([^<>]+?)">([^<>]+?)</a></h2>', raw)
            for i in m:
                #print i
                news[i[0]] = h.unescape(i[1])
            
            news2 = []
            m = re.findall(ur'(?im)data-url="(http://www\.lamarea\.com/(\d\d\d\d/\d\d/\d\d)/[^<> ]+?)" class="social-button ot-share"', raw)
            for i in m:
                #print i
                news2.append([i[0], re.sub('/', '-', i[1])])
            
            for url, fecha in news2:
                if news.has_key(url):
                    title = news[url]
                    output = u"* {{noticia|titular=%s|enlace=%s|fuente=La Marea|fecha=%s}}" % (title, url, fecha)
                    l.append([fecha, output])
    
    l.sort()
    c = 0
    for ll in l:
        if c % 10 == 0:
            print '\n== %d-%d ==\n' % (c, c+10)
        print ll[1].encode('utf-8')
        c += 1

if __name__ == '__main__':
    main()
