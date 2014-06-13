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
import os
import pagegenerators
import re
import urllib
import wikipedia

def main():
    entities = {
        u'Acampadas': {'category': u'Category:Acampadas', 'infobox': u'Infobox Acampada', }, 
        u'Asambleas': {'category': u'Category:Asambleas', 'infobox': u'Infobox Asamblea', }, 
        u'Centros sociales': {'category': u'Category:Centros sociales', 'infobox': u'Infobox Centro social', }, 
        u'Comisiones': {'category': u'Category:Comisiones', 'infobox': u'Infobox Comisión', }, 
        u'Nodos': {'category': u'Category:Nodos', 'infobox': u'Infobox Nodo', }, 
        u'Plataformas': {'category': u'Category:Plataformas', 'infobox': u'Infobox Plataforma', }, 
    }
    for entity, props in entities.items():
        site = wikipedia.Site('15mpedia', '15mpedia')
        #cat = catlib.Category(site, props['category'])
        #gen = pagegenerators.CategorizedPageGenerator(cat)
        gen = pagegenerators.ReferringPageGenerator(wikipedia.Page(site, u"Template:%s" % (props['infobox'])), onlyTemplateInclusion=True)
        pre = pagegenerators.PreloadingGenerator(gen, pageNumber=60)
        
        for page in pre:
            if page.isRedirectPage():
                continue
            wtitle = page.title()
            wtext = page.get()
            
            if not re.search(ur"(?im)\{\{\s*%s" % (props['infobox']), wtext):
                continue
            
            print '\n===', wtitle, '==='
            newtext = wtext
                    
            #imagen del perfil de twitter
            if not re.search(ur"(?im)\|\s*imagen\s*=", newtext):
                twitter = re.findall(ur"(?im)\|\s*twitter\s*=([^\r\n]+)\r\n", newtext)
                if twitter:
                    twitter = twitter[0].split(',')[0].strip()
                    f = urllib.urlopen("https://twitter.com/%s" % twitter)
                    html = unicode(f.read(), 'utf-8')
                    imageurl = re.findall(ur"data-resolved-url-large=\"(https://pbs.twimg.com/profile_images/[^\"]+)\"", html)
                    if imageurl:
                        imageurl = imageurl[0]
                        if 'default_profile' in imageurl:
                            print 'Default twitter image, skiping'
                            continue
                        desc = u"{{Infobox Archivo\n|embebido id=\n|embebido usuario=\n|embebido título=\n|descripción=Logotipo de [[%s]].\n|fuente={{twitter|%s}}\n}}" % (wtitle, twitter)
                        if imageurl.endswith('jpeg') or imageurl.endswith('jpg'):
                            ext = 'jpg'
                        elif imageurl.endswith('pneg') or imageurl.endswith('png'):
                            ext = 'png'
                        else:
                            print 'Twitter image extension is %s, skipping' % (imageurl.split('.')[-1])
                            continue
                        imagename = u"%s.%s" % (re.sub(u'[":/]', u'', wtitle), ext)
                        #https://www.mediawiki.org/wiki/Manual:Pywikibot/upload.py
                        os.system('python upload.py -lang:15mpedia -family:15mpedia -keep -filename:"%s" -noverify "%s" "%s"' % (imagename.encode('utf-8'), imageurl.encode('utf-8'), desc.encode('utf-8')))
                        newtext = re.sub(ur"(?im)\{\{%s" % (props['infobox']), ur"{{%s\n|imagen=%s" % (props['infobox'], imagename), newtext)
                        wikipedia.showDiff(wtext, newtext)
                        page.put(newtext, u"BOT - Añadiendo imagen")
        
if __name__ == '__main__':
    main()
