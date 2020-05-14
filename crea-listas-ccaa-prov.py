#!/usr/bin/env python
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

import pywikibot
import sys

site = pywikibot.Site('15mpedia', '15mpedia')
ccaa = {
    "Andalucía": ["Almería", "Cádiz", "Córdoba", "Granada", "Huelva", "Jaén", "Málaga", "Sevilla"], 
    "Aragón": ["Huesca", "Teruel", "Zaragoza"], 
    "Canarias": ["Las Palmas", "Santa Cruz de Tenerife"], 
    "Cantabria": ["Cantabria"], 
    "Castilla-La Mancha": ["Albacete", "Ciudad Real", "Cuenca", "Guadalajara", "Toledo"], 
    "Castilla y León": ["Ávila", "Burgos", "León", "Palencia", "Salamanca", "Segovia", "Soria", "Valladolid", "Zamora"], 
    "Cataluña": ["Barcelona", "Girona", "Lleida", "Tarragona"], 
    "Comunidad de Madrid": ["Madrid"], 
    "Comunidad Foral de Navarra": ["Navarra"], 
    "Comunidad Valenciana": ["Alicante", "Castellón", "Valencia"], 
    "Extremadura": ["Badajoz", "Cáceres"], 
    "Galicia": ["A Coruña", "Lugo", "Ourense", "Pontevedra"], 
    "Islas Baleares": ["Baleares"], 
    "La Rioja": ["La Rioja"], 
    "País Vasco": ["Álava", "Gipuzkoa", "Vizcaya"], 
    "Principado de Asturias": ["Asturias"], 
    "Región de Murcia": ["Murcia"], 
}
tema = "Movimiento 15M"
preposicion = 'en' #de o en
for comunidad, provincias in ccaa.items():
    prep = preposicion
    if comunidad == 'Islas Baleares':
        if preposicion == 'de':
            prep = 'de las'
        elif preposicion == 'en':
            prep = 'en las'
    elif comunidad in ['País Vasco', 'Principado de Asturias']:
        if preposicion == 'de':
            prep = 'del'
        elif preposicion == 'en':
            prep = 'en el'
    elif comunidad in ['Comunidad Foral de Navarra', 'Comunidad de Madrid', 'Comunidad Valenciana', 'Región de Murcia']:
        if preposicion == 'de':
            prep = 'de la'
        elif preposicion == 'en':
            prep = 'en la'
    
    wtitle = "%s %s %s" % (tema, prep, comunidad)
    wtext = "{{%s por lugar|país=España|comunidad autónoma=%s}}" % (tema, comunidad)
    page = pywikibot.Page(site, wtitle)
    if page.exists():
        print("La pagina %s ya existe" % (wtitle))
    else:
        page.text = wtext
        page.save("BOT - Creando página por comunidad autónoma", botflag=False)
    
    if len(provincias) > 1:
        for provincia in provincias:
            wtitle = "%s %s la provincia de %s" % (tema, preposicion, provincia)
            wtext = "{{%s por lugar|país=España|comunidad autónoma=%s|provincia=Provincia de %s}}" % (tema, comunidad, provincia)
            page = pywikibot.Page(site, wtitle)
            if page.exists():
                print("La pagina %s ya existe" % (wtitle))
            else:
                page.text = wtext
                page.save("BOT - Creando página por provincia", botflag=False)
    else:
        wtitle = "%s %s la provincia de %s" % (tema, preposicion, provincias[0])
        redtitle = "%s %s %s" % (tema, prep, comunidad)
        wtext = u"#REDIRECT [[%s]]" % (redtitle)
        page = pywikibot.Page(site, wtitle)
        if page.exists():
            print("La pagina %s ya existe" % (wtitle))
        else:
            page.text = wtext
            page.save("BOT - Creando redirect hacia [[%s]]" % (redtitle), botflag=False)


