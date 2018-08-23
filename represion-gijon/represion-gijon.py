#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2018 emijrp <emijrp@gmail.com>
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
import re

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
    f = open('1934nombres.txt', 'r')
    raw = f.read().splitlines()
    f.close()
    """
      1 
     41 Asesinada
    480 Asesinado
      1 Ejectuado
      9 Ejecutada
   1267 Ejecutado
      2 Fallecida en prisión
    124 Fallecido en prisión
      1 Se ignora
    """
    
    personas = []
    skip = 'Francisco Alonso Rodríguez'
    for line in raw:
        line = line.strip()
        if not line:
            continue
        if not '\t' in line:
            continue
        if not ', ' in line.split('\t')[0]:
            continue
        
        persona = []
        for x in line.split('\t'):
            persona.append(x.strip())
        if len(persona) == 8:
            #personas.append(persona)
            print(persona)
            apellidos, nombrepila = persona[0].split(', ')
            apellidos2 = ' '.join([x[0]+x[1:].lower() for x in apellidos.split(' ')])
            nombrepila = nombrepila.strip()
            apodo = ''
            if '“' in nombrepila:
                apodo = nombrepila.split('“')[1].split('”')[0].strip()
                nombrepila = nombrepila.split('“')[0].strip()
            apellidos = apellidos.strip()
            apellidos2 = apellidos2.strip()
            nombrecompleto2 = apellidos2 + ', ' + nombrepila
            edad = persona[1].strip()
            lugnacimiento = persona[2].strip()
            lugresidencia = persona[3].strip()
            prof = persona[4].strip()
            fechamuerte = persona[5].strip()
            causamuerte = persona[6].strip()
            
            apellido1 = ''
            apellido2 = ''
            if len(apellidos2.split(' ')) == 2:
                apellido1 = apellidos2.split(' ')[0]
                apellido2 = apellidos2.split(' ')[1]
            else:
                apellido1 = apellidos2
                apellido2 = ''
            
            if not causamuerte.lower() in ["ejecutado", "ejecutada", "asesinado", "asesinada"]:
                continue
            
            if not nombrepila or not apellidos:
                continue
            
            sexo = 'Hombre'
            if causamuerte.lower() in ["ejecutada", "asesinada"]:
                sexo = 'Mujer'
            
            nombrecompleto = nombrepila + ' ' + apellidos2
            if skip:
                print('Skiping', nombrecompleto)
                if nombrecompleto == skip:
                    skip = ''
                continue
            
            #como los lugares a veces llevan entre parentesis el municipio o la provicina o ccaa
            #lo quitamos y listo, ya se crearan las paginas oportunas o redirects en el wiki
            lugnacimiento = lugnacimiento.split('(')[0].strip()
            lugresidencia = lugresidencia.split('(')[0].strip()
            
            print(nombrecompleto)
            if len(re.findall('/', fechamuerte)) != 2:
                continue
            
            fechamuerte = '%02d/%02d/%04d' % (int(fechamuerte.split('/')[0]), int(fechamuerte.split('/')[1]), int(fechamuerte.split('/')[2]))
            
            if prof.lower() == 'labores':
                prof = 'ama de casa'
            
            bio = ''
            if lugnacimiento:
                bio += '%s nació en [[%s]].' % (nombrepila, lugnacimiento)
            if prof:
                if edad:
                     if bio:
                         bio += ' Era %s y tenía %s años cuando fue %s.' % (prof.lower(), edad, sexo=='Hombre' and 'fusilado' or 'fusilada')
                     else:
                         bio += '%s era %s y tenía %s años cuando fue %s.' % (nombrepila, prof.lower(), edad, sexo=='Hombre' and 'fusilado' or 'fusilada')
                else:
                     if bio:
                         bio += ' Era %s.' % (prof.lower())
                     else:
                         bio += '%s era %s.' % (nombrepila, prof.lower())
            else:
                if edad:
                     if bio:
                         bio += ' Tenía %s años cuando fue %s.' % (edad, sexo=='Hombre' and 'fusilado' or 'fusilada')
                     else:
                         bio += '%s tenía %s años cuando fue %s.' % (nombrepila, edad, sexo=='Hombre' and 'fusilado' or 'fusilada')
            
            if bio:
                bio += '<ref name="memoriagijon" />'
            
            desc = '%s por el franquismo, %s el %s.' % (sexo=='Hombre' and 'Represaliado' or 'Represaliada', sexo=='Hombre' and 'fusilado' or 'fusilada', traducirfecha(invertirfecha(fechamuerte)))
            
            output = """{{Infobox Persona
|nombre=%s
|primer apellido=%s
|segundo apellido=%s
|apodo=%s
|sexo=%s
|lugar de nacimiento=%s
|fecha de nacimiento=
|lugar de fallecimiento=
|fecha de fallecimiento=%s
|lugar de residencia=%s
|ocupación=%s
|descripción=%s
|represión={{persona represaliada
|represión=Fusilamiento
|represor=Franquismo
|fecha=%s
|lugar=Gijón
}}
}}
'''%s''', %s por el [[franquismo]], [[Lista de personas fusiladas por el franquismo|%s]] el [[%s]].<ref name="memoriagijon">{{Memoria-de-Gijón}}</ref>

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
{{represión}}""" % (nombrepila, apellido1, apellido2, apodo, sexo, lugnacimiento, invertirfecha(fechamuerte), lugresidencia, prof and prof.lower() or '', desc, invertirfecha(fechamuerte), nombrecompleto, sexo=='Hombre' and 'represaliado' or 'represaliada', sexo=='Hombre' and 'fusilado' or 'fusilada', traducirfecha(invertirfecha(fechamuerte)), bio and bio or '{{expandir}}')
            
            page = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), nombrecompleto)
            if page.exists():
                print('Ya existe', nombrecompleto)
                f = open('memoriagijon-yaexiste.txt', 'a')
                output2 = '%s\n%s' % (output, '-'*50)
                f.write(output2)
                f.close()
            else:
                print(output)
                print('-'*50)
                page.text = output
                page.save('BOT - Creando página', botflag=False)
                
                redtext = '#REDIRECT [[%s]]' % (nombrecompleto)
                red = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), nombrecompleto2)
                red.text = redtext
                red.save('BOT - Creando redirección a [[%s]]' % (nombrecompleto), botflag=True)

if __name__ == '__main__':
    main()
