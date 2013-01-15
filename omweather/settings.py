# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012-2013 qnub <qnub.ru@gmail.com>
# This file is distributed under the license LGPL version 3 or later
### END LICENSE

import os
import codecs
import logging

try:
    import ConfigParser as configparser
except ImportError:
    import configparser


DEFAULT = {
    'WEATHER_LINK': 'http://dove.omsk.otpbank.ru/files/weather.xml',
    'MENU_LABEL': u'Обновить',
    'MENU_SCHEDULE_LABEL': u'Прогноз',
    'MENU_AUTOSTART_ON_LABEL': u'Включить автостарт',
    'MENU_AUTOSTART_OFF_LABEL': u'Выключить автостарт',
    'MENU_QUIT_LABEL': u'Выход',
    'UPDATE_LABEL': u'Обновлено',
    'WEATHER_SCHEDULE_LINK': 'http://pogoda.yandex.ru/omsk/',
    'WEATHER_METRIC': u'°C',
    'WEATHER_UPDATE_TIMEOUT': '15',
    'TEMP_TAG_NAME': 'temperature',
    'TEMP_TAG_NUMBER': '0',
}


class Settings(object):
    def __init__(self):
        """
        Импорт настроек из ~/.config/omweather.cfg
        """
        cfg = os.path.expanduser('~/.config/omweather.cfg')
        if os.path.exists(cfg):
            cf = codecs.open(cfg, 'r', 'utf-8')
        else:
            from shutil import copyfile

            try:
                copyfile('/usr/share/omweather/omweather.cfg', cfg)
                cf = codecs.open(cfg, 'r', 'utf-8')
            except IOError:
                cf = None

        self.reader = configparser.SafeConfigParser(DEFAULT)

        if cf:
            self.reader.readfp(cf)
            self.main = True
        else:
            self.main = False

    def __getattr__(self, item):
        """
        Выдача элемента конфигурации.
        """
        sect = self.main and 'main' or 'DEFAULT'
        if item == 'WEATHER_UPDATE_TIMEOUT' or item == 'TEMP_TAG_NUMBER':
            return self.reader.getint(sect, item)
        else:
            return self.reader.get(sect, item)


settings = Settings()
