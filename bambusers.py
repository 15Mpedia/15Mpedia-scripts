#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012-2014 emijrp <emijrp@gmail.com>
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
import sys
import time
import urllib
import wikipedia

"""
Este bot lee los nicks de usuarios de bambusers de
http://wiki.15m.cc/wiki/Lista_de_streamings_en_Bambuser
Y mira en la web de Bambuser a ver si hay nuevos streamings para esos
usuarios. En caso afirmativo, sube una captura y los metadatos de 
cada nuevo streaming.
"""

month2number = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}

def main():
    users = []
    if len(sys.argv) > 1:
        users.append(re.sub(u'\+', u' ', sys.argv[1]))
    else:
        f = urllib.urlopen(u'http://wiki.15m.cc/wiki/Lista_de_streamings_en_Bambuser')
        html = unicode(f.read(), 'utf-8')
        html = html.split(u'id="Nube_de_usuarios"')[1].split(u'<h2>')[0]
        users = re.findall(ur">([^<>]+?)</a>", html)
        
    print u'Downloading Bambuser metadata for %d users:\n%s' % (len(users), users)
    
    skip = u''
    for user in users:
        if skip:
            if skip == user:
                skip = ''
            else:
                print 'Skipping', user
                continue
        
        print u'=== %s ===' % user
        channel = u'http://bambuser.com/channel/%s' % (user)
        rss = u'http://feed.bambuser.com/channel/%s.rss' % (user)

        #load bambuser ids imported in the past (to exclude them)
        print u'Loading ids of bambuser videos uploaded in the past, please wait'
        
        """
        pageimported = wikipedia.Page(wikipedia.Site("15mpedia", "15mpedia"), u"Usuario:Emijrp/bambuser ids")
        pageimported.put(u"{{#ask:[[embebido::Bambuser]]|mainlabel=-|?embebido id=|limit=100000}}", u"BOT - Updating")
        f = urllib.urlopen('http://wiki.15m.cc/wiki/Usuario:Emijrp/bambuser_ids')
        html = unicode(f.read(), 'utf-8')
        imported = html.split('<div id="mw-content-text" lang="es" dir="ltr" class="mw-content-ltr"><p>')[1].split('</p>')[0].strip().split(', ')
        """
        queryurl = "http://wiki.15m.cc/w/index.php?title=Especial:Ask&offset=0&limit=5000&q=[[embebido%%3A%%3ABambuser]][[embebido%%20usuario%%3A%%3A%s]]&p=mainlabel%%3D-2D%%2Fformat%%3Dbroadtable&po=%%3FEmbebido+id%%3D%%0A" % (re.sub(ur"[ \+]", u"%20", user).encode('utf-8'))
        f = urllib.urlopen(queryurl)
        html = unicode(f.read(), 'utf-8')
        imported = re.findall(ur"(?im)<td data-sort-value=\"(\d+)\">", html)
        print '%d bambuser streamings imported in the past' % len(imported)
        
        raw = unicode(urllib.urlopen(channel.encode('utf-8')).read(), 'utf-8')
        user = re.findall(ur"(?im)<span class=\"username\" title=\"([^<>]+?)\"></span>", raw)[0]
        raw =  unicode(urllib.urlopen(rss.encode('utf-8')).read(), 'utf-8')
        lastvideoid = re.findall(ur"(?im)<link>http://bambuser\.com/v/(\d+)</link>", raw)[0]

        videoids = []
        thumbs = []
        c = 0
        pageurl = u"http://bambuser.com/v/%s?page_profile_more_user=" % (lastvideoid)
        raw2 = unicode(urllib.urlopen(pageurl).read(), 'utf-8')
        limit = 1
        try:
            limit = int(re.findall(ur"(?im)page_profile_more_user=\d+\">(\d+)</a></li></ul>", raw2)[0])
        except:
            pass
        print u'Scraping videos from %d pages' % (limit)
        while c < limit:
            pageurl2 = pageurl + str(c)
            raw3 = urllib.urlopen(pageurl2).read()
            videoids += re.findall(ur"(?im)<a class=\"preview-wrapper\" href=\"http://bambuser.com/v/(\d+)\">", raw3)
            c += 1
            sys.stderr.write('.') # progress
            time.sleep(1)
            #break

        print u'Loaded ids for %d videos' % (len(videoids))
        
        videos = {}
        c = 0
        for videoid in videoids:
            if videoid in imported:
                print u'Video %s was imported in the past, skipping' % (videoid)
                continue
            else:
                print u'Downloading metadata and screenshot for video %s' % (videoid)
            
            videourl = u"http://bambuser.com/v/%s" % (videoid)
            raw4 = unicode(urllib.urlopen(videourl).read(), 'utf-8')
            title = re.findall(ur"<span class=\"title\" title=\"([^>]*?)\"></span>", raw4)[0]
            title = re.sub(ur"[\"\[\]]", u"", title)
            thumburl = re.findall(ur"(?im)<meta property=\"og:image\" content=\"([^>]*?)\" />", raw4)[0].split('?')[0] #removing trailing .jpg?2
            imagename = u"Bambuser - %s - %s.%s" % (user, videoid, thumburl.split('.')[-1])
                
            try:
                [likes, views, lives] = re.findall(ur"(?im)<div class=\"like\" data-upvotes=\"([0-9]+?)\">.*?<span class=\"broadcast-views\"><span class=\"views-total\">([0-9]+?)</span> views \(<span class=\"views-live\">([0-9]+?)</span>", raw4)[0]
            except:
                [likes, views, lives] = ['0', '0', '0']
            comments = ''
            try:
                coord = re.findall(ur"(?im)<meta property=\"bambuser_com:position:latitude\" content=\"([^\"]+?)\" /><meta property=\"bambuser_com:position:longitude\" content=\"([^\"]+?)\" />", raw4)[0]
                if coord:
                    coord = u'%s, %s' % (coord[0], coord[1])
            except:
                coord = u''
            date = u''
            date2 = u''
            hour = u''
            try:
                date2 = re.findall(ur"(?im)<div id=\"broadcast-date\">\s*<p>([^<]*?)</p>", raw4)[0]
            except:
                date2 = re.findall(ur"(?im)<div id=\"broadcast-date\">\s*<p id=\"upload-recorded-date\"><span class=\"date-label\">Recorded </span>([^<]*?)<br>", raw4)[0]
            #9 Nov 2009 18:39 CET
            if not ':' in date2.split(' ')[2] and int(date2.split(' ')[2]) > 2000 and int(date2.split(' ')[2]) < 2020:
                date = u'%s/%s/%02d' % (date2.split(' ')[2], month2number[date2.split(' ')[1].lower()], int(date2.split(' ')[0]))
                hour = date2.split(' ')[3]
            else:
                date = u'%s/%s/%02d' % (datetime.datetime.now().year, month2number[date2.split(' ')[1].lower()], int(date2.split(' ')[0]))
                hour = date2.split(' ')[2]
            
            if not likes:
                likes = u'0'
            tags = re.findall(ur"(?im)<span class=\"tag\" style=\"display:none;\" title=\"([^>]*?)\"></span>", raw4)
            
            device = ''
            m = re.findall(ur"(?im)<h4 class=\"n-semibold\">Phone model</h4>\s*?<p class=\"less-margin\">(.*?)</p>", raw4)
            if m:
                device = m[0]
            else:
                m = re.findall(ur"(?im)<h4 class=\"n-semibold\">Broadcast client</h4>\s*?<p class=\"less-margin\">(.*?)</p>", raw4)
                if m:
                    device = m[0]
            print device
            
            duration = ''
            duration = subprocess.Popen(["python", "youtube-dl", videorurl, "--get-duration"], stdout=subprocess.PIPE).communicate()[0].strip()
            print duration
            
            ignoredupes = u'default-preview' in thumburl and True or False
            #[videoid, coord, date, hour, likes, views, lives, title, ', '.join(tags), user]
            infobox = u"{{Infobox Archivo\n|embebido=Bambuser\n|embebido id=%s\n|embebido usuario=%s\n|embebido título=%s\n|fecha de creación=%s %s\n|fecha de publicación=%s %s\n|duración=%s\n|dispositivo=%s\n|autor={{bambuser channel|%s}}\n|coordenadas=%s\n}}" % (videoid, user, title, date, hour, date, hour, duration, device, user, coord)
            #https://www.mediawiki.org/wiki/Manual:Pywikibot/upload.py
            execmd = u'python upload.py -lang:15mpedia -family:15mpedia -keep %s -filename:"%s" -noverify "%s" "%s"' % (ignoredupes and u'-ignoredupes' or u'', imagename, thumburl, infobox)
            os.system(execmd.encode('utf-8'))

            c += 1
            time.sleep(1)

if __name__ == '__main__':
    main()
