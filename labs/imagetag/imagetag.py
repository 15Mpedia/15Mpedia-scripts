#!/usr/bin/env python
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

import csv
import datetime
import hashlib
import os
import random
import re
import sys
import urllib
from twython import Twython

#config
botscreenname = '15MpediaLabs'
thumbname = 'thumb.jpg'
csvtweets = 'imagetag-tweets.csv'
csvreplies = 'imagetag-replies.csv'

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

def loadcsvtweets():
    tweets = []
    if os.path.exists(csvtweets):
        f = csv.reader(open(csvtweets, 'r'), delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in f:
            tweets.append(row)
    return tweets

def loadcsvreplies():
    replies = []
    if os.path.exists(csvreplies):
        f = csv.reader(open(csvreplies, 'r'), delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in f:
            replies.append(row)
    return replies

def getwhitelist():
    #load user whitelist
    raw = urllib.request.urlopen('https://raw.githubusercontent.com/15Mpedia/15Mpedia-scripts/master/labs/imagetag/whitelist.txt').readall()
    whitelist = [x.decode("utf-8") for x in raw.splitlines()]
    print(len(whitelist),'users in whitelist')
    return whitelist
    
def tweet(twitter):
    #seleccionar imagen aleatoria
    raw = urllib.request.urlopen('https://15mpedia.org/w/index.php?title=Especial:Ask&q=[[Page+has+default+form%3A%3AArchivo]]+[[Categor%C3%ADa%3AArchivos+de+Foto+Spanish+Revolution]]+[[Categor%C3%ADa%3AArchivos+sin+palabras+clave]]&p=format%3Dbroadtable%2Flink%3Dall%2Fheaders%3Dshow%2Fsearchlabel%3D-26hellip%3B-20siguientes-20resultados%2Fclass%3Dsortable-20wikitable-20smwtable&po=%3FAutor%0A&order=random&limit=1&eq=no').read().decode('utf-8')
    m = re.findall(r'(?im)<td><a href="/wiki/Archivo:([^<> ]*?)" title=[^>]*?>[^<>]*?</a></td>[^<>]*?<td class="Autor">([^<>]*?)</td>', raw)
    filename = m[0][0]
    authorship = ' '.join(m[0][1].split(']')[0].split(' ')[1:])
    md5 = hashlib.md5(filename.encode('utf-8')).hexdigest()
    urlfile = 'https://15mpedia.org/wiki/Archivo:%s' % (filename)
    urlfile2 = 'https://15mpedia.org/w/images/%s/%s/%s' % (md5[0], md5[:2], filename)
    if os.path.exists(thumbname): #remove previous thumb
        os.remove(thumbname)
    urllib.request.urlretrieve(urlfile2, thumbname)
    os.system('convert -resize 1024X768 %s %s2' % (thumbname, thumbname)) #resize
    os.system('mv %s2 %s' % (thumbname, thumbname)) #rename
    
    #tuitear imagen aleatoria
    thumb = open(thumbname, 'rb')
    status = 'Indica #tags para esta foto tomada por %s %s' % (authorship, urlfile)
    print(status)
    response = twitter.upload_media(media=thumb)
    raw = twitter.update_status(status=status, media_ids=[response['media_id']])
    tweetid = raw['id_str']
    print('Status:',status)
    print('Returned ID:',tweetid)
    
    #guardar tuit en csv
    if not os.path.exists(csvtweets):
        f = open(csvtweets, 'w')
        f.write('tweetid|filename|text\n')
        f.close()
    f = csv.writer(open(csvtweets, 'a'), delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    f.writerow([tweetid,filename,status])

def getreplies(twitter):
    whitelist = getwhitelist()
    tweets = loadcsvtweets()
    
    #guardar replies en csv
    if not os.path.exists(csvreplies):
        f = open(csvreplies, 'w')
        f.write('replyid|replyauthor|replyto|text\n')
        f.close()
    repliesold = []
    if os.path.exists(csvreplies):
        f = csv.reader(open(csvreplies, 'r'), delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in f:
            repliesold.append(row)
    replies = twitter.get_mentions_timeline(count=200)
    repliesnew = []
    for reply in replies:
        #saltar si no es whitelist
        if not reply['user']['screen_name'] in whitelist:
            #print('Not in whitelist',reply['user']['screen_name'])
            continue
        #saltar si no responde al bot, a un tuit o a un tuit del bot
        if reply['in_reply_to_screen_name'] != botscreenname or \
           reply['in_reply_to_status_id_str'] == None or \
           not reply['in_reply_to_status_id_str'] in [tweet[0] for tweet in tweets]:
            continue
        if reply['id_str'] in [replyold[0] for replyold in repliesold]: #evitar duplicados
            continue
        repliesnew.append([reply['id_str'],reply['user']['screen_name'],reply['in_reply_to_status_id_str'],reply['text']])
    
    f = csv.writer(open(csvreplies, 'a'), delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in repliesnew:
        f.writerow(row)

def extractkeywords(replytext):
    keywords = []
    temp = re.sub(',', ' ', replytext)
    temp = ' '.join(temp.split(' ')[1:]).split(' ') # remove "@15MpediaLabs " prefix
    for k in temp:
        k = re.sub('_', ' ', k.strip())
        if not k.startswith('#') or len(k) <= 2: #   #BN (blanco y negro) es tag tipico
            continue
        k = k[1:] # remove first #
        if not k in keywords:
            keywords.append(k)
    keywords.sort()
    return keywords

def stats(twitter):
    tweets = loadcsvtweets()
    replies = loadcsvreplies()
    stats = {}
    for replyid, replyauthor, replyto, replytext in replies:
        if replyauthor == 'replyauthor':
            continue
        if replyauthor in stats:
            stats[replyauthor] += len(extractkeywords(replytext))
        else:
            stats[replyauthor] = len(extractkeywords(replytext))
    stats_l = [[v, k] for k, v in stats.items()]
    stats_l.sort(reverse=True)
    
    status = 'Estadísticas de #tags: %s https://15mpedia.org/w/index.php?limit=50&tagfilter=&title=Especial%%3AContribuciones&contribs=user&target=BotQuincemayista&namespace=6&year=&month=-1' % (', '.join(['@%s (%s)' % (user, score) for score, user in stats_l[:4]]))
    print(status)
    twitter.update_status(status=status)
    print('Estadísticas completas:')
    print(', '.join(['@%s (%s)' % (user, score) for score, user in stats_l]))

def main():
    APP_KEY, APP_SECRET = read_keys()
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET = read_tokens()
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    if len(sys.argv) < 2:
        print('Missing option: --tweet or --get-replies')
        sys.exit()
    else:
        if sys.argv[1] == '--tweet':
            tweet(twitter)
        elif sys.argv[1] == '--get-replies':
            getreplies(twitter)
        elif sys.argv[1] == '--whitelist':
            print(getwhitelist())
        elif sys.argv[1] == '--stats':
            stats(twitter)
        else:
            print('Wrong parameter')
            sys.exit()
    
if __name__ == '__main__':
    main()
