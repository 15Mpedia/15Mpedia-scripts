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
import re

def cleancell(cell):
    cell = cell.split('</span>')[0].split('>')[-1]
    cell = cell.replace('&nbsp;', '')
    cell = cell.replace('\n', '')
    cell = cell.replace('\r', '')
    cell = re.sub('  +', ' ', cell)
    
    return cell

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
    """
    <tr style="height:26.25pt" height="35">
    <td class="xl106" style="height:26.25pt;width:204pt" width="272" height="35">NOMBRE</td>
    <td class="xl90" style="border-left:none;width:71pt" width="94">FECHA DE LA
    MUERTE</td>
    <td class="xl90" style="border-left:none;width:68pt" width="90">FECHA NACIMIENTO</td>
    <td class="xl106" style="border-left:none;width:32pt" width="43">EDAD</td>
    <td class="xl106" style="border-left:none;width:167pt" width="222">LUGAR DE
    NACIMIENTO</td>
    <td class="xl106" style="border-left:none;width:68pt" width="91">PROVINCIA</td>
    <td class="xl106" style="border-left:none;width:153pt" width="204">LUGAR DE
    RESIDENCIA</td>
    <td class="xl106" style="border-left:none;width:77pt" width="102">PROVINCIA DE
    RESIDENCIA</td>
    <td class="xl106" style="border-left:none;width:76pt" width="101">APODO</td>
    <td colspan="2" class="xl170" style="border-right:1.0pt solid black;
    border-left:none;width:145pt" width="193">AFILIACI�N POL�TICA Y SINDICAL</td>
    <td class="xl113" style="width:161pt" width="214">CARGO/RANGO</td>
    <td class="xl106" style="border-left:none;width:125pt" width="166">PROFESI�N</td>
    <td class="xl90" style="border-left:none;width:62pt" width="83">FECHA DE
    DETENCI�N</td>
    <td class="xl106" style="border-left:none;width:112pt" width="149">LUGAR DE
    DETENCI�N</td>
    <td colspan="3" class="xl170" style="border-right:1.0pt solid black;
    border-left:none;width:332pt" width="442">CENTROS DE RECLUSI�N</td>
    <td class="xl106" style="border-left:none;width:72pt" width="96">CAUSA DE LA
    MUERTE</td>
    <td class="xl106" style="border-left:none;width:122pt" width="163">LUGAR DE LA
    MUERTE</td>
    <td colspan="3" class="xl170" style="border-right:1.0pt solid black;
    border-left:none;width:189pt" width="251">EXPEDIENTE SUMARIO / CAUSA</td>
    <td class="xl106" style="border-left:none;width:274pt" width="365">PROCEDENCIA DE
    LA INFORMACI�N</td>
    <td class="xl106" style="border-left:none;width:33pt" width="44">SEXO</td>
    <td class="xl106" style="border-left:none;width:329pt" width="438">OBSERVACIONES</td>
    </tr>
    """
    
    """
    <tr style="height:15.75pt" height="21">
    <td class="xl129" style="height:15.75pt;border-top:none;
    width:204pt" width="272" height="21">Abad Ramos, Sotero</td>
    <td class="xl67" style="border-top:none;border-left:none;width:71pt" width="94">10/07/1940</td>
    <td class="xl67" style="border-top:none;border-left:none;width:68pt" width="90">&nbsp;</td>
    <td class="xl68" style="border-top:none;border-left:none;width:32pt" width="43">30</td>
    <td class="xl68" style="border-top:none;border-left:none;width:167pt" width="222">Muduex</td>
    <td class="xl68" style="border-top:none;border-left:none;width:68pt" width="91">Guadalajara</td>
    <td class="xl68" style="border-top:none;border-left:none;width:153pt" width="204">Chamart�n
    de la Rosa</td>
    <td class="xl68" style="border-top:none;border-left:none;width:77pt" width="102">Madrid</td>
    <td class="xl68" style="border-top:none;border-left:none;width:76pt" width="101">&nbsp;</td>
    <td class="xl68" style="border-top:none;border-left:none;width:89pt" width="118">&nbsp;</td>
    <td class="xl68" style="border-top:none;border-left:none;width:56pt" width="75">&nbsp;</td>
    <td class="xl68" style="border-top:none;border-left:none;width:161pt" width="214">&nbsp;</td>
    <td class="xl68" style="border-top:none;border-left:none;width:125pt" width="166">Guardia
    de Asalto</td>
    <td class="xl67" style="border-top:none;border-left:none;width:62pt" width="83">&nbsp;</td>
    <td class="xl68" style="border-top:none;border-left:none;width:112pt" width="149">&nbsp;</td>
    <td class="xl68" style="border-top:none;border-left:none;width:113pt" width="150">&nbsp;</td>
    <td class="xl68" style="border-top:none;border-left:none;width:110pt" width="147">&nbsp;</td>
    <td class="xl68" style="border-top:none;border-left:none;width:109pt" width="145">&nbsp;</td>
    <td class="xl68" style="border-top:none;border-left:none;width:72pt" width="96">Fusilamiento</td>
    <td class="xl68" style="border-top:none;border-left:none;width:122pt" width="163">Cementerio
    del Este</td>
    <td class="xl68" style="border-top:none;border-left:none;width:77pt" width="102">25055-39</td>
    <td class="xl68" style="border-top:none;border-left:none;width:61pt" width="81">&nbsp;</td>
    <td class="xl68" style="border-top:none;border-left:none;width:51pt" width="68">&nbsp;</td>
    <td class="xl68" style="border-top:none;border-left:none;width:274pt" width="365">N��ez
    / Rojas / MyL (Archivo Gral M. Int. Fondo DGIIPP)</td>
    <td class="xl68" style="border-top:none;border-left:none;width:33pt" width="44">V</td>
    <td class="xl68" style="border-top:none;border-left:none;width:329pt" width="438">Lugar
    de nacimiento Muduex (C. Paramio)</td>
    </tr>
    """
    f = open('fusilados-tabla.html', 'r')
    html = unicode(f.read(), 'latin-1')
    f.close()
    
    rows = html.split('<tr ')[2:-2]
    for row in rows:
        row = '<tr ' + row
        cells = ['>'.join(x.split('>')[1:]).strip() for x in row.split('</td>')[:-1]]
        #print len(cells)
        
        nombre = '>'.join(cells[0].split('>')[1:])
        nombre = nombre.replace('\n', ' ')
        nombre = re.sub('  +', ' ', nombre)
        nombre = re.sub(r'(?im)(<span[^<>]*?>|</span>)', '', nombre)
        nombreurl = ''
        if '</a>' in nombre:
            nombreurl = nombre.split('href="')[1].split('" target="')[0]
            nombre = nombre.split('>')[1].split('<')[0]
        nombre = cleancell(nombre)
        if ', ' in nombre:
            nombrepila = nombre.split(', ')[1]
            apellidos = nombre.split(', ')[0]
            nombrecompleto = '%s %s' % (nombrepila, apellidos)
        else:
            nombrepila = nombre
            apellidos = ''
            nombrecompleto = nombre
        apellido1 = ''
        apellido2 = ''
        if apellidos:
            if len(apellidos.split(' ')) == 2:
                apellido1 = apellidos.split(' ')[0]
                apellido2 = apellidos.split(' ')[1]
            else:
                apellido1 = apellidos
                apellido2 = ''
        
        fecha_muerte = invertirfecha(cleancell(cells[1]))
        fecha_nacimiento = invertirfecha(cleancell(cells[2]))
        edad = cleancell(cells[3])
        lugar_nacimiento = cleancell(cells[4])
        provincia_nacimiento = cleancell(cells[5])
        lugar_residencia = cleancell(cells[6])
        provincia_residencia = cleancell(cells[7])
        apodo = cleancell(cells[8])
        afiliacion1 = cleancell(cells[9])
        afiliacion2 = cleancell(cells[10])
        cargo = cleancell(cells[11])
        profesion = cleancell(cells[12])
        fecha_detencion = invertirfecha(cleancell(cells[13]))
        lugar_detencion = cleancell(cells[14])
        centro1 = cleancell(cells[15])
        centro2 = cleancell(cells[16])
        centro3 = cleancell(cells[17])
        causa_muerte = cleancell(cells[18])
        lugar_muerte = cleancell(cells[19])
        expediente1 = cleancell(cells[20])
        expediente2 = cleancell(cells[21])
        expediente3 = cleancell(cells[22])
        procedencia_info = cleancell(cells[23])
        sexo = cleancell(cells[24])
        if sexo == 'V':
            sexo = 'Hombre'
        elif sexo == 'M':
            sexo = 'Mujer'
        else:
            sexo = ''
        observaciones = cleancell(cells[25])
        
        #print nombre, fecha_muerte, fecha_nacimiento, edad, lugar_nacimiento, provincia_nacimiento, lugar_residencia, provincia_residencia, apodo, afiliacion1, afiliacion2, cargo, profesion, fecha_detencion, lugar_detencion, centro1, centro2, centro3, causa_muerte, lugar_muerte, expediente1, expediente2, expediente3, procedencia_info, sexo, observaciones
        
        #print causa_muerte.encode('utf-8'), lugar_muerte.encode('utf-8')
        
        # Sotero nació en la [[provincia de Guadalajara]]. Era Guardia Civil y fue fusilado cuando tenía 30 años.
        bio = ''
        if lugar_nacimiento:
            bio += u'%s nació en [[%s]]%s.' % (nombrepila, lugar_nacimiento, provincia_nacimiento and provincia_nacimiento!=lugar_nacimiento and ', [[%s]]' % provincia_nacimiento or '')
        
        if profesion:
            if edad:
                 bio += u' Era %s y tenía %s años cuando fue %s.' % (profesion.lower(), edad, sexo=='Hombre' and 'fusilado' or 'fusilada')
            else:
                 bio += u' Era %s.' % (profesion.lower())
        
        if bio:
            bio += u'<ref name="myl" />'
        
        ee = u''
        if nombreurl:
            bio += u'<ref name="quieneseran">[%s %s] en [[Quiénes eran]]</ref>' % (nombreurl, nombrecompleto)
            ee = u'\n* [%s %s] en [[Quiénes eran]]' % (nombreurl, nombrecompleto)
        
        refrojas = u'<ref name="nr1997">{{Núñez-Rojas-1997}}</ref>'
        refcemeste = u'<ref name="fuscemeste">{{Fusilados-Cementerio-Este}}</ref>'
        
        if causa_muerte.lower() == 'fusilamiento':
            #print edad.encode('utf-8'), nombre.encode('utf-8')
            output = u"""{{Infobox Persona
|nombre=%s
|primer apellido=%s
|segundo apellido=%s
|sexo=%s
|lugar de nacimiento=%s%s
|fecha de nacimiento=%s
|lugar de fallecimiento=Madrid
|fecha de fallecimiento=%s
|ocupación=%s
|represión={{represión datos|represión=Fusilamiento|represor=Franquismo|fecha=%s|lugar=%s}}
}}
'''%s''', %s por el [[franquismo]], %s el [[%s]] en %s[[Madrid]].<ref name="myl">{{memoria-y-libertad}}</ref>%s%s<ref name="mmpce">{{Memorial-Madrid-PCE}}</ref>

== Biografía ==

%s

== Véase también ==
* [[Memoria histórica]]
* [[Represión franquista]]
* [[Lista de personas]]

== Referencias ==
{{reflist}}

== Enlaces externos ==
{{enlaces externos}}%s
<!--
* {{memoria pública|}}
* {{mcu represión|}}
-->
{{represión}}""" % (nombrepila, apellido1, apellido2, sexo, lugar_nacimiento, provincia_nacimiento and provincia_nacimiento!=lugar_nacimiento and ', %s' % (provincia_nacimiento) or '', fecha_nacimiento, fecha_muerte, profesion.lower(), fecha_muerte, 'Cementerio del Este' in lugar_muerte and 'Cementerio del Este' or '', nombrecompleto, sexo=='Hombre' and 'represaliado' or 'represaliada', sexo=='Hombre' and 'fusilado' or 'fusilada', traducirfecha(fecha_muerte), 'Cementerio del Este' in lugar_muerte and 'el Cementerio del Este de ' or '', 'Rojas' in procedencia_info and refrojas or '', 'Cementerio del Este' in lugar_muerte and refcemeste or '', bio and bio or '{{expandir}}', ee)
            print output.encode('utf-8')
            page = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), nombrecompleto)
            if page.exists():
                f = open('yaexiste.txt', 'a')
                f.write(u'%s\n%s' % (output.encode('utf-8'), '-'*50))
                f.close()
            else:
                page.text = output
                page.save(u'BOT - Creando página', botflag=False)
                
                redtext = u'#REDIRECT [[%s]]' % (nombrecompleto)
                red = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), nombre)
                red.text = redtext
                red.save(u'BOT - Creando redirección a [[%s]]' % (nombrecompleto), botflag=True)

if __name__ == '__main__':
    main()
