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
    users = set(re.findall(ur'(?im)title="Lista de streamings de [^<>\n\r]+? en Bambuser(?: \(la página no existe\))?">([^<>\n\r]+?)</a></span>', unicode(urllib.urlopen('http://wiki.15m.cc/wiki/Lista_de_streamings_en_Bambuser').read(), 'utf-8')))
    
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
        print user
        p = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), u'Lista de streamings de %s en Bambuser' % (user))
        if p.exists():
            print 'La lista ya existe'
            continue
        
        output = u'{{Streamings de usuario en Bambuser|%s}}' % (user)

        if not p.exists():
            p.put(output, u"BOT - Creando lista de streamings de Bambuser", botflag=True)
            time.sleep(5)

if __name__ == '__main__':
    main()
