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
    provtrans = {'Corunya': 'Provincia de A Coruña', 'Melilla': 'Melilla', 'Zamora': 'provincia de Zamora', 'Àvila': 'provincia de Ávila', 'Ceuta': 'Ceuta', 'Pontevedra': 'provincia de Pontevedra', 'Àlaba': 'provincia de Álava', 'Còrdova': 'provincia de Córdoba', 'Lleó': 'provincia de León', 'Lugo': 'provincia de Lugo', 'Palència': 'provincia de Palencia', 'Burgos': 'provincia de Burgos', 'Guipúscoa': 'provincia de Guipuzkoa', 'Huelva': 'provincia de Huelva', 'Ourense': 'provincia de Ourense', 'Segòvia': 'provincia de Segovia', 'Astúries': 'Asturias', 'Ciudad Real': 'provincia de Ciudad Real', 'Toledo': 'provincia de Toledo', 'Biscaia': 'provincia de Bizkaia', 'Càceres': 'provincia de Cáceres', 'Guadalajara': 'provincia de Guadalajara', 'Cantàbria': 'Cantabria', 'Conca': 'provincia de Cuenca', 'Badajoz': 'provincia de Badajoz', 'Illes Balears': 'Islas Baleares', 'Jaén': 'provincia de Jaén', 'Navarra': 'Navarra', 'Rioja': 'La Rioja', 'Salamanca': 'provincia de Salamanca', 'Sòria': 'provincia de Soria', 'Sevilla': 'provincia de Sevilla', 'Cadis': 'provincia de Cádiz', 'Màlaga': 'provincia de Málaga', 'Albacete': 'provincia de Albacete', 'Granada': 'provincia de Granada', 'Valladolid': 'provincia de Valladolid', 'Madrid': 'provincia de Madrid', 'Saragossa': 'provincia de Zaragoza', 'Castelló': 'provincia de Castellón', 'Alacant': 'provincia de Alicante', 'Osca': 'provincia de Huesca', 'Terol': 'provincia de Teruel', 'València': 'provincia de Valencia', 'Almeria': 'provincia de Almería', 'Múrcia': 'Región de Murcia', 'Lleida': 'provincia de Lleida', 'Girona': 'provincia de Girona', 'Tarragona': 'provincia de Tarragona', 'Barcelona': 'provincia de Barcelona'}
    
    fusilados = []
    with open('represaliados-catalunya.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if row[25] == 'executat/da':
                if row[11] != 'Espanya': #meter estos casos especiales a mano
                    #print(row)
                    continue
                fusilados.append(row)
                #print(row)
    
    #Codi,Cognoms nom,Cognoms,Nom,Sexe,Edat,Municipi naixement,Pedanies/Agregats naixement,Comarca naixement,Província naixement,Comunitat autònoma naixement,País naixement,Municipi residència,Pedanies/Agregats residencia,Comarca residència,Província residència,Comunitat autònoma residència,País residència,Tipus procediment 1,Tipus procediment 2,Num causa,Any inicial,Any aprovació sen o altra resol,Pena,Commutació/indult (demanat),Afusellades,Ref num arxiu,Autoria de la descripció,Data de la descripció,Data correccio registre,Municipi_Naixement_Longitud_ETRS89,Municipi_Naixement_Latitud_ETRS89,Municipi_Residencia_Longitud_ETRS89,Municipi_Residencia_Latitud_ETRS89
    for fusilado in fusilados:
        apellidos = fusilado[2]
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
        nombrepila = fusilado[3]
        nombrecompleto = '%s %s' % (nombrepila, apellidos_)
        nombrecompleto2 = '%s, %s' % (apellidos_, nombrepila)
        sexo = fusilado[4]
        if sexo == 'Home':
            sexo = 'Hombre'
        elif sexo == 'Dona':
            sexo = 'Mujer'
        else:
            sexo = ''
        edad = fusilado[5]
        
        nacmuni = fusilado[6]
        if ', ' in nacmuni:
            nacmuni = nacmuni.split(', ')[1] + ' ' + nacmuni.split(', ')[0]
            nacmuni = nacmuni.replace("' ", "'")
        if nacmuni == '--':
            nacmuni = ''
        nacprov = fusilado[9]
        
        resmuni = fusilado[12]
        if ', ' in resmuni:
            resmuni = resmuni.split(', ')[1] + ' ' + resmuni.split(', ')[0]
            resmuni = resmuni.replace("' ", "'")
        if resmuni == '--':
            resmuni = ''
        
        pena = fusilado[23]
        if pena != 'Mort':
            print(fusilado)
            continue
        afuse = fusilado[25]
        if afuse != 'executat/da':
            print(fusilado)
            continue
        #print(fusilado[29])
        #print(nacprov)
        
        bio = ''
        if nacmuni:
            bio += '%s nació en [[%s]], [[%s]].' % (nombrepila, nacmuni, provtrans[nacprov])
        elif nacprov:
            bio += '%s nació en  [[%s]].' % (nombrepila, provtrans[nacprov])
        if edad:
            bio += ' Tenía %s años cuando fue %s.' % (edad, sexo=='Hombre' and 'fusilado' or 'fusilada')
        if bio:
            bio += '<ref name="transparenciacat-procediments">{{transparenciacat-procediments}}</ref>'
        print(bio)
        
        desc = '%s por el franquismo, %s.' % (sexo=='Hombre' and 'Represaliado' or 'Represaliada', sexo=='Hombre' and 'fusilado' or 'fusilada')
        print(desc)
        
        output = """{{Infobox Persona
|nombre=%s
|primer apellido=%s
|segundo apellido=%s
|sexo=%s
|lugar de nacimiento=%s
|lugar de fallecimiento=Cataluña
|lugar de residencia=%s
|edad=%s
|descripción=%s
|represión={{persona represaliada
|represión=Fusilamiento
|represor=Franquismo
|fecha=
|lugar=Cataluña
}}
}}
'''%s''', %s por el [[franquismo]], [[Lista de personas fusiladas por el franquismo|%s]] en [[Cataluña]].<ref name="arxiu-procediments">{{arxiu-procediments}}</ref><ref name="arxiu-sumarissims">{{arxiu-sumarissims}}</ref>

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
{{represión}}""" % (nombrepila, apellido1, apellido2, sexo, nacmuni and nacmuni or provtrans[nacprov], resmuni, edad, desc, nombrecompleto, sexo=='Hombre' and 'represaliado' or 'represaliada', sexo=='Hombre' and 'fusilado' or 'fusilada', bio and bio or '{{expandir}}')
        print(output)
        
        page = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), nombrecompleto)
        if page.exists() and len(page.text) > 1:
            print('Ya existe', nombrecompleto)
            f = open('fusilados-catalunya-yaexiste.txt', 'a')
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
