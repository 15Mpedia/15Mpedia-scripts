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
import datetime
import re
import os
import subprocess
import sys
import time
import pagegenerators
import urllib2
import wikipedia

"""
Bot para copiar la duración y tags de YouTube
"""

def main():
    site = wikipedia.Site('15mpedia', '15mpedia')
    cat = catlib.Category(site, u"Category:Archivos en YouTube")
    gen = pagegenerators.CategorizedPageGenerator(cat, start=u'Archivo:YouTube - raffaellopinta - mnQdKhVzRek.jpg')
    pre = pagegenerators.PreloadingGenerator(gen, pageNumber=60)
    
    for page in pre:
        wtitle = page.title()
        wtext = page.get()
        
        print wtitle
        if re.search(ur"\|\s*palabras[ _]clave\s*=", wtext) and \
            re.search(ur"\|\s*duración\s*=", wtext):
            print u"Nada que añadir"
            continue
        
        youtubeid = re.findall(ur'(?im)\|\s*embebido id\s*=\s*([^\r\n]*?)[\r\n]', wtext)[0]
        youtubeid = re.sub(' ', '_', youtubeid)
        youtubeurl = 'http://www.youtube.com/watch?v=%s' % (youtubeid)
        req = urllib2.Request(youtubeurl, headers={ 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0' })
        raw = unicode(urllib2.urlopen(req).read(), 'utf-8')
        
        if not re.search(ur"'IS_UNAVAILABLE_PAGE': false,", raw) and re.search(ur"<h1 id=\"unavailable-message\"", raw): 
            disponibilidad = u""
            if re.search(ur"<h1 id=\"unavailable-message\" class=\"message\">[^<]*?(This video is unavailable|Este vídeo no está disponible)[^<]*?</h1>", raw):
                disponibilidad = u"unavailable"
            elif re.search(ur"<h1 id=\"unavailable-message\" class=\"message\">[^<]*?(This video is private|Este vídeo es privado)[^<]*?</h1>", raw):
                disponibilidad = u"private"
            elif re.search(ur"<h1 id=\"unavailable-message\" class=\"message\">[^<]*?(cancelado la cuenta)[^<]*?</h1>", raw):
                disponibilidad = u"canceled-account"
            elif re.search(ur"<h1 id=\"unavailable-message\" class=\"message\">[^<]*?(El usuario ha suprimido este vídeo)[^<]*?</h1>", raw):
                disponibilidad = u"deleted-by-user"
            elif re.search(ur"<h1 id=\"unavailable-message\" class=\"message\">[^<]*?(el usuario que lo ha subido ha cerrado su cuenta)[^<]*?</h1>", raw):
                disponibilidad = u"account-closed-by-user"
            else:
                print u"New error message for video"
                print youtubeid
                print re.findall(ur"<h1 id=\"unavailable-message\"[^>]*?>\s*([^<]*?)\s*</h1>", raw)
                sys.exit()
            
            if disponibilidad:
                newtext = wtext
                summary = []
                if re.search(ur"(?im)\|\s*disponibilidad\s*=", newtext):
                    newtext = re.sub(ur"(?im)\|\s*disponibilidad\s*=\s*[a-z\s*-]+?(?P<g1>[\r\n])", ur"|disponibilidad=%s\g<g1>" % (disponibilidad), newtext)
                else:
                    newtext = re.sub(ur"(?im)(?P<g1>\|autor)", ur"|disponibilidad=%s\n\g<g1>" % (disponibilidad), newtext)
                summary.append(u"disponibilidad=%s" % (disponibilidad))
                
                if newtext != wtext:
                    wikipedia.showDiff(wtext, newtext)
                    summary = u', '.join(summary)
                    print summary
                    page.put(newtext, u"BOT - Añadiendo: %s" % summary)
                    time.sleep(3)
        else:
            youtubetags = []
            m = re.findall(ur"(?im)<meta property=\"og:video:tag\" content=\"([^>]*?)\">", raw)
            if m:
                for tag in m:
                    youtubetags.append(tag)
            youtubetags = ', '.join(youtubetags)
            print youtubetags
            
            youtubeduration = ''
            youtubeduration = subprocess.Popen(["python", "youtube-dl", youtubeurl, "--get-duration"], stdout=subprocess.PIPE).communicate()[0].strip()
            print youtubeduration
            
            newtext = wtext
            summary = []
            if youtubeduration and not re.search(ur"(?im)\|\s*duración\s*=", newtext):
                newtext = re.sub(ur"(?im)(?P<g1>\|autor)", ur"|duración=%s\n\g<g1>" % (youtubeduration), newtext)
                summary.append(u"duración=%s" % (youtubeduration))
            if youtubetags and not re.search(ur"(?im)\|\s*palabras clave\s*=", newtext):
                newtext = re.sub(ur"(?im)(?P<g1>\|autor)", ur"|palabras clave=%s\n\g<g1>" % (youtubetags), newtext)
                summary.append(u"palabras clave=%s" % (youtubetags))
            
            if newtext != wtext:
                wikipedia.showDiff(wtext, newtext)
                summary = u', '.join(summary)
                print summary
                page.put(newtext, u"BOT - Añadiendo: %s" % summary)
                time.sleep(3)
        
if __name__ == '__main__':
    main()

