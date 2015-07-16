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

"Este script lee el fichero mjusticia_fosas.json de fosas del proyecto https://github.com/VidasContadas/datasets"

def main():
    """[{"latitud": ["37.2542"], "provincia": ["Sevilla"], "tipo": ["DESAPARECIDA"], "comunidad": ["Andaluc\u00eda"], "url": "http://mapadefosas.mjusticia.es/exovi_externo/CargarDetalleFosa.htm?fosaId=1", "fecha": ["01/01/1936"], "victimas": ["17"], "longitud": ["-4.9923835"], "descripcion": ["Se sabe por los registros civiles de varias localidades y fuentes informantes que fueron fusiladas personas de pueblos vecinos y del propio. Hay constancia de al  menos cuatro pedrere\u00f1os, uno de Gilena, dos de Casariche, uno de Marinaleda, un grupo de seis vecinos y vecinas de Los Corrales, m\u00e1s las propias v\u00edctimas locales proporcionando un listado de 17 v\u00edctimas. "], "nombre": ["Fosa en el Cementerio de Aguadulce"], "codigo": ["1/2009 SEVI"], "municipio": ["Aguadulce"]},"""
    
    tipos = {
        u'DESAPARECIDA': u'Desaparecida', 
        u'EXHUMADA PARCIAL': u'Exhumada parcial', 
        u'EXHUMADA TOTAL': u'Exhumada total', 
        u'NO INTERVENIDA': u'No intervenida', 
        u'Sin Estado': u'Desconocido', 
        u'TRASLADADA AL VALLE DE LOS CAÍDOS': u'Trasladada al Valle de los caídos',
        u'': u'', 
    }
    
    with open('mjusticia_fosas.json') as data_file:    
        data = json.load(data_file)
    
    setinternal = u''
    for fosa in data:
        coord = u''
        if fosa['latitud'] and fosa['longitud']:
            coord = u'%s, %s' % (fosa['latitud'][0], fosa['longitud'][0])
        url = fosa['url'] and fosa['url'] or u''
        id = url.split('fosaId=')[1]
        codigo = fosa['codigo'] and fosa['codigo'][0] or u''
        nombre = fosa['nombre'] and fosa['nombre'][0] or u''
        desc = fosa['descripcion'] and fosa['descripcion'][0] or u''
        fecha = u''
        if fosa['fecha']:
            t = fosa['fecha'][0].split('/')
            fecha = u'%s-%s-%s' % (t[2], t[1], t[0])
        ccaa = fosa['comunidad'] and fosa['comunidad'][0] or u''
        #print ccaa.encode('utf-8')
        provincia = fosa['provincia'] and fosa['provincia'][0] or u''
        if '/' in provincia:
            provincia = provincia.split('/')[0]
        #print provincia.encode('utf-8')
        municipio = fosa['municipio'] and fosa['municipio'][0] or u''
        if ', ' in municipio:
            municipio = u'%s %s' % (municipio.split(', ')[1], municipio.split(', ')[0])
        tipo = fosa['tipo'] and fosa['tipo'][0] or u''
        #print tipo.encode('utf-8')
        victimas = fosa['victimas'] and fosa['victimas'][0] or u''
        
        #la descripcion no se añade (de momento) pq ocupará mucho y la página se iría a 1500 kb
        setinternal += u"""{{#set_internal:fosa
|id=%s
|url=%s
|código fosa=%s
|dataset=Mapa de fosas de España
|nombre=%s
|descripción=
|coordenadas=%s
|fecha=%s
|comunidad autónoma=%s
|provincia=Provincia de %s
|municipio=%s
|tipo=%s
|número de víctimas=%s
}}""" % (id, url, codigo, nombre, coord, fecha, ccaa, provincia, municipio, tipos[tipo], victimas)

    print setinternal.encode('utf-8')

if __name__ == '__main__':
    main()

