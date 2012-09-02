# -*- coding: utf-8 -*-

# ссылка на сервис погоды
WEATHER_LINK = 'http://dove.omsk.otpbank.ru/files/weather.xml'
# надпись на пункте меню до первого обновления
MENU_LABEL = u'Обновить'
# начало надписи на пункте меню после первого обновления
UPDATE_LABEL = u'Обновлено'

# ссылка на страницу с прогнозом и надпись на пунтке меню
WEATHER_SCHEDULE_LINK = 'http://pogoda.yandex.ru/omsk/'
# надпись на пункте меню открытия прогноза
MENU_SCHEDULE_LABEL = u'Прогноз'

# отображаемая единица измерения температуры
WEATHER_METRIC = u'°C'
# интервал обновления температуры в мин
WEATHER_UPDATE_TIMEOUT = 15

# имя тега в XML ответе содержащего показания температуры
# к примеру текущий сервис отдаёт информацию в таком виде:
#
# <?xml version="1.0" encoding="windows-1251" ?>
# <OPSB>
#   <temperature>20.0</temperature>
# </OPSB>
TEMP_TAG_NAME = 'temperature'
# порядковый номер тега в ответе (если их несколько), 0 - первый
TEMP_TAG_NUMBER = 0
