#!/usr/bin/python
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

import re
import os
import sys
import time
import urllib

""" arreglar para que cargue mas de 10 audios por usuario """

def main():
    users = ['drytenerife', 'sonsacampadabcn']
    
    #load track ids imported in the past (to exclude them)
    print u'Loading ids of tracks uploaded in the past, please wait'
    queryurl = "http://wiki.15m.cc/w/index.php?title=Especial:Ask&offset=0&limit=5000&q=[[embebido%3A%3ASoundCloud]]&p=mainlabel%3D-2D%2Fformat%3Dbroadtable&po=%3FEmbebido+url%3D%0A"
    f = urllib.urlopen(queryurl)
    html = unicode(f.read(), 'utf-8')
    imported = re.findall(ur"(?im)<td>(https://soundcloud.com/[^<>]+)</td>", html)
    print '%d tracks imported in the past' % len(imported)
    
    for user in users:
        url = 'https://soundcloud.com/%s' % (user)
        html = unicode(urllib.urlopen(url).read(), 'utf-8')
        m = re.findall(ur'<a itemprop="url" href="/[^/]+/([^>]+)">', html)
        for track in m:
            time.sleep(3)
            print '\n##################################\n', user, track
            trackurl = 'https://soundcloud.com/%s/%s' % (user, track)
            print trackurl
            if trackurl in imported:
                print u'Audio was imported in the past, skipping'
                continue
            else:
                print u'Downloading metadata and screenshot for audio'
            
            html2 = unicode(urllib.urlopen(trackurl).read(), 'utf-8')
            
            trackid = re.findall(ur'content="soundcloud://sounds:([\d]+)">', html2)[0]
            
            title = re.findall(ur'<meta property="og:title" content="([^>]+)">', html2)[0]
            duration = re.findall(ur'<meta itemprop="duration" content="([^>]+)" />', html2)[0] #PT00H06M24S
            duration = re.sub('(PT|S)', '', duration)
            duration = re.sub(r'[HM]', r':', duration)
            if duration.startswith('00:'):
                duration = duration[3:]
                if duration.startswith('00:'):
                    duration = duration[3:]
            if duration.startswith('0'):
                duration = duration[1:]
            
            taglist = []
            try:
                tags = re.findall(ur'"tag_list":"([^\n\r,]+)","', html2)[0].strip()
                tags = re.sub(ur'\\', ur'', tags)
                taglist = re.findall(ur'(?i)"([a-záéíóúñç0-9\-][a-záéíóúñç0-9\- ]+[a-záéíóúñç0-9\-])"', tags)
                taglist += (' '.join(re.findall(ur'(?i)" ([a-záéíóúñç0-9\-][a-záéíóúñç0-9\- ]+[a-záéíóúñç0-9\-]) "', tags))).split(' ')
                taglist += re.findall(ur'(?im)^([^" ]+) ', tags)
                taglist += re.findall(ur'(?im) ([^" ]+)$', tags)
            except:
                taglist = []
            tags = set()
            for tag in taglist:
                if len(tag) > 1:
                    tags.add(tag)
            print 'Tags', tags
            
            try:
                thumburl = re.findall(ur'<meta property="og:image" content="([^>]+)">', html2)[0]
            except:
                if re.search(ur'<meta property="og:image" content="">', html2):
                    #pues ponemos el dummy
                    thumburl = 'http://wiki.15m.cc/w/images/5/59/SoundCloud_-_acampada-badajoz_-_172709099.jpg'
                else:
                    print 'Error al leer la pagina?'
                    sys.exit()
            
            try:
                desc = re.findall(ur'"description":"([^"]+)"', html2)[0]
                desc = re.sub(ur"\\r\\n", "\n", desc)
            except:
                desc = ''
            date = re.findall(ur'<time pubdate>(\d\d\d\d/\d\d/\d\d \d\d:\d\d:\d\d)[^<]+</time>', html2)[0]
            license = re.findall(ur'"license":"([^"]+)"', html2)[0]
            if license == 'all-rights-reserved':
                license = '{{arr}}'
            if license.startswith('cc'):
                license = '{{%s}}' % (license)
            
            imagename = 'SoundCloud - %s - %s.jpg' % (user, trackid)
            infobox = u"""{{Infobox Archivo\n|embebido=SoundCloud\n|embebido id=%s\n|embebido usuario=%s\n|embebido título=%s\n|embebido url=%s\n|descripción=%s\n|fecha de publicación=%s\n|duración=%s\n|palabras clave=%s\n|autor={{soundcloud user|%s}}\n|licencia=%s\n}}""" % (trackid, user, title, trackurl, desc and u'{{descripción de soundcloud|1=%s}}' % (desc) or u'', date, duration, ', '.join(tags), user, license)
            
            ignoredupes = u'default-preview' in thumburl and True or False
            execmd = u'python upload.py -lang:15mpedia -family:15mpedia -keep %s -filename:"%s" -noverify "%s" "%s"' % (ignoredupes and u'-ignoredupes' or u'', imagename, thumburl, infobox)
            os.system(execmd.encode('utf-8'))
            
if __name__ == '__main__':
    main()

