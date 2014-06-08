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

month2number = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}

def main():
    user = re.sub(u'\+', u' ', sys.argv[1])
    print 'Downloading videos for user:', user
    skipuntil = ''
    if len(sys.argv) > 2:
        skipuntil = sys.argv[2]

    channel = 'http://bambuser.com/channel/%s' % (user)
    rss = 'http://feed.bambuser.com/channel/%s.rss' % (user)

    #load bambuser ids imported in the past (to exclude them)
    print 'Loading ids of bambuser videos uploaded in the past, please wait'
    pageimported = wikipedia.Page(wikipedia.Site("15mpedia", "15mpedia"), u"Usuario:Emijrp/bambuser ids")
    pageimported.put(u"{{#ask:[[embebido::Bambuser]]|mainlabel=-|?embebido id=|limit=100000}}", u"BOT - Updating")
    f = urllib.urlopen('http://wiki.15m.cc/wiki/Usuario:Emijrp/bambuser_ids')
    html = unicode(f.read(), 'utf-8')
    imported = html.split('<div id="mw-content-text" lang="es" dir="ltr" class="mw-content-ltr"><p>')[1].split('</p>')[0].strip().split(', ')
    print len(imported), 'bambuser streamings imported in the past'
    
    raw = urllib.urlopen(channel).read()
    user = re.findall(ur"(?im)<span class=\"username\" title=\"([^<>]+?)\"></span>", raw)[0]
    raw = urllib.urlopen(rss).read()
    lastvideoid = re.findall(ur"(?im)<link>http://bambuser\.com/v/(\d+)</link>", raw)[0]

    videoids = []
    thumbs = []
    c = 0
    pageurl = "http://bambuser.com/v/%s?page_profile_more_user=" % (lastvideoid)
    raw2 = unicode(urllib.urlopen(pageurl).read(), 'utf-8')
    limit = 1
    try:
        limit = int(re.findall(ur"(?im)page_profile_more_user=\d+\">(\d+)</a></li></ul>", raw2)[0])
    except:
        pass
    print 'Scraping videos from %d pages' % (limit)
    while c < limit:
        pageurl2 = pageurl + str(c)
        raw3 = urllib.urlopen(pageurl2).read()
        videoids += re.findall(ur"(?im)<a class=\"preview-wrapper\" href=\"http://bambuser.com/v/(\d+)\">", raw3)
        c += 1
        #break

    print 'Loaded ids for %d videos' % (len(videoids))
    
    videos = {}
    c = 0
    if skipuntil:
        print 'Skipping until', skipuntil

    for videoid in videoids:
        if skipuntil:
            if videoid == skipuntil:
                skipuntil = ''
            continue
            
        if videoid in imported:
            print 'Video %s was imported in the past, skipping' % (videoid)
            continue
        else:
            print 'Downloading metadata and screenshot for video %s' % (videoid)
        
        videourl = "http://bambuser.com/v/%s" % (videoid)
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
                coord = '%s, %s' % (coord[0], coord[1])
        except:
            coord = ''
        date = ''
        date2 = ''
        hour = ''
        try:
            date2 = re.findall(ur"(?im)<div id=\"broadcast-date\">\s*<p>([^<]*?)</p>", raw4)[0]
        except:
            date2 = re.findall(ur"(?im)<div id=\"broadcast-date\">\s*<p id=\"upload-recorded-date\"><span class=\"date-label\">Recorded </span>([^<]*?)<br>", raw4)[0]
        #9 Nov 2009 18:39 CET
        if not ':' in date2.split(' ')[2] and int(date2.split(' ')[2]) > 2000 and int(date2.split(' ')[2]) < 2020:
            date = '%s/%s/%02d' % (date2.split(' ')[2], month2number[date2.split(' ')[1].lower()], int(date2.split(' ')[0]))
            hour = date2.split(' ')[3]
        else:
            date = '%s/%s/%02d' % (datetime.datetime.now().year, month2number[date2.split(' ')[1].lower()], int(date2.split(' ')[0]))
            hour = date2.split(' ')[2]
        
        if not likes:
            likes = '0'
        tags = re.findall(ur"(?im)<span class=\"tag\" style=\"display:none;\" title=\"([^>]*?)\"></span>", raw4)
        
        ignoredupes = 'default-preview' in thumburl and True or False
        #[videoid, coord, date, hour, likes, views, lives, title, ', '.join(tags), user]
        infobox = u"{{Infobox Archivo\n|embebido=Bambuser\n|embebido id=%s\n|embebido usuario=%s\n|embebido título=%s\n|fecha de creación=%s\n|fecha de publicación=%s\n|autor={{bambuser channel|%s}}\n|coordenadas=%s\n}}" % (videoid, user, title, date, date, user, coord)
        #https://www.mediawiki.org/wiki/Manual:Pywikibot/upload.py
        os.system('python upload.py -lang:15mpedia -family:15mpedia -keep %s -filename:"%s" -noverify "%s" "%s"' % (ignoredupes and '-ignoredupes' or '', imagename.encode('utf-8'), thumburl.encode('utf-8'), infobox.encode('utf-8')))

        c += 1

if __name__ == '__main__':
    main()
