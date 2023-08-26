#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2023 emijrp <emijrp@gmail.com>
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
import sys
import pywikibot

def main():
    ccaa = {
    u"Andalucía": [u"Almería", u"Cádiz", u"Córdoba", u"Granada", u"Huelva", u"Jaén", u"Málaga", u"Sevilla"], 
    u"Aragón": [u"Huesca", u"Teruel", u"Zaragoza"], 
    u"Canarias": [u"Las Palmas", u"Santa Cruz de Tenerife"], 
    u"Cantabria": [u"Cantabria"], 
    u"Castilla-La Mancha": [u"Albacete", u"Ciudad Real", u"Cuenca", u"Guadalajara", u"Toledo"], 
    u"Castilla y León": [u"Ávila", u"Burgos", u"León", u"Palencia", u"Salamanca", u"Segovia", u"Soria", u"Valladolid", u"Zamora"], 
    u"Cataluña": [u"Barcelona", u"Girona", u"Lleida", u"Tarragona"], 
    u"Comunidad de Madrid": [u"Madrid"], 
    u"Comunidad Foral de Navarra": [u"Navarra"], 
    u"Comunidad Valenciana": [u"Alicante", u"Castellón", u"Valencia"], 
    u"Extremadura": [u"Badajoz", u"Cáceres"], 
    u"Galicia": [u"A Coruña", u"Lugo", u"Ourense", u"Pontevedra"], 
    u"Islas Baleares": [u"Baleares"], 
    u"La Rioja": [u"La Rioja"], 
    u"País Vasco": [u"Álava", u"Gipuzkoa", u"Vizcaya"], 
    u"Principado de Asturias": [u"Asturias"], 
    u"Región de Murcia": [u"Murcia"], 
    }
    site = pywikibot.Site('15mpedia', '15mpedia')
    with open("campos-franquistas.txt", "r") as f:
        raw = unicode(f.read(), "utf-8")
    splits = raw.split("var infoWindow")[1:]
    for split in splits:
        nombre = re.findall(ur"(?im)<div><strong>([^<>]+?)</strong>", split)[0]
        localidad = re.findall(ur"(?im)Localidad: ([^\(\)]+?) \(([^\(\)]+?)\)", split)
        provincia = u""
        ccaa1 = u""
        campoid = re.findall(ur"(?im)/campos/(\d+)\"", split)
        if campoid:
            campoid = campoid[0]
        if localidad:
            localidad, provincia = localidad[0][0], localidad[0][1]
            if provincia in [u"Ceuta",u"Melilla", u"Protectorado de Marruecos", u"Sáhara"]:
                provincia = u""
            if provincia == u"Islas Baleares":
                provincia = u"Baleares"
            if provincia == u"Lérida":
                provincia = u"Lleida"
            if provincia == u"Gerona":
                provincia = u"Girona"
            if provincia == u"Orense":
                provincia = u"Ourense"
            if provincia == u"La Coruña":
                provincia = u"A Coruña"
            for ca, caprov in ccaa.items():
                if provincia in caprov:
                    ccaa1 = ca
        coord = re.findall(ur"(?im)google.maps.LatLng\(([^,]+?), ([^\)]+?)\)", split)
        lat, lon = coord[0][0][:9], coord[0][1][:9]
        
        print(nombre, localidad, provincia, ccaa1, lat, lon, campoid)
        output = u"""{{Infobox Campo
|nombre=%s
|tipo=Campo de concentración franquista
|país=España
|comunidad autónoma=%s
|provincia=%s
|municipio=%s
|coordenadas=%s, %s
|enlaces externos=* {{Los campos de concentración de Franco|%s}}
}}""" % (nombre, ccaa1, provincia and "Provincia de %s" % (provincia) or "", localidad, lat, lon, campoid)
        print(output)
        page = pywikibot.Page(site, nombre)
        if not page.exists():
            page.text = output
            page.save(u"BOT - Creando página")
        
        nombrered1 = re.sub(ur"Campo de concentración de ", u"Campo de concentración franquista de ", nombre)
        nombrered2 = re.sub(ur"Campo de concentración de ", u"Campo franquista de ", nombre)
        redoutput = "#REDIRECT [[%s]]" % (nombre)
        for nombrered in [nombrered1, nombrered2]:
            redpage = pywikibot.Page(site, nombrered)
            redpage.text = redoutput
            redpage.save(u"BOT - Creando redirección")
        
        #sys.exit()

if __name__ == '__main__':
    main()
