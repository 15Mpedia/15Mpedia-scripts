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
import time
import pagegenerators
import urllib2
import wikipedia

"""
Bot para copiar la fecha/hora, duración y modelo teléfono de Bambuser
"""

month2number = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}

def main():
    site = wikipedia.Site('15mpedia', '15mpedia')
    cat = catlib.Category(site, u"Category:Streamings filmados a una hora desconocida")
    gen = pagegenerators.CategorizedPageGenerator(cat) #, start=u'Archivo:Bambuser - suysulucha - 2956009.jpg')
    pre = pagegenerators.PreloadingGenerator(gen, pageNumber=60)
    
    for page in pre:
        wtitle = page.title()
        wtext = page.get()
        
        print wtitle
        if re.search(ur"\d\d\d\d[/-]\d\d[/-]\d\d \d\d:\d\d", wtext) and \
            re.search(ur"\|\s*duración", wtext) and \
            re.search(ur"\|\s*dispositivo", wtext):
            print u"Nada que añadir"
            continue
        
        bambuserid = wtitle.split('.jpg')[0].split(' - ')[-1]
        bambuserurl = 'http://bambuser.com/v/%s' % (bambuserid)
        req = urllib2.Request(bambuserurl, headers={ 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0' })
        raw = urllib2.urlopen(req).read()
                
        date = u''
        date2 = u''
        hour = u''
        try:
            date2 = re.findall(ur"(?im)<div id=\"broadcast-date\">\s*<p>([^<]*?)</p>", raw)[0]
        except:
            try:
                date2 = re.findall(ur"(?im)<div id=\"broadcast-date\">\s*<p id=\"upload-recorded-date\"><span class=\"date-label\">Recorded </span>([^<]*?)<br>", raw)[0]
            except:
                print u"El vídeo parece no disponible"
                continue
        #9 Nov 2009 18:39 CET
        if not ':' in date2.split(' ')[2] and int(date2.split(' ')[2]) > 2000 and int(date2.split(' ')[2]) < 2020:
            date = u'%s/%s/%02d' % (date2.split(' ')[2], month2number[date2.split(' ')[1].lower()], int(date2.split(' ')[0]))
            hour = date2.split(' ')[3]
        else:
            date = u'%s/%s/%02d' % (datetime.datetime.now().year, month2number[date2.split(' ')[1].lower()], int(date2.split(' ')[0]))
            hour = date2.split(' ')[2]
        
        bambuserdatetime = u'%s %s' % (date, hour)
        print bambuserdatetime
        
        bambuserdevice = ''
        m = re.findall(ur"(?im)<h4 class=\"n-semibold\">Phone model</h4>\s*?<p class=\"less-margin\">(.*?)</p>", raw)
        if m:
            bambuserdevice = m[0]
        else:
            m = re.findall(ur"(?im)<h4 class=\"n-semibold\">Broadcast client</h4>\s*?<p class=\"less-margin\">(.*?)</p>", raw)
            if m:
                bambuserdevice = m[0]
                                                
        bambuserduration = ''
        bambuserduration = subprocess.Popen(["python", "youtube-dl", bambuserurl, "--get-duration"], stdout=subprocess.PIPE).communicate()[0].strip()
        print bambuserduration
        
        newtext = wtext
        summary = []
        if bambuserdatetime and not re.search(ur"(?im)\d\d\d\d/\d\d/\d\d \d\d:\d\d", newtext):
            bambuserdatetime2 = u"(%s|%s)" % (bambuserdatetime.split(' ')[0], re.sub('/', '-', bambuserdatetime.split(' ')[0]))
            newtext = re.sub(ur"(?im)(?P<ini>\| *?fecha de creación *?= *?)%s(?P<end> *?\r\n)" % (bambuserdatetime2), ur"\g<ini>%s\g<end>" % (bambuserdatetime), newtext)
            newtext = re.sub(ur"(?im)(?P<ini>\| *?fecha de publicación *?= *?)%s(?P<end> *?\r\n)" % (bambuserdatetime2), ur"\g<ini>%s\g<end>" % (bambuserdatetime), newtext)
            summary.append(u"fecha de creación=%s" % (bambuserdatetime))
            summary.append(u"fecha de publicación=%s" % (bambuserdatetime))
        if bambuserduration and not re.search(ur"(?im)\|\s*duración\s*=", newtext):
            newtext = re.sub(ur"(?im)(?P<g1>\|autor)", ur"|duración=%s\n\g<g1>" % (bambuserduration), newtext)
            summary.append(u"duración=%s" % (bambuserduration))
        if bambuserdevice and not re.search(ur"(?im)\|\s*dispositivo\s*=", newtext):
            newtext = re.sub(ur"(?im)(?P<g1>\|autor)", ur"|dispositivo=%s\n\g<g1>" % (bambuserdevice), newtext)
            summary.append(u"dispositivo=%s" % (bambuserdevice))
        
        if newtext != wtext:
            wikipedia.showDiff(wtext, newtext)
            summary = u', '.join(summary)
            print summary
            page.put(newtext, u"BOT - Añadiendo: %s" % summary)
            time.sleep(2)
        
if __name__ == '__main__':
    main()

