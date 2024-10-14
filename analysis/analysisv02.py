#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Manual imports
#import csv
import datetime
import math
#import matplotlib.pyplot as plt
import nltk
#import numpy as np
import openpyxl
import pandas as pd
#import pprint
#import pymysql.cursors
import re
#import seaborn as sns
#import statsmodels.api as sm
#import sys

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
# Sólo la primera vez:
'''
  Resource stopwords not found.
  Please use the NLTK Downloader to obtain the resource:

  >>> import nltk
  >>> nltk.download('stopwords') # OK: ESP MX y ESP ES
  
  Resource punkt not found.
  Please use the NLTK Downloader to obtain the resource:

  >>> import nltk
  >>> nltk.download('punkt')
'''

#pd.set_option('display.max_rows', 500)
#pd.set_option('display.max_columns', 100)

#USB = "TOSH08"
USB = "KING16-3"

# Path for tables for TEX
#sys.path.append('/media/clm/' + USB + '/info/LIBS')
#import textables # file is textables
#import graphs # file is graphs
#import wkd # days in Spanish & English (python days 0-6 = Mon-Sun)

#_______________________________________________________________________

# Análisis para recomendación de productos

# Definimos la ruta del proyecto
PATHP = "/media/clm/" + USB + "/" + \
    "48-2022FEB11-recom_prods/"
#PATHP = "/home/admin/rec/"

#_______________________________________________________________________
#_______________________________________________________________________

# CONFIGURATION

# To display more rows in the shell:

#pd.set_option('display.max_rows', 500)
#pd.set_option('display.max_columns', 500)

#_______________________________________________________________________
#_______________________________________________________________________

# FILE READING

# READ from XLS FILE
archList = ["IEBS", "COURSERA", "UNICEF", "ONU", "GOOGLE ADS", "FB", \
"CIFAL"]
tmpList = []
for archivo in archList:
    print(archivo)
    arcDF = pd.read_excel(PATHP + 'data/alianzas.xlsx',
        header = 0,
        usecols = ['MATRICULA', 'FECHA_ESTATUS', 'PRIMER_INSCRIPCION',\
        'NIVEL', 'PROGRAMA', 'ALIANZA', 'MODALIDAD'],
        sheet_name = archivo
    )
    arcDF['ALSH'] = archivo
    print(arcDF.head())
    tmpList.append(arcDF)
data = pd.concat(tmpList)

# Esto ya no, Ahora hacenos ciclo para leer archivos
'''
# Using PATHP variable - MIXED TYPE column: specify dtype of username
d1 = pd.read_excel(PATHP + 'data/alianzas.xlsx',
    header = 0,
    usecols = ['MATRICULA', 'FECHA_ESTATUS', 'PRIMER_INSCRIPCION', \
    'NIVEL', 'PROGRAMA', 'ALIANZA', 'MODALIDAD'],
    sheet_name = 'IEBS'
    )
d1['ALSH'] = 'IEBS'
d2 = pd.read_excel(PATHP + 'data/alianzas.xlsx',
    header = 0,
    usecols = ['MATRICULA', 'FECHA_ESTATUS', 'PRIMER_INSCRIPCION', \
    'NIVEL', 'PROGRAMA', 'ALIANZA', 'MODALIDAD'],
    sheet_name = 'COURSERA'
    )
d2['ALSH'] = 'COURSERA'
d3 = pd.read_excel(PATHP + 'data/alianzas.xlsx',
    header = 0,
    usecols = ['MATRICULA', 'FECHA_ESTATUS', 'PRIMER_INSCRIPCION', \
    'NIVEL', 'PROGRAMA', 'ALIANZA', 'MODALIDAD'],
    sheet_name = 'UNICEF'
    )
d3['ALSH'] = 'UNICEF'
d4 = pd.read_excel(PATHP + 'data/alianzas.xlsx',
    header = 0,
    usecols = ['MATRICULA', 'FECHA_ESTATUS', 'PRIMER_INSCRIPCION', \
    'NIVEL', 'PROGRAMA', 'ALIANZA', 'MODALIDAD'],
    sheet_name = 'ONU'
    )
d4['ALSH'] = 'ONU'
d5 = pd.read_excel(PATHP + 'data/alianzas.xlsx',
    header = 0,
    usecols = ['MATRICULA', 'FECHA_ESTATUS', 'PRIMER_INSCRIPCION', \
    'NIVEL', 'PROGRAMA', 'ALIANZA', 'MODALIDAD'],
    sheet_name = 'GOOGLE ADS'
    )
d5['ALSH'] = 'GOOGLE_ADS'
d6 = pd.read_excel(PATHP + 'data/alianzas.xlsx',
    header = 0,
    usecols = ['MATRICULA', 'FECHA_ESTATUS', 'PRIMER_INSCRIPCION', \
    'NIVEL', 'PROGRAMA', 'ALIANZA', 'MODALIDAD'],
    sheet_name = 'FB'
    )
d6['ALSH'] = 'FB'
d7 = pd.read_excel(PATHP + 'data/alianzas.xlsx',
    header = 0,
    usecols = ['MATRICULA', 'FECHA_ESTATUS', 'PRIMER_INSCRIPCION', \
    'NIVEL', 'PROGRAMA', 'ALIANZA', 'MODALIDAD'],
    sheet_name = 'CIFAL'
    )
d7['ALSH'] = 'CIFAL'
# Pegamos
data = pd.concat([d1, d2, d3, d4, d5, d6, d7])
'''

# No funciona el object con matrícula porque viene como int de source
#, y se tiene que hacer conversion a str explicit
data["MATRICULA"] = data["MATRICULA"].astype(str).str.zfill(9)
# Convert from excel date to python date
data['date'] = pd.to_datetime(data['FECHA_ESTATUS'], unit='D', \
    origin='1899-12-30')
data.drop('FECHA_ESTATUS', axis = 1, inplace = True)
data.columns = ['username', 'primer_inscrip', \
    'nivel', 'proglong', 'etiqueta', 'modal', 'alsh', 'date']

# -----------BEG - bloque exploración
data[:5]
Out[50]: 
     username               primer_inscrip nivel  ... modal   alsh       date
0   010411136  03/01/2022  Periodo  012242    LI  ...    OL   IEBS 2022-01-03
1   290403651  25/10/2021  Periodo  292242    LI  ...   EXE   IEBS 2021-10-27
2   290354695  05/07/2021  Periodo  292241    MA  ...   EXE   IEBS 2021-06-28
3   200347748  05/07/2021  Periodo  202241    MA  ...   EXE   IEBS 2021-05-19
4   010403098  25/10/2021  Periodo  012242    MA  ...   EXE   IEBS 2021-10-27
..        ...                          ...   ...  ...   ...    ...        ...
len(data)
Out[24]: 4857
len(data.username.unique())
Out[17]: 4843
# -----------END - bloque exploración


# eliminate those with alphanumeric chars
data = data[[x.isnumeric() for x in data['username']]]
# eliminate teachers
data = data[~(data['username'].str.contains("^0198"))]
len(data)
# 4857
len(data.username.unique())
# 4843
#DIF = 14

# Data string deaggregation
tempList1 = []
tempList2 = []
tempList3 = []
tempList4 = []
for line in data['proglong']:
    progsh = line[:10]
    escuela = progsh[:3]
    carreraid = progsh[5:7]
    carreradesc = line[11:]
    tempList1.append(progsh)
    tempList2.append(escuela)
    tempList3.append(carreraid)
    tempList4.append(carreradesc)
data['progsh'] = tempList1
data['escuela'] = tempList2
data['progmid'] = tempList3
data['progmdesc'] = tempList4


# -----------BEG - bloque exploración # Frequencies

data['alsh'].value_counts()
UNICEF        3669
COURSERA       929
ONU            217
IEBS            25
GOOGLE_ADS       9
FB               7
CIFAL            1

data['etiqueta'].value_counts()
UNIC            3206
COUR             853
UNICEJEC         460
MONU             217
COUREJEC          67
GADSEJECIEBS       8
EJECIEBS           8
FCBKEJECIEBS       6
GADSFCBKEJEC       6
SENICOUR           6
UNICEJECIEBS       4
MUBAEJECIEBS       3
COURIEBS           2
COURUNIC           2
COUREJECIEBS       2
UNICFCBKEJEC       2
GADSEJEC           2
IEBS               1
UNICMUBAEJEC       1
EJECCIFA           1

dat2 = data.groupby(["alsh", "etiqueta"], sort = False)\
    .count()["username"]
dat2 = dat2.to_frame()
dat2
# dat2.reset_index(inplace = True)
alsh       alianza               
IEBS       IEBS                 1
           EJECIEBS             8
           MUBAEJECIEBS         3
           COUREJECIEBS         1 D IEBS/COUR
           UNICEJECIEBS         4 D IEBS/UNIC
           COURIEBS             1 D IEBS/COUR
           GADSEJECIEBS         4 D IEBS/GADS
           FCBKEJECIEBS         3 D IEBS/FCBK
COURSERA   COUR               853
           SENICOUR             6
           COUREJEC            67
           COUREJECIEBS         1 D COUR/IEBS
           COURIEBS             1 D COUR/IEBS
           COURUNIC             1 D COUR/UNIC
UNICEF     UNIC              3206
           UNICEJEC           460
           COURUNIC             1 D UNIC/COUR
           UNICFCBKEJEC         1 D UNIC/FCBK
           UNICMUBAEJEC         1 D UNIC/MUBA
ONU        MONU               217
GOOGLE ADS GADSEJECIEBS         4 D GADS/IEBS
           GADSFCBKEJEC         3 D GADS/FCBK
           GADSEJEC             2
FB         UNICFCBKEJEC         1 D FCBK/UNIC
           GADSFCBKEJEC         3 D FCBK/GADS
           FCBKEJECIEBS         3 D FCBK/IEBS

---------

IEBS       COUREJECIEBS         1 D IEBS/COUR - A
           UNICEJECIEBS         4 D IEBS/UNIC - B
           COURIEBS             1 D IEBS/COUR - A
           GADSEJECIEBS         4 D IEBS/GADS - C
           FCBKEJECIEBS         3 D IEBS/FCBK - D
COURSERA   COUREJECIEBS         1 D COUR/IEBS - A
           COURIEBS             1 D COUR/IEBS - A
           COURUNIC             1 D COUR/UNIC
UNICEF     COURUNIC             1 D UNIC/COUR
           UNICFCBKEJEC         1 D UNIC/FCBK
           UNICMUBAEJEC         1 D UNIC/MUBA
GOOGLE ADS GADSEJECIEBS         4 D GADS/IEBS - C
           GADSFCBKEJEC         3 D GADS/FCBK
FB         UNICFCBKEJEC         1 D FCBK/UNIC
           GADSFCBKEJEC         3 D FCBK/GADS
           FCBKEJECIEBS         3 D FCBK/IEBS - D

IEBS/COUR 2 - COUR/IEBS 2
IEBS/UNIC 4 - UNIC/IEBS 0
IEBS/GADS 4 - GADS/IEBS 4
IEBS/FCBK 3 - FCBK/IEBS 3
COUR/UNIC 1 - UNIC/COUR 1
COUR/GADS 0 - GADS/COUR 0
COUR/FCBK 0 - FCBK/COUR 0
UNIC/GADS 0 - GADS/UNIC 0
UNIC/FCBK 1 - FCBK/UNIC 1
GADS/FCNK 3 - FCBK/GADS 3
TOT COMBINACIONES = 18

data[(data["etiqueta"].str.contains("COUR")) & \
    (data["etiqueta"].str.contains("IEBS"))]\
    [['alsh', 'username', 'progmdesc', 'etiqueta']]
         alsh   username                       progmdesc      etiqueta
12       IEBS  010314075  MAE ADMIN NEGOCIOS IEBS EJECUT  COUREJECIEBS
17       IEBS  010382941   LI ADMINISTRACION DE NEGOCIOS      COURIEBS
926  COURSERA  010314075  MAE ADMIN NEGOCIOS IEBS EJECUT  COUREJECIEBS
927  COURSERA  010382941   LI ADMINISTRACION DE NEGOCIOS      COURIEBS

data[(data["etiqueta"].str.contains("UNIC")) & \
    (data["etiqueta"].str.contains("IEBS"))]\
    [['alsh', 'username', 'progmdesc', 'etiqueta']]
    alsh   username                       progmdesc      etiqueta
13  IEBS  010413436  LIC EN CONTADURIA PUBLICA EJEC  UNICEJECIEBS
14  IEBS  010412175     LICEN PEDAGOGIA-UNICEF EJEC  UNICEJECIEBS
15  IEBS  010400894  LIC CIENC POLIT Y ADM PUB EJEC  UNICEJECIEBS
16  IEBS  010375025  LIC INGENIERIA INDUSTRIAL EJEC  UNICEJECIEBS
... FALTAN LOS 4 UNIC-IEBS

data[(data["etiqueta"].str.contains("GADS")) & \
    (data["etiqueta"].str.contains("IEBS"))]\
    [['alsh', 'username', 'progmdesc', 'etiqueta']]
...

# -- BEG: NO SIRVE
data2 = data[:]
data2['alsh2'] = data2['alsh']
a = data2.groupby(["alsh", "alsh2"], sort = False)\
    .count()["username"]
a = a.to_frame()
a.reset_index(inplace = True)
data2.pivot_table('username', 'alsh', 'alsh2')

pd.crosstab(data2['alsh'], data2['alsh'])
data2.pivot_table('username', 'alsh', 'alsh2')

a = data.groupby(['username', 'alsh']).count()['progmdesc']
a = a.to_frame()
a.reset_index(inplace = True)
a = a.pivot_table('progmdesc', 'username', 'alsh')
# 4843 rows
a['tot'] = a.sum(axis = 1)
a.sort_values(by="tot", ascending=False)
alsh       CIFAL  COURSERA   FB  GOOGLE ADS  IEBS  ONU  UNICEF  tot
username                                                           
010314075    NaN       1.0  NaN         NaN   1.0  NaN     NaN  2.0
010382941    NaN       1.0  NaN         NaN   1.0  NaN     NaN  2.0
010386979    NaN       1.0  NaN         NaN   NaN  NaN     1.0  2.0
010407125    NaN       NaN  NaN         1.0   1.0  NaN     NaN  2.0

columnas = ["CIFAL", "COURSERA", "FB", "GOOGLE ADS", "IEBS", "ONU", \
    "UNICEF"]
b = pd.DataFrame(columns = columnas)
for col_name in b.columns:
    tmpList = []
    Serie = a[col_name]
    print(Serie)
    for item in Serie:
        print(item)
        if math.isnan(item):
            tmpList.append(None)
        else:
            tmpList.append(col_name)
    b[col_name] = tmpList

# Factorize (pero no sirve de mucho)
# b.apply(lambda x : pd.factorize(x)[0]).corr(method='pearson', min_periods=1)

rows = b.shape[0]
cols = b.shape[1]
for col1 in range(cols - 1):
    tmpList = []
    Serie1 = b.iloc[:, col1]
    print("Serie1\n", Serie1)
    for col2 in range((col1 + 1), cols):
        Serie2 = b.iloc[:, col2]
        #tmpList.append()
        print("Serie2\n", Serie2)
        for row in range(rows):
        #Serie2 = b.iloc[:, col]
        #tmpList.append()

c = [b.groupby(x, as_index=False).count() for x in columnas]
[   CIFAL  COURSERA  FB  GOOGLE ADS  IEBS  ONU  UNICEF
 0  CIFAL         0   0           0     0    0       0,
    COURSERA  CIFAL  FB  GOOGLE ADS  IEBS  ONU  UNICEF
 0  COURSERA      0   0           0     2    0       1,
    FB  CIFAL  COURSERA  GOOGLE ADS  IEBS  ONU  UNICEF
 0  FB      0         0           3     3    0       1,
...
# -- END: NO SIRVE (pero sirvió como exploración para lo que sí sirve)

columnas = ["CIFAL", "COURSERA", "FB", "GOOGLE ADS", "IEBS", "ONU", \
    "UNICEF"]
a = data.groupby(['username', 'alsh']).count()['progmdesc']
a = a.to_frame()
a.reset_index(inplace = True)
a = a.pivot_table('progmdesc', 'username', 'alsh')
# 4843 rows
'''
alsh       CIFAL  COURSERA  FB  GOOGLE ADS  IEBS  ONU  UNICEF
username                                                     
010000573    NaN       NaN NaN         NaN   NaN  NaN     1.0
010001001    NaN       1.0 NaN         NaN   NaN  NaN     NaN
010001876    NaN       NaN NaN         NaN   NaN  NaN     1.0
010002966    NaN       1.0 NaN         NaN   NaN  NaN     NaN
010003209    NaN       NaN NaN         NaN   NaN  NaN     1.0
...          ...       ...  ..         ...   ...  ...     ...
'''
b = pd.concat([a.groupby(x, as_index=False).count() for x in columnas])
b = b.fillna(0).astype(int)
b.index = b.columns
'''
alsh        CIFAL  COURSERA  FB  GOOGLE ADS  IEBS  ONU  UNICEF
alsh                                                          
CIFAL           1         0   0           0     0    0       0
COURSERA        0         1   0           0     2    0       1
FB              0         0   1           3     3    0       1
GOOGLE ADS      0         0   3           1     4    0       0
IEBS            0         2   3           4     1    0       0
ONU             0         0   0           0     0    1       0
UNICEF          0         1   1           0     0    0       1
'''
diag = a.sum() - (b.sum() - 1)
alsh
'''
CIFAL            1.0
COURSERA       926.0
FB               0.0
GOOGLE ADS       2.0
IEBS            16.0
ONU            217.0
UNICEF        3667.0
'''
for col_name in columnas:
    b.loc[col_name, col_name] = diag.loc[col_name]
'''
alsh        CIFAL  COURSERA  FB  GOOGLE ADS  IEBS  ONU  UNICEF
alsh                                                          
CIFAL           1         0   0           0     0    0       0
COURSERA        0       926   0           0     2    0       1
FB              0         0   0           3     3    0       1
GOOGLE ADS      0         0   3           2     4    0       0
IEBS            0         2   3           4    16    0       0
ONU             0         0   0           0     0  217       0
UNICEF          0         1   1           0     0    0    3667
'''




data["nivel"].value_counts()
Out[14]: 
LI    3281
MA    1415
MS     161

data.groupby(["nivel", "alianza"]).count()["username"]
nivel  alianza     
LI     COUR             785
       COUREJEC          39
       COURIEBS           2
       COURUNIC           2
       EJECCIFA           1
       EJECIEBS           4
       FCBKEJECIEBS       6
       GADSEJECIEBS       8
       GADSFCBKEJEC       6
       IEBS               1
       MUBAEJECIEBS       3
       SENICOUR           5
       UNIC            2282
       UNICEJEC         130
       UNICEJECIEBS       4
       UNICFCBKEJEC       2
       UNICMUBAEJEC       1
MA     COUR              62
       COUREJEC          28
       COUREJECIEBS       2
       EJECIEBS           4
       GADSEJEC           2
       MONU             207
       SENICOUR           1
       UNIC             810
       UNICEJEC         299
MS     COUR               6
       MONU              10
       UNIC             114
       UNICEJEC          31

data.groupby(["nivel", "alsh"]).count()["username"]
LI     CIFAL            1
       COURSERA       831
       FB               7
       GOOGLE_ADS       7
       IEBS            20
       UNICEF        2415
MA     COURSERA        92
       GOOGLE_ADS       2
       IEBS             5
       ONU            207
       UNICEF        1109
MS     COURSERA         6
       ONU             10
       UNICEF         145

data.groupby(["nivel", "carreraid", "carreradesc"]).count()["username"]
nivel  carreraid  carreradesc                   
LI     AA         LICENCIATURA ADMINISTRACION         32
       AF         LIC ADMINISTRACION Y FINANZAS       35
       AN         LI ADMINISTRACION DE NEGOCIOS       27
       AR         LI ADMINISTRACION REC HUMANOS       17
       AT         LI ADMINISTRACION TEC DE INFO       14
...
# -----------END - bloque exploración



# TABLA Alianzas cruzadas
columnas = ["CIFAL", "COURSERA", "FB", "GOOGLE ADS", "IEBS", "ONU", \
    "UNICEF"]
a = data.groupby(['username', 'alsh']).count()['progmdesc']
a = a.to_frame()
a.reset_index(inplace = True)
a = a.pivot_table('progmdesc', 'username', 'alsh')
# 4843 rows
'''
alsh       CIFAL  COURSERA  FB  GOOGLE ADS  IEBS  ONU  UNICEF
username                                                     
010000573    NaN       NaN NaN         NaN   NaN  NaN     1.0
010001001    NaN       1.0 NaN         NaN   NaN  NaN     NaN
010001876    NaN       NaN NaN         NaN   NaN  NaN     1.0
010002966    NaN       1.0 NaN         NaN   NaN  NaN     NaN
010003209    NaN       NaN NaN         NaN   NaN  NaN     1.0
...          ...       ...  ..         ...   ...  ...     ...
'''
b = pd.concat([a.groupby(x, as_index=False).count() for x in columnas])
b = b.fillna(0).astype(int)
b.index = columnas
'''
alsh        CIFAL  COURSERA  FB  GOOGLE ADS  IEBS  ONU  UNICEF
alsh                                                          
CIFAL           1         0   0           0     0    0       0
COURSERA        0         1   0           0     2    0       1
FB              0         0   1           3     3    0       1
GOOGLE ADS      0         0   3           1     4    0       0
IEBS            0         2   3           4     1    0       0
ONU             0         0   0           0     0    1       0
UNICEF          0         1   1           0     0    0       1
'''
diag = a.sum() - (b.sum() - 1)
'''
alsh
CIFAL            1.0
COURSERA       926.0
FB               0.0
GOOGLE ADS       2.0
IEBS            16.0
ONU            217.0
UNICEF        3667.0
'''
for col_name in columnas:
    b.loc[col_name, col_name] = diag.loc[col_name]
'''
alsh        CIFAL  COURSERA  FB  GOOGLE ADS  IEBS  ONU  UNICEF
alsh                                                          
CIFAL           1         0   0           0     0    0       0
COURSERA        0       926   0           0     2    0       1
FB              0         0   0           3     3    0       1
GOOGLE ADS      0         0   3           2     4    0       0
IEBS            0         2   3           4    16    0       0
ONU             0         0   0           0     0  217       0
UNICEF          0         1   1           0     0    0    3667
'''
# Acomodamos para exportar:
b.reset_index(inplace = True)
columnas2 = (["ALIANZA"] + columnas)
b.columns = columnas2
b.to_csv(PATHP + "res/07_tablacruz.csv", index = False)


# Estandarización y limpieza del campo 'progmdesc'
# Algoritmo p' limpiar y desmenuzar el archivo y obtener infop de carrer
# y relacionar 1. la info de carreras limpia y desmenuzada y 2. alianzas
# 1. tokenize
# 2. eliminate stop words
# 3. lemmatize automatico (a ver que sale, si no, manual)

# Explode "-"
# IN: ['LICEN PEDAGOGIA-UNICEF'], ['LICEN PEDAGOGIA UNICEF'],
# INTERMED:  ['LICEN PEDAGOGIA', 'UNICEF'], ['LICEN PEDAGOGIA UNICEF'],
# OUT:  ['LICEN PEDAGOGIA UNICEF'], ['LICEN PEDAGOGIA UNICEF'],
lista_exploded = []
for sentence in data['progmdesc']:
    exploded = sentence.split("-")
    exploded = " ".join(exploded) # Hacemos el join de nuevo
    lista_exploded.append(exploded)

# Tokenize [OK, pero cambiamos]
'''
# IN Series w/each line: 'It is a great learning management software.'
# OUT ['It','is','a','great','learning','management', 'software', '.']
tokn_sntnce = []
for sentence in data['carreradesc']:
    tokenized = nltk.word_tokenize(sentence)
    tokn_sntnce.append(tokenized)
    #OK print(sentence, tokenized)
'''
# Tokenize (a aplicar después de explode, sólo cambia INPUT)
# IN Series w/each line: 'It is a great learning management software.'
# OUT ['It','is','a','great','learning','management', 'software', '.']
tokn_sntnce = []
for sentence in lista_exploded:
    tokenized = nltk.word_tokenize(sentence)
    tokn_sntnce.append(tokenized)
    #OK print(sentence, tokenized)

# Remove stop words
# IN [..., ['It','is','a','great','learning','management', '.']]]
# OUT [..., ['great', 'learning', 'management', '.']]
stop_words_sp = set(stopwords.words('spanish'))
# STOPWORDS manuales
extra_words = {"p", "b", "d"} # set
# la unión de las dos:
stop_words_all = stop_words_sp.union(extra_words)
#OK print(stop_words)
list_filtered = []
for sentence in tokn_sntnce:
    words_filtered = []
    for palabra in sentence:
        palabra_lower = palabra.lower()
        if palabra_lower not in stop_words_all:
            words_filtered.append(palabra_lower)
    list_filtered.append(words_filtered)

# -----------BEG - bloque exploración para stemming
pal = pd.DataFrame(list_filtered)
pd.DataFrame(list_filtered)
Out[25]: 
                 0          1          2          3       4     5     6
0     licenciatura    derecho       None       None    None  None  None
1               li      admin   negocios       iebs    ejec  None  None
2              mae      admin   negocios       iebs  ejecut  None  None
3              mae      admin   negocios       iebs  ejecut  None  None
...

da = pd.DataFrame(data[['progsh', 'nivel']]).reset_index(drop = True)
pal = pd.concat([da, pal], axis = 1)
del da

# Revisamos la primera columna, pero esta se va a quitar y después
# ...se va a sustitir por el nivel. Esta se queda aquí como REFERENCIA
pal[0].value_counts().reset_index().sort_values(by = 'index')
Out[28]: 
           index     0
17             l     1
7             li    68
2            lic   369
4           lice   181
0          licen  2468
16        licenc     1
8        licenci    34
6   licenciatura   143
9          llcen    16
13            ma     7
3            mae   272
1           maes  1109
10         maest    15
15        maestr     1
11      maestria    11
12          mast    10
5         master   147
14          mstr     4

pal['nivel'].value_counts()
Out[54]: 
LI    3281
MA    1415
MS     161

# Revisamos correspondencias entre nivel y col 0
pal[pal['nivel'] == "MA"][0].value_counts()
maes        1109
mae          272
maest         15
maestria      11
ma             7
maestr         1

pal[pal['nivel'] == "MS"][0].value_counts()
master    147
mast       10
mstr        4


# Tiramos columna 0 y se usará nivel
pal.drop(0, axis = 1, inplace = True)

pal[1].value_counts().reset_index().sort_values(by = 'index')
16           admin    16
19       administr    10
41      administra     1
43    administraci     1
2   administracion   350
39          admins     1
14           admon    24
25           cienc     4
18          cienci    10
28         ciencia     3
31        ciencias     2
27          coachi     3
33        coaching     2
29        comercio     3
15    comunicacion    22
23           conci     4
24      conciencia     4
7       contaduria    81
10       criminolo    48
38     criminologi     1
22            dere     5
8          derecho    67
17         desarro    10
36            dire     1
34           direc     2
35          direcc     2
26       direccion     4
1              edu  1104
4             educ   114
11           educa    31
20       educacion     8
12             ges    27
42          gestio     1
37         gestion     1
3              ing   202
32          ingeni     2
40        ingenier     1
6       ingenieria    82
21           merca     6
30          mercad     3
13   mercadotecnia    26
9         negocios    51
0        pedagogia  2435
5       psicologia    82

pal[2].value_counts().reset_index().sort_values(by = 'index')
39           comput     2
11        criminali    48
48       criminalis     1
29            datos     5
23              dig     9
24          digital     9
27              dir     8
14            direc    20
1               doc   552
2        doc-unicef   552
7              doce   114
13            docen    31
26         docencia     8
5              ejec   132
17        ejecutivo    15
16          empresa    16
45      empresarial     1
9          finanzas    81
28          industr     7
6        industrial   123
46            ingen     1
40           ingeni     2
47           instit     1
52         instituc     1
49       institucio     1
33          integra     3
34         integral     2
31         internac     4
20    internacional    12
12  internacionales    47
43        mercadote     1
51          negocio     1
10         negocios    51
44        organizac     1
36       organizaci     2
8    organizacional    81
25            plena     8
41            polit     2
21          politic    10
32              pro     3
35            proce     2
38           proyec     2
3           publica   251
15              rec    17
37            recur     2
4              sist   154
22         sustenta    10
19              tec    14
42            tecno     1
30           tecnol     5
50          tecnolo     1
0            unicef  2404
18           ventas    15

pal[3].value_counts().reset_index().sort_values(by = 'index')
32            adm    2
12          admin    7
4           admon   51
38          ambie    1
30      ambiental    2
16           apli    4
15       aplicada    4
13           come    6
21          comer    3
8       computaci   14
3   computacional  140
35      deportivo    1
11        ecoturi   10
37           educ    1
31          educa    2
1            ejec  312
41        ejecuti    1
14       ejecutiv    4
19      ejecutivo    3
34         estrat    1
27          human    2
6         humanos   17
10           iebs   10
9            info   14
18         inform    3
36      informaci    1
22          innov    2
5            inst   28
17             ju    3
24            jui    2
39           nego    1
23          negoc    2
29         negoci    2
2             onu  205
20        organiz    3
25       organiza    2
33       positiva    1
28          softw    2
40       software    1
26       telecomu    2
7         turisti   16
0          unicef 1249

pal[4].value_counts().reset_index().sort_values(by = 'index')
1     eje  31
0    ejec  32
3  ejecut  13
6    elec   6
7   elect   3
9     ora   2
8    oral   3
4     pub  12
5     sal   8
2   salud  20

pal2[5].value_counts().reset_index().sort_values(by = 'index')
0  ejec  18


# Pruebas de stemming a mano:
primer posición: se borra y se toma el nivel del campo 'nivel'
segunda posición

admon
-----
17             admin    16
18         administr    10
42        administra     1
44      administraci     1
3     administracion   350
40            admins     1
15             admon    24

patt = re.compile('^adm[io]*n*')
e = ["admin", "administr", "administra", "admins", "adm", "admen", \
    "admon", "admmn", "admn", "hi"] # <- todos, ok, flexible
[patt.match(x) for x in e]
[re.sub(patt, "admon", x) for x in e] # npo funciona

tempList = []
for x in e:
    if patt.match(x):
        tempList.append("admon")
    else:
        tempList.append(x)

ciencia
-------
25             cienc     4
20            cienci    10
29           ciencia     3
32          ciencias     2
patt = re.compile('^cienc')
e = ["cienc", "cienci", "ciencia", "ciencias", "cencia"]
[patt.match(x) for x in e]

patterns = \
    (
        ('^adm[io]*n*', ),
        ('^cienc', , )
    )


31            coachi     3
36          coaching     2
patt = re.compile('^coach')
e = ["coach", "coachi", "ciencia", "ciencias", "cencia"]
[patt.match(x) for x in e]

8         contaduria    81
--------------------------
patt = re.compile('^contad*')
e = ["conta", "contad", "contaduria", "ciencias", "cencia"]
[patt.match(x) for x in e]

#---

# OK

patterns = (
    ('^adm[io]*n*', "admon"),
    ('^cien', "ciencia"),
    ('^coach', "coaching")
)

def buildMatchAndApplyFunctions(pattern, replace):
    def matchFunction(word):
        return re.search(pattern, word)
    def applyFunction(word):
        return replace
    return (matchFunction, applyFunction)

rules = []
for (pattern, replace) in patterns:
    print("hola rules", pattern, replace)
    rules.append(buildMatchAndApplyFunctions(pattern, replace))

#OK
def plural(noun):
    contador = 0
    for matchesRule, applyRule in rules:
        contador += 1
        #print("hola", matchesRule, applyRule)
        print("hola plural", contador, matchesRule(noun))
        print("hola plural", contador, matchesRule(noun))
        print("hola plural", contador, matchesRule(noun))
        print("hola plural", contador, matchesRule(noun))
        if matchesRule(noun):
            print("match")
            return applyRule(noun)
    print("no match")
    return (noun)

# -----------END - bloque exploración para stemming


# En limpio
patterns = (
    ('^adm[io]*n*', "admon"),
    ('^ambie', "ambiental"),
    ('^apli', "aplicada"),
    ('^cien', "ciencia"),
    ('^coach', "coaching"),
    ('^come', "comercio"),
    ('^compu', "computaci"),
    ('^conci', "conciencia"),
    ('^crimina', "criminali"),
    ('^crimino', "criminolo"),
    ('^dere', "derecho"),
    ('^desarro', "desarrollo"),
    ('^dig', "digital"),
    ('^dir', "direccion"),
    ('^doc', "docencia"),
    ('^edu', "educacion"),
    ('^eje', "ejec"),
    ('^elec', "electr"),
    ('(^empresa$|^empresas)', "empresas"),
    ('^empresa.', "empresarial"),
    ('^estrat', "estrat"),
    ('^ges', "gestion"),
    ('^human', "humanos"),
    ('^industr', "industrial"),
    ('^info', "informaci"),
    ('^ing', "ing"),
    ('^inst', "instituc"),
    ('^integr', "integral"),
    ('^internac', "internaci"),
    ('^ju', "juici"),
    ('^merca', "mercadotec"),
    ('^nego', "negocios"),
    ('^ora', "oral"),
    ('^organiz', "organizac"),
    ('^pedag', "pedagog"),
    ('^polit', "politic"),
    ('(^pro$|^proc(es)?|^proce?$)', "procesal"),
    ('^psic', "psicolog"),
    ('^pub', "public"),
    ('^rec', "recurs"),
    ('^sal', "salud"),
    ('^softw', "software"),
    ('^tec', "tecnolog"),
    ('^telecom', "telecom"),
    ('^turisti', "turist")
)

def buildMatchAndApplyFunctions(pattern, replace):
    def matchFunction(word):
        return re.search(pattern, word)
    def applyFunction(word):
        return replace
    return (matchFunction, applyFunction)

rules = []
for (pattern, replace) in patterns:
    rules.append(buildMatchAndApplyFunctions(pattern, replace))

def plural(noun):
    for matchesRule, applyRule in rules:
        if matchesRule(noun):
            return applyRule(noun)
    return (noun)

# Transform words with manual stemming
# IN [..., ['great','learning','management', '.']]]
# OUT [..., ['great', 'learn', 'manage', '.']]
list_filtered2 = []
for sentence in list_filtered:
    words_filtered = []
    for palabra in sentence:
        words_filtered.append(plural(palabra))
    list_filtered2.append(words_filtered)


# -----------BEG - bloque exploración para limpieza extra
# si queremos nivel como parte del nombre
for index, sentence in enumerate(list_filtered2):
    sentence[0] = data['nivel'].iloc[index].lower()
# si NO queremos nivel como parte del nombre
for sentence in list_filtered2:
    sentence.pop(0)
# Separamos el ejec
lista_ejec = []
for sentence in list_filtered2:
    if "ejec" in sentence:
        sentence.pop()
        lista_ejec.append("ejec")
    else:
        lista_ejec.append(None)
# -----------END - bloque exploración


# si NO queremos nivel como parte del nombre & Separamos el ejec
# También pegamos y ponemos en lista_limpia
lista_ejec = []
lista_limpia = []
for sentence in list_filtered2:
    sentence.pop(0)
    if "ejec" in sentence:
        sentence.pop()
        lista_ejec.append("ejec")
    else:
        lista_ejec.append(None)
    lista_limpia.append(" ".join(sentence))
data['progmlimpio'] = lista_limpia
data['ejec'] = lista_ejec


# -----------BEG - bloque exploración
data[['carrlimpia', 'carreradesc', 'ejec']]
                     carrlimpia                    carreradesc  ejec
3496  educacion docencia unicef  MAES EN EDU Y DOC-UNICEF EJEC  ejec
3497  educacion docencia unicef  MAES EN EDU Y DOC-UNICEF EJEC  ejec
...

data["carrlimpia"].value_counts().reset_index().sort_values(by = 'index')
                                 index  carrlimpia
14                               admon          32
20               admon empresas turist          16
13                      admon finanzas          35
36            admon instituc educacion           3
43             admon mercadotec estrat           1
...
# -----------END - bloque exploración


# Se leen areas de c/carrera porque ese proceso de asignacion es manual
areas = pd.read_csv(PATHP + 'data/areas.csv',
    header = 0,
    sep = ","
    )
areas["area"] = areas["area"].str.upper()
    
# DATA2 = Copia para RESPALDO de proceso + areas
data2 = pd.merge(data, areas, left_on = ['progmlimpio'],
    right_on = ['progmlimpio'], how = "left"
)
data2['progmlimpio'] = data2['progmlimpio'].str.title()





# -----------BEG - bloque exploración # Frequencies

data2.iloc[0]
username                                   010411136
primer_inscrip           03/01/2022  Periodo  012242
nivel                                             LI
proglong          UTLLIDDFED LICENCIATURA EN DERECHO <- nombre largo
alianza                                         IEBS <- nombre largo
modal                                             OL
alsh                                            IEBS <- nombre corto
date                             2022-01-03 00:00:00
progsh                                    UTLLIDDFED <- nombre corto
escuela                                          UTL
carreraid                                         DD
carreradesc                  LICENCIATURA EN DERECHO <- nombre original
carrlimpia                                   Derecho <- nombre estándar
ejec                                            None
area                                         DERECHO

# -----------END - bloque exploración # Frequencies

# ALIANZAS ***
t1 = data2['alsh'].value_counts()
t1 = t1.to_frame()
t1.reset_index(inplace = True)
t1['percent'] = t1['alsh']/t1['alsh'].sum()
t1.columns = ['ALIANZA', 'CANTIDAD', 'PORCENT']
t1.to_csv(PATHP + "res/01_alianzas.csv", index = False)
'''
      ALIANZA  CANTIDAD   PORCENT
0      UNICEF  3669  0.755405
1    COURSERA   929  0.191270
2         ONU   217  0.044678
3        IEBS    25  0.005147
4  GOOGLE ADS     9  0.001853
5          FB     7  0.001441
6       CIFAL     1  0.000206
'''

# ALIANZAS DETALLE
data2['alianza'].value_counts()
UNIC            3206
COUR             853
UNICEJEC         460
MONU             217
COUREJEC          67
GADSEJECIEBS       8
EJECIEBS           8
FCBKEJECIEBS       6
GADSFCBKEJEC       6
SENICOUR           6
UNICEJECIEBS       4
MUBAEJECIEBS       3
COURIEBS           2
COURUNIC           2
COUREJECIEBS       2
UNICFCBKEJEC       2
GADSEJEC           2
IEBS               1
UNICMUBAEJEC       1
EJECCIFA           1


# ALIANZAS x ALIANZAS DETALLE
dat2 = data2.groupby(["alsh", "alianza"], sort = False)\
    .count()["username"]
dat2 = dat2.to_frame()
dat2
# dat2.reset_index(inplace = True)
alsh       alianza               
IEBS       IEBS                 1
           EJECIEBS             8
           MUBAEJECIEBS         3
           COUREJECIEBS         1
           UNICEJECIEBS         4
           COURIEBS             1
           GADSEJECIEBS         4
           FCBKEJECIEBS         3
COURSERA   COUR               853
           SENICOUR             6
           COUREJEC            67
           COUREJECIEBS         1
           COURIEBS             1
           COURUNIC             1
UNICEF     UNIC              3206
           UNICEJEC           460
           COURUNIC             1
           UNICFCBKEJEC         1
           UNICMUBAEJEC         1
ONU        MONU               217
GOOGLE ADS GADSEJECIEBS         4
           GADSFCBKEJEC         3
           GADSEJEC             2
FB         UNICFCBKEJEC         1
           GADSFCBKEJEC         3
           FCBKEJECIEBS         3
CIFAL      EJECCIFA             1


# NIVEL
data["nivel"].value_counts()
Out[14]: 
LI    3281
MA    1415
MS     161


# ALIANZAS DETALLE x NIVEL
data2.groupby(["nivel", "alianza"]).count()["username"]
nivel  alianza     
LI     COUR             785
       COUREJEC          39
       COURIEBS           2
       COURUNIC           2
       EJECCIFA           1
       EJECIEBS           4
       FCBKEJECIEBS       6
       GADSEJECIEBS       8
       GADSFCBKEJEC       6
       IEBS               1
       MUBAEJECIEBS       3
       SENICOUR           5
       UNIC            2282
       UNICEJEC         130
       UNICEJECIEBS       4
       UNICFCBKEJEC       2
       UNICMUBAEJEC       1
MA     COUR              62
       COUREJEC          28
       COUREJECIEBS       2
       EJECIEBS           4
       GADSEJEC           2
       MONU             207
       SENICOUR           1
       UNIC             810
       UNICEJEC         299
MS     COUR               6
       MONU              10
       UNIC             114
       UNICEJEC          31


# ALIANZAS x NIVEL
data2.groupby(["nivel", "alsh"]).count()["username"]
LI     CIFAL            1
       COURSERA       831
       FB               7
       GOOGLE_ADS       7
       IEBS            20
       UNICEF        2415
MA     COURSERA        92
       GOOGLE_ADS       2
       IEBS             5
       ONU            207
       UNICEF        1109
MS     COURSERA         6
       ONU             10
       UNICEF         145


# AREA x ALIANZAS ***
a = data2.groupby(["area", "alsh"]).count()["username"]
a = a.to_frame()
a.reset_index(inplace = True)
'''
              area        alsh  username
0            ADMON    COURSERA       156
1            ADMON  GOOGLE ADS         1
2            ADMON        IEBS        11
3            ADMON         ONU       214
4            ADMON      UNICEF         3
5         AMBIENTE    COURSERA        10
6            COACH    COURSERA         5
'''
# Borramos valores repetidos en la columna ÁREA:
tmpList = []
user1 = a['area'].iloc[0]
#user2 = ara2['username'].iloc[1]
#fecha2 = ara2['fechahora'].iloc[1]
tmpList.append(user1)
for index in range(1, len(a)):
#for index in range(1, 43):
    user2 = a['area'].iloc[index]
    print("\nEntra for", index)
    print("user1:", user1, "user2:", user2)
    if (user2 != user1):
        tmpList.append(user2)
    else:
        tmpList.append(None)
    user1 = user2

# La hacemnos función
# IN: lista con valores repetidos (ORDENADOS)
# OUT: lista con valores repetidos eliminados (IGUAL ORDENADOS) con None
def limpia_reps(lista):
    tmpList = []
    user1 = lista.iloc[0]
    #user2 = ara2['username'].iloc[1]
    #fecha2 = ara2['fechahora'].iloc[1]
    tmpList.append(user1)
    for index in range(1, len(lista)):
    #for index in range(1, 43):
        user2 = lista.iloc[index]
        #ok: print("\nEntra for", index)
        #ok: print("user1:", user1, "user2:", user2)
        if (user2 != user1):
            tmpList.append(user2)
        else:
            tmpList.append(None)
        user1 = user2
    return tmpList
    
a['area'] = limpia_reps(a['area'])
'''
area            alsh      
ADMON           COURSERA       156
                GOOGLE ADS       1
                IEBS            11
                ONU            214
                UNICEF           3
AMBIENTE        COURSERA        10
COACH           COURSERA         5
COMERCIO        COURSERA         3
...
'''
a.columns = ['AREA', 'ALIANZA', 'CANTIDAD']
a.to_csv(PATHP + "res/02_alianzas_area.csv", index = False)


# AREA x ALIANZAS x NIVEL - TABLA PLANA
data2.groupby(['nivel', "area", "alsh"]).count()["username"]
nivel  area            alsh      
LI     ADMON           COURSERA       135
                       GOOGLE ADS       1
                       IEBS             6
                       UNICEF           3
       AMBIENTE        COURSERA        10
       COMUNICACION    COURSERA        22
       CONTA           COURSERA        79
                       IEBS             1
                       UNICEF           1
       CRIMINOL        CIFAL            1
...


# AREA x ALIANZAS x NIVEL*** PIVOTE
a = data2.groupby(['nivel', "area", "alsh"]).count()["username"]
a = a.to_frame()
a.reset_index(inplace = True)
a = a.pivot_table('username', ['area', 'alsh'], 'nivel')
'''
nivel                          LI      MA     MS
area           alsh                             
ADMON          COURSERA     135.0    18.0    3.0
               GOOGLE ADS     1.0     NaN    NaN
               IEBS           6.0     5.0    NaN
               ONU            NaN   204.0   10.0
               UNICEF         3.0     NaN    NaN
AMBIENTE       COURSERA      10.0     NaN    NaN
...
'''
a.reset_index(inplace = True)
a['area'] = limpia_reps(a['area'])
a.columns = ['AREA', 'ALIANZA', 'LIC', 'MAE', 'MAS']
a.to_csv(PATHP + "res/03_alian_area_nivel.csv", index = False)



# CARRERA  ***
a = data2.groupby('progmlimpio').count()['username'].\
    sort_values(ascending = False)
a = a.to_frame()
a.reset_index(inplace = True)
a.columns = ['PROGRAMA', 'CANTIDAD']
a.to_csv(PATHP + "res/t4.csv", index = False)


# CARRERA x ALIANZA ***
a = data2.groupby(["progmlimpio", "alsh"]).count()["username"]
carrlimpia                          alsh      
Admon                               COURSERA        31
                                    UNICEF           1
Admon Empresas Turist               COURSERA        16
Admon Finanzas                      COURSERA        35
Admon Instituc Educacion            COURSERA         2
                                    ONU              1
Admon Mercadotec Estrat             COURSERA         1
Admon Negocios                      COURSERA        34
...
a.to_csv(PATHP + "res/t5.csv", index = True)
# SE copia a mano y se modifica a mano


# CARRERA x ALIANZA X NIVEL - TABLA PLANA
data2.groupby(['nivel', "progmlimpio", "alsh"]).count()["username"]
nivel  carrlimpia                          alsh      
LI     Admon                               COURSERA        31
                                           UNICEF           1
       Admon Empresas Turist               COURSERA        16
       Admon Finanzas                      COURSERA        35
       Admon Negocios                      COURSERA        25
                                           GOOGLE ADS       1
                                           IEBS             2
                                           UNICEF           2
       Admon Negocios Iebs                 IEBS             4
...


# CARRERA x ALIANZA X NIVEL*** - TABLA PIVOTE
a = data2.groupby(['nivel', "progmlimpio", "alsh"]).count()["username"]
a = a.to_frame()
a.reset_index(inplace = True)
a.pivot_table('username', ['progmlimpio', 'alsh'], 'nivel')
nivel                                              LI      MA     MS
carrlimpia                         alsh                             
Admon                              COURSERA      31.0     NaN    NaN
                                   UNICEF         1.0     NaN    NaN
Admon Empresas Turist              COURSERA      16.0     NaN    NaN
Admon Finanzas                     COURSERA      35.0     NaN    NaN
Admon Instituc Educacion           COURSERA       NaN     1.0    1.0
                                   ONU            NaN     1.0    NaN
...

# SE MODIFICA A MANO t6 (se convierte en tabla plana con sólo un header)






# Para tabla pivote usar:  'nivel', "area", 'carrlimpia', "alsh"
data3 = data2[['nivel', "area", 'carrlimpia', "alsh", 'alianza']]
data3.to_csv(PATHP + "res/data3.csv", index = False)
