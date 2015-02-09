#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 emijrp
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
import datetime
import re
import os
import subprocess
import sys
import time
import pagegenerators
import urllib
import urllib2
import wikipedia

"""
Bot para copiar los tags de Flickr
"""

def main():
    site = wikipedia.Site('15mpedia', '15mpedia')
    cat = catlib.Category(site, u"Category:Imágenes")
    gen = pagegenerators.CategorizedPageGenerator(cat, start=u'Archivo:Carlosgimpera - 72157629735821900 - 7199341736.jpg')
    pre = pagegenerators.PreloadingGenerator(gen, pageNumber=60)
    
    for page in pre:
        wtitle = page.title()
        wtext = page.get()
        
        print wtitle
        if not re.search(ur"\|\s*autor\s*=\s*\{\{\s*flickr\s*\|", wtext) or \
           not re.search(ur"\|\s*fuente\s*=\s*\[https?://www\.flickr\.com\/photos\/[^/]+/\d+/", wtext):
            print u"No parece una imagen de Flickr"
            continue
        
        if re.search(ur"\|\s*palabras[ _]clave\s*=", wtext):
            print u"Nada que añadir"
            continue
        
        flickrphotourl = re.findall(ur"\|\s*fuente\s*=\s*\[(https?://www\.flickr\.com\/photos\/[^/]+/\d+/)", wtext)[0]
        req = urllib2.Request(flickrphotourl, headers={ 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0' })
        try:
            raw = unicode(urllib2.urlopen(req).read(), 'utf-8')
        except:
            time.sleep(10)
            try:
                raw = unicode(urllib2.urlopen(req).read(), 'utf-8')
            except:
                print "Error al leer la web"
                f = open('error-flickr.log', 'a')
                log = u'\n%s' % (wtitle)
                f.write(log.encode('utf-8'))
                f.close()
                continue
                #sys.exit()
        
        f = open('flickr.html', 'w')
        f.write(raw.encode('utf-8'))
        f.close()
        time.sleep(1)

        flickrtags = []
        m = re.findall(ur"(?im)data-ywa-name=\"Tag\(s\)\">([^>]+?)</a>", raw) #data-ywa-name="Tag(s)">educación</a>
        if m:
            for tag in m:
                flickrtags.append(tag)
            flickrtags_ = ', '.join(flickrtags)
            print flickrtags_
            
            newtext = wtext
            summary = []
            if flickrtags_ and not re.search(ur"(?im)\|\s*palabras clave\s*=", newtext):
                newtext = re.sub(ur"(?im)(?P<g1>\|\s*autor)", ur"|palabras clave=%s\n\g<g1>" % (flickrtags_), newtext)
                summary.append(u"palabras clave=%s" % (flickrtags_))
            
            if newtext != wtext:
                wikipedia.showDiff(wtext, newtext)
                summary = u', '.join(summary)
                print summary
                page.put(newtext, u"BOT - Añadiendo: %s" % summary)
                time.sleep(5)
        else:
            print u"No parece haber tags en Flickr para esta imagen"
        
if __name__ == '__main__':
    main()

