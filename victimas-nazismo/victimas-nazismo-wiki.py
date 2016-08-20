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

def destraducirfecha(fecha):
    trad = fecha
    meses = {'enero':1, 'febrero':2, 'marzo':3, 'abril':4, 'mayo':5, 'junio':6, 'julio':7, 'agosto':8, 'septiembre':9, 'octubre':10, 'noviembre':11, 'diciembre':12}
    if len(fecha.split(' de ')) == 3:
        try:
            trad = '%s/%02d/%02d' % (int(fecha.split(' de ')[2]), int(meses[fecha.split(' de ')[1]]), int(fecha.split(' de ')[0]))
        except:
            trad = fecha
    
    return trad

def main():
    f = open('victimas-nazismo.csv', 'r')
    csv = unicode(f.read(), 'utf-8')
    f.close()
    
    rows = csv.split('\n')
    skip = u''
    for row in rows:
        print row
        nombre = ''
        nombreapellidos = ''
        apellidos = ''
        apellido1 = ''
        apellido2 = ''
        procedenciamuni = ''
        procedenciaprov = ''
        lugarfallecimiento = ''
        fechafallecimiento = ''
        oficio = ''
        
        try:
            apellidosnombre, edad, procedencia, oficio, lugarfallecimiento, fechafallecimiento = row.split(';;;')
        except:
            continue
        
        apellidosnombre = apellidosnombre.strip()
        edad = edad.strip()
        procedencia = procedencia.strip()
        oficio = oficio.strip()
        lugarfallecimiento = lugarfallecimiento.strip()
        fechafallecimiento = fechafallecimiento.strip()
        
        if skip:
            if skip != apellidosnombre:
                continue
            else:
                skip = ''
        
        if ', ' in apellidosnombre:
            nombre = apellidosnombre.split(', ')[1]
            apellidos = apellidosnombre.split(', ')[0]
            nombreapellidos = u'%s %s' % (nombre, apellidos)
            if ' ' in apellidos:
                apellido1 = apellidos.split(' ')[0]
                apellido2 = ' '.join(apellidos.split(' ')[1:])
            else:
                apellido1 = apellidos
        elif ',' in apellidosnombre:
            nombre = apellidosnombre.split(',')[1]
            apellidos = apellidosnombre.split(',')[0]
            nombreapellidos = u'%s %s' % (nombre, apellidos)
            if ' ' in apellidos:
                apellido1 = apellidos.split(' ')[0]
                apellido2 = ' '.join(apellidos.split(' ')[1:])
            else:
                apellido1 = apellidos
        else:
            nombre = apellidosnombre
            nombreapellidos = apellidosnombre
            apellidos = ''
            apellido1 = ''
            apellido2 = ''
        
        paiscampo = {}
        if 'gusen' in lugarfallecimiento.lower():
            lugarfallecimiento = u'Campo de concentración de Gusen'
            paiscampo[lugarfallecimiento] = u'Austria'
            #continue #skiping done bios
        elif 'mauth' in lugarfallecimiento.lower():
            lugarfallecimiento = u'Campo de concentración de Mauthausen'
            paiscampo[lugarfallecimiento] = u'Austria'
        elif 'harth' in lugarfallecimiento.lower():
            lugarfallecimiento = u'Campo de concentración de Hartheim'
            paiscampo[lugarfallecimiento] = u'Austria'
        elif 'dachau' in lugarfallecimiento.lower():
            lugarfallecimiento = u'Campo de concentración de Dachau'
            paiscampo[lugarfallecimiento] = u'Alemania'
        elif 'steyr' in lugarfallecimiento.lower():
            lugarfallecimiento = u'Campo de concentración de Steyr'
            paiscampo[lugarfallecimiento] = u'Austria'
        elif 'buchen' in lugarfallecimiento.lower():
            lugarfallecimiento = u'Campo de concentración de Buchenwald'
            paiscampo[lugarfallecimiento] = u'Alemania'
        elif 'floss' in lugarfallecimiento.lower():
            lugarfallecimiento = u'Campo de concentración de Flossenbürg'
            paiscampo[lugarfallecimiento] = u'Alemania'
        elif 'neuen' in lugarfallecimiento.lower():
            lugarfallecimiento = u'Campo de concentración de Neuengamme'
            paiscampo[lugarfallecimiento] = u'Alemania'
        elif 'melk' in lugarfallecimiento.lower():
            lugarfallecimiento = u'Campo de concentración de Melk'
            paiscampo[lugarfallecimiento] = u'Austria'
        elif 'ternberg' in lugarfallecimiento.lower():
            lugarfallecimiento = u'Campo de concentración de Ternberg'
            paiscampo[lugarfallecimiento] = u'Austria'
        elif 'bergen' in lugarfallecimiento.lower():
            lugarfallecimiento = u'Campo de concentración de Bergen-Belsen'
            paiscampo[lugarfallecimiento] = u'Alemania'
        elif 'ausch' in lugarfallecimiento.lower():
            lugarfallecimiento = u'Campo de concentración de Auschwitz'
            paiscampo[lugarfallecimiento] = u'Polonia'
        elif 'ravens' in lugarfallecimiento.lower():
            lugarfallecimiento = u'Campo de concentración de Ravensbrück'
            paiscampo[lugarfallecimiento] = u'Alemania'
        else:
            continue
        
        if ' (' in procedencia:
            procedenciamuni = procedencia.split(' (')[0]
            procedenciaprov = procedencia.split(' (')[1].split(')')[0]
        else:
            procedenciamuni = procedencia
            procedenciaprov = ''
        
        #if oficio == '-':
        #    oficio = u''
        oficio = u''
        
        fechafallecimiento2 = fechafallecimiento
        
        desc = u'Víctima española del nazismo'
        bio = u'%s era de [[%s]]%s. Cuando murió en el campo de concentración tenía %s años.<ref name="enrecuerdode" /><ref name="pares" />' % (nombre, procedenciamuni, procedenciaprov and u', [[provincia de %s]]' % (procedenciaprov) or u'', edad)
        
        output = u"""{{Infobox Persona
|nombre=%s
|primer apellido=%s
|segundo apellido=%s
|sexo=Hombre
|lugar de nacimiento=%s
|fecha de nacimiento=
|lugar de fallecimiento=%s
|fecha de fallecimiento=%s
|ocupación=%s
|descripción=%s
|represión={{persona represaliada
|represión=Campo de concentración
|represor=Nazismo
|fecha=%s
|lugar=%s
|fallecimiento=Sí
}}
}}

'''%s''', [[Lista de víctimas españolas del nazismo|víctima española]] del [[nazismo]], fue deportado al [[%s]] en [[%s]], donde murió el [[%s]].<ref name="enrecuerdode">{{en recuerdo de}}</ref><ref name="pares">{{PARES deportados}}</ref>

== Biografía ==

%s

== Véase también ==
* [[Memoria histórica]]
* [[Nazismo]]
* [[Lista de víctimas españolas del nazismo]]

== Referencias ==
{{reflist}}

== Enlaces externos ==
{{enlaces externos}}
<!--
* {{PARES deportados|id=}}
-->
{{represión}}""" % (nombre, apellido1, apellido2, procedenciamuni, lugarfallecimiento, destraducirfecha(fechafallecimiento), oficio, desc, destraducirfecha(fechafallecimiento), lugarfallecimiento, nombreapellidos, lugarfallecimiento, paiscampo[lugarfallecimiento], fechafallecimiento, bio)
        #print output.encode('utf-8')
                
        page = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), nombreapellidos)
        if page.exists():
            if page.text != output:
                pywikibot.showDiff(page.text, output)
                page.text = output
                page.save(u'BOT - Actualizando datos')
            """print 'Ya existe', nombreapellidos.encode('utf-8')
            f = open('victimas-yaexiste.txt', 'a')
            output2 = u'%s\n%s' % (output, '-'*50)
            f.write(output2.encode('utf-8'))
            f.close()"""
        else:
            print output.encode('utf-8')
            page.text = output
            page.save(u'BOT - Creando página', botflag=False)
            
            redtext = u'#REDIRECT [[%s]]' % (nombreapellidos)
            red = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), apellidosnombre)
            red.text = redtext
            red.save(u'BOT - Creando redirección a [[%s]]' % (nombreapellidos), botflag=True)

if __name__ == '__main__':
    main()
