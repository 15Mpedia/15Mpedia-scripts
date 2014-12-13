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
import time
import urllib
import urllib2
import wikipedia

def main():
    #users = set(re.findall(ur'(?im)title="Lista de vídeos de [^<>\n\r]+? en YouTube(?: \(la página no existe\))?">([^<>\n\r]+?)</a></span>', unicode(urllib.urlopen('http://wiki.15m.cc/wiki/Lista_de_v%C3%ADdeos_en_YouTube').read(), 'utf-8')))
    users = set(re.findall(ur'(?im)title="Lista de vídeos de [^<>\n\r]+? en YouTube(?: \(la página no existe\))">([^<>\n\r]+?)</a></span>', unicode(urllib.urlopen('http://wiki.15m.cc/wiki/Lista_de_v%C3%ADdeos_en_YouTube').read(), 'utf-8')))
    
    users = list(users)
    users.sort()
    print "Encontradas %d listas por crear" % len(users)
    skip = ''
    for user in users:
        if skip:
            if user == skip:
                skip = ''
            else:
                print 'Skiping', user
                continue
        print '#'*50
        nick = ''
        url = 'https://www.youtube.com/user/%s/about' % (user)
        print 'Leyendo', url
        p = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), u'Lista de vídeos de %s en YouTube' % (user))
        if p.exists():
            print 'La lista ya existe'
            continue
        
        req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0 (Chrome)'})
        try:
            raw = unicode(urllib2.urlopen(req).read(), 'utf-8')
        except:
            print 'Error al leer'
            
            try:
                url2 = 'https://www.youtube.com/channel/%s/about' % (user)
                print 'Leyendo', url2
                req2 = urllib2.Request(url2, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0 (Chrome)'})
                raw2 = unicode(urllib2.urlopen(req2).read(), 'utf-8')
                if re.search(ur'<div class="channel-empty-message banner-message">', raw2):
                    print 'Error, canal no existe'
                    continue
                else:
                    nick = re.findall('(?im)<meta itemprop="name" content="([^<>\n\r]+?)">', raw2)[0]
                    if not nick:
                        print 'Error, no pude parsear el nick'
                        continue
            except:
                print 'Error al leer'
                continue
        
        print user, nick
        
        output = u''
        if nick:
            output = u'{{Vídeos de usuario en YouTube|%s|%s}}' % (user, nick)
        else:
            output = u'{{Vídeos de usuario en YouTube|%s}}' % (user)

        if not p.exists():
            p.put(output, u"BOT - Creando lista de vídeos de YouTube", botflag=True)
            if nick:
                p.move(u'Lista de vídeos de %s en YouTube' % (nick), 'BOT - Renombrando canal de %s a %s' % (user, nick))
            time.sleep(5)

if __name__ == '__main__':
    main()
