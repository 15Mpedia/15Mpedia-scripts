#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2014-2020 emijrp
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
    
    for year in range(1976, 2021):
        for month in range(1, 13):
            outputmonth = u"{{Lista de noticias por año y mes|año=%d|mes=%02d}}" % (year, month)
            print(outputmonth)
            pagemonth = pywikibot.Page(site, "Lista de noticias en %s de %s" % (monthnames[month].lower(), year))
            if True or not pagemonth.exists():
                pagemonth.text = outputmonth
                pagemonth.save("BOT - Creando lista de noticias por mes")
            redmonth = pywikibot.Page(site, "Lista de noticias de %s de %s" % (monthnames[month].lower(), year))
            if True or not redmonth.exists():
                redmonth.text = "#REDIRECT [[Lista de noticias en %s de %s]]" % (monthnames[month].lower(), year)
                redmonth.save("BOT - Creando redirección")
        
        outputyear = u"{{Lista de noticias por año|año=%d}}" % (year)
        print(outputyear)
        pageyear = pywikibot.Page(site, "Lista de noticias en %s" % (year))
        if True or not pageyear.exists():
            pageyear.text = outputyear
            pageyear.save("BOT - Creando lista de noticias por año")
        redyear = pywikibot.Page(site, "Lista de noticias de %s" % (year))
        if True or not redyear.exists():
            redyear.text = "#REDIRECT [[Lista de noticias en %s]]" % (year)
            redyear.save("BOT - Creando redirección")

if __name__ == '__main__':
    main()
