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

""" Importa los audios de un podcast de Ivoox """

def main():
    podcasts = ['http://www.ivoox.com/podcast-podcast-iskra-radio_sq_f168737_1.html']
    
    #load track ids imported in the past (to exclude them)
    print u'Loading ids of tracks uploaded in the past, please wait'
    queryurl = "http://wiki.15m.cc/w/index.php?title=Especial:Ask&offset=0&limit=5000&q=[[embebido%3A%3AIvoox]]&p=mainlabel%3D-2D%2Fformat%3Dbroadtable&po=%3FEmbebido+url%3D%0A"
    f = urllib.urlopen(queryurl)
    html = unicode(f.read(), 'utf-8')
    imported = re.findall(ur"(?im)<td>(http://www.ivoox.com/[^<>]+)</td>", html)
    print '%d tracks imported in the past' % len(imported)
    
    for podcast in podcasts:
        tracks = []
        url = podcast
        html = unicode(urllib.urlopen(url).read(), 'utf-8')
        while True:
            m = re.findall(ur'<a  class="titulo" href="([^>]+)" id="\d+"', html)
            for n in m:
                tracks.append('http://www.ivoox.com/%s' % (n))
            
            if re.findall(ur'(?im)<a rel="nofollow" href="http://www.ivoox.com/[^>]+=all">&raquo;</a>', html):
                print u'Leyendo más resultados'
                url = re.findall(ur'(?im)<a rel="nofollow" href="(http://www.ivoox.com/[^>]+=all)">&raquo;</a>', html)[0]
                html = unicode(urllib.urlopen(url).read(), 'utf-8')
                time.sleep(5)
            else:
                print u'Ya no hay más tracks'
                break
        
        print len(tracks), 'tracks'
        
        f = open('ivoox.html', 'w')
        f.write(html.encode('utf-8'))
        f.close()
        
        for trackurl in tracks:
            print '\n##################################\n', trackurl
            if trackurl in imported:
                print u'Audio was imported in the past, skipping'
                continue
            else:
                print u'Downloading metadata and screenshot for audio'
            
            time.sleep(3)
            try:
                html2 = unicode(urllib.urlopen(trackurl).read(), 'utf-8')
            except:
                try:
                    html2 = unicode(urllib.urlopen(trackurl).read(), 'iso-5589-1')
                except:
                    print u'Codificación desconocida'
                    continue
            
            trackid = re.findall(ur'var id             = ([\d]+);', html2)[0]
            title = re.findall(ur'<meta property="og:title" content="([^>]+)" />', html2)[0]
            duration = re.findall(ur"var audio_duration = '([^']+)'", html2)[0]
            thumburl = re.findall(ur'<meta property="og:image" content="([^>]+)" />', html2)[0]

            desc = html2.split('<p itemprop="description" style="margin:0;">')[1].split('<span id="masinfo_audio">')[0].strip()
            desc = re.sub(ur'(?im)(<span id="puntos">\.\.\.</span>)?\s*?<span id="descripcion_audio">\s*', ur'', desc)
            desc = re.sub(ur'<br\s*/>\s*', ur'\n\n', desc)
            desc = re.sub(ur'(?im)\n\n\n+', ur'\n\n', desc)
            desc = desc.strip()
            
            infourl = 'http://www.ivoox.com/%s' % (re.findall(ur"(?im)load\('(info_[^>]+?\.html)'\);\s*\">Mostrar más</a>", html2)[0])
            html3 = unicode(urllib.urlopen(infourl).read(), 'utf-8')
            user = re.findall(ur"(?im)<a rel='nofollow' href='escuchar[^>]+?'>([^<>]+?)</a>", html3)[0]
            tags = []
            try:
                tags = re.findall(ur"(?im)<a rel='nofollow' href='audios-[^>]+?\.html'>([^<>]+?)</a>", html3.split("title='Tags'/>")[1].split('</p>')[0])
            except:
                pass
            
            date = ''
            try:
                date = re.findall(ur'(?im)<span class="glyphicon glyphicon-calendar glyphicon13">\s*</span>\s*?(\d\d/\d\d/\d\d\d\d)\s*</div>', html2)[0]
                date = u'%s-%s-%s' % (date.split('/')[2], date.split('/')[1], date.split('/')[0])
            except:
                pass
            [date2, hour] = re.findall(ur'(?im)<meta property="og:description" content="[^<>]+?Subido ([^<>]+?) a las (\d\d:\d\d:\d\d) \d+\s*?" />', html2)[0]
            if not date:
                date = u'{{subst:CURRENTYEAR}}-%s-%s' % (date2.split('/')[1], date2.split('/')[0])
            date = u'%s %s' % (date, hour)
            
            license = u''
            if u"<a rel='nofollow' class='license' href='http://creativecommons.org" in html3:
                [cc, ccversion] = re.findall(ur"(?im)<a rel='nofollow' class='license' href='http://creativecommons.org/licenses/([^/]+?)/([\d\.]+?)/'>", html3)[0]
                if cc and ccversion:
                    license = '{{cc-%s-%s}}' % (cc, ccversion)
            
            imagename = 'Ivoox - %s - %s.jpg' % (user, trackid)
            infobox = u"""{{Infobox Archivo\n|embebido=Ivoox\n|embebido id=%s\n|embebido usuario=%s\n|embebido título=%s\n|embebido url=%s\n|descripción=%s\n|fecha de publicación=%s\n|duración=%s\n|palabras clave=%s\n|autor={{ivoox user|%s}}\n|licencia=%s\n}}""" % (trackid, user, title, trackurl, desc and u'{{descripción de ivoox|1=%s}}' % (desc) or u'', date, duration, ', '.join(tags), user, license)
            
            ignoredupes = True
            execmd = u'python upload.py -lang:15mpedia -family:15mpedia -keep %s -filename:"%s" -noverify "%s" "%s"' % (ignoredupes and u'-ignoredupes' or u'', imagename, thumburl, infobox)
            os.system(execmd.encode('utf-8'))
            
if __name__ == '__main__':
    main()

