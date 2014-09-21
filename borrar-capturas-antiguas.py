#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012-2014 emijrp <emijrp@gmail.com>
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
import pagegenerators
import re
import urllib
import wikipedia

"""
Bot de un solo uso, hecho para borrar capturas de Bambuser que fueron
subidas hace mucho siguiendo un sistema antiguo. Ahora se suben de otra forma, con bambusers.py.
No debería hacer falta volver a correr este bot.
"""

def main():
    site = wikipedia.Site('15mpedia', '15mpedia')
    cat = catlib.Category(site, u"Category:Capturas")
    gen = pagegenerators.CategorizedPageGenerator(cat)
    pre = pagegenerators.PreloadingGenerator(gen, pageNumber=200)
    
    users = {}
    for page in pre:
        wtitle = page.title()
        if not wtitle.startswith('Archivo:Bambuser'):
            continue
        bid = wtitle.split('Bambuser ')[1].split(' ')[0]
        buser = re.sub(r"\+", " ", ' '.join(wtitle.split('.jpg')[0].split(' ')[2:]))
        print bid, buser
        page2 = wikipedia.Page(site, u"Archivo:Bambuser - %s - %s.jpg" % (buser, bid))
        if page2.exists():
            page.delete(reason=u"BOT - Borrando captura antigua. Nueva ubicación: [[:%s]]" % (page2.title()), prompt=False)

if __name__ == '__main__':
    main()
