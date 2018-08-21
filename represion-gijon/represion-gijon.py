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

#import pywikibot
import re


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
            personas.append(persona)
            print(persona)

if __name__ == '__main__':
    main()
