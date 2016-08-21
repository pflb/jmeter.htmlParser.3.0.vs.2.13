
# coding: utf-8

# In[2]:

import pandas as pd
import codecs
from os import listdir
import numpy as np


# Настройки - каталог с логами и настройки считывания логов
dirPath = "D:/project/jmeter.htmlParser.3.0.vs.2.13/logs"

read_csv_param = dict( index_col=['timeStamp'],
                       low_memory=False,
                       sep = ";",
                       na_values=[' ','','null'])

# Получение списка csv-файлов в каталоге с логами
files = filter(lambda a: '.csv' in a, listdir(dirPath))


# Чтение содержимого всех csv-файлов в DataFrame dfs
csvfile = dirPath + "/" + files[0]
print(files[0])
dfs = pd.read_csv(csvfile,**read_csv_param)
for csvfile in files[1:]:
    print(csvfile)
    tempDfs = pd.read_csv(dirPath + "/" + csvfile, **read_csv_param)
    dfs = dfs.append(tempDfs)

#dfs.to_excel(dirPath + "/total.xlsx")

# Убрать из выборки все JSR223, по ним статистику строить не надо, оставить только HTTP Request Sampler
# У JSR223 
dfs = dfs[(pd.isnull(dfs.URL) == False)]


# Сводная таблица по количеству запросов, сохраняется в report.requests.html - основной результат работы
pd.pivot_table(dfs, 
               index=['siteKey', "jmeterVersion", "htmlParser"], 
               values="URL", 
               columns=["i"], 
               aggfunc="count").to_html(dirPath + "/report.requests.html")
# Сводная таблица по длительности выполнения, сохраняется в report.time.html
pd.pivot_table(dfs[dfs.transactionLevel==0], 
               index=['siteKey', "jmeterVersion", "htmlParser"], 
               values="elapsed", 
               columns=["i"], 
               aggfunc="sum").to_html(dirPath + "/report.time.html")
# Сводная таблица по объёму трафика, сохраняется в report.bytes.html
pd.pivot_table(dfs[dfs.transactionLevel==0], 
               index=['siteKey', "jmeterVersion", "htmlParser"], 
               values="bytes", 
               columns=["i"], 
               aggfunc="sum").to_html(dirPath + "/report.bytes.html")


# In[ ]:

dfs[]


# In[ ]:



