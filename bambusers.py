#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012-2014 emijrp <emijrp@gmail.com>
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
import os
import re
import sys
import time
import urllib

def month2number(month):
    m = month.lower()
    if m == 'jan':
        return '01'
    elif m == 'feb':
        return '02'
    elif m == 'mar':
        return '03'
    elif m == 'apr':
        return '04'
    elif m == 'may':
        return '05'
    elif m == 'jun':
        return '06'
    elif m == 'jul':
        return '07'
    elif m == 'aug':
        return '08'
    elif m == 'sep':
        return '09'
    elif m == 'oct':
        return '10'
    elif m == 'nov':
        return '11'
    elif m == 'dec':
        return '12'
    return ''

user = re.sub(u'\+', u' ', sys.argv[1])
print 'Downloading videos for user:', user
skipuntil = ''
if len(sys.argv) > 2:
    skipuntil = sys.argv[2]
path = user
if not os.path.exists('%s/' % (path)):
    os.makedirs(user)

channel = 'http://bambuser.com/channel/%s' % (user)
rss = 'http://feed.bambuser.com/channel/%s.rss' % (user)

#load bambuser ids imported in the past (to exclude them)
f = open('imported', 'r')
imported = f.read()
imported = imported.split('\n')
f.close()

raw = urllib.urlopen(rss).read()
lastvideoid = re.findall(ur"(?im)<link>http://bambuser\.com/v/(\d+)</link>", raw)[0]

videoids = []
thumbs = []
c = 0
pageurl = "http://bambuser.com/v/%s?page_profile_more_user=" % (lastvideoid)
raw2 = unicode(urllib.urlopen(pageurl).read(), 'utf-8')
limit = 1
try:
    limit = int(re.findall(ur"(?im)page_profile_more_user=\d+\">(\d+)</a></li></ul>", raw2)[0])
except:
    pass
print 'Scraping videos from %d pages' % (limit)
while c < limit:
    pageurl2 = pageurl + str(c)
    raw3 = urllib.urlopen(pageurl2).read()
    videoids += re.findall(ur"(?im)<a class=\"preview-wrapper\" href=\"http://bambuser.com/v/(\d+)\">", raw3)
    c += 1
    #break

print 'Loaded ids for %d videos' % (len(videoids))

#save ids
f = open('bambuser-%s-ids.txt' % (user), 'w')
save = '\n'.join(videoids)
f.write(save.encode('utf-8'))
f.close()
save = ''

videos = {}
c = 0
if skipuntil:
    print 'Skipping until', skipuntil

f = open('bambuser-%s-metadata.txt' % (user), 'a')
for videoid in videoids:
    if skipuntil:
        if videoid == skipuntil:
            skipuntil = ''
        continue
        
    if videoid in imported:
        print 'Video %s was imported in the past, skipping' % (videoid)
        continue
    else:
        print 'Downloading metadata and screenshot for video %s' % (videoid)
    
    videourl = "http://bambuser.com/v/%s" % (videoid)
    raw4 = unicode(urllib.urlopen(videourl).read(), 'utf-8')
    title = re.findall(ur"<span class=\"title\" title=\"([^>]*?)\"></span>", raw4)[0]
    thumb = re.findall(ur"(?im)<meta property=\"og:image\" content=\"([^>]*?)\" />", raw4)[0].split('?')[0] #removing trailing .jpg?2
    try:
        urllib.urlretrieve(thumb, '%s/Bambuser - %s - %s.%s' % (path, user, videoid, thumb.split('.')[-1]))
    except:
        print 'Error while downloading image, trying again in 10 seconds'
        time.sleep(10)
        try:
            urllib.urlretrieve(thumb, '%s/Bambuser - %s - %s.%s' % (path, user, videoid, thumb.split('.')[-1]))
        except:
            print 'Failed again, skipping this video'
            continue
        
    try:
        [likes, views, lives] = re.findall(ur"(?im)<div class=\"like\" data-upvotes=\"([0-9]+?)\">.*?<span class=\"broadcast-views\"><span class=\"views-total\">([0-9]+?)</span> views \(<span class=\"views-live\">([0-9]+?)</span>", raw4)[0]
    except:
        [likes, views, lives] = ['0', '0', '0']
    comments = ''
    try:
        coord = re.findall(ur"(?im)<meta property=\"bambuser_com:position:latitude\" content=\"([^\"]+?)\" /><meta property=\"bambuser_com:position:longitude\" content=\"([^\"]+?)\" />", raw4)[0]
        if coord:
            coord = '%s, %s' % (coord[0], coord[1])
    except:
        coord = ''
    date = ''
    date2 = ''
    hour = ''
    try:
        date2 = re.findall(ur"(?im)<div id=\"broadcast-date\">\s*<p>([^<]*?)</p>", raw4)[0]
    except:
        date2 = re.findall(ur"(?im)<div id=\"broadcast-date\">\s*<p id=\"upload-recorded-date\"><span class=\"date-label\">Recorded </span>([^<]*?)<br>", raw4)[0]
    #9 Nov 2009 18:39 CET
    if not ':' in date2.split(' ')[2] and int(date2.split(' ')[2]) > 2000 and int(date2.split(' ')[2]) < 2020:
        date = '%s/%s/%02d' % (date2.split(' ')[2], month2number(date2.split(' ')[1]), int(date2.split(' ')[0]))
        hour = date2.split(' ')[3]
    else:
        date = '%s/%s/%02d' % (datetime.datetime.now().year, month2number(date2.split(' ')[1]), int(date2.split(' ')[0]))
        hour = date2.split(' ')[2]
    
    if not likes:
        likes = '0'
    tags = re.findall(ur"(?im)<span class=\"tag\" style=\"display:none;\" title=\"([^>]*?)\"></span>", raw4)
    videos[videoid] = {
        'likes': likes, 'views': views, 'lives': lives,
        'coord': coord,
        'date': date,
        'hour': hour,
        'tags': tags,
        'user': user,
    }
    save1 = u';;;'.join([videoid, coord, date, hour, likes, views, lives, title, ', '.join(tags), user])
    save1 += u'\n'
    #print save1
    f.write(save1.encode('utf-8'))
    c += 1
    time.sleep(0.3)

f.close()
