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

import datetime
import Image
import ImageDraw
import ImageFont
import re

def main():
    month2name = {'01': u'enero', '02': u'febrero', '03': u'marzo', '04': u'abril', '05': u'mayo', '06': u'junio', 
                  '07': u'julio', '08': u'agosto', '09': u'septiembre', '10': u'octubre', '11': u'noviembre', '12': u'diciembre' }
    fusiladosnum = 5
    d = datetime.datetime.now()
    today = '%s de %s' % (int(d.strftime('%d')), month2name[d.strftime('%m')])
    today_ = re.sub(' ', '_', today)
    high = 25
    img = Image.new('RGB', (500, fusiladosnum*high+220), (255, 255, 200))
    fonttitle = ImageFont.truetype("OpenSans-Regular.ttf", 25)
    fonttext = ImageFont.truetype("OpenSans-Regular.ttf", 18)
    fontfooter = ImageFont.truetype("OpenSans-Regular.ttf", 15)
    d = ImageDraw.Draw(img)
    d.text((20, high), u'Represión franquista', fill=(255, 0, 0), font=fonttitle)
    d.text((20, high*3), u'Estas personas fueron fusiladas un %s:' % (today), fill=(0, 0, 0), font=fonttext)
    for i in range(fusiladosnum):
        d.text((30, high*i+110), u'%s) José José José José (1940)' % (i+1), fill=(0, 0, 0), font=fonttext)

    d.text((20, high*(i+1)+90+high), u'Que sus nombres no caigan en el olvido.', fill=(0, 0, 255), font=fonttext)
    d.text((260, high*(i+1)+130+high), u'Fuente: Memoria y Libertad', fill=(0, 0, 0), font=fontfooter)
    d.text((260, high*(i+1)+150+high), u'Elaboración gráfica: 15Mpedia', fill=(0, 0, 0), font=fontfooter)
    
    img.save('memoria.png')

if __name__ == '__main__':
    main()
