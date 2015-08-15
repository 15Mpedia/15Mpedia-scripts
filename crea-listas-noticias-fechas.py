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
    monthnames = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
    monthdays = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    site = pywikibot.Site('15mpedia', '15mpedia')
    
    for year in range(1976, 1999):
        for month in range(1, 13):
            outputmonth = u"""La siguiente es una '''lista de noticias en %(monthname2)s de %(year)s'''. En este momento hay información sobre '''{{noticias por fecha|fecha inicio=%(year)s-%(month)02d-01|fecha fin=%(year)s-%(month)02d-%(monthdays)s|format=count}} noticias'''.

== Noticias en %(monthname2)s de %(year)s ==
{{semántica}}
{{noticias por fecha|fecha inicio=%(year)s-%(month)02d-01|fecha fin=%(year)s-%(month)02d-%(monthdays)s}}

== Véase también ==
* [[Lista de noticias en %(year)s]]
* [[%(monthname)s de %(year)s]]
* [[Hemeroteca]]

{{noticias}}

[[Categoría:Listas|Noticias en %(monthname2)s de %(year)s]]
[[Categoría:Noticias en %(year)s| %(year)s-%(month)02d]]
[[Categoría:%(monthname)s de %(year)s| Noticias en %(monthname2)s de %(year)s]]

""" % ({"monthname": monthnames[month], "monthname2": monthnames[month].lower(), "year": year, "month": month, "monthdays": monthdays[month]})
            print outputmonth
            pagemonth = pywikibot.Page(site, u"Lista de noticias en %s de %s" % (monthnames[month].lower(), year))
            pagemonth.text = outputmonth
            pagemonth.save(u"BOT - Creando lista de noticias por mes")
            redmonth = pywikibot.Page(site, u"Lista de noticias de %s de %s" % (monthnames[month].lower(), year))
            redmonth.text = u"#REDIRECT [[Lista de noticias en %s de %s]]" % (monthnames[month].lower(), year)
            redmonth.save(u"BOT - Creando redirección")
        
        outputyear = u"""La siguiente es una '''lista de noticias en %(year)s'''. En este momento hay información sobre '''{{noticias por fecha|fecha inicio=%(year)s-01-01|fecha fin=%(year)s-12-31|format=count}} noticias'''.

Según el '''mes''':
{{div col|2}}
* [[Lista de noticias en enero de %(year)s]] ({{noticias por fecha|fecha inicio=%(year)s-01-01|fecha fin=%(year)s-01-31|format=count}})
* [[Lista de noticias en febrero de %(year)s]] ({{noticias por fecha|fecha inicio=%(year)s-02-01|fecha fin=%(year)s-02-28|format=count}})
* [[Lista de noticias en marzo de %(year)s]] ({{noticias por fecha|fecha inicio=%(year)s-03-01|fecha fin=%(year)s-03-31|format=count}})
* [[Lista de noticias en abril de %(year)s]] ({{noticias por fecha|fecha inicio=%(year)s-04-01|fecha fin=%(year)s-04-30|format=count}})
* [[Lista de noticias en mayo de %(year)s]] ({{noticias por fecha|fecha inicio=%(year)s-05-01|fecha fin=%(year)s-05-31|format=count}})
* [[Lista de noticias en junio de %(year)s]] ({{noticias por fecha|fecha inicio=%(year)s-06-01|fecha fin=%(year)s-06-30|format=count}})
* [[Lista de noticias en julio de %(year)s]] ({{noticias por fecha|fecha inicio=%(year)s-07-01|fecha fin=%(year)s-07-31|format=count}})
* [[Lista de noticias en agosto de %(year)s]] ({{noticias por fecha|fecha inicio=%(year)s-08-01|fecha fin=%(year)s-08-31|format=count}})
* [[Lista de noticias en septiembre de %(year)s]] ({{noticias por fecha|fecha inicio=%(year)s-09-01|fecha fin=%(year)s-09-30|format=count}})
* [[Lista de noticias en octubre de %(year)s]] ({{noticias por fecha|fecha inicio=%(year)s-10-01|fecha fin=%(year)s-10-31|format=count}})
* [[Lista de noticias en noviembre de %(year)s]] ({{noticias por fecha|fecha inicio=%(year)s-11-01|fecha fin=%(year)s-11-30|format=count}})
* [[Lista de noticias en diciembre de %(year)s]] ({{noticias por fecha|fecha inicio=%(year)s-12-01|fecha fin=%(year)s-12-31|format=count}})
{{div col end}}

== Noticias en %(year)s ==
{{semántica}}
{{noticias por fecha|fecha inicio=%(year)s-01-01|fecha fin=%(year)s-12-31}}

== Véase también ==
* [[Lista de noticias]]
* [[%(year)s]]
* [[Hemeroteca]]

{{noticias}}

[[Categoría:Listas|Noticias en %(year)s]]
[[Categoría:Noticias| %(year)s]]
[[Categoría:%(year)s| Noticias en %(year)s]]""" % ({"year":year})
        print outputyear
        pageyear = pywikibot.Page(site, u"Lista de noticias en %s" % (year))
        pageyear.text = outputyear
        pageyear.save(u"BOT - Creando lista de noticias por año")
        redyear = pywikibot.Page(site, u"Lista de noticias de %s" % (year))
        redyear.text = u"#REDIRECT [[Lista de noticias en %s]]" % (year)
        redyear.save(u"BOT - Creando redirección")

if __name__ == '__main__':
    main()
