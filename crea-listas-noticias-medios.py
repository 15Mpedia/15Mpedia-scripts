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
import wikipedia

def main():
    site = wikipedia.Site('15mpedia', '15mpedia')
    page = wikipedia.Page(site, u"Lista de noticias")
    wtext = page.get()
    medios = re.findall(ur"(?im){{noticias por fuente\|fuente=([^|]*?)\|format=count}}", wtext)
    
    for medio in medios:
        page2 = wikipedia.Page(site, u"Lista de noticias de %s" % (medio))
        if page2.exists():
            continue
        output = u"""La siguiente es una '''lista de noticias de %s'''. En este momento hay información sobre '''{{noticias por fuente|fuente=%s|format=count}} noticias'''.

== Noticias de %s ==
{{semántica}}
{{noticias por fuente|fuente=%s}}

== Véase también ==
* [[Lista de noticias]]
* [[%s]]

{{noticias}}

[[Categoría:Listas|Noticias de %s]]
[[Categoría:Noticias|%s]]
""" % (medio, medio, medio, medio, medio, medio, medio, )
        print output
        page2.put(output, u"BOT - Creando lista de noticias")
        

if __name__ == '__main__':
    main()
