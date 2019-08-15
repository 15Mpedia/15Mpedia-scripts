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

def main():
    fusilados = []
    with open('fusilados-guadalajara.txt', 'r') as f:
        raw = f.read()
        for x in raw.split('</tr>'):
            x = x.strip()
            if not x:
                continue
            if '<b>' in x:
                continue
            values = re.findall(r'(?im)<td[^<>]*?>(.*?)</td>', x)
            fusilados.append(values)
    
    for fusilado in fusilados:
        nombrecompleto2 = fusilado[0]
        nombrepila = fusilado[0].split(', ')[1]
        apellidos = fusilado[0].split(', ')[0]
        print(nombrecompleto2)
        nombrecompleto = nombrepila + ' ' + apellidos
        
        apellido1 = ''
        apellido2 = ''
        if apellidos:
            if not ' ' in apellidos:
                apellido1 = apellidos
            elif len(apellidos.split(' ')) == 2:
                apellido1, apellido2 = apellidos.split(' ')
            else:
                apellido1 = apellidos.split(' ')[0]
                apellido2 = ' '.join(apellidos.split(' ')[1:])
        
        edad = fusilado[1]
        prof = fusilado[2]
        if prof == 's.l.':
            prof = ''
        resmuni = fusilado[3]
        resmuni = re.sub(r'(?im) *\([^\(\)]+\) *', '', resmuni)
        resmuni = resmuni.replace('/', ',')
        resmuni = re.sub(r' *, *', ', ', resmuni)
        print(nombrecompleto, edad, prof, resmuni)
        
        sexo = 'Hombre' #asumimos todos son, luego corregimos a mano
        bio = ''
        if resmuni:
            bio += '%s era de [[%s]]. ' % (nombrepila, resmuni.split(',')[0])
        if prof:
            if edad:
                bio += 'Era %s y tenía %s años cuando fue %s.' % (prof, edad, sexo=='Hombre' and 'fusilado' or 'fusilada')
            else:
                bio += 'Era %s.' % (prof)
        else:
            if edad:
                bio += 'Tenía %s años cuando fue %s.' % (edad, sexo=='Hombre' and 'fusilado' or 'fusilada')
        if bio:
            bio += '<ref name="fuscemguadalajara" />'
        print(bio)
        
        desc = '%s por el franquismo, %s.' % (sexo=='Hombre' and 'Represaliado' or 'Represaliada', sexo=='Hombre' and 'fusilado' or 'fusilada')
        print(desc)
        
        output = """{{Infobox Persona
|nombre=%s
|primer apellido=%s
|segundo apellido=%s
|sexo=%s
|lugar de fallecimiento=Guadalajara
|lugar de residencia=%s
|ocupación=%s
|edad=%s
|descripción=%s
|represión={{persona represaliada
|represión=Fusilamiento
|represor=Franquismo
|fecha=
|lugar=Guadalajara
}}
}}
'''%s''', %s por el [[franquismo]], [[Lista de personas fusiladas por el franquismo|%s]] en [[Guadalajara]].<ref name="fuscemguadalajara">{{Fusilados-Cementerio-Guadalajara}}</ref>

== Biografía ==

%s

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
{{represión}}""" % (nombrepila, apellido1, apellido2, sexo, resmuni, prof, edad, desc, nombrecompleto, sexo=='Hombre' and 'represaliado' or 'represaliada', sexo=='Hombre' and 'fusilado' or 'fusilada', bio and bio or '{{expandir}}')
        print(output)
        
        page = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), nombrecompleto)
        if page.exists() and len(page.text) > 1:
            print('Ya existe', nombrecompleto)
            f = open('fusilados-guadalajara-yaexiste.txt', 'a')
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
