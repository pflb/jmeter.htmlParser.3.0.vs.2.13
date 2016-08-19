# Описание проекта

## Объект тестирования
Тестируются htmlParser-ы для **Apache.JMeter 2.13** и **Apache.JMeter 3.0**.

Парсеры **Apache.JMeter 2.13**:

- LagartoBasedHtmlParser
- HtmlParserHTMLParser
- JTidyHTMLParser
- RegexpHTMLParser
- JsoupBasedHtmlParser

Парсесы **Apache.JMeter 3.0**:

- LagartoBasedHtmlParser
- JTidyHTMLParser
- RegexpHTMLParser
- JsoupBasedHtmlParser

Парсеры разбирают стартовые страницы различных веб-сайтов:

- stackoverflow.com
- habrahabr.ru
- yandex.ru
- mos.ru
- jmeter.apache.org
- google.ru
- linkedin.com
- github.com

## Основа тестирования

Основой для тестирования послужили изменения в **Apache.JMeter 3.0**, см. [http://jmeter.apache.org/changes.html](http://jmeter.apache.org/changes.html).

Выдержки из списка изменений:


> #### Core improvements
> ##### Dependencies refresh
> 
> Deprecated Libraries dropped or replaced by up to date ones:
> 
> - htmllexer, htmlparser removed
> - jdom removed
> 
> > Удалён парсер **htmlparser** и более неиспользуемая библиотека **jdom**.
> 
> #### Protocols and Load Testing improvements
> ##### Parallel Downloads is now realistic and scales much better:
> 
> - Parsing of CSS imported files (through @import) or embedded resources (background, images, …)
> 
> > Добавлен новый парсер для CSS-файлов, будут извлекаться ссылки на другие CSS-файлы (через @import) и ссылки на ресурсы, указанные в CSS-файлах: фоновые изображения, картинки, ...
> 
> #### Incompatible changes
> 
> - Since version 3.0, the parser for embedded resources (replaced since 2.10 by Lagarto based implementation) which relied on the htmlparser library (HtmlParserHTMLParser) has been dropped along with its dependencies.
> - The following jars have been removed:
>    - htmllexer-2.1.jar (see [Bug 59037](http://bz.apache.org/bugzilla/show_bug.cgi?id=59037))
>    - htmlparser-2.1.jar (see [Bug 59037](http://bz.apache.org/bugzilla/show_bug.cgi?id=59037))
>    - jdom-1.1.3.jar (see [Bug 59156](http://bz.apache.org/bugzilla/show_bug.cgi?id=59156))
> 
> > Удалён парсер **htmlparser** и более неиспользуемые библиотеки **htmllexer** и **jdom**.
> 
> #### Improvements
> ##### HTTP Samplers and Test Script Recorder
> 
> - [Bug 59036](http://bz.apache.org/bugzilla/show_bug.cgi?id=59036) - FormCharSetFinder : Use JSoup instead of deprecated HTMLParser
> - [Bug 59033](http://bz.apache.org/bugzilla/show_bug.cgi?id=59033) - Parallel Download : Rework Parser classes hierarchy to allow plug-in parsers for different mime types
> - [Bug 59140](http://bz.apache.org/bugzilla/show_bug.cgi?id=59140) - Parallel Download : Add CSS Parsing to extract links from CSS files
> 
> > Для поиска аттрибута `accept-charset` в тегах `form` теперь используется **JSoup** вместо удалённого **HTMLParser** [Bug 59036]. Реализован парсер CSS-файлов [Bug 59140] и этот парсер используется по умолчанию [Bug 59033].



## Цели тестирования

Сравнить работу всех доступных парсеров. В частности сравнить между собой парсеры версий 2.13 и 3.0, убедиться, что загрузка встроенных ресурсов стала реалистичнее и лучше.

## Стратегия тестирования

Этап 1:

1. Выполнить загрузку стартовых страниц списка сайтов используя все 5 парсеров **Apache.JMeter** 2.13 и записать логи.
2. Выполнить загрузку стартовых страниц списка сайтов используя все 4 парсера **Apache.JMeter** 3.0 и записать логи.
3. Проанализировать логи работы **Apache.JMeter** и сравнить их между собой. Оценить, стала ли загрузка встроенных ресурсов лучше, расширился ли перечень загружаемых встроенных ресурсов.

Этап 2:

1. Выполнить загрузку стартовых страниц списка популярных сайтов, используя **Google Chrome** и сервис **webpagetest.org**.
2. Проанализировать отчёты из **webpagetest.org** и сравнить их с результатами анализа логов **Apache.JMeter**. Оценить, реалистичность загрузки встроенных ресурсов.

## Подход к тестированию

Чтобы точно определить сколько запросов посылается во время открытия страницы сайта из **Apache.JMeter** все запросы логируются:

- **View Results Tree** — стандратный логгер, логирование в XML-формат с логированием подзапросов, XML-лог будет использоваться для выяснения деталей запросов/ответов/ошибок;
- **CsvLogWriter** — кастомный логгер [https://github.com/pflb/Jmeter.Plugin.CsvLogWriter](https://github.com/pflb/Jmeter.Plugin.CsvLogWriter), логирование в CSV-формат с логированием подзапросов, CSV-лог будет использоваться для программного подсчёта статистики по работе различных парсеров.

Чтобы иметь возможность сгруппировать запросы по версиям **Apache.JMeter**, парсерам и сайтам, в лог будут записываться дополнительные переменные для каждого запроса:

- **siteKey** — тестируемый сайт;
- **jmeterVersion** — версия **Apache.JMeter**;
- **htmlParser** — название html-парсера, используемого в данный момент.


# Состав проекта

- **jmeter.testfile.jmx** — тестовый скрипт для **Apache.JMeter 2.13** и **Apache.JMeter 3.0** принимающий на вход параметры:
  - `URL` — адрес тестируемого сайта, например, https://yandex.ru/;
  - `siteKey` — строка по которой будет осуществляться группировка записей в логах, например, yandex.ru;
  - `loopCount` — количество итераций теста, используется несколько итераций из-за того, что работа веб-сайтов может быть нестабильной;
  - `htmlParser.className` — парсер для извлечения ссылок на встроенные ресурсы;
  - для работы скрипта необходимо скачать и установить дополнительный плагин [CsvLogWriter](https://github.com/pflb/Jmeter.Plugin.CsvLogWriter/releases).
- **jmeter.3.0.bat** — командный файл запуска теста для **Apache.JMeter 3.0**, тут задаётся путь к папке `/bin/` **Apache.JMeter 3.0**, путь к тестовому скрипту **jmeter.testfile.jmx**, опции запуска теста, а также список htmlParser-ов проверка работы которых выполняется;
- **jmeter.2.13.bat** — командный файл запуска теста для **Apache.JMeter 2.13**, тут задаётся путь к папке `/bin/` **Apache.JMeter 2.13**, путь к тестовому скрипту **jmeter.testfile.jmx**, опции запуска теста, а также список htmlParser-ов проверка работы которых выполняется;
- **test.bat** — командный файл запуска теста на двух версиях **Apache.JMeter**, 2.13 и 3.0, файл содержит количество итераций тестирования и адреса тестируемых сайтов. Файл вызывает файлы **jmeter.2.13.bat** и **jmeter.3.0.bat**;



# Результаты

## Сводка

### Оценка улучшения работы парсеров для версии 3.0 по сравнению с версией 2.13

Кардинальных улучшений полноты разбора html-страниц нет.

Разницы между работой парсеров для версий 2.13 и 3.0 почти нет. Единственное отличие - в парсерах версии 3.0 есть дефект, приводящий к рекурсивной загрузке встроенных ресурсов, если страница ссылается на саму себя, и сервер в заголовках отдаёт директуву no-cashe. Это проявляется при загрузке https://yandex.ru/.

#### Сайты с малым количеством контента — хороший результат

На простых сайтах, таких как *jmeter.apache.org*, все парсеры работают одинаково. Создавая то же количество запрсов, которое создаётся браузером на момент наступления события **Before Start Render** — 10. Качество работы парсеров для *jmeter.apache.org* — идеально, 100%.

#### Сайты с большим количеством контента — плохой результат

Но на таком сайте как *mos.ru*, парсеры найдут в среднем 23 ссылки на встроенные ресурсы, тогда как полная загрузка страницы — 13 запросов, а с загрузкой всех встроенных ресурсов браузером — 144 запроса. Качество — 16%.

Аналогично на сайте *habrahabr.ru*, парсер **Lagardo** из **Apache.JMeter** 3.0 найдёт 41 ссылку, тогда как браузер сделает 113 запросов. Качество —  36,3%. Низкое качество полноты извлечения ссылок на встроенные ресурсы.


## Количество запросов при использовании различных парсеров

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th rowspan="2">Сайт</th>
      <th colspan="8">Apache.JMeter </th>
      <th colspan="2">Chrome, webpagetest.org</th>
      <th rowspan="2" title="Качество парсинга (Avg / Document&nbsp;Complete)">Качество</th>
    </tr>
    <tr>
      <th>Версия</th>
      <th>Парсер</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th title="Среднее значение по пяти итерациям">Avg</th>
      <th>Document Complete</th>
      <th>Fully Loaded</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="9" valign="top">github.com</th>
      <th rowspan="5" valign="top">2.13</th>
      <th>HtmlParser</th>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td><!--1.AP-->
      <td rowspan="9"  style="font-weight:bold">19</td><!--4.DC-->
      <td rowspan="9">22</td><!--5.FL-->
    </tr>
    <tr>
      <th>JTidy</th>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td><!--1-->
    </tr>
    <tr>
      <th>Jsoup</th>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td><!--1-->
    </tr>
    <tr>
      <th>Lagarto</th>
      <td style="font-weight:bold">13</td>
      <td style="font-weight:bold">13</td>
      <td style="font-weight:bold">13</td>
      <td style="font-weight:bold">13</td>
      <td style="font-weight:bold">13</td>
      <td style="font-weight:bold">13</td><!--1-->
    </tr>
    <tr>
      <th>Regexp</th>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td><!--1-->
    </tr>
    <tr>
      <th rowspan="4" valign="top">3.0</th>
      <th>JTidy</th>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td><!--1-->
    </tr>
    <tr>
      <th>Jsoup</th>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td><!--1-->
    </tr>
    <tr>
      <th>Lagarto</th>
      <td style="font-weight:bold">13</td>
      <td style="font-weight:bold">13</td>
      <td style="font-weight:bold">13</td>
      <td style="font-weight:bold">13</td>
      <td style="font-weight:bold">13</td>
      <td style="font-weight:bold">13</td><!--1-->
    </tr>
    <tr>
      <th>Regexp</th>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td><!--1-->
    </tr>
    <tr>
      <th rowspan="9" valign="top">google.ru</th>
      <th rowspan="5" valign="top">2.13</th>
      <th>HtmlParser</th>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td><!--1.AP-->
      <td rowspan="9"  style="font-weight:bold">9</td><!--4.DC-->
      <td rowspan="9">12</td><!--5.FL-->
    </tr>
    <tr>
      <th>JTidy</th>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>4</td>
      <td>4,8</td><!--1.AP-->
    </tr>
    <tr>
      <th>Jsoup</th>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td><!--1.AP-->
    </tr>
    <tr>
      <th>Lagarto</th>
      <td style="font-weight:bold">5</td>
      <td style="font-weight:bold">5</td>
      <td style="font-weight:bold">5</td>
      <td style="font-weight:bold">5</td>
      <td style="font-weight:bold">5</td>
      <td style="font-weight:bold">5</td><!--1.AP-->
    </tr>
    <tr>
      <th>Regexp</th>
      <td>3</td>
      <td>3</td>
      <td>3</td>
      <td>3</td>
      <td>3</td>
      <td>3</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="4" valign="top">3.0</th>
      <th>JTidy</th>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td><!--1.AP-->
    </tr>
    <tr>
      <th>Jsoup</th>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td><!--1.AP-->
    </tr>
    <tr>
      <th>Lagarto</th>
      <td style="font-weight:bold">5</td>
      <td style="font-weight:bold">5</td>
      <td style="font-weight:bold">5</td>
      <td style="font-weight:bold">5</td>
      <td style="font-weight:bold">5</td>
      <td style="font-weight:bold">5</td><!--1.AP-->
    </tr>
    <tr>
      <th>Regexp</th>
      <td>3</td>
      <td>3</td>
      <td>3</td>
      <td>3</td>
      <td>3</td>
      <td>3</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="9" valign="top">habrahabr.ru</th>
      <th rowspan="5" valign="top">2.13</th>
      <th>HtmlParser</th>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td><!--1.AP-->
      <td rowspan="9"  style="font-weight:bold">113</td><!--4.DC-->
      <td rowspan="9">120</td><!--5.FL-->
    </tr>
    <tr>
      <th>JTidy</th>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td><!--1.AP-->
    </tr>
    <tr>
      <th>Jsoup</th>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td><!--1.AP-->
    </tr>
    <tr>
      <th>Lagarto</th>
      <td style="font-weight:bold">41</td>
      <td style="font-weight:bold">41</td>
      <td style="font-weight:bold">41</td>
      <td style="font-weight:bold">41</td>
      <td style="font-weight:bold">41</td>
      <td style="font-weight:bold">41</td><!--1.AP-->
    </tr>
    <tr>
      <th>Regexp</th>
      <td>45</td>
      <td>45</td>
      <td>45</td>
      <td>45</td>
      <td>45</td>
      <td>45</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="4" valign="top">3.0</th>
      <th>JTidy</th>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td><!--1.AP-->
    </tr>
    <tr>
      <th>Jsoup</th>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td><!--1.AP-->
    </tr>
    <tr>
      <th>Lagarto</th>
      <td style="font-weight:bold">41</td>
      <td style="font-weight:bold">41</td>
      <td style="font-weight:bold">41</td>
      <td style="font-weight:bold">41</td>
      <td style="font-weight:bold">41</td>
      <td style="font-weight:bold">41</td><!--1.AP-->
    </tr>
    <tr>
      <th>Regexp</th>
      <td>45</td>
      <td>45</td>
      <td>45</td>
      <td>45</td>
      <td>45</td>
      <td>45</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="9" valign="top">jmeter.apache.org</th>
      <th rowspan="5" valign="top">2.13</th>
      <th>HtmlParser</th>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td><!--1.AP-->
      <td rowspan="9" style="font-weight:bold">10</td><!--4.DC-->
      <td rowspan="9">11</td><!--5.FL-->
    </tr>
    <tr>
      <th>JTidy</th>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td><!--1.AP-->
    </tr>
    <tr>
      <th>Jsoup</th>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td><!--1.AP-->
    </tr>
    <tr>
      <th>Lagarto</th>
      <td style="font-weight:bold">10</td>
      <td style="font-weight:bold">10</td>
      <td style="font-weight:bold">10</td>
      <td style="font-weight:bold">10</td>
      <td style="font-weight:bold">10</td>
      <td style="font-weight:bold">10</td><!--1.AP-->
    </tr>
    <tr>
      <th>Regexp</th>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="4" valign="top">3.0</th>
      <th>JTidy</th>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td><!--1.AP-->

    </tr>
    <tr>
      <th>Jsoup</th>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td><!--1.AP-->
    </tr>
    <tr>
      <th>Lagarto</th>
      <td style="font-weight:bold">10</td>
      <td style="font-weight:bold">10</td>
      <td style="font-weight:bold">10</td>
      <td style="font-weight:bold">10</td>
      <td style="font-weight:bold">10</td>
      <td style="font-weight:bold">10</td><!--1.AP-->
    </tr>
    <tr>
      <th>Regexp</th>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="9" valign="top">linkedin.com</th>
      <th rowspan="5" valign="top">2.13</th>
      <th>HtmlParser</th>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td><!--1.AP-->
      <td rowspan="9" style="font-weight:bold">20</td><!--4.DC-->
      <td rowspan="9">22</td><!--5.FL-->
    </tr>
    <tr>
      <th>JTidy</th>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td><!--1.AP-->
    </tr>
    <tr>
      <th>Jsoup</th>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td><!--1.AP-->
    </tr>
    <tr>
      <th>Lagarto</th>
      <td style="font-weight:bold">11</td>
      <td style="font-weight:bold">11</td>
      <td style="font-weight:bold">11</td>
      <td style="font-weight:bold">11</td>
      <td style="font-weight:bold">11</td>
      <td style="font-weight:bold">11</td><!--1.AP-->
    </tr>
    <tr>
      <th>Regexp</th>
      <td>7</td>
      <td>7</td>
      <td>7</td>
      <td>7</td>
      <td>7</td>
      <td>7</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="4" valign="top">3.0</th>
      <th>JTidy</th>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td><!--1.AP-->
    </tr>
    <tr>
      <th>Jsoup</th>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td><!--1.AP-->
    </tr>
    <tr>
      <th>Lagarto</th>
      <td style="font-weight:bold">11</td>
      <td style="font-weight:bold">11</td>
      <td style="font-weight:bold">11</td>
      <td style="font-weight:bold">11</td>
      <td style="font-weight:bold">11</td>
      <td style="font-weight:bold">11</td><!--1.AP-->
    </tr>
    <tr>
      <th>Regexp</th>
      <td>7</td>
      <td>7</td>
      <td>7</td>
      <td>7</td>
      <td>7</td>
      <td>7</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="9" valign="top">mos.ru</th>
      <th rowspan="5" valign="top">2.13</th>
      <th>HtmlParser</th>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td><!--1.AP-->
      <td rowspan="9" style="font-weight:bold">98</td><!--4.DC-->
      <td rowspan="9">144</td><!--5.FL-->
    </tr>
    <tr>
      <th>JTidy</th>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td><!--1.AP-->
    </tr>
    <tr>
      <th>Jsoup</th>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td><!--1.AP-->
    </tr>
    <tr>
      <th>Lagarto</th>
      <td style="font-weight:bold">14</td>
      <td style="font-weight:bold">14</td>
      <td style="font-weight:bold">14</td>
      <td style="font-weight:bold">14</td>
      <td style="font-weight:bold">14</td>
      <td style="font-weight:bold">14</td><!--1.AP-->
    </tr>
    <tr>
      <th>Regexp</th>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="4" valign="top">3.0</th>
      <th>JTidy</th>
      <td>26</td>
      <td>26</td>
      <td>26</td>
      <td>26</td>
      <td>26</td>
      <td>26</td><!--1.AP-->
    </tr>
    <tr>
      <th>Jsoup</th>
      <td>26</td>
      <td>26</td>
      <td>26</td>
      <td>26</td>
      <td>26</td>
      <td>26</td><!--1.AP-->
    </tr>
    <tr>
      <th>Lagarto</th>
      <td style="font-weight:bold">15</td>
      <td style="font-weight:bold">15</td>
      <td style="font-weight:bold">15</td>
      <td style="font-weight:bold">15</td>
      <td style="font-weight:bold">15</td>
      <td style="font-weight:bold">15</td><!--1.AP-->
    </tr>
    <tr>
      <th>Regexp</th>
      <td>26</td>
      <td>26</td>
      <td>26</td>
      <td>26</td>
      <td>26</td>
      <td>26</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="9" valign="top">stackoverflow.com</th>
      <th rowspan="5" valign="top">2.13</th>
      <th>HtmlParser</th>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>16</td><!--1.AP-->
      <td rowspan="9" style="font-weight:bold">39</td><!--4.DC-->
      <td rowspan="9">40</td><!--5.FL-->
    </tr>
    <tr>
      <th>JTidy</th>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>16</td><!--1.AP-->
    </tr>
    <tr>
      <th>Jsoup</th>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>18</td>
      <td>18</td>
      <td>16,8</td><!--1.AP-->
    </tr>
    <tr>
      <th>Lagarto</th>
      <td style="font-weight:bold">14</td>
      <td style="font-weight:bold">14</td>
      <td style="font-weight:bold">15</td>
      <td style="font-weight:bold">15</td>
      <td style="font-weight:bold">15</td>
      <td style="font-weight:bold">14,6</td><!--1.AP-->
    </tr>
    <tr>
      <th>Regexp</th>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>16</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="4" valign="top">3.0</th>
      <th>JTidy</th>
      <td>17</td>
      <td>17</td>
      <td>17</td>
      <td>17</td>
      <td>17</td>
      <td>17</td><!--1.AP-->
    </tr>
    <tr>
      <th>Jsoup</th>
      <td>17</td>
      <td>17</td>
      <td>17</td>
      <td>17</td>
      <td>17</td>
      <td>17</td><!--1.AP-->
    </tr>
    <tr>
      <th>Lagarto</th>
      <td style="font-weight:bold">14</td>
      <td style="font-weight:bold">16</td>
      <td style="font-weight:bold">16</td>
      <td style="font-weight:bold">16</td>
      <td style="font-weight:bold">16</td>
      <td style="font-weight:bold">15,6</td><!--1.AP-->
    </tr>
    <tr>
      <th>Regexp</th>
      <td>17</td>
      <td>17</td>
      <td>17</td>
      <td>17</td>
      <td>17</td>
      <td>17</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="9" valign="top">yandex.ru</th>
      <th rowspan="5" valign="top">2.13</th>
      <th>HtmlParser</th>
      <td>69</td>
      <td>68</td>
      <td>69</td>
      <td>68</td>
      <td>69</td>
      <td>68,6</td><!--1.AP-->
      <td rowspan="9" style="font-weight:bold">34</td><!--4.DC-->
      <td rowspan="9">36</td><!--5.FL-->
    </tr>
    <tr>
      <th>JTidy</th>
      <td>20</td>
      <td>19</td>
      <td>19</td>
      <td>19</td>
      <td>19</td>
      <td>19,2</td><!--1.AP-->
    </tr>
    <tr>
      <th>Jsoup</th>
      <td>20</td>
      <td>19</td>
      <td>19</td>
      <td>20</td>
      <td>19</td>
      <td>19,4</td><!--1.AP-->
    </tr>
    <tr>
      <th>Lagarto</th>
      <td style="font-weight:bold">15</td>
      <td style="font-weight:bold">15</td>
      <td style="font-weight:bold">15</td>
      <td style="font-weight:bold">15</td>
      <td style="font-weight:bold">15</td>
      <td style="font-weight:bold">15</td><!--1.AP-->
    </tr>
    <tr>
      <th>Regexp</th>
      <td>19</td>
      <td>19</td>
      <td>19</td>
      <td>19</td>
      <td>19</td>
      <td>19</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="4" valign="top">3.0</th>
      <th>JTidy</th>
      <td>639</td>
      <td>642</td>
      <td>642</td>
      <td>513</td>
      <td>644</td>
      <td>616</td><!--1.AP-->
    </tr>
    <tr>
      <th>Jsoup</th>
      <td>643</td>
      <td>334</td>
      <td>639</td>
      <td>641</td>
      <td>643</td>
      <td>580</td><!--1.AP-->
    </tr>
    <tr>
      <th>Lagarto</th>
      <td style="font-weight:bold">349</td>
      <td style="font-weight:bold">449</td>
      <td style="font-weight:bold">451</td>
      <td style="font-weight:bold">449</td>
      <td style="font-weight:bold">13</td>
      <td style="font-weight:bold">342,2</td><!--1.AP-->
    </tr>
    <tr>
      <th>Regexp</th>
      <td>641</td>
      <td>635</td>
      <td>638</td>
      <td>436</td>
      <td>645</td>
      <td>599</td><!--1.AP-->
    </tr>
  </tbody>
</table>

Таблица на Google Docs: [JMeter.HtmlParser.Compare (Results)](https://docs.google.com/spreadsheets/d/16l32BFuUdrJmexTgF155HMAGW7EBaBT-rRjuuLc524c/edit#gid=871370540).

Описание столбцов:

-    **Before Start Render** — количество запросов, сделанных браузером, до момента начала отображения содержимого страницы. Это html-разметка, основные js и css-файлы, основные изображения.
-    **Document Complete** — количество запросов, сделанных браузером, на момент полной загрузки документа. Тут уже загрузились все ресурсы страницы.
-    **Fully Loaded** — количество запросов, сделанных браузером, на момент когда отработал javascript, когда сработали все виджеты.

Отличным результатом работы парсеров будет, если запросов будет столько же, сколько браузер **Google Chrome** делает на момент **Document Complete**. Мерилом реалистичности работы **Apache.JMeter** при использовании конкретного парсера является близость количества запросов к количеству запросов, выполняемых браузером на момент **Document Complete**.

Если исключить результаты тестирования сайта yandex.ru, где:

-    сайт ссылается сам на себя
-    кеширование стартовой страницы настроено необычно для Apache.JMeter и парсеров
-    в результате парсинг уходит в рекурсию делая снова и снова запросы к yandex.ru пока глубина рекурсии не достигает максимального уровня и завершается ошибкой:
> `java.lang.Exception: Maximum frame/iframe nesting depth exceeded`.

и за мерило качества работы парсеров принять количество запросов на момент **Document Complete**, то получим такую таблицу качества работы парсеров: 


<table class="wikitable collapsible sortable jquery-tablesorter">
<thead><tr>
<th class="headerSort" tabindex="0" role="columnheader button" title="Упорядочить по возрастанию"> Парсер HTML </th>
<th class="headerSort" tabindex="0" role="columnheader button" title="Упорядочить по возрастанию"> 2.13 r1665067 </th>
<th class="headerSort" tabindex="0" role="columnheader button" title="Упорядочить по возрастанию"> 3.0 r1743807 </th>
<th class="headerSort" tabindex="0" role="columnheader button" title="Упорядочить по возрастанию"> Общий итог
</th></tr></thead><tbody>
<tr>
<td> HtmlParserHTMLParser </td>
<td style="background: #dbe182;">54,92% </td>
<td>                                     </td>
<td style="background: #dbe182;">54,92%
</td></tr>
<tr>
<td> JsoupBasedHtmlParser </td>
<td style="background: #96cd7e;">55,21% </td>
<td style="background: #63be7b;">55,43% </td>
<td style="background: #7dc67d;">55,32%
</td></tr>
<tr>
<td> JTidyHTMLParser      </td>
<td style="background: #fee783;">54,60% </td>
<td style="background: #63be7b;">55,43% </td>
<td style="background: #c4da81;">55,02%
</td></tr>
<tr>
<td>LagartoBasedHtmlParser</td>
<td style="background: #fcb679;">52,43% </td>
<td style="background: #fcc17c;">52,94% </td>
<td style="background: #fcbb7a;">52,68%
</td></tr>
<tr>
<td> RegexpHTMLParser     </td>
<td style="background: #f8696b;">49,02% </td>
<td style="background: #f8746d;">49,53% </td>
<td style="background: #f86e6c;">49,27%
</td></tr>
<tr>
<td> <b>Общий итог</b>     </td>
<td>  53,24%                             </td>
<td>  53,33%                             </td>
<td>  53,28%
</td></tr></tbody><tfoot></tfoot></table>

Таблица на Google Docs: [JMeter.HtmlParser.Compare (TotalResult)](https://docs.google.com/spreadsheets/d/16l32BFuUdrJmexTgF155HMAGW7EBaBT-rRjuuLc524c/edit#gid=2130783480).

Самый точный парсер **Jsoup**. В **Apache.JMeter** 3.0 парсеры **Jsoup** и **JTidy** показали одинаковое качество. Парсер **Lagarto** отстаёт от лидера **Jsoup** по качеству разбора на 2,49%.

Качество работы парсера **Lagarto** на актуальной версии **Apache.JMeter** 3.0 составило 52,94%, лишь половина всех запросов не была послана.

# Логи и их обработка

## Исходные данные

Все логи доступны по ссылке: [https://drive.google.com/drive/folders/0B5nKzHDZ1RIiVkN4dDlFWDR1ZGM](https://drive.google.com/drive/folders/0B5nKzHDZ1RIiVkN4dDlFWDR1ZGM "jmeter.htmlParser.compare.logs").

### Отчёты WebPageTest.org

<table>
	<tr>
		<th>sytekey</th>
		<th>webpagetest.org</th>
		<th>Raw page data (.csv)</th>
		<th>Raw object data (.csv)</th>
		<th>HTTP Archive (.har)</th>
	</tr>
	<tr>
		<td>github.com</td>
		<td><a href="https://www.webpagetest.org/result/160819_VF_FM8/">160819_VF_FM8</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIiblRnUzNUVFM3SUk">github.com.summary.csv</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIieGFaaWFXTU9MWlE">github.com.details.csv</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIidGNQRzJYUXprVzQ">github.com.har</a></td>
	</tr>
	<tr>
		<td>google.ru</td>
		<td><a href="https://www.webpagetest.org/result/160819_C9_FQD/">160819_C9_FQD</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIiczE1OVdCaUs5Mkk">google.ru.summary.csv</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIiTUNjRk1mOHJIMEk">google.ru.details.csv</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIiYm9EejNNdHBUWnM">google.ru.har</a></td>
	</tr>
	<tr>
		<td>habrahabr.ru</td>
		<td><a href="https://www.webpagetest.org/result/160819_8N_FRB/">160819_8N_FRB</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIiM2FsMnVLLTMwb2M">habrahabr.ru.summary.csv</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIiaFZjZ2paTlUzaUE">habrahabr.ru.details.csv</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIiMG1wZkVub0NRUlU">habrahabr.ru.har</a></td>
	</tr>
	<tr>
		<td>jmeter.apache.org</td>
		<td><a href="https://www.webpagetest.org/result/160819_CG_FSM/">160819_CG_FSM</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIiVzlua0tlTnNXd28">jmeter.apache.org.summary.csv</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIieGk0TjVvZlJVd1U">jmeter.apache.org.details.csv</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIieWdLSGFOeEdZMEE">jmeter.apache.org.har</a></td>
	</tr>
	<tr>
		<td>linkedin.com</td>
		<td><a href="https://www.webpagetest.org/result/160819_K2_FY1/">160819_K2_FY1</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIiV19IMjhCUThhTVE">linkedin.com.summary.csv</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIiUmdHcWxTc1hGcVk">linkedin.com.details.csv</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIiWHVfRU1zNE84ODg">linkedin.com.har</a></td>
	</tr>
	<tr>
		<td>mos.ru</td>
		<td><a href="https://www.webpagetest.org/result/160819_91_G0F/">160819_91_G0F</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIibFJqU0hzX1IxbmM">mos.ru.summary.csv</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIibzRGNWVXNVRoQW8">mos.ru.details.csv</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIiSUczcXFSXzMzb0E">mos.ru.har</a></td>
	</tr>
	<tr>
		<td>stackoverflow.com</td>
		<td><a href="https://www.webpagetest.org/result/160819_S0_G18/">160819_S0_G18</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIidlFMbXRObkFyVzA">stackoverflow.com.summary.csv</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIiYm0wSUV4YWZzWEk">stackoverflow.com.details.csv</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIiWW1nck4tU0tvb2c">stackoverflow.com.har</a></td>
	</tr>
	<tr>
		<td>yandex.ru</td>
		<td><a href="https://www.webpagetest.org/result/160819_MR_G1R/">160819_MR_G1R</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIiUW5PSXBWMlU4Skk">yandex.ru.summary.csv</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIiWml6R3NNQ0J4bk0">yandex.ru.details.csv</a></td>
		<td><a href="https://drive.google.com/open?id=0B5nKzHDZ1RIiQTNkaWFFN0NhOFU">yandex.ru.har</a></td>
	</tr>
</table>

![github.com via webpagetest.org](images/github.com.PNG)
![google.ru via webpagetest.org](images/google.ru.PNG)
![habrahabr.ru via webpagetest.org](images/habrahabr.ru.PNG)
![jmeter.apache.org via webpagetest.org](images/jmeter.apache.org.PNG)
![linkedin.com via webpagetest.org](images/linkedin.com.PNG)
![mos.ru via webpagetest.org](images/mos.ru.PNG)
![stackoverflow.com via webpagetest.org](images/stackoverflow.com.PNG)
![yandex.ru via webpagetest.org](images/yandex.ru.PNG)

### Логи Apache.JMeter

Для обработки используются csv-логи, сформированные плагином **CsvLogWriter**:

- описание: [https://habrahabr.ru/post/308098/](https://habrahabr.ru/post/308098/ "Плагин CsvLogWriter для JMeter ");
- проект: [https://github.com/pflb/Jmeter.Plugin.CsvLogWriter](https://github.com/pflb/Jmeter.Plugin.CsvLogWriter "Jmeter.Plugin.CsvLogWriter").

В результате работы которого формируется лог, в список колонок которого входят:

- ***timeStamp*** — момент времени;
- ***URL*** — адрес запроса;
- ***elapsed*** — длительность получения ответа на запрос;
- ***bytes*** — размер ответа;
- ***siteKey*** — используемый сайт;
- ***htmlParser*** — название используемого ;
- ***jmeterVersion*** — используемая версия Apache.JMeter;
- ***i*** — номер итерации тестирования.

Аггрегация csv-логов **Apache.JMeter** выполняется при помощь **pandas** вот таким кодом на **python**:

	import pandas as pd
	import codecs
	from os import listdir
	import numpy as np
	

	# Настройки - каталог с логами и настройки считывания логов
	dirPath = "D:/project/jmeter.3.0.vs.jmeter.2.13/logs"
	
	read_csv_param = dict( index_col=['timeStamp'],
	                       low_memory=False,
	                       sep = ";",
	                       na_values=[' ','','null'])
	
	# Получение списка csv-файлов в каталоге с логами
	files = filter(lambda a: '.csv' in a, listdir(dirPath))
	
	
	# Чтение содержимого всех csv-файлов в DataFrame dfs
	csvfile = dirPath + "/" + files[0]
	print(files[0])
	dfs = pd.read_csv(csvfile, **read_csv_param)
	for csvfile in files[1:]:
	    print(csvfile)
	    tempDfs = pd.read_csv(dirPath + "/" + csvfile, **read_csv_param)
	    dfs = dfs.append(tempDfs)
	
	dfs.to_excel(dirPath + "/total.xlsx")
	
	# Убрать из выборки все JSR223, по ним статистику строить не надо, оставить только HTTP Request Sampler
	# У JSR223 поле URL пустое, у http-запросов поле URL заполнено
	dfs = dfs[(pd.isnull(dfs.URL) == False)]
	
	
	# Сводная таблица по количеству запросов, сохраняется в report.requests.html - основной результат работы
	pd.pivot_table(dfs, 
	               index=['siteKey', "jmeterVersion", "htmlParser"], 
	               values="URL", 
	               columns=["i"], 
	               aggfunc="count").to_html(dirPath + "/report.requests.html")