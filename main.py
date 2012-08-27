#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import urllib2
from xml.dom import minidom
from datetime import datetime

import gobject
import gtk
import appindicator

logging.basicConfig(level=logging.DEBUG)
WEATHER_LINK = 'http://dove.omsk.otpbank.ru/files/weather.xml'
WEATHER_METRIC = u'°C'
WEATHER_UPDATE_TIMEOUT = 1000 * 60 * 15  # every 15 min
MENU_LABEL = u'Обновить'
LASTUPDATE = None


def update_weather(w, ind):
    try:
        xml = minidom.parseString(urllib2.urlopen(WEATHER_LINK).read())
        result = xml.getElementsByTagName(
            'temperature')[0].childNodes[0].data
    except:
        result = None

    dt_template = '%H:%M'
    menu = ind.get_menu().get_children()[0]

    if result:
        ind.set_label('{0} {1}'.format(result, WEATHER_METRIC))

        time = datetime.now()

        LASTUPDATE = time

        menu.set_label(
            u'Обновлено: {0}'.format(time.strftime(dt_template))
        )
    elif LASTUPDATE and LASTUPDATE.date.day < time.date.day:
        dt_template = '%x ' + dt_template

        menu.set_label(
            u'Обновлено: {0}'.format(time.strftime(dt_template))
        )

    return True


if __name__ == '__main__':
    ind = appindicator.Indicator('om_weather_client',
                              'om_weather_client_icon',
                              appindicator.CATEGORY_APPLICATION_STATUS)
    ind.set_status(appindicator.STATUS_ACTIVE)
    ind.set_label(WEATHER_METRIC)

    # create a menu
    menu = gtk.Menu()

    menu_item = gtk.MenuItem(MENU_LABEL)

    menu.append(menu_item)

    # this is where you would connect your menu item up with a function:

    menu_item.connect('activate', update_weather, ind)

    # show the items
    menu_item.show()

    ind.set_menu(menu)

    update_weather(None, ind)

    gobject.timeout_add(WEATHER_UPDATE_TIMEOUT, update_weather, None, ind)

    gtk.main()
