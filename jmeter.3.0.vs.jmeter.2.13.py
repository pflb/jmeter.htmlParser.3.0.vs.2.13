
# coding: utf-8

# In[5]:

import pandas as pd
import codecs
from os import listdir
import numpy as np


# Настройки - каталог с логами и настройки считывания логов.
dirPath = "D:/project/jmeter.htmlParser.3.0.vs.2.13/logs"

read_csv_param = dict( index_col=['timeStamp'],
                       low_memory=False,
                       sep = ";",
                       na_values=[' ','','null'])

# Получение списка csv-файлов в каталоге с логами.
files = filter(lambda a: '.csv' in a, listdir(dirPath))


# Чтение содержимого всех csv-файлов в DataFrame dfs.
csvfile = dirPath + "/" + files[0]
print(files[0])
dfs = pd.read_csv(csvfile,**read_csv_param)
for csvfile in files[1:]:
    print(csvfile)
    tempDfs = pd.read_csv(dirPath + "/" + csvfile, **read_csv_param)
    dfs = dfs.append(tempDfs)

#dfs.to_excel(dirPath + "/total.xlsx")

# Убрать из выборки все JSR223, по ним статистику строить не надо, оставить только HTTP Request Sampler.
# У JSR223 URL пустой, у HTTP-запросов URL указан.
dfs = dfs[(pd.isnull(dfs.URL) == False)]


# Сводная таблица по количеству подзапросов, сохраняется в report.subrequests.html - основной результат работы.
# Из количества запросов удаляется один запрос, чтобы исключить корневой запрос.
# Цель данного исследования - подсчёт количества подзапросов, поэтому корневой исключается.
pd.pivot_table(dfs, 
               index=['siteKey', "jmeterVersion", "htmlParser"], 
               values="URL", 
               columns=["i"], 
               aggfunc=lambda url: url.count()-1).to_html(dirPath + "/report.subrequest.count.html")


# In[ ]:

dfs[]


# In[ ]:



