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
import os
import re
import urllib
from twython import Twython

#config
botscreenname = '15MpediaLabs'
imagename = 'memjora.png'

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
    
    #raw = urllib.request.urlopen('https://15mpedia.org/w/index.php?title=Especial:Ask&q=[[Page+has+default+form%3A%3AArchivo]]+[[Categor%C3%ADa%3AArchivos+de+Foto+Spanish+Revolution]]+[[Categor%C3%ADa%3AArchivos+sin+palabras+clave]]&p=format%3Dbroadtable%2Flink%3Dall%2Fheaders%3Dshow%2Fsearchlabel%3D-26hellip%3B-20siguientes-20resultados%2Fclass%3Dsortable-20wikitable-20smwtable&po=%3FAutor%0A&order=random&limit=1&eq=no').read().decode('utf-8')
    #m = re.findall(r'(?im)<td><a href="/wiki/Archivo:([^<> ]*?)" title=[^>]*?>[^<>]*?</a></td>[^<>]*?<td class="Autor">([^<>]*?)</td>', raw)
    
    #generar imagen
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
    d.text((20, high), 'Represión franquista', fill=(255, 0, 0), font=fonttitle)
    d.text((20, high*3), 'Estas personas fueron fusiladas un %s:' % (today), fill=(0, 0, 0), font=fonttext)
    for i in range(fusiladosnum):
        d.text((30, high*i+110), '%s) José José José José (1940)' % (i+1), fill=(0, 0, 0), font=fonttext)

    d.text((20, high*(i+1)+90+high), 'Que sus nombres no caigan en el olvido.', fill=(0, 0, 255), font=fonttext)
    d.text((260, high*(i+1)+130+high), 'Fuente: Memoria y Libertad', fill=(0, 0, 0), font=fontfooter)
    d.text((260, high*(i+1)+150+high), 'Elaboración gráfica: 15Mpedia', fill=(0, 0, 0), font=fontfooter)
    
    img.save('memoria.png')
    
    #tuitear imagen
    img = open(imagename, 'rb')
    status = 'Personas fusiladas un %s. Que sus nombres no caigan en el olvido https://15mpedia.org/wiki/%s #memoria' % (today, today_)
    print(status)
    response = twitter.upload_media(media=img)
    raw = twitter.update_status(status=status, media_ids=[response['media_id']])
    tweetid = raw['id_str']
    print('Status:',status)
    print('Returned ID:',tweetid)

if __name__ == '__main__':
    main()
