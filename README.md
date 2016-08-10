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

Основой для тестирования послужили изменения в **Apache.JMeter 3.0** http://jmeter.apache.org/changes.html

#### Core improvements
##### Dependencies refresh

Deprecated Libraries dropped or replaced by up to date ones:

- htmllexer, htmlparser removed
- jdom removed


#### Protocols and Load Testing improvements
##### Parallel Downloads is now realistic and scales much better:

- Parsing of CSS imported files (through @import) or embedded resources (background, images, …)

#### Incompatible changes

- Since version 3.0, the parser for embedded resources (replaced since 2.10 by Lagarto based implementation) which relied on the htmlparser library (HtmlParserHTMLParser) has been dropped along with its dependencies.
- The following jars have been removed:
   - htmllexer-2.1.jar (see [Bug 59037](http://bz.apache.org/bugzilla/show_bug.cgi?id=59037))
   - htmlparser-2.1.jar (see [Bug 59037](http://bz.apache.org/bugzilla/show_bug.cgi?id=59037))
   - jdom-1.1.3.jar (see [Bug 59156](http://bz.apache.org/bugzilla/show_bug.cgi?id=59156))

#### Improvements
##### HTTP Samplers and Test Script Recorder

- [Bug 59036](http://bz.apache.org/bugzilla/show_bug.cgi?id=59036) - FormCharSetFinder : Use JSoup instead of deprecated HTMLParser
- [Bug 59033](http://bz.apache.org/bugzilla/show_bug.cgi?id=59033) - Parallel Download : Rework Parser classes hierarchy to allow plug-in parsers for different mime types
- [Bug 59140](http://bz.apache.org/bugzilla/show_bug.cgi?id=59140) - Parallel Download : Add CSS Parsing to extract links from CSS files

##### General

- [Bug 59093](http://bz.apache.org/bugzilla/show_bug.cgi?id=59093) - Option parsing error message can be 'lost'


## Цели тестирования

Сравнить работу всех доступных парсеров. В частности сравнить между собой парсеры версий 2.13 и 3.0, убедиться, что загрузка встроенных ресурсов стала реалистичнее и лучше.

## Стратегия тестирования

Этап 1:

1. Выполнить загрузку стартовых страниц списка сайтов используя все 5 парсеров Apache.JMeter 2.13 и записать логи.
2. Выполнить загрузку стартовых страниц списка сайтов используя все 4 парсера Apache.JMeter 3.0 и записать логи.
3. Проанализировать логи работы Apache.JMeter и сравнить их между собой. Оценить, стала ли загрузка встроенных ресурсов лучше, расширился ли перечень загружаемых встроенных ресурсов.

Этап 2:

1. Выполнить загрузку стартовых страниц списка популярных сайтов, используя Google Chrome и сервис webpagetest.org.
2. Проанализировать отчёты из webpagetest.org и сравнить их с результатами анализа логов Apache.JMEter. Оценить, реалистичность загрузки встроенных ресурсов.


# Состав проекта

- **test.bat** — командный файл запуска теста на двух версиях **Apache.JMeter**, 2.13 и 3.0, файл содержит количество итераций тестирования и адреса тестируемых сайтов. Файл вызывает файлы **jmeter.2.13.bat** и **jmeter.3.0.bat**;
- **jmeter.3.0.bat** — командный файл запуска теста для **Apache.JMeter 3.0**, тут задаётся путь к папке `/bin/` **Apache.JMeter 3.0**, путь к тестовому скрипту **jmeter.testfile.jmx**, опции запуска теста, а также список htmlParser-ов проверка работы которых выполняется;
- **jmeter.2.13.bat** — командный файл запуска теста для **Apache.JMeter 2.13**, тут задаётся путь к папке `/bin/` **Apache.JMeter 2.13**, путь к тестовому скрипту **jmeter.testfile.jmx**, опции запуска теста, а также список htmlParser-ов проверка работы которых выполняется;
- **jmeter.testfile.jmx** — тестовый скрипт принимающий на вход параметры:
  - URL — адрес тестируемого сайта, например, https://yandex.ru/;
  - siteKey — строка по которой будет осуществляться группировка записей в логах, например, yandex.ru;
  - loopCount — количество итераций теста, используется несколько итераций из-за того, что работа веб-сайтов может быть нестабильной;
  - htmlParser.className — парсер для извлечения ссылок на встроенные ресурсы.

#Результаты

##Количество запросов при использовании различных парсеров

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th colspan="9"> Apache.JMeter </th>
      <th colspan="3">Chrome, webpagetest.org</th>
    </tr>
    <tr>
      <th>siteKey</th>
      <th>jmeter.version</th>
      <th>htmlParser</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>Среднее по парсеру</th>
      <th>Среднее по jmeter</th>
      <th>Before Start Render</th>
      <th>Document Complete</th>
      <th>Fully Loaded</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="9" valign="top">github.com</th>
      <th rowspan="5" valign="top">2.13 r1665067</th>
      <th>HtmlParserHTMLParser</th>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td><!--1.AP-->
      <td rowspan="5">13</td><!--2.AJ-->
      <td rowspan="9">17</td><!--3.BSR-->
      <td rowspan="9">19</td><!--4.DC-->
      <td rowspan="9">22</td><!--5.FL-->
    </tr>
    <tr>
      <th>JTidyHTMLParser</th>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td><!--1-->
    </tr>
    <tr>
      <th>JsoupBasedHtmlParser</th>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td><!--1-->
    </tr>
    <tr>
      <th>LagartoBasedHtmlParser</th>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td><!--1-->
    </tr>
    <tr>
      <th>RegexpHTMLParser</th>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td><!--1-->
    </tr>
    <tr>
      <th rowspan="4" valign="top">3.0 r1743807</th>
      <th>JTidyHTMLParser</th>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td><!--1-->
      <td rowspan="4">13</td><!--2.AJ-->
    </tr>
    <tr>
      <th>JsoupBasedHtmlParser</th>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td><!--1-->
    </tr>
    <tr>
      <th>LagartoBasedHtmlParser</th>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td><!--1-->
    </tr>
    <tr>
      <th>RegexpHTMLParser</th>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td>
      <td>13</td><!--1-->
    </tr>
    <tr>
      <th rowspan="9" valign="top">google.ru</th>
      <th rowspan="5" valign="top">2.13 r1665067</th>
      <th>HtmlParserHTMLParser</th>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td><!--1.AP-->
      <td rowspan="5">4,56</td><!--2.AJ-->
      <td rowspan="9">4</td><!--3.BSR-->
      <td rowspan="9">9</td><!--4.DC-->
      <td rowspan="9">12</td><!--5.FL-->
    </tr>
    <tr>
      <th>JTidyHTMLParser</th>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>4</td>
      <td>4,8</td><!--1.AP-->
    </tr>
    <tr>
      <th>JsoupBasedHtmlParser</th>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td><!--1.AP-->
    </tr>
    <tr>
      <th>LagartoBasedHtmlParser</th>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td><!--1.AP-->
    </tr>
    <tr>
      <th>RegexpHTMLParser</th>
      <td>3</td>
      <td>3</td>
      <td>3</td>
      <td>3</td>
      <td>3</td>
      <td>3</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="4" valign="top">3.0 r1743807</th>
      <th>JTidyHTMLParser</th>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td><!--1.AP-->
      <td rowspan="4">4,5</td><!--2.AJ-->
    </tr>
    <tr>
      <th>JsoupBasedHtmlParser</th>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td><!--1.AP-->
    </tr>
    <tr>
      <th>LagartoBasedHtmlParser</th>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td>
      <td>5</td><!--1.AP-->
    </tr>
    <tr>
      <th>RegexpHTMLParser</th>
      <td>3</td>
      <td>3</td>
      <td>3</td>
      <td>3</td>
      <td>3</td>
      <td>3</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="9" valign="top">habrahabr.ru</th>
      <th rowspan="5" valign="top">2.13 r1665067</th>
      <th>HtmlParserHTMLParser</th>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td><!--1.AP-->
      <td rowspan="5">43,6</td><!--2.AJ-->
      <td rowspan="9">34</td><!--3.BSR-->
      <td rowspan="9">113</td><!--4.DC-->
      <td rowspan="9">120</td><!--5.FL-->
    </tr>
    <tr>
      <th>JTidyHTMLParser</th>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td><!--1.AP-->
    </tr>
    <tr>
      <th>JsoupBasedHtmlParser</th>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td><!--1.AP-->
    </tr>
    <tr>
      <th>LagartoBasedHtmlParser</th>
      <td>41</td>
      <td>41</td>
      <td>41</td>
      <td>41</td>
      <td>41</td>
      <td>41</td><!--1.AP-->
    </tr>
    <tr>
      <th>RegexpHTMLParser</th>
      <td>45</td>
      <td>45</td>
      <td>45</td>
      <td>45</td>
      <td>45</td>
      <td>45</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="4" valign="top">3.0 r1743807</th>
      <th>JTidyHTMLParser</th>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td><!--1.AP-->
      <td rowspan="4">43,5</td><!--2.AJ-->
    </tr>
    <tr>
      <th>JsoupBasedHtmlParser</th>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td>
      <td>44</td><!--1.AP-->
    </tr>
    <tr>
      <th>LagartoBasedHtmlParser</th>
      <td>41</td>
      <td>41</td>
      <td>41</td>
      <td>41</td>
      <td>41</td>
      <td>41</td><!--1.AP-->
    </tr>
    <tr>
      <th>RegexpHTMLParser</th>
      <td>45</td>
      <td>45</td>
      <td>45</td>
      <td>45</td>
      <td>45</td>
      <td>45</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="9" valign="top">jmeter.apache.org</th>
      <th rowspan="5" valign="top">2.13 r1665067</th>
      <th>HtmlParserHTMLParser</th>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td><!--1.AP-->
      <td rowspan="5">10</td><!--2.AJ-->
      <td rowspan="9">10</td><!--3.BSR-->
      <td rowspan="9">10</td><!--4.DC-->
      <td rowspan="9">11</td><!--5.FL-->
    </tr>
    <tr>
      <th>JTidyHTMLParser</th>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td><!--1.AP-->
    </tr>
    <tr>
      <th>JsoupBasedHtmlParser</th>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td><!--1.AP-->
    </tr>
    <tr>
      <th>LagartoBasedHtmlParser</th>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td><!--1.AP-->
    </tr>
    <tr>
      <th>RegexpHTMLParser</th>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="4" valign="top">3.0 r1743807</th>
      <th>JTidyHTMLParser</th>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td><!--1.AP-->
      <td rowspan="4">10</td><!--2.AJ-->
    </tr>
    <tr>
      <th>JsoupBasedHtmlParser</th>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td><!--1.AP-->
    </tr>
    <tr>
      <th>LagartoBasedHtmlParser</th>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td><!--1.AP-->
    </tr>
    <tr>
      <th>RegexpHTMLParser</th>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td>
      <td>10</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="9" valign="top">linkedin.com</th>
      <th rowspan="5" valign="top">2.13 r1665067</th>
      <th>HtmlParserHTMLParser</th>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td><!--1.AP-->
      <td rowspan="5">10,2</td><!--2.AJ-->
      <td rowspan="9">14</td><!--3.BSR-->
      <td rowspan="9">20</td><!--4.DC-->
      <td rowspan="9">22</td><!--5.FL-->
    </tr>
    <tr>
      <th>JTidyHTMLParser</th>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td><!--1.AP-->
    </tr>
    <tr>
      <th>JsoupBasedHtmlParser</th>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td><!--1.AP-->
    </tr>
    <tr>
      <th>LagartoBasedHtmlParser</th>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td><!--1.AP-->
    </tr>
    <tr>
      <th>RegexpHTMLParser</th>
      <td>7</td>
      <td>7</td>
      <td>7</td>
      <td>7</td>
      <td>7</td>
      <td>7</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="4" valign="top">3.0 r1743807</th>
      <th>JTidyHTMLParser</th>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td><!--1.AP-->
      <td rowspan="4">10</td><!--2.AJ-->
    </tr>
    <tr>
      <th>JsoupBasedHtmlParser</th>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td><!--1.AP-->
    </tr>
    <tr>
      <th>LagartoBasedHtmlParser</th>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td>
      <td>11</td><!--1.AP-->
    </tr>
    <tr>
      <th>RegexpHTMLParser</th>
      <td>7</td>
      <td>7</td>
      <td>7</td>
      <td>7</td>
      <td>7</td>
      <td>7</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="9" valign="top">mos.ru</th>
      <th rowspan="5" valign="top">2.13 r1665067</th>
      <th>HtmlParserHTMLParser</th>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td><!--1.AP-->
      <td rowspan="5">22,8</td><!--2.AJ-->
      <td rowspan="9">13</td><!--3.BSR-->
      <td rowspan="9">98</td><!--4.DC-->
      <td rowspan="9">144</td><!--5.FL-->
    </tr>
    <tr>
      <th>JTidyHTMLParser</th>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td><!--1.AP-->
    </tr>
    <tr>
      <th>JsoupBasedHtmlParser</th>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td><!--1.AP-->
    </tr>
    <tr>
      <th>LagartoBasedHtmlParser</th>
      <td>14</td>
      <td>14</td>
      <td>14</td>
      <td>14</td>
      <td>14</td>
      <td>14</td><!--1.AP-->
    </tr>
    <tr>
      <th>RegexpHTMLParser</th>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td>
      <td>25</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="4" valign="top">3.0 r1743807</th>
      <th>JTidyHTMLParser</th>
      <td>26</td>
      <td>26</td>
      <td>26</td>
      <td>26</td>
      <td>26</td>
      <td>26</td><!--1.AP-->
      <td rowspan="4">23,25</td><!--2.AJ-->
    </tr>
    <tr>
      <th>JsoupBasedHtmlParser</th>
      <td>26</td>
      <td>26</td>
      <td>26</td>
      <td>26</td>
      <td>26</td>
      <td>26</td><!--1.AP-->
    </tr>
    <tr>
      <th>LagartoBasedHtmlParser</th>
      <td>15</td>
      <td>15</td>
      <td>15</td>
      <td>15</td>
      <td>15</td>
      <td>15</td><!--1.AP-->
    </tr>
    <tr>
      <th>RegexpHTMLParser</th>
      <td>26</td>
      <td>26</td>
      <td>26</td>
      <td>26</td>
      <td>26</td>
      <td>26</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="9" valign="top">stackoverflow.com</th>
      <th rowspan="5" valign="top">2.13 r1665067</th>
      <th>HtmlParserHTMLParser</th>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>16</td><!--1.AP-->
      <td rowspan="5">15,88</td><!--2.AJ-->
      <td rowspan="9">25</td><!--3.BSR-->
      <td rowspan="9">39</td><!--4.DC-->
      <td rowspan="9">40</td><!--5.FL-->
    </tr>
    <tr>
      <th>JTidyHTMLParser</th>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>16</td><!--1.AP-->
    </tr>
    <tr>
      <th>JsoupBasedHtmlParser</th>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>18</td>
      <td>18</td>
      <td>16,8</td><!--1.AP-->
    </tr>
    <tr>
      <th>LagartoBasedHtmlParser</th>
      <td>14</td>
      <td>14</td>
      <td>15</td>
      <td>15</td>
      <td>15</td>
      <td>14,6</td><!--1.AP-->
    </tr>
    <tr>
      <th>RegexpHTMLParser</th>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>16</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="4" valign="top">3.0 r1743807</th>
      <th>JTidyHTMLParser</th>
      <td>17</td>
      <td>17</td>
      <td>17</td>
      <td>17</td>
      <td>17</td>
      <td>17</td><!--1.AP-->
      <td rowspan="4">16,65</td><!--2.AJ-->
    </tr>
    <tr>
      <th>JsoupBasedHtmlParser</th>
      <td>17</td>
      <td>17</td>
      <td>17</td>
      <td>17</td>
      <td>17</td>
      <td>17</td><!--1.AP-->
    </tr>
    <tr>
      <th>LagartoBasedHtmlParser</th>
      <td>14</td>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>16</td>
      <td>15,6</td><!--1.AP-->
    </tr>
    <tr>
      <th>RegexpHTMLParser</th>
      <td>17</td>
      <td>17</td>
      <td>17</td>
      <td>17</td>
      <td>17</td>
      <td>17</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="9" valign="top">yandex.ru</th>
      <th rowspan="5" valign="top">2.13 r1665067</th>
      <th>HtmlParserHTMLParser</th>
      <td>69</td>
      <td>68</td>
      <td>69</td>
      <td>68</td>
      <td>69</td>
      <td>68,6</td><!--1.AP-->
      <td rowspan="5">28,24</td><!--2.AJ-->
      <td rowspan="9">23</td><!--3.BSR-->
      <td rowspan="9">34</td><!--4.DC-->
      <td rowspan="9">36</td><!--5.FL-->
    </tr>
    <tr>
      <th>JTidyHTMLParser</th>
      <td>20</td>
      <td>19</td>
      <td>19</td>
      <td>19</td>
      <td>19</td>
      <td>19,2</td><!--1.AP-->
    </tr>
    <tr>
      <th>JsoupBasedHtmlParser</th>
      <td>20</td>
      <td>19</td>
      <td>19</td>
      <td>20</td>
      <td>19</td>
      <td>19,4</td><!--1.AP-->
    </tr>
    <tr>
      <th>LagartoBasedHtmlParser</th>
      <td>15</td>
      <td>15</td>
      <td>15</td>
      <td>15</td>
      <td>15</td>
      <td>15</td><!--1.AP-->
    </tr>
    <tr>
      <th>RegexpHTMLParser</th>
      <td>19</td>
      <td>19</td>
      <td>19</td>
      <td>19</td>
      <td>19</td>
      <td>19</td><!--1.AP-->
    </tr>
    <tr>
      <th rowspan="4" valign="top">3.0 r1743807</th>
      <th>JTidyHTMLParser</th>
      <td>639</td>
      <td>642</td>
      <td>642</td>
      <td>513</td>
      <td>644</td>
      <td>616</td><!--1.AP-->
      <td rowspan="4">534,3</td><!--2.AJ-->
    </tr>
    <tr>
      <th>JsoupBasedHtmlParser</th>
      <td>643</td>
      <td>334</td>
      <td>639</td>
      <td>641</td>
      <td>643</td>
      <td>580</td><!--1.AP-->
    </tr>
    <tr>
      <th>LagartoBasedHtmlParser</th>
      <td>349</td>
      <td>449</td>
      <td>451</td>
      <td>449</td>
      <td>13</td>
      <td>342,2</td><!--1.AP-->
    </tr>
    <tr>
      <th>RegexpHTMLParser</th>
      <td>641</td>
      <td>635</td>
      <td>638</td>
      <td>436</td>
      <td>645</td>
      <td>599</td><!--1.AP-->
    </tr>
  </tbody>
</table>

Альтернативный вариант таблицы с результатом: [result.html](results.htm).