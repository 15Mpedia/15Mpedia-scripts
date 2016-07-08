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
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import re
import sys
import urllib
from twython import Twython

#config
botscreenname = 'Emijrp'
imagename = 'memoria.png'

def read_keys():
    f = open('%s/.twitter_keys' % (os.path.dirname(os.path.realpath(__file__))), 'r')
    w = f.read()
    APP_KEY = re.findall(r'(?im)^AP[IP]_KEY\s*=\s*([^\n]+?)\s*$', w)[0].strip()
    APP_SECRET = re.findall(r'(?im)^AP[IP]_SECRET\s*=\s*([^\n]+?)\s*$', w)[0].strip()
    return APP_KEY, APP_SECRET

def read_tokens():
    f = open('%s/.twitter_tokens' % (os.path.dirname(os.path.realpath(__file__))), 'r')
    w = f.read()
    OAUTH_TOKEN = re.findall(r'(?im)^OAUTH_TOKEN\s*=\s*([^\n]+?)\s*$', w)[0].strip()
    OAUTH_TOKEN_SECRET = re.findall(r'(?im)^OAUTH_TOKEN_SECRET\s*=\s*([^\n]+?)\s*$', w)[0].strip()
    return OAUTH_TOKEN, OAUTH_TOKEN_SECRET

def main():
    APP_KEY, APP_SECRET = read_keys()
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET = read_tokens()
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    month2name = {'01': 'enero', '02': 'febrero', '03': 'marzo', '04': 'abril', '05': 'mayo', '06': 'junio', 
                  '07': 'julio', '08': 'agosto', '09': 'septiembre', '10': 'octubre', '11': 'noviembre', '12': 'diciembre' }
    
    d = datetime.datetime.now()
    today = '%s de %s' % (int(d.strftime('%d')), month2name[d.strftime('%m')])
    today_ = re.sub(' ', '_', today)
    
    raw = urllib.request.urlopen('https://15mpedia.org/w/index.php?title=Especial:Ask&q=[[persona+represaliada%%3A%%3A%%2B]]+[[represor%%3A%%3AFranquismo]]+[[represi%%C3%%B3n%%3A%%3AFusilamiento]]+[[fecha+string%%3A%%3A~*%%2F%s%%2F%s]]&p=format%%3Dbroadtable%%2Flink%%3Dall%%2Fheaders%%3Dshow%%2Fsearchlabel%%3D-26hellip%%3B-20siguientes-20resultados%%2Fclass%%3Dsortable-20wikitable-20smwtable&po=%%3FFecha+string%%0A&limit=500&eq=no' % (d.strftime('%m'), d.strftime('%d'))).read().decode('utf-8')
    m = re.findall(r'(?im)<td><a href="[^<>]*?" title="[^<>]*?">([^<>]*?)</a></td>\s*<td class="Fecha-string">(\d\d\d\d)[^<>]+?</td>', raw)
    fusilados = []
    for i in m:
        fusilados.append([i[1],i[0]])
    fusilados.sort()
    
    if not fusilados:
        sys.exit()
    
    #generar imagen
    fusiladosnum = len(fusilados)
    high = 25
    img = Image.new('RGB', (500, fusiladosnum*high+220), (255, 255, 200))
    fonttitle = ImageFont.truetype("OpenSans-Regular.ttf", 25)
    fonttext = ImageFont.truetype("OpenSans-Regular.ttf", 18)
    fontfooter = ImageFont.truetype("OpenSans-Regular.ttf", 15)
    d = ImageDraw.Draw(img)
    d.text((20, high), 'Represión franquista', fill=(255, 0, 0), font=fonttitle)
    d.text((20, high*3), 'Estas personas fueron fusiladas un %s:' % (today), fill=(0, 0, 0), font=fonttext)
    c = 0
    for year, name in fusilados:
        d.text((30, high*c+110), '%d) %s (%s)' % (c+1, name, year), fill=(0, 0, 0), font=fonttext)
        c += 1

    d.text((20, high*c+90+high), 'Que sus nombres no caigan en el olvido.', fill=(0, 0, 255), font=fonttext)
    d.text((260, high*c+130+high), 'Fuente: Memoria y Libertad', fill=(0, 0, 0), font=fontfooter)
    d.text((260, high*c+150+high), 'Elaboración gráfica: 15Mpedia', fill=(0, 0, 0), font=fontfooter)
    
    img.save(imagename)
    
    #tuitear imagen
    img = open(imagename, 'rb')
    status = 'Un %s el franquismo los fusiló https://15mpedia.org/wiki/%s Que sus nombres no caigan en el olvido #memoria' % (today, today_)
    print(status)
    response = twitter.upload_media(media=img)
    raw = twitter.update_status(status=status, media_ids=[response['media_id']])
    tweetid = raw['id_str']
    print('Status:',status)
    print('Returned ID:',tweetid)

if __name__ == '__main__':
    main()
