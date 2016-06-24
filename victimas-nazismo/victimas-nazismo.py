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

"""
 cut -d';' -f13 victimas-nazismo.csv | sort | uniq -c | sort -n
 
     21 Dachau (Alemania)
     22 Mauthausen - campo exterminio nazi - Austria
     23 Buchenwald ?
     25 Buchenwald (Alemania) ? desaparecido
     27 Steyr
     49 Dachau
     55 Mauthausen (Gusen) - Alemania - campo nazi 
     59 Mauthausen (Austria)
     62 
     67 Gusen (Austria) - campo de exterminio nazi
     69 Hartheim (Austria)
    201 Mauthausen
    243 Gusen (campo exterminio) Austria
    286 Hartheim
    410 Gusen (Austria)
   1312 Gusen - Campo de concentración (Austria)
   1506 Gusen
"""

import re
import time
import urllib

def traducirfecha(fecha):
    trad = fecha
    meses = {1:'enero', 2:'febrero', 3:'marzo', 4:'abril', 5:'mayo', 6:'junio', 7:'julio', 8:'agosto', 9:'septiembre', 10:'octubre', 11:'noviembre', 12:'diciembre'}
    if len(fecha.split('.')) == 3:
        try:
            trad = '%s de %s de %s' % (int(fecha.split('.')[0]), meses[int(fecha.split('.')[1])], fecha.split('.')[2])
        except:
            trad = fecha.split('.')[0]
    
    return trad

def main():
    g = open('victimas-nazismo.csv', 'w')
    output = 'apellidosnombre;;;edad;;;procedencia;;;oficio;;;lugarfallecimiento;;;fechafallecimiento\n'
    g.write(output.encode('utf-8'))
    g.close()
    for page in range(1, 204):
        time.sleep(3)
        print 'pagina', page
        url = 'http://www.enrecuerdode.com/inclusiones.php?p=%s&name=&id_event=15&passawaydate=&passawayplace=&age=&placeoforigin=&job=' % (page)
        f = urllib.urlopen(url)
        html = unicode(f.read(), 'utf-8')
        html = re.sub(r'[\n\r]', '', html)
        m = re.findall(r'(?im)<tr class="(even|odd)">\s*<td class="date">([^<>]+?)</td>\s*<td>([^<>]+?)</td>\s*<td>([^<>]+?)</td>\s*<td class="age">([^<>]+?)</td>\s*<td>([^<>]+?)</td>\s*<td>([^<>]+?)</td>\s*<!--<td><a href="crear_homenaje\.php\?id=([^<>]+?)">Hacer un Homenaje</a></td>-->', html)
        for i in m:
            fechafallecimiento = i[1]
            lugarfallecimiento = i[2]
            apellidosnombre = i[3]
            if ', ' in i[3]:
                nombre = i[3].split(', ')[1]
                nombreapellidos = '%s %s' % (i[3].split(', ')[1], i[3].split(', ')[0])
            elif ',' in i[3]:
                nombre = i[3].split(',')[1]
                nombreapellidos = '%s %s' % (i[3].split(',')[1], i[3].split(',')[0])
            else:
                nombre = i[3]
                nombreapellidos = i[3]
            edad = i[4]
            procedencia = i[5]
            oficio = i[6] == '-' and '' or i[6]
            vicid = i[7]
            output = ';;;'.join([apellidosnombre, edad, procedencia, oficio, lugarfallecimiento, traducirfecha(fechafallecimiento)])
            output += '\n'
            g = open('victimas-nazismo.csv', 'a')
            g.write(output.encode('utf-8'))
            g.close()
        
if __name__ == '__main__':
    main()


