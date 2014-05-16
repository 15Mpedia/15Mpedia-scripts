#!/usr/bin/python
# -*- coding: utf-8 -*-

import wikipedia

site = wikipedia.Site('15mpedia', '15mpedia')

overwrite = False
colectivo = u"Manifestación"
colectivos = u"Manifestaciones"

ccaa = {
	u"Andalucía": [u"Almería", u"Cádiz", u"Córdoba", u"Granada", u"Huelva", u"Jaén", u"Málaga", u"Sevilla"], 
	u"Aragón": [u"Huesca", u"Teruel", u"Zaragoza"], 
	u"Canarias": [u"Las Palmas", u"Santa Cruz de Tenerife"], 
	u"Cantabria": [u"Cantabria"], 
	u"Castilla-La Mancha": [u"Albacete", u"Ciudad Real", u"Cuenca", u"Guadalajara", u"Toledo"], 
	u"Castilla y León": [u"Ávila", u"Burgos", u"León", u"Palencia", u"Salamanca", u"Segovia", u"Soria", u"Valladolid", u"Zamora"], 
	u"Cataluña": [u"Barcelona", u"Girona", u"Lleida", u"Tarragona"], 
	u"Comunidad de Madrid": [u"Madrid"], 
	u"Comunidad Foral de Navarra": [u"Navarra"], 
	u"Comunidad Valenciana": [u"Alicante", u"Castellón", u"Valencia"], 
	u"Extremadura": [u"Badajoz", u"Cáceres"], 
	u"Galicia": [u"A Coruña", u"Lugo", u"Ourense", u"Pontevedra"], 
	u"Islas Baleares": [u"Baleares"], 
	u"La Rioja": [u"La Rioja"], 
	u"País Vasco": [u"Álava", u"Gipuzkoa", u"Vizcaya"], 
	u"Principado de Asturias": [u"Asturias"], 
	u"Región de Murcia": [u"Murcia"], 
}

for comunidad, provincias in ccaa.items():
	de = u'de'
	if comunidad == u'Islas Baleares':
		de = u'de las'
	elif comunidad in [u'País Vasco', u'Principado de Asturias']:
		de = u'del'
	elif comunidad in [u'Comunidad Foral de Navarra', u'Comunidad de Madrid', u'Comunidad Valenciana', u'Región de Murcia']:
		de = u'de la'
	
	entradilla = u""
	if len(provincias) == 1: #CC.AA. uniprovinciales
		entradilla = u"""<!--
Según la '''provincia''':
* [[Lista de %s de la provincia de %s]]
-->""" % (colectivos.lower(), provincias[0])
		redtitle = u"Lista de %s de la provincia de %s" % (colectivos.lower(), provincias[0])
		redpage = wikipedia.Page(site, redtitle)
		if overwrite or not redpage.exists():
			redtext = u"#REDIRECT [[Lista de %s %s %s]]" % (colectivos.lower(), de, comunidad)
			redpage.put(redtext, u"BOT - %s" % (redtext))
	else: #CC.AA. de varias provincias
		entradilla = u"""\nSegún la '''provincia''':
%s""" % (u'\n'.join([u"""* [[Lista de %s de la provincia de %s]] ({{%s por lugar|país=España|comunidad autónoma=%s|provincia=Provincia de %s|format=count}})""" % (colectivos.lower(), provincia, colectivos.lower(), comunidad, provincia) for provincia in provincias]))
	
	#CC.AA. página
	wtitle = u"Lista de %s %s %s" % (colectivos.lower(), de, comunidad)
	wtext = u"""La siguiente es una '''lista de %s %s %s'''. En este momento hay información sobre '''{{%s por lugar|país=España|comunidad autónoma=%s|format=count}} %s'''.
%s

{{cómo crear|%s}}

== %s %s %s ==
{{semántica}}
{{%s por lugar|país=España|comunidad autónoma=%s}}

== Véase también ==
* [[Lista de %s]]
* [[%s]]

{{%s}}
{{%s}}

[[Categoría:%s|%s %s %s]]
[[Categoría:%s| %s %s %s]]
[[Categoría:Listas|%s %s %s]]
""" % (colectivos.lower(), de, comunidad, colectivos.lower(), comunidad, colectivos.lower(), entradilla, colectivo, colectivos, de, comunidad, colectivos.lower(), comunidad, colectivos.lower(), comunidad, comunidad.lower(), colectivos.lower(), comunidad, colectivos, de, comunidad, colectivos, colectivos, de, comunidad, colectivos, de, comunidad)
	
	page = wikipedia.Page(site, wtitle)
	if overwrite or not page.exists():
		page.put(wtext, u"BOT - Creando lista de comunidad autónoma", botflag=False)
	
	#Provincias páginas
	if len(provincias) > 1: #solo cuando no es uniprovincial
		for provincia in provincias:
			wtitle = u"Lista de %s de la provincia de %s" % (colectivos.lower(), provincia)
			wtext = u"""La siguiente es una '''lista de %s de la provincia de %s'''. En este momento hay información sobre '''{{%s por lugar|país=España|comunidad autónoma=%s|provincia=Provincia de %s|format=count}} %s'''.

{{cómo crear|%s}}

== %s de la provincia de %s ==
{{semántica}}
{{%s por lugar|país=España|comunidad autónoma=%s|provincia=Provincia de %s}}

== Véase también ==
* [[Lista de %s %s %s]]
* [[Lista de %s]]
* [[Provincia de %s]]

{{%s}}

[[Categoría:%s| %s de la provincia de %s]]
[[Categoría:Listas|%s de la provincia de %s]]
""" % (colectivos.lower(), provincia, colectivos.lower(), comunidad, provincia, colectivos.lower(), colectivo, colectivos, provincia, colectivos.lower(), comunidad, provincia, colectivos.lower(), de, comunidad, colectivos.lower(), provincia, colectivos.lower(), colectivos, colectivos, provincia, colectivos, provincia)
			page = wikipedia.Page(site, wtitle)
			if overwrite or not page.exists():
				page.put(wtext, u"BOT - Creando lista de provincia", botflag=False)

		
		
