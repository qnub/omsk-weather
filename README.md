Omsk Weather
============

Данные о температуре воздуха в **г. Омск (Россия)** для
системного трея **Ubuntu**. Обновляется раз в 15 минут.

Показания берутся с сервера [«ОТП Банка»](http://dove.omsk.otpbank.ru/),
(старая ссылка «муха» [myxa.opsb.ru](http://myxa.opsb.ru/)) который,
в совою очередь, получает их с датчика расположенного на здании этого банка в
[центре города](http://goo.gl/maps/ObctK) (за кинотеатром «Маяковский»).

На сайте также доступен архив данных. На сайте температура обновляется
ежеминутно.


Руководство
-----------

Для установки:

    sudo apt-add-repository ppa:qnub/utils
    sudo apt-get update
    sudo apt-get install omweather

Дальше можно добавить `omweather` в автозапуск.

При клике на темепературу в выпадающем меню можно посмотреть время последнего
обновления температуры. Клик по этому пункту обновляет температуру.

Клик по меню «Прогноз» открывает [прогноз погоды для Омска на Яндексе](http://pogoda.yandex.ru/omsk/).

Файл `settings.py` содержит переопределяемые переменные виджета
(см. комментарии в файле).