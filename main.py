#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import urllib2
from xml.dom import minidom
from datetime import datetime

import gobject
import gtk
import appindicator

from settings import *


VERSION = 0.2
LASTUPDATE = None
WEATHER_UPDATE_TIMEOUT = 1000 * 60 * WEATHER_UPDATE_TIMEOUT

logging.basicConfig(level=logging.DEBUG)


def update_weather(w, ind):
    try:
        xml = minidom.parseString(urllib2.urlopen(WEATHER_LINK).read())
        result = xml.getElementsByTagName(
            TEMP_TAG_NAME)[TEMP_TAG_NUMBER].childNodes[0].data
    except:
        result = None

    dt_template = '%H:%M'
    menu = ind.get_menu().get_children()[0]

    if result:
        ind.set_label('{0} {1}'.format(result, WEATHER_METRIC))

        time = datetime.now()

        LASTUPDATE = time

        menu.set_label(
            u'{0}: {1}'.format(UPDATE_LABEL, time.strftime(dt_template))
        )
    elif LASTUPDATE and LASTUPDATE.date.day < time.date.day:
        dt_template = '%x ' + dt_template

        menu.set_label(
            u'{0}: {1}'.format(UPDATE_LABEL, time.strftime(dt_template))
        )

    return True


def open_schedule(w):
    os.system('xdg-open ' + WEATHER_SCHEDULE_LINK)

    return True


if __name__ == '__main__':
    ind = appindicator.Indicator('om_weather_client',
                              'om_weather_client_icon',
                              appindicator.CATEGORY_APPLICATION_STATUS)
    ind.set_status(appindicator.STATUS_ACTIVE)
    ind.set_label(WEATHER_METRIC)

    # create a menu
    menu = gtk.Menu()

    menu_update = gtk.MenuItem(MENU_LABEL)
    menu_update.connect('activate', update_weather, ind)
    menu.append(menu_update)

    menu_schedule = gtk.MenuItem(MENU_SCHEDULE_LABEL)
    menu_schedule.connect('activate', open_schedule)
    menu.append(menu_schedule)

    # show the items
    menu_update.show()
    menu_schedule.show()

    ind.set_menu(menu)

    update_weather(None, ind)

    gobject.timeout_add(WEATHER_UPDATE_TIMEOUT, update_weather, None, ind)

    gtk.main()
