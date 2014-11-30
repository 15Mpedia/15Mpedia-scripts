#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 emijrp <emijrp@gmail.com>
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

from lxml import etree
import datetime
import time
import re
import sys
import urllib
import urllib2
import wikipedia
from xml.sax.saxutils import unescape

month2month = { 'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}

def uncode(s):
    try:
        xml = unicode(s, 'utf-8')
    except:
        try:
            xml = unicode(s, 'iso-8859-1')
        except:
            return s
    return xml

def getLines(page):
    p = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), page)
    raw = p.get()
    raw = re.sub(ur"(?im)^\*\s*", ur"", raw)
    rss = []
    for l in raw.splitlines():
        if not l.startswith('#'):
            rss.append(l)
    return rss

def sortLines(page):
    p = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), page)
    raw = list(set(p.get().splitlines()))
    raw.sort()
    p.put(ur"%s" % (u'\n'.join(raw)), u"BOT - Ordenando enlaces")

def getBlogs():
    print u'Loading RSS for blogs'
    queryurl = "http://wiki.15m.cc/w/index.php?title=Especial:Ask&limit=5000&q=[[Page+has+default+form%3A%3AAcampada||Asamblea||Banco_de_tiempo||Centro_social||Comisión||Grupo_de_trabajo||Realojo]]+[[nombre%3A%3A%2B]]+[[rss%3A%3A%2B]]&p=format%3Dbroadtable%2Flink%3Dall%2Fheaders%3Dshow%2Fmainlabel%3D-2D%2Fsearchlabel%3D-26hellip%3B-20siguientes-20resultados%2Fclass%3Dsortable-20wikitable-20smwtable&po=%3FRss%0A&eq=no"
    f = urllib.urlopen(queryurl)
    html = unicode(f.read(), 'utf-8')
    rss = list(set(re.findall(ur'(?im)<td class="Rss"><a class="external" href="([^<>]+)">', html)))
    rss.sort()
    print '%d RSS loaded' % (len(rss))
    
    content = []
    for url in rss:
        try:
            req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0 (Chrome)' })
            xml = uncode(urllib2.urlopen(req).read())
        except:
            continue
        #print xml[:100]
        
        if not re.search(ur'(<entry>|<item>)', xml):
            print u'Wrong RSS %s' % (url)
            continue
        
        sitetitle = u''
        if re.search(ur"(?im)>([^<>]*?)</title>", xml):
            sitetitle = re.findall(ur"(?im)>([^<>]*?)</title>", xml)[0]
        else:
            sitetitle = url
        print sitetitle
        
        try:
            chunks = []
            if re.search(ur'<entry>', xml):
                chunks = '</entry>'.join('<entry>'.join(xml.split('<entry>')[1:]).split('</entry>')[:-1]).split('</entry><entry>') #</entry><entry>
            elif re.search(ur'<item>', xml):
                chunks = ('<item>'.join('</item>'.join(xml.split('</item>')[:-1]).split('<item>')[1:])).split('</item>')
            
            for chunk in chunks:
                if not re.search(ur"(?im)</title>", chunk) or not re.search(ur"(?im)</(updated|pubdate)>", chunk):
                    continue
                
                title = u'Sin título'
                title = re.findall(ur"(?im)>([^<>]*?)</title>", chunk)[0].strip()
                updated = ''
                if re.search(ur'(?im)</updated>', chunk): #blogspot
                    updated = re.findall(ur"(?im)>([^<>]*?)</updated>", chunk)[0].strip()
                    updated = updated.split('T')[0]
                elif re.search(ur'(?im)</pubdate>', chunk): #wordpress, others
                    #<pubDate>Thu, 18 Sep 2014 11:30:44 +0000</pubDate>
                    t = re.findall(ur"(?im)<pubdate>[a-z]+, (\d\d) ([a-z]+) (\d\d\d\d) \d\d:\d\d:\d\d[\d \+]*?</pubdate>", chunk)[0]
                    updated = u'%s-%02d-%02d' % (t[2], int(month2month[t[1].lower()]), int(t[0]))
                url = ''
                if re.search(ur'<link rel=', chunk):
                    url = re.findall(ur"(?im)<link rel='alternate' type='text/html' href='([^<>]*?)' title='", chunk)[0].strip()
                elif re.search(ur'</link>', chunk):
                    url = re.findall(ur"(?im)<link>([^<>]*?)</link>", chunk)[0].strip()
                #print updated, title, url
                content.append([updated, sitetitle, title, url])
            #time.sleep(1)
        except:
            print u'Error'
        
    content.sort(reverse=True)
    return content

def getFacebook():
    # https://www.facebook.com/feeds/page.php?format=atom10&id=132849786851571
    
    rss = getLines(u'Actualizaciones en las redes/Facebook (RSS)')
    print 'Loaded %d RSS for Facebook' % (len(rss))
    
    content = []
    for url in rss:
        try:
            req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0 (Chrome)' })
            xml = uncode(urllib2.urlopen(req).read())
        except:
            continue
        chunks = [u'%s</entry>' % (s) for s in '</entry>'.join('<entry>'.join(xml.split('<entry>')[1:]).split('</entry>')[:-1]).split("""</entry>""")]
        
        sitetitle = u''
        if re.search(ur"(?im)>([^<>]*?)</name>", xml):
            sitetitle = re.findall(ur"(?im)>([^<>]*?)</name>", xml)[0]
        else:
            sitetitle = url
        
        for chunk in chunks:
            if not re.search(ur"(?im)</title>", chunk) or not re.search(ur"(?im)</published>", chunk):
                continue
        
            title = u'Sin título'
            title = unescape(re.findall(ur"(?im)<title>([^\n]*?)</title>", chunk)[0][10:-3])
            published = re.findall(ur"(?im)>([^<>]*?)</published>", chunk)[0]
            published = published.split('T')[0]
            url = re.findall(ur'(?im)<link rel="alternate" type="text/html" href="([^>]*?)" />', chunk)[0]
            
            #print published, title, url
            content.append([published, sitetitle, title, url])
        time.sleep(1)
    content.sort(reverse=True)
    return content 

def getFlickr():
    
    return []

def getN1():
    
    return []

def getYouTube():
    print u'Loading RSS for YouTube'
    queryurl = "http://wiki.15m.cc/w/index.php?title=Especial:Ask&limit=5000&q=[[Page+has+default+form%3A%3AAcampada||Asamblea||Banco_de_tiempo||Centro_social||Comisión||Grupo_de_trabajo||Realojo]]+[[nombre%3A%3A%2B]]+[[youtube%3A%3A%2B]]&p=format%3Dbroadtable%2Flink%3Dall%2Fheaders%3Dshow%2Fmainlabel%3D-2D%2Fsearchlabel%3D-26hellip%3B-20siguientes-20resultados%2Fclass%3Dsortable-20wikitable-20smwtable&po=%3FYoutube%0A&eq=no"
    f = urllib.urlopen(queryurl)
    html = unicode(f.read(), 'utf-8')
    t = list(set(re.findall(ur'(?im)<td class="Youtube"><a class="external" href="https?://www.youtube.com/(?:channel|user)/([^<>]+)/?">', html)))
    t.sort()
    rss = []
    for i in t:
        rss.append('http://gdata.youtube.com/feeds/base/videos?orderby=published&author=%s' % (i))
    print '%d RSS for YouTube loaded' % (len(rss))
    
    content = []
    for url in rss:
        try:
            req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0 (Chrome)' })
            xml = uncode(urllib2.urlopen(req).read())
        except:
            continue

        sitetitle = u''
        if re.search(ur"(?im)>([^<>]*?)</name>", xml):
            sitetitle = re.findall(ur"(?im)>([^<>]*?)</name>", xml)[1] #el 0 es YouTube, el 1 el nombre del canal
        else:
            sitetitle = url
        
        print sitetitle
        chunks = '</entry>'.join('<entry>'.join(xml.split('<entry>')[1:]).split('</entry>')[:-1]).split('</entry><entry>') #</entry><entry>
        
        try:
            for chunk in chunks:
                if not re.search(ur"(?im)</title>", chunk) or not re.search(ur"(?im)</published>", chunk):
                    continue
            
                title = u'Sin título'
                title = re.findall(ur"(?im)>([^<>]*?)</title>", chunk)[0]
                published = re.findall(ur"(?im)>([^<>]*?)</published>", chunk)[0]
                published = published.split('T')[0]
                url = re.findall(ur"(?im)<link rel='alternate' type='text/html' href='([^>&]*?)&", chunk)[0]
                
                #print published, title, url
                content.append([published, sitetitle, title, url])
            time.sleep(1)
        except:
            print u'Error'

    content.sort(reverse=True)
    return content

def getMonthName(m):
    if m == 1:
        return u'enero'
    elif m == 2:
        return u'febrero'
    elif m == 3:
        return u'marzo'
    elif m == 4:
        return u'abril'
    elif m == 5:
        return u'mayo'
    elif m == 6:
        return u'junio'
    elif m == 7:
        return u'julio'
    elif m == 8:
        return u'agosto'
    elif m == 9:
        return u'septiembre'
    elif m == 10:
        return u'octubre'
    elif m == 11:
        return u'noviembre'
    elif m == 12:
        return u'diciembre'
    else:
        return ''
    
def printContent(l, source=''):
    day0 = datetime.datetime.now().strftime('%Y-%m-%d')
    day1 = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    day2 = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
    day3 = (datetime.datetime.now() - datetime.timedelta(days=3)).strftime('%Y-%m-%d')
    
    day0_stuff = u"<noinclude>{{actualizaciones en las redes/inicio}}</noinclude>\n"
    day1_stuff = u"<noinclude>{{actualizaciones en las redes/inicio}}</noinclude>\n"
    day2_stuff = u"<noinclude>{{actualizaciones en las redes/inicio}}</noinclude>\n"
    day3_stuff = u"<noinclude>{{actualizaciones en las redes/inicio}}</noinclude>\n"
    for ll in l:
        [updated, sitetitle, title, url] = ll
        if updated == day0:
            day0_stuff += u"* {{actualización|titular=%s|enlace=%s|fuente=%s|fecha=%s}}\n" % (title, url, sitetitle, updated)
        if updated == day1:
            day1_stuff += u"* {{actualización|titular=%s|enlace=%s|fuente=%s|fecha=%s}}\n" % (title, url, sitetitle, updated)
        if updated == day2:
            day2_stuff += u"* {{actualización|titular=%s|enlace=%s|fuente=%s|fecha=%s}}\n" % (title, url, sitetitle, updated)
        if updated == day3:
            day3_stuff += u"* {{actualización|titular=%s|enlace=%s|fuente=%s|fecha=%s}}\n" % (title, url, sitetitle, updated)
    day0_stuff += u"<noinclude>{{actualizaciones en las redes/fin}}</noinclude>"
    day1_stuff += u"<noinclude>{{actualizaciones en las redes/fin}}</noinclude>"
    day2_stuff += u"<noinclude>{{actualizaciones en las redes/fin}}</noinclude>"
    day3_stuff += u"<noinclude>{{actualizaciones en las redes/fin}}</noinclude>"
    
    for k, v in [[day0, day0_stuff], [day1, day1_stuff], [day2, day2_stuff], [day3, day3_stuff], ]:
        if v:
            page = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), u'Plantilla:Actualizaciones en las redes/%s/%s' % (source, k))
            if not page.exists() or (page.exists and len(v) > len(page.get())):
                page.put(v, u"BOT - Añadiendo actualizaciones: %s [%d], %s [%d], %s [%d], %s [%d]" % (day0, len(re.findall(ur'\n', day0_stuff))-1, day1, len(re.findall(ur'\n', day1_stuff))-1, day2, len(re.findall(ur'\n', day2_stuff))-1, day3, len(re.findall(ur'\n', day3_stuff))-1, ))
    
def main():
    b = getBlogs()
    printContent(b, source='Blogs')
    #f = getFacebook()
    #fl = getFlickr()
    #n = getN1()
    y = getYouTube()
    printContent(y, source='YouTube')
    
if __name__ == '__main__':
    main()
