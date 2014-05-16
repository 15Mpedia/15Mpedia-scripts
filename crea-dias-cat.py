#!/usr/bin/python
# -*- coding: utf-8 -*-

import wikipedia

for year in ['2011', '2012', '2013', '2014']:
    for month, monthnum in [['enero', '01'], ['febrero', '02'], ['marzo', '03'], ['abril', '04'], ['mayo', '05'], ['junio', '06'], ['julio', '07'], ['agosto', '08'], ['septiembre', '09'], ['octubre', '10'], ['noviembre', '11'], ['diciembre', '12']]:
        for day in range(1, 32):
            if month == 'febrero' and day > 28:
                continue
            if month in ['abril', 'junio', 'septiembre', 'noviembre'] and day > 30:
                continue
            print day, month, year
            dianombre = u'%s de %s de %s' % (day, month, year)
            diaiso = u'%s-%s-%02d' % (year, monthnum, day)

            p = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), u'Categoría:%s' % dianombre)
            #if not p.exists():
            output = u"""{{navegación por día categoría|día=%s}}""" % (diaiso)
            p.put(output, u"BOT - Creando categoría día")

