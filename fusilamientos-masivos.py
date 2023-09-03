#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2023 emijrp <emijrp@gmail.com>
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

import urllib.request
import pywikibot
import pywikibot.pagegenerators as pagegenerators
import re
import sys

def getURL(url=''):
    raw = ''
    req = urllib.request.Request(url, headers={ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0' })
    try:
        raw = urllib.request.urlopen(req).read().strip().decode('utf-8')
    except:
        try:
            raw = urllib.request.urlopen(req).read().strip().decode('latin-1')
        except:
            sleep = 10 # seconds
            maxsleep = 0
            while sleep <= maxsleep:
                print('Error while retrieving: %s' % (url))
                print('Retry in %s seconds...' % (sleep))
                time.sleep(sleep)
                try:
                    raw = urllib.request.urlopen(req).read().strip().decode('utf-8')
                except:
                    pass
                sleep = sleep * 2
    return raw

def month2number(month=""):
    month = month.lower().strip()
    months = {"enero":1,"febrero":2,"marzo":3,"abril":4,"mayo":5,"junio":6,"julio":7,"agosto":8,"septiembre":9,"octubre":10,"noviembre":11,"diciembre":12}
    if month in months.keys():
        return months[month]
    return 1

def main():
    month2number
    site = pywikibot.Site('15mpedia', '15mpedia')
    for year in range(1936, 1940):
        for month in ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]:
            if year == 1936:
                if month2number(month) <= 6:
                    continue
            if year == 1939:
                if month2number(month) >= 4:
                    continue
            for day in range(1, 32):
                dateslash = "%s/%02d/%02d" % (year, month2number(month), day)
                datetitle = "%s de %s de %s" % (day, month, year)
                datetitle_ = re.sub(" ", "_", datetitle)
                print(datetitle_)
                url = "https://15mpedia.org/wiki/%s" % (datetitle_)
                raw = getURL(url=url)
                m = re.findall(r"(?im)title=\"([^<>]+?)\">\1</a>\s*</td>\s*<td>\s*Represaliad[ao] por el franquismo, fusilad[ao]", raw)
                if m:
                    print(m)
                    places = m
                    placesunique = list(set(places))
                    placesunique.sort()
                    for place in placesunique:
                        #if " " in place: #temp de momento solo sitios con nombre sin espacios
                        #    continue
                        if re.search(r"(?im)[\(\)\?\,\.àèìòùñç]", place):
                            continue
                        if places.count(place) >= 10:
                            print(place)
                            title = "Fusilamientos del %s en %s" % (datetitle, place)
                            text = """{{Infobox Acontecimiento Masacre
|tipo=Fusilamiento masivo
|perpretador=Franquismo
|fecha=%s
|municipio=%s
}}""" % (dateslash, place)
                            print(title)
                            print(text)
                            page = pywikibot.Page(site, title)
                            if not page.exists():
                                page.text = text
                                page.save("BOT - Creando página")

if __name__ == '__main__':
    main()

