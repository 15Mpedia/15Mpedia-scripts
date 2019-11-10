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
    f = open('tln-asturias.txt', 'r')
    raw = f.read().strip().splitlines()
    f.close()
    for line in raw:
        if not ';Fusilamiento;' in line and not ';Asesinato;' in line:
            #asumimos que fueron 'paseos' o similar, los consideramos fusilamientos igualmente
            continue
        fus = line.split(';')
        fusilados.append([fus[0], fus[1], fus[2], fus[3], fus[4], fus[5], fus[6], fus[7], fus[8], fus[9], fus[10]])
    #print(fusilados)
    
    skip = ''
    for fusilado in fusilados:
        if skip:
            if skip == fusilado[1]:
                skip = ''
            continue
        
        if not ', ' in fusilado[1] or not ' ' in fusilado[1]:
            continue
        if '-' in fusilado[1]: #nombres duplicados -1, -2, etc, los evitamos por ahora, quizas en otra pasada los creemos
            continue
        
        nombrepila = fusilado[1].split(', ')[1].strip()
        apellidos = fusilado[1].split(', ')[0].strip()
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
        nombrecompleto = '%s %s' % (nombrepila, apellidos)
        nombrecompleto2 = '%s, %s' % (apellidos, nombrepila)
        
        lugarfus = fusilado[3].strip().split(',')[0].strip()
        fechafus = fusilado[4].strip().replace('-', '/')
        nacmuni = fusilado[5].strip().split(',')[0].strip()
        resmuni = fusilado[6].strip().split(',')[0].strip()
        edad = fusilado[7].strip()
        estadocivil = fusilado[8].strip()
        padres = fusilado[9].strip()
        prof = fusilado[10].strip().lower()
        print(nombrecompleto, lugarfus, fechafus, nacmuni, resmuni, edad, estadocivil, padres, prof)
        
        sexo = 'Hombre'
        if nombrepila in nombresmujer:
            sexo = 'Mujer'
        bio = ''
        if nacmuni or resmuni:
            bio += '%s era de [[%s]].' % (nombrepila, nacmuni or resmuni)
            if prof:
                if edad:
                    bio += ' Era %s y tenía %s años cuando fue %s.' % (prof, edad, sexo=='Hombre' and 'fusilado' or 'fusilada')
                else:
                    bio += ' Era %s.' % (prof)
            else:
                if edad:
                    bio += ' %s tenía %s años cuando fue %s.' % (nombrepila, edad, sexo=='Hombre' and 'fusilado' or 'fusilada')
        
        if bio:
            bio += '<ref name="TodoslosnombresAsturias" />'
        print(bio)
        
        if fechafus:
            desc = '%s por el franquismo, %s el %s.' % (sexo=='Hombre' and 'Represaliado' or 'Represaliada', sexo=='Hombre' and 'fusilado' or 'fusilada', traducirfecha(fechafus))
        else:
            desc = '%s por el franquismo, %s.' % (sexo=='Hombre' and 'Represaliado' or 'Represaliada', sexo=='Hombre' and 'fusilado' or 'fusilada')
        print(desc)
        
        output = """{{Infobox Persona
|nombre=%s
|primer apellido=%s
|segundo apellido=%s
|sexo=%s
|lugar de nacimiento=%s
|lugar de fallecimiento=%s
|fecha de fallecimiento=%s
|lugar de residencia=%s
|edad=%s
|ocupación=%s
|descripción=%s
|represión={{persona represaliada
|represión=Fusilamiento
|represor=Franquismo
|fecha=%s
|lugar=%s
}}
}}
'''%s''', %s por el [[franquismo]], [[Lista de personas fusiladas por el franquismo|%s]]%s%s.<ref name="TodoslosnombresAsturias">{{Todos los nombres Asturias}}</ref>

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
{{represión}}""" % (nombrepila, apellido1, apellido2, sexo, nacmuni, lugarfus, fechafus, resmuni, edad, prof, desc, fechafus, lugarfus, nombrecompleto, sexo=='Hombre' and 'represaliado' or 'represaliada', sexo=='Hombre' and 'fusilado' or 'fusilada', fechafus and (' el [[%s]]' % traducirfecha(fechafus)), lugarfus and (' en [[%s]]' % lugarfus), bio and bio or '{{expandir}}')
        print(output)
        
        page = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), nombrecompleto)
        if page.exists() and len(page.text) > 1:
            print('Ya existe', nombrecompleto)
            f = open('fusilados-asturias-yaexiste.txt', 'a')
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
