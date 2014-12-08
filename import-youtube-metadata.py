#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 emijrp
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

import os
import re
import subprocess
import sys
import time
import urllib
import urllib2
import wikipedia

""" Bot que importa metadatos y capturas de vídeos de YouTube """

month2month = { 'ene': '01', 'feb': '02', 'mar': '03', 'abr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'ago': '08', 'sep': '09', 'sept': '09', 'oct': '10', 'nov': '11', 'dic': '12'}

def unquote(s):
    s = re.sub(ur"&quot;", u'"', s)
    s = re.sub(ur"&#39;", u"'", s)
    s = re.sub(ur"\|", u"-", s)
    s = re.sub(ur'\\"', u'"', s)
    s = re.sub(ur'[\[\]]', u'', s)
    return s

def main():
    ids = open('youtube-videoids.txt', 'r').read().splitlines()
    
    for id in ids:
        url = 'http://www.youtube.com/watch?v=%s' % (id)
        print '\n#########################################\n', url
        
        queryurl = 'http://wiki.15m.cc/w/index.php?title=Especial:Ask&q=[[embebido%3A%3AYouTube]][[embebido+id%3A%3A'+id+']]&p=format%3Dbroadtable%2Flink%3Dall%2Fheaders%3Dshow%2Fsearchlabel%3D-26hellip%3B-20siguientes-20resultados%2Fclass%3Dsortable-20wikitable-20smwtable&eq=no'
        f = urllib.urlopen(queryurl)
        html = unicode(f.read(), 'utf-8')
        m = re.findall(ur'(?im)<td><a href=[^<>]+?>(YouTube - [^<>]+?)</a></td>', html)
        if m:
            print u'Video %s was imported in the past, skipping http://wiki.15m.cc/wiki/File:%s' % (id, re.sub(' ', '_', m[0]))
            continue
        else:
            print u'Downloading metadata and screenshot for video %s' % (id)
        
        req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0 (Chrome)'})
        raw = unicode(urllib2.urlopen(req).read(), 'utf-8')
                
        try:
            title = re.findall(ur'<meta property="og:title" content="([^>]+?)">', raw)[0]
            title = unquote(title)
            thumburl = re.findall(ur'<meta property="og:image" content="([^>]+?)">', raw)[0]
            desc = unquote(unicode(subprocess.Popen(["python", "youtube-dl", url, "--get-description"], stdout=subprocess.PIPE).communicate()[0], 'utf-8')).strip()
            if desc == u'No description available.':
                desc = u''
            date = re.findall(ur'<strong class="watch-time-text">(?:Actualizado|Publicado) el (\d+) de ([^<>\.]+)\.? de (\d\d\d\d)</strong>', raw)[0]
            date = u'%s-%s-%02d' % (date[2], month2month[date[1]], int(date[0]))
            embebeduser = ''
            uploaderuser = ''
            uploaderchannel = ''
            uploadernick = ''
            if re.search(ur'<link itemprop="url" href="http://www.youtube.com/user/([^>]+?)">', raw):
                uploaderuser = re.findall(ur'<link itemprop="url" href="http://www.youtube.com/user/([^>]+?)">', raw)[0]
                embebeduser = uploaderuser
            else:
                uploadernick = re.findall(ur'"author": "([^>,"]+?)",', raw)[0]
                uploaderchannel = re.findall(ur'<link itemprop="url" href="http://www.youtube.com/channel/([^>]+?)">', raw)[0]
                embebeduser = uploaderchannel
            license = u'{{cc-by-3.0}}'
            if not re.search(ur"(?i)/t/creative_commons", raw):
                license = u'{{lye}}'
            tags = []
            m = re.findall(ur"(?im)<meta property=\"og:video:tag\" content=\"([^>]*?)\">", raw)
            if m:
                for tag in m:
                    tag = re.sub('&39;', "'", tag)
                    tags.append(tag)
            tags = ', '.join(tags)
            duration = subprocess.Popen(["python", "youtube-dl", url, "--get-duration"], stdout=subprocess.PIPE).communicate()[0].strip()
        except:
            print u'Error accediendo a los parámetros del vídeo', id
            g = open('youtube-errors.ids', 'a')
            g.write(u'%s\n' % (id))
            g.close()
            time.sleep(5)
            continue
        
        infobox = ''
        if uploaderuser:
            infobox = u"""{{Infobox Archivo\n|embebido=YouTube\n|embebido id=%s\n|embebido usuario=%s\n|embebido título=%s\n|descripción=%s\n|fecha de publicación=%s\n|autor={{youtube channel|%s}}\n|palabras clave=%s\n|duración=%s\n|licencia=%s\n}}""" % (id, embebeduser, title, desc and u'{{descripción de youtube|1=%s}}' % (desc) or u'', date, uploaderuser, tags, duration, license)
        else:
            infobox = u"""{{Infobox Archivo\n|embebido=YouTube\n|embebido id=%s\n|embebido usuario=%s\n|embebido título=%s\n|descripción=%s\n|fecha de publicación=%s\n|autor={{youtube channel|%s|%s}}\n|palabras clave=%s\n|duración=%s\n|licencia=%s\n}}""" % (id, embebeduser, title, desc and u'{{descripción de youtube|1=%s}}' % (desc) or u'', date, uploaderchannel, uploadernick, tags, duration, license)
        
        imagename = 'YouTube - %s - %s.jpg' % (embebeduser, id)
        print 'Importing here http://wiki.15m.cc/wiki/Archivo:%s' % (re.sub(' ', '_', imagename))
        #print infobox
        infoboxfilename = 'youtube-infobox.txt'
        with open(infoboxfilename, 'w') as d:
            d.write(infobox.encode('utf-8'))
        execmd = u'python upload.py -lang:15mpedia -family:15mpedia -keep -ignoredupes -filename:"%s" -noverify -description-file:%s "%s"' % (imagename, infoboxfilename, thumburl)
        os.system(execmd.encode('utf-8'))
        os.remove(infoboxfilename)
        time.sleep(5)
        
if __name__ == '__main__':
    main()
