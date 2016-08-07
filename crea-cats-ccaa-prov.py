#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016 emijrp <emijrp@gmail.com>
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

def main():
    site = pywikibot.Site('15mpedia', '15mpedia')
    tema = 'Fosas'
    temamin = 'fosas'
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
        en = 'en'
        if comunidad == 'Islas Baleares':
            de = 'de las'
            en = 'en las'
        elif comunidad in ['País Vasco', 'Principado de Asturias']:
            de = 'del'
            en = 'en el'
        elif comunidad in ['Comunidad Foral de Navarra', 'Comunidad de Madrid', 'Comunidad Valenciana', 'Región de Murcia']:
            de = 'de la'
            en = 'en la'
            
        ccaacat = pywikibot.Page(site, "Categoría:%s %s %s" % (tema, en, comunidad))
        if not ccaacat.exists():
            ccaacat.text = "{{Categoría %s por lugar|comunidad autónoma=%s}}" % (temamin, comunidad)
            ccaacat.save("BOT - Creando categoría")
        
        ccaacat = pywikibot.Page(site, "Categoría:%s %s %s" % (tema, de, comunidad))
        ccaacat.delete("BOT - Moviendo a [[Categoría:%s %s %s]]" % (tema, en, comunidad))
        
        for provincia in provincias:
            provcat = pywikibot.Page(site, "Categoría:%s en la provincia de %s" % (tema, provincia))
            if not provcat.exists():
                provcat.text = "{{Categoría %s por lugar|provincia=Provincia de %s}}" % (temamin, provincia)
                provcat.save("BOT - Creando categoría")
            
            provcat = pywikibot.Page(site, "Categoría:%s de la provincia de %s" % (tema, provincia))
            provcat.delete("BOT - Moviendo a [[Categoría:%s en la provincia de %s]]" % (tema, provincia))

if __name__ == '__main__':
    main()
