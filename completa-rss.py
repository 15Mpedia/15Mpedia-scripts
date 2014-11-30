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
import re
import pagegenerators
import wikipedia

def main():
    site = wikipedia.Site('15mpedia', '15mpedia')
    cat = catlib.Category(site, u"Category:Centros sociales")
    gen = pagegenerators.CategorizedPageGenerator(cat)
    pre = pagegenerators.PreloadingGenerator(gen, pageNumber=250)
    
    for page in pre:
        wtitle = page.title()
        wtext = page.get()
        
        print '\n===', wtitle, '==='
        if not re.search(ur"(?im)\{\{\s*Infobox", wtext):
            print u"Le falta la infobox"
            continue
        
        if not re.search(ur"(?im)\|\s*rss\s*=", wtext):
            if re.search(ur"(?im)\|\s*sitio web\s*=", wtext):
                m = re.findall(ur"(?im)\|\s*sitio web\s*=\s*(https?://[^\r\n ]+\.(blogspot|wordpress)\.[^\r\n ]+)\r\n", wtext)
                newtext = wtext
                rss = ''
                if m:
                    sitioweb = m[0][0].strip().rstrip('/')
                    if m[0][1] == 'blogspot':
                        rss = '%s/feeds/posts/default' % (re.sub(ur'\.blogspot\.com\...', '.blogspot.com', sitioweb))
                    elif m[0][1] == 'wordpress':
                        rss = '%s/feed/' % (re.sub('.wordpress.com', '.wordpress.com', sitioweb))
                    else:
                        continue
                else:
                    print u"No se pudo autodetectar el RSS"
                
                if rss:
                    newtext = re.sub(ur'(?im)(\|\s*sitio web\s*=)', ur'|rss=%s\n\1' % (rss), newtext)
                    if wtext != newtext:
                        wikipedia.showDiff(wtext, newtext)
                        page.put(newtext, u'BOT - Añadiendo RSS %s usando el sitio web %s' % (rss, sitioweb))
            else:
                print u"No tiene sitio web"
        else:
            print u"Ya tiene RSS"
                
if __name__ == '__main__':
    main()

