#!/usr/bin/python
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

import datetime
import os
import re
import subprocess
import sys
import time
import urllib
import urllib2
import pywikibot
import upload

""" Bot que importa metadatos y capturas de vídeos de Livestream """

month2month = { 'ene': '01', 'feb': '02', 'mar': '03', 'abr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'ago': '08', 'sep': '09', 'sept': '09', 'oct': '10', 'nov': '11', 'dic': '12'}

def unquote(s):
    s = re.sub(ur"&quot;", u'"', s)
    s = re.sub(ur"&#39;", u"'", s)
    s = re.sub(ur"\|", u"-", s)
    s = re.sub(ur'\\"', u'"', s)
    s = re.sub(ur'[\[\]]', u'', s)
    return s

def main():
    site = pywikibot.Site('15mpedia', '15mpedia')
    
    users = ['spanishrevolutionsol']
    skip = 'http://livestre.am/4IVFh'
    
    for user in users:
        folderurl = 'http://original.livestream.com/%s/folder' % (user)
        req = urllib2.Request(folderurl, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0 (Chrome)'})
        raw = unicode(urllib2.urlopen(req).read(), 'utf-8')
        
        streamings = re.findall(ur'(?im)<li class="video">\s*<a href="(http://livestre.am/[^"]+?)"\s*rel="nofollow"\s*title="([^>]+?)"\s*class="thumbnail">\s*<span class="mask"></span>\s*<span\s*class="time">([^<]+?)</span>\s*<img\s*class="img"\s*style="[^"]+?"\s*src="/images/blank.png"\s*original="([^"]+?)"\s*onerror="handlingBrokenThumbnail\(this\)"\s*/>\s*<span\s*class="isMobileCompatible"\s*style="display:none;">true</span>\s*</a>\s*<h3><a href="http://livestre.am/[^"]+"\s*rel="nofollow"\s*title="[^>]+?">[^<]+?</a></h3>\s*<ul class="meta">\s*</ul>\s*<div class="tooltip-content" style="display:none">\s*<div class="header">\s*<h4 class="title">[^<]+?</h4>\s*<p class="date">([^<]+?)</p>\s*</div>', raw)
        for streaming in streamings:
            streamingurl, title, duration, thumburl, recorddate = streaming
            
            if skip:
                if skip == streamingurl:
                    skip = ''
                else:
                    continue
            
            title2 = re.sub(ur'[\[\]]', ur'', title)
            print '#'*50, '\n', title, '\n', '#'*50, '\n'
            print streamingurl, duration
            #print thumburl
            req2 = urllib2.Request(streamingurl, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0 (Chrome)'})
            raw2 = unicode(urllib2.urlopen(req2).read(), 'utf-8')
            clipid = re.findall(ur'(?im)<meta property="og:url" content="http://original.livestream.com/[^/]+/video/([^"]+?)"/>', raw2)[0]
            #print clipid
            
            date = u''
            if thumburl == '/images/blank.png':
                thumburl = 'https://upload.wikimedia.org/wikipedia/commons/e/e7/Empty_place.jpg'
                days = int(re.findall(ur'(?im)class="time">Created (\d+) days ago', raw2)[0])
                d = datetime.datetime.now() - datetime.timedelta(days=days)
                date = d.strftime('%Y-%m-%d')
            else:
                date = thumburl.split('/')
                date = u'%s-%s-%s' % (date[-4], date[-3], date[-2])
            #print date
            desc = re.findall(ur'(?im)<meta name="description" content="([^>]+?)" />', raw2)[0]
            if desc.startswith(title) and desc.endswith('Be There.'):
                desc = ''
            #print desc
              
            keywords = re.findall(ur'(?im)<meta name="keywords" content="([^>]+?)" />', raw2)[0].split(' ')
            keywords.remove('@')
            keywords.remove('ustream:')
            #print keywords
            
            queryurl = 'http://15mpedia.org/w/index.php?title=Especial:Ask&q=[[embebido%3A%3ALivestream]][[embebido+id%3A%3A'+clipid+']]&p=format%3Dbroadtable%2Flink%3Dall%2Fheaders%3Dshow%2Fsearchlabel%3D-26hellip%3B-20siguientes-20resultados%2Fclass%3Dsortable-20wikitable-20smwtable&eq=no'
            req3 = urllib.urlopen(queryurl)
            raw3 = unicode(req3.read(), 'utf-8')
            m3 = re.findall(ur'(?im)<td><a href=[^<>]+?>(Livestream - [^<>]+?)</a></td>', raw3)
            if m3:
                print u'Streaming %s was imported in the past, skipping https://15mpedia.org/wiki/Archivo:%s' % (clipid, re.sub(' ', '_', m3[0]))
                continue
            else:
                print u'Importing streaming %s' % (clipid)
            
            infobox = u"""{{Infobox Archivo\n|embebido=Livestream\n|embebido id=%s\n|embebido usuario=%s\n|embebido título=%s\n|descripción=%s\n|fecha de creación=%s\n|fecha de publicación=%s\n|autor={{livestream channel|%s}}\n|palabras clave=%s\n|duración=%s\n}}""" % (clipid, user, title2, desc and u'{{descripción de livestream|1=%s}}' % (desc) or u'', date, date, user, u', '.join(keywords), duration)
            
            #print infobox
            
            imagename = 'Livestream - %s - %s.jpg' % (user, clipid)
            print 'Importing here https://15mpedia.org/wiki/Archivo:%s' % (re.sub(' ', '_', imagename))
            
            imagepage = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), u'File:%s' % imagename)
            if imagepage.exists():
                print 'La pagina de imagen File:%s ya existe. No subimos' % (imagename)
                continue
            
            bot = upload.UploadRobot([thumburl], description=infobox, useFilename=imagename, keepFilename=True, verifyDescription=False, targetSite=site, uploadByUrl=True, ignoreWarning=['duplicate'])
            bot.run()
            
            time.sleep(1)
        sys.exit()
    
    time.sleep(5)
        
if __name__ == '__main__':
    main()
