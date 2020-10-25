#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2020 emijrp <emijrp@gmail.com>
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

import urllib
import os
import re
import sys
import urllib.parse
import urllib.request
import pywikibot

def getURL(url=''):
    raw = ''
    req = urllib.request.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    try:
        raw = urllib.request.urlopen(req, timeout=15).read().strip().decode('utf-8')
    except:
        pass
    return raw

def main():
    #url = "http://www.todoslosnombres.org/biblioteca?page=1"
    #raw = getURL(url=url)
    #print(raw) #falla el geturl
    
    f = open('libros-memoria.txt', 'r')
    raw = f.read()
    f.close()
    
    raw2 = raw.split('<tr  class')
    for tr in raw2[1:]:
        tr = tr.split('</tr>')[0]
        if not '</a>' in tr:
            continue
        
        title = tr.split('<td  class="views-field views-field-title')[1].split('</a>')[0].split('>')[2].strip().strip('.').strip(':')
        title = re.sub(r'&quote?;', r'', title)
        if '&' in title:
            continue
        title = re.sub(r'(?im)(\d) - (\d)', r'\1-\2', title)
        print(title)
        
        author = tr.split('<td  class="views-field views-field-field-autor')[1].split('</td>')[0].split('>')[1].strip()
        authors = []
        if len(re.findall(', ', author)) == 1:
            authors = [author.split(', ')[1] + ' ' + author.split(', ')[0]]
        elif len(re.findall(', ', author)) > 1:
            aa = ''
            for a in author.split(', '):
                if aa:
                    aa = a + ' ' + aa
                    authors.append(aa)
                    aa = ''
                else:
                    aa = a
        else:
            pass
        print(authors)
        
        editorial = tr.split('<td  class="views-field views-field-field-editorial')[1].split('</td>')[0].split('>')[1].strip()
        year = re.findall(r'(\d{4})', editorial)
        year = year and year[0] or ''
        print(year)
        
        isbn = tr.split('<td  class="views-field views-field-field-c-digo-isbn')[1].split('</td>')[0].split('>')[1].strip()
        print(isbn)
        
        """
        thumb = re.findall(r'/thumbnail/public/([^\?/=]+)\?itok=', tr)
        if thumb:
            thumb = 'http://www.todoslosnombres.org/sites/default/files/' + thumb[0]
            print(thumb)
            
            ext = thumb.split('.')[-1]
            filename = title + '.' + ext
            filename = re.sub('[\'\"\:]', '', filename)
            print(filename)
            command = 'python upload.py -keep -filename:"%s" %s' % (filename, thumb)
            print(command)
            #os.system(command)
        """
        
        output = """{{Infobox Libro
|título=%s
|tema=Memoria histórica
|autoría=%s
|año=%s
|isbn=%s
|idioma=Castellano
}}""" % (title, ', '.join(authors), year, isbn)
        print(output)
        print('-'*10)
        
        page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), title)
        if not page.exists():
            page.text = output
            page.save('BOT - Creando página', botflag=False)
        #sys.exit()
    
if __name__ == '__main__':
    main()


