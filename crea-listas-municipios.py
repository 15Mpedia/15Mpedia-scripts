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

for comunidad, provincias in ccaa.items():
    de = 'de'
    if comunidad == 'Islas Baleares':
        de = 'de las'
    elif comunidad in ['País Vasco', 'Principado de Asturias']:
        de = 'del'
    elif comunidad in ['Comunidad Foral de Navarra', 'Comunidad de Madrid', 'Comunidad Valenciana', 'Región de Murcia']:
        de = 'de la'
    
    for por in ["altitud", "población", "superficie"]:
        wtitle = "Lista de municipios %s %s por %s" % (de, comunidad, por)
        wtext = "{{Lista de municipios por lugar|país=España|comunidad autónoma=%s|sort=%s}}" % (comunidad, por)
        page = pywikibot.Page(site, wtitle)
        if page.exists():
            print("La pagina %s ya existe" % (wtitle))
        else:
            page.text = wtext
            page.save("BOT - Creando lista de comunidad autónoma", botflag=False)
        
        if len(provincias) > 1:
            for provincia in provincias:
                wtitle = "Lista de municipios de la provincia de %s por %s" % (provincia, por)
                wtext = "{{Lista de municipios por lugar|país=España|comunidad autónoma=%s|provincia=Provincia de %s|sort=%s}}" % (comunidad, provincia, por)
                page = pywikibot.Page(site, wtitle)
                if False and page.exists():
                    print("La pagina %s ya existe" % (wtitle))
                else:
                    page.text = wtext
                    page.save("BOT - Creando lista de provincia", botflag=False)
        else:
            wtitle = "Lista de municipios de la provincia de %s por %s" % (provincias[0], por)
            redtitle = "Lista de municipios %s %s por %s" % (de, comunidad, por)
            wtext = u"#REDIRECT [[%s]]" % (redtitle)
            page = pywikibot.Page(site, wtitle)
            if page.exists():
                print("La pagina %s ya existe" % (wtitle))
            else:
                page.text = wtext
                page.save("BOT - Creando redirect hacia [[%s]]" % (redtitle), botflag=False)


