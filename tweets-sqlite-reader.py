#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2014 emijrp
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
import sqlite3

def main():
    hashtags_dic = {}
    conn = sqlite3.connect('occupy_tweets_8.sqlite')
    c = conn.cursor()
    for row in c.execute('SELECT * FROM swdata WHERE 1'):
        tweet = re.sub(ur'\n', ur' ', row[2])
        hashtags = re.findall(ur'(?im)\#[a-z0-9áéíóúñç]+', tweet)
        for hashtag in hashtags:
            if hashtag.lower() in hashtags_dic:
                hashtags_dic[hashtag.lower()] += 1
            else:
                hashtags_dic[hashtag.lower()] = 1
    
    hashtags = []
    for hashtag, c in hashtags_dic.items():
        hashtags.append([c, hashtag])
    hashtags.sort()
    hashtags.reverse()
    line = u'\n'.join([u' '.join([str(c), hashtag]) for c, hashtag in hashtags[:1000]])
    print line.encode('utf-8')

if __name__ == '__main__':
    main()
