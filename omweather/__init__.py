# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012-2013 qnub <qnub.ru@gmail.com>
# This file is distributed under the license LGPL version 3 or later
### END LICENSE

import optparse
import logging
import os
import urllib2
from xml.dom import minidom
from datetime import datetime
from shutil import copyfile

from locale import gettext as _
from gi.repository import Gtk  # pylint: disable=E0611
from gi.repository import GObject
from gi.repository import AppIndicator3

from settings import settings

from omweather_lib import set_up_logging, get_version


LASTUPDATE = None


def parse_options():
    """
    Support for command line options
    """
    parser = optparse.OptionParser(version="%%prog %s" % get_version())
    parser.add_option(
        "-v", "--verbose", action="count", dest="verbose",
        help=_("Show debug messages (-vv debugs omweather_lib also)"))
    (options, args) = parser.parse_args()

    set_up_logging(options)


def update_weather(w, ind):
    """
    Update temperature
    """
    try:
        xml = minidom.parseString(urllib2.urlopen(settings.WEATHER_LINK).read())
        result = xml.getElementsByTagName(
            settings.TEMP_TAG_NAME)[settings.TEMP_TAG_NUMBER].childNodes[0].data
    except:
        result = None

    dt_template = '%H:%M'
    menu = ind.get_menu().get_children()[0]

    if result:
        ind.set_label(u'{0} {1}'.format(result, settings.WEATHER_METRIC), '100% thrust')

        time = datetime.now()

        LASTUPDATE = time

        menu.set_label(
            u'{0}: {1}'.format(settings.UPDATE_LABEL,
                time.strftime(dt_template), '100% thrust')
        )
    elif LASTUPDATE and LASTUPDATE.date.day < time.date.day:
        dt_template = '%x ' + dt_template

        menu.set_label(
            u'{0}: {1}'.format(settings.UPDATE_LABEL,
                time.strftime(dt_template), '100% thrust')
        )

    return True


def open_schedule(w):
    """
    Open weather schedule in browser
    """
    os.system('xdg-open ' + settings.WEATHER_SCHEDULE_LINK)

    return True


def autostart_label():
    """
    Check is autostart enabled
    """
    if os.path.exists(os.path.expanduser('~/.config/autostart/omweather.desktop')):
        return settings.MENU_AUTOSTART_OFF_LABEL
    else:
        return settings.MENU_AUTOSTART_ON_LABEL


def switch_autostart(w):
    """
    Switch autostart option
    """
    label = autostart_label()
    autostart_path = os.path.expanduser('~/.config/autostart/omweather.desktop')

    if label == settings.MENU_AUTOSTART_ON_LABEL:
        try:
            copyfile('/usr/share/applications/omweather.desktop',
                autostart_path)
            w.set_label(settings.MENU_AUTOSTART_OFF_LABEL)
        except IOError:
            w.set_label(settings.MENU_AUTOSTART_ON_LABEL)
    else:
        os.unlink(autostart_path)
        w.set_label(settings.MENU_AUTOSTART_ON_LABEL)


def main():
    parse_options()
    WEATHER_UPDATE_TIMEOUT = 1000 * 60 * settings.WEATHER_UPDATE_TIMEOUT
    ind = AppIndicator3.Indicator.new('om_weather_client',
                          'om_weather_client_icon',
                          AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
    ind.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    ind.set_label(settings.WEATHER_METRIC, '100% thrust')

    # create a menu
    menu = Gtk.Menu()

    menu_update = Gtk.MenuItem(settings.MENU_LABEL)
    menu_update.connect('activate', update_weather, ind)
    menu.append(menu_update)

    menu_autostart = Gtk.MenuItem(autostart_label())
    menu_autostart.connect('activate', switch_autostart)
    menu.append(menu_autostart)

    menu_schedule = Gtk.MenuItem(settings.MENU_SCHEDULE_LABEL)
    menu_schedule.connect('activate', open_schedule)
    menu.append(menu_schedule)

    # show the items
    menu_update.show()
    menu_autostart.show()
    menu_schedule.show()

    ind.set_menu(menu)

    update_weather(None, ind)

    GObject.timeout_add(WEATHER_UPDATE_TIMEOUT, update_weather, None, ind)

    Gtk.main()
