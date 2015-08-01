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

import re
import urllib

def main():
    url = 'http://www.todoslosnombres.org/busqueda-personas'
    f = urllib.urlopen(url)
    html = f.read()
    
    html = html.split('<label for="edit-field-municipio-de-nac-term">')[1].split('</select>')[0]
    
    output = ''
    m = re.findall(ur'(?im)<option value="(\d+)">([^<]+?)</option>', html)
    for i in m:
        output += """{{#set_internal:todos_los_nombres
|id=%s
|municipio=%s
}}""" % (i[0], i[1])
    
    print output

if __name__ == '__main__':
    main()
