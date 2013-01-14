# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012-2013 qnub <qnub.ru@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
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
    'UPDATE_LABEL': u'Обновлено',
    'WEATHER_SCHEDULE_LINK': 'http://pogoda.yandex.ru/omsk/',
    'MENU_SCHEDULE_LABEL': u'Прогноз',
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
