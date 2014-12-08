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

import HTMLParser
import os
import re
import subprocess
import sys
import time
import urllib
import urllib2
import wikipedia

""" Bot que importa metadatos y capturas de vídeos de Vimeo """

def main():
    ids = open('vimeo-videoids.txt', 'r').read().splitlines()
    
    for id in ids:
        url = 'http://vimeo.com/%s' % (id)
        print '\n#########################################\n', url
        
        queryurl = 'http://wiki.15m.cc/w/index.php?title=Especial:Ask&q=[[embebido%3A%3AVimeo]][[embebido+id%3A%3A'+id+']]&p=format%3Dbroadtable%2Flink%3Dall%2Fheaders%3Dshow%2Fsearchlabel%3D-26hellip%3B-20siguientes-20resultados%2Fclass%3Dsortable-20wikitable-20smwtable&eq=no'
        f = urllib.urlopen(queryurl)
        html = unicode(f.read(), 'utf-8')
        m = re.findall(ur'(?im)<td><a href=[^<>]+?>(Vimeo - [^<>]+?)</a></td>', html)
        if m:
            print u'Video %s was imported in the past, skipping http://wiki.15m.cc/wiki/File:%s' % (id, re.sub(' ', '_', m[0]))
            continue
        else:
            print u'Downloading metadata and screenshot for video %s' % (id)
        
        req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0 (Chrome)'})
        raw = unicode(urllib2.urlopen(req).read(), 'utf-8')
                
        try:
            l = unicode(subprocess.Popen(["python", "youtube-dl", url, "--get-title", "--get-duration", "--get-description", "--get-thumbnail"], stdout=subprocess.PIPE).communicate()[0], 'utf-8').splitlines()
            title = l[0]
            thumburl = l[1]
            desc = '\n'.join(l[2:-1])
            duration = l[-1]
            if 'high quality videos and the people who love them' in desc:
                desc = u''
            date = re.findall(ur'<meta itemprop="uploadDate" content="(\d\d\d\d-\d\d-\d\d)T[^<>]+?">', raw)[0]
            
            embebeduser, uploadernick = re.findall(ur'<a rel="author" href="/([^<>]+?)">([^<>]+?)</a>', raw)[0]
            uploadernick = urllib.unquote(uploadernick)
            
            license = u''
            if not re.search(ur'(?i)rel="license">', raw):
                license = u'' #licencia desconocida, seguramente All Rights Reserved, pero lo dejamos en blanco
            elif re.search(ur'(?i)<a href="http://creativecommons.org/licenses/([a-z-]+?)/(\d\.\d)/" title="[^<>]+" target="_blank" rel="license">', raw):
                cc, vers = re.findall(ur'(?i)<a href="http://creativecommons.org/licenses/([a-z-]+?)/(\d\.\d)/" title="[^<>]+" target="_blank" rel="license">', raw)[0]
                license = u'{{%s-%s}}' % (cc, vers)
            tags = []
            m = re.findall(ur"(?im)<meta property=\"video:tag\" content=\"([^<>]*?)\">", raw)
            if m:
                for tag in m:
                    tag = HTMLParser.HTMLParser().unescape(tag)
                    tags.append(tag)
            tags = ', '.join(tags)

        except:
            print u'Error accediendo a los parámetros del vídeo', id
            g = open('vimeo-errors.ids', 'a')
            g.write(u'%s\n' % (id))
            g.close()
            time.sleep(5)
            continue
        
        infobox = u"""{{Infobox Archivo\n|embebido=Vimeo\n|embebido id=%s\n|embebido usuario=%s\n|embebido título=%s\n|descripción=%s\n|fecha de publicación=%s\n|autor={{vimeo channel|%s|%s}}\n|palabras clave=%s\n|duración=%s\n|licencia=%s\n}}""" % (id, embebeduser, title, desc and u'{{descripción de vimeo|1=%s}}' % (desc) or u'', date, embebeduser, uploadernick, tags, duration, license)
        
        imagename = 'Vimeo - %s - %s.jpg' % (embebeduser, id)
        print 'Importing here http://wiki.15m.cc/wiki/Archivo:%s' % (re.sub(' ', '_', imagename))
        print infobox
        infoboxfilename = 'vimeo-infobox.txt'
        with open(infoboxfilename, 'w') as d:
            d.write(infobox.encode('utf-8'))
        execmd = u'python upload.py -lang:15mpedia -family:15mpedia -keep -ignoredupes -filename:"%s" -noverify -description-file:%s "%s"' % (imagename, infoboxfilename, thumburl)
        #os.system(execmd.encode('utf-8'))
        os.remove(infoboxfilename)
        time.sleep(5)
        
if __name__ == '__main__':
    main()
