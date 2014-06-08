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
    site = wikipedia.Site('15mpedia', '15mpedia')
    cat = catlib.Category(site, u"Category:Círculos de Podemos")
    gen = pagegenerators.CategorizedPageGenerator(cat)
    pre = pagegenerators.PreloadingGenerator(gen, pageNumber=60)
    
    for page in pre:
        wtitle = page.title()
        wtext = page.get()
        
        if not re.search(ur"(?im)\{\{\s*Infobox Nodo", wtext):
            continue
        
        print '\n===', wtitle, '==='
        newtext = wtext
        suffix = ' '.join(wtitle.split(' ')[1:])
        
        if re.search(ur"(?im)\{\{\s*nodos\s*\}\}", newtext) and not re.search(ur"(?im)\{\{\s*podemos\s*\}\}", newtext):
            newtext = re.sub(ur"(?im)\{\{\s*nodos\s*\}\}", ur"{{podemos}}", newtext)
        
        if re.search(ur"(?im)^'''([^\']+)''' es un \[\[nodo\]\] de \[\[Podemos\]\]\.", newtext):
            newtext = re.sub(ur"(?im)^'''([^\']+)''' es un \[\[nodo\]\] de \[\[Podemos\]\]\.", ur"'''\1''' es un [[Lista de círculos de Podemos|círculo]] de [[Podemos]] de [[%s]]." % (suffix), newtext)
        
        if re.search(ur"(?im)== Enlaces externos ==\s*\*[^\r\n]+\r\n", newtext):
            newtext = re.sub(ur"(?im)== Enlaces externos ==\s*\*[^\r\n]+\r\n", ur"== Enlaces externos ==\n{{enlaces externos}}\n", newtext)
        
        newtext = re.sub(ur"(?im)\[\[Categoría:Podemos\]\]", ur"", newtext)
        newtext = re.sub(ur"(?im)\[\[Categoría:Nodos\]\]", ur"[[Categoría:Círculos de Podemos|%s]]" % (suffix), newtext)
        newtext = re.sub(ur"(?im)\[\[Categoría:Círculos de Podemos\]\]", ur"[[Categoría:Círculos de Podemos|%s]]" % (suffix), newtext)
        
        newtext = re.sub(ur"(?im)== Véase también ==\r\n\* \[\[Lista de nodos de Podemos\]\]\r\n\r\n", ur"== Véase también ==\n* [[Podemos]]\n* [[Lista de círculos de Podemos]]\n\n", newtext)

        if wtext != newtext:
            wikipedia.showDiff(wtext, newtext)
            page.put(newtext, u"BOT - Unificando círculos")
        
        #imagen
        if not re.search(ur"(?im)\|\s*imagen\s*=", newtext):
            twitter = re.findall(ur"(?im)\|\s*twitter\s*=([^\r\n]+)\r\n", newtext)
            if twitter:
                twitter = twitter[0].strip()
                f = urllib.urlopen("https://twitter.com/%s" % twitter)
                html = unicode(f.read(), 'utf-8')
                imageurl = re.findall(ur"data-resolved-url-large=\"(https://pbs.twimg.com/profile_images/[^\"]+)\"", html)
                if imageurl:
                    imageurl = imageurl[0]
                    if 'default_profile' in imageurl:
                        print 'Default twitter image, skiping'
                        continue
                    desc = u"{{Infobox Archivo\n|embebido id=\n|embebido usuario=\n|embebido título=\n|descripción=Logotipo de {{t|%s}}\n|fuente={{twitter|%s}}\n}}" % (twitter, twitter)
                    if imageurl.endswith('jpeg') or imageurl.endswith('jpg'):
                        ext = 'jpg'
                    elif imageurl.endswith('pneg') or imageurl.endswith('png'):
                        ext = 'png'
                    else:
                        print 'Twitter image extension is %s, skiping' % (imageurl.split('.')[-1])
                        continue
                    imagename = u"%s.%s" % (wtitle, ext)
                    #https://www.mediawiki.org/wiki/Manual:Pywikibot/upload.py
                    os.system('python upload.py -lang:15mpedia -family:15mpedia -filename:"%s" -noverify "%s" "%s"' % (imagename.encode('utf-8'), imageurl.encode('utf-8'), desc.encode('utf-8')))
                    newtext = re.sub(ur"(?im)\{\{Infobox Nodo", ur"{{Infobox Nodo\n|imagen=%s" % (imagename), newtext)
                    wikipedia.showDiff(wtext, newtext)
                    page.put(newtext, u"BOT - Añadiendo imagen")
        
if __name__ == '__main__':
    main()
