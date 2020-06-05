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

import re
import pywikibot

def main():
    site = pywikibot.Site('15mpedia', '15mpedia')
    page = pywikibot.Page(site, "Lista de noticias")
    wtext = page.get()
    medios = re.findall(ur"(?im){{noticias por fuente\|fuente=([^|]*?)\|format=count}}", wtext)
    
    for medio in medios:
        page2 = pywikibot.Page(site, "Lista de noticias de %s" % (medio))
        if True or not page2.exists():
            output = u"{{Lista de noticias por fuente|fuente=%s}}" % (medio)
            print(output)
            page2.put(output, "BOT - Creando lista de noticias")

if __name__ == '__main__':
    main()
