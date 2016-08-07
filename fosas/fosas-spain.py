#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 emijrp <emijrp@gmail.com>
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

import json
import pywikibot

"Este script lee el fichero mjusticia_fosas.json de fosas del proyecto https://github.com/VidasContadas/datasets"

def main():
    site = pywikibot.Site('15mpedia', '15mpedia')
    
    """[{"latitud": ["37.2542"], "provincia": ["Sevilla"], "tipo": ["DESAPARECIDA"], "comunidad": ["Andaluc\u00eda"], "url": "http://mapadefosas.mjusticia.es/exovi_externo/CargarDetalleFosa.htm?fosaId=1", "fecha": ["01/01/1936"], "victimas": ["17"], "longitud": ["-4.9923835"], "descripcion": ["Se sabe por los registros civiles de varias localidades y fuentes informantes que fueron fusiladas personas de pueblos vecinos y del propio. Hay constancia de al  menos cuatro pedrere\u00f1os, uno de Gilena, dos de Casariche, uno de Marinaleda, un grupo de seis vecinos y vecinas de Los Corrales, m\u00e1s las propias v\u00edctimas locales proporcionando un listado de 17 v\u00edctimas. "], "nombre": ["Fosa en el Cementerio de Aguadulce"], "codigo": ["1/2009 SEVI"], "municipio": ["Aguadulce"]},"""
    
    tipos = {
        'DESAPARECIDA': 'Desaparecida', 
        'EXHUMADA PARCIAL': 'Exhumada parcial', 
        'EXHUMADA TOTAL': 'Exhumada total', 
        'NO INTERVENIDA': 'No intervenida', 
        'Sin Estado': 'Desconocido', 
        'TRASLADADA AL VALLE DE LOS CAÍDOS': 'Trasladada al Valle de los caídos',
        '': '', 
    }
    
    with open('mjusticia_fosas.json') as data_file:    
        data = json.load(data_file)
    
    setinternal = ''
    for fosa in data:
        coord = ''
        if fosa['latitud'] and fosa['longitud']:
            coord = '%s, %s' % (fosa['latitud'][0], fosa['longitud'][0])
        url = fosa['url'] and fosa['url'] or ''
        id = url.split('fosaId=')[1]
        codigo = fosa['codigo'] and fosa['codigo'][0] or ''
        nombre = fosa['nombre'] and fosa['nombre'][0] or ''
        nombre = nombre.strip('.')
        desc = fosa['descripcion'] and fosa['descripcion'][0] or ''
        fecha = ''
        if fosa['fecha']:
            t = fosa['fecha'][0].split('/')
            fecha = '%s-%s-%s' % (t[2], t[1], t[0])
        ccaa = fosa['comunidad'] and fosa['comunidad'][0] or ''
        #print ccaa.encode('utf-8')
        provincia = fosa['provincia'] and fosa['provincia'][0] or ''
        if '/' in provincia:
            provincia = provincia.split('/')[0]
        #print provincia.encode('utf-8')
        municipio = fosa['municipio'] and fosa['municipio'][0] or ''
        if ', ' in municipio:
            municipio = '%s %s' % (municipio.split(', ')[1], municipio.split(', ')[0])
        tipo = fosa['tipo'] and fosa['tipo'][0] or ''
        #print tipo.encode('utf-8')
        victimas = fosa['victimas'] and fosa['victimas'][0] or ''
        
        #la descripcion no se añade (de momento) pq ocupará mucho y la página se iría a 1500 kb
        setinternal += """{{#set_internal:fosa
|id=%s
|url=%s
|código fosa=%s
|dataset=Mapa de fosas de España
|nombre=%s
|descripción=
|coordenadas=%s
|fecha=%s
|país=España
|comunidad autónoma=%s
|provincia=Provincia de %s
|municipio=%s
|tipo=%s
|número de víctimas=%s
}}""" % (id, url, codigo, nombre, coord, fecha, ccaa, provincia, municipio, tipos[tipo], victimas)
        
        # articulo
        textopagina = """{{Infobox Fosa
|nombre=%s
|país=España
|comunidad autónoma=%s
|provincia=Provincia de %s
|municipio=%s
|coordenadas=%s
|estado=%s
|número de víctimas=%s
|mjusticia código=%s
|mjusticia url=%s
}}""" % (nombre.strip() or 'Fosa %s' % (codigo), ccaa, provincia, municipio, coord, tipos[tipo], victimas, codigo, url)
        
        nombrepagina = nombre.strip()
        if nombrepagina:
            nombrepagina = '%s (%s)' % (nombrepagina, codigo)
        else:
            nombrepagina = 'Fosa %s' % (codigo)
        page = pywikibot.Page(site, nombrepagina)
        if not page.exists():
            page.text = textopagina
            print(page.text)
            page.save('BOT - Creando artículo sobre fosa')
        
        #redirects
        redtitle = "Fosa %s" % (codigo)
        redtext = "#REDIRECCIÓN [[%s]]" % (nombrepagina)
        if redtitle != nombrepagina:
            redpage = pywikibot.Page(site, redtitle)
            if not redpage.exists():
                redpage.text = redtext
                redpage.save('BOT - Creando redirección')
        
    #print(setinternal.encode('utf-8'))

if __name__ == '__main__':
    main()

