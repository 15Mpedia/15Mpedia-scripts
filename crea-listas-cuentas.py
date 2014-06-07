#!/usr/bin/python
# -*- coding: utf-8 -*-

import wikipedia

for colectivo in ['Acampadas', 'Asambleas', 'Asociaciones', 'Bancos de tiempo', 'Centros sociales', 'Comisiones', 'Cooperativas', 'Grupos de trabajo', 'Nodos', u'Partidos políticos', 'Plataformas', 'Realojos']:
    for servicio in ['Bambuser', 'Facebook', 'Flickr', 'Livestream', 'N-1', 'Twitter', 'Ustream', 'Vimeo', 'YouTube']:
        output = u"""La siguiente es una '''lista de cuentas de %s en %s'''. En este momento hay información sobre '''{{cuentas de %s por servicio|servicio=%s|format=count}} cuentas'''.

== Cuentas de %s en %s ==
{{semántica}}
{{cuentas de %s por servicio|servicio=%s}}

== Véase también ==

* [[Lista de cuentas de %s]]
* [[Lista de cuentas en %s]]
* [[%s]]

{{cuentas}}
{{%s}}

[[Categoría:Listas|Cuentas de %s en %s]]
[[Categoría:%s|Cuentas de %s en %s]]
[[Categoría:%s|Cuentas de %s en %s]]
[[Categoría:Cuentas|%s en %s]]""" % (colectivo.lower(), servicio, colectivo.lower(), servicio.lower(), colectivo.lower(), servicio, colectivo.lower(), servicio.lower(), colectivo.lower(), servicio, servicio, colectivo.lower(), colectivo.lower(), servicio, colectivo, colectivo.lower(), servicio, servicio, colectivo.lower(), servicio, colectivo, servicio)

        p = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), u'Lista de cuentas de %s en %s' % (colectivo.lower(), servicio))
        p.put(output, u"BOT - Creando lista de cuentas de colectivo", botflag=True)




