#!/usr/bin/python
# -*- coding: utf-8 -*-

import wikipedia

for year in ['2011', '2012', '2013', '2014']:
    for month, monthnum in [['enero', '01'], ['febrero', '02'], ['marzo', '03'], ['abril', '04'], ['mayo', '05'], ['junio', '06'], ['julio', '07'], ['agosto', '08'], ['septiembre', '09'], ['octubre', '10'], ['noviembre', '11'], ['diciembre', '12']]:
		print month, year
		mesnombre = u'%s de %s' % (month, year)
		mesiso = u'%s-%s' % (year, monthnum)

		p = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), u'Categoría:%s' % mesnombre)
		#if not p.exists():
		output = u"""{{navegación por mes categoría|mes=%s}}""" % (mesiso)
		p.put(output, u"BOT - Creando categoría mes")

