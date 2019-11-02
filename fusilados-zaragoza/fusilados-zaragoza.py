#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2019 emijrp <emijrp@gmail.com>
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

import csv
import pywikibot
import re
import time

def invertirfecha(fecha):
    if len(fecha.split('/')) == 3:
        fecha = '%s/%s/%s' % (fecha.split('/')[2], fecha.split('/')[1], fecha.split('/')[0])
    
    return fecha

def traducirfecha(fecha):
    trad = fecha
    meses = {1:'enero', 2:'febrero', 3:'marzo', 4:'abril', 5:'mayo', 6:'junio', 7:'julio', 8:'agosto', 9:'septiembre', 10:'octubre', 11:'noviembre', 12:'diciembre'}
    if len(fecha.split('/')) == 3:
        try:
            trad = '%s de %s de %s' % (int(fecha.split('/')[2]), meses[int(fecha.split('/')[1])], fecha.split('/')[0])
        except:
            trad = fecha.split('/')[0]
    
    return trad

def main():
    nombresmujer = []
    f = open('nombrespilamujer', 'r')
    nombresmujer = f.read().strip().splitlines()
    f.close()
    fusilados = []
    f = open('fusilados-zaragoza.txt', 'r')
    raw = f.read().strip().splitlines()
    f.close()
    for line in raw:
        #quitar * en los campos
        line = line.replace('*','')
        fus = line.split('\t')
        fusilados.append([fus[0], fus[1], fus[2], fus[3]])
    #print(fusilados)
    
    for fusilado in fusilados:
        if not ', ' in fusilado[0] or not ' ' in fusilado[0]:
            continue
        
        nombrepila = fusilado[0].split(', ')[1].strip()
        apellidos = fusilado[0].split(', ')[0].strip()
        apellidos_ = ' '.join(['%s%s' % (x[0], x[1:].lower()) for x in apellidos.split(' ')])
        apellido1 = ''
        apellido2 = ''
        if apellidos_:
            if not ' ' in apellidos_:
                apellido1 = apellidos_
            elif len(apellidos_.split(' ')) == 2:
                apellido1, apellido2 = apellidos_.split(' ')
            else:
                apellido1 = apellidos_.split(' ')[0]
                apellido2 = ' '.join(apellidos_.split(' ')[1:])
        nombrecompleto = '%s %s' % (nombrepila, apellidos_)
        nombrecompleto2 = '%s, %s' % (apellidos_, nombrepila)
        
        edad = fusilado[1]
        fechafus = fusilado[2]
        resmuni = fusilado[3].rstrip('(').strip()
        print(nombrecompleto, edad, fechafus, resmuni)
        
        sexo = 'Hombre'
        if nombrepila in nombresmujer:
            sexo = 'Mujer'
        bio = ''
        if resmuni:
            bio += '%s era de [[%s]].' % (nombrepila, resmuni)
            if edad:
                bio += ' Tenía %s años cuando fue %s.' % (edad, sexo=='Hombre' and 'fusilado' or 'fusilada')
        else:
            bio += '%s tenía %s años cuando fue %s.' % (nombrepila, edad, sexo=='Hombre' and 'fusilado' or 'fusilada')
        
        if bio:
            bio += '<ref name="Casanova-2001" /><ref name="Memorial-Torrero" />'
        print(bio)
        
        desc = '%s por el franquismo, %s el %s.' % (sexo=='Hombre' and 'Represaliado' or 'Represaliada', sexo=='Hombre' and 'fusilado' or 'fusilada', traducirfecha(invertirfecha(fechafus)))
        print(desc)
        
        output = """{{Infobox Persona
|nombre=%s
|primer apellido=%s
|segundo apellido=%s
|sexo=%s
|lugar de fallecimiento=Zaragoza
|fecha de fallecimiento=%s
|lugar de residencia=%s
|edad=%s
|descripción=%s
|represión={{persona represaliada
|represión=Fusilamiento
|represor=Franquismo
|fecha=%s
|lugar=Zaragoza
}}
}}
'''%s''', %s por el [[franquismo]], [[Lista de personas fusiladas por el franquismo|%s]] el [[%s]] en [[Zaragoza]].<ref name="Casanova-2001">{{Casanova-2001}}</ref><ref name="Memorial-Torrero">{{Memorial-Torrero}}</ref>

== Biografía ==

%s

== Memoria ==

{{Homenaje-Zaragoza-20101027}}

== Véase también ==
* [[Memoria histórica]]
* [[Represión franquista]]
* [[Lista de personas fusiladas por el franquismo]]

== Referencias ==
{{reflist}}

== Enlaces externos ==
{{enlaces externos}}
<!--
* {{memoria pública|}}
* {{mcu represión|}}
-->
{{represión}}""" % (nombrepila, apellido1, apellido2, sexo, invertirfecha(fechafus), resmuni, edad, desc, invertirfecha(fechafus), nombrecompleto, sexo=='Hombre' and 'represaliado' or 'represaliada', sexo=='Hombre' and 'fusilado' or 'fusilada', traducirfecha(invertirfecha(fechafus)), bio and bio or '{{expandir}}')
        print(output)
        
        page = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), nombrecompleto)
        if page.exists() and len(page.text) > 1:
            print('Ya existe', nombrecompleto)
            f = open('fusilados-zaragoza-yaexiste.txt', 'a')
            output2 = '%s\n%s' % (output, '-'*50)
            f.write(output2)
            f.close()
        else:
            print(output)
            print('-'*50)
            page.text = output
            page.save(u'BOT - Creando página', botflag=True)
            
            redtext = '#REDIRECT [[%s]]' % (nombrecompleto)
            red = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), nombrecompleto2)
            red.text = redtext
            red.save(u'BOT - Creando redirección a [[%s]]' % (nombrecompleto), botflag=True)

if __name__ == '__main__':
    main()
