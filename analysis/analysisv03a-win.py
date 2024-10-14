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
PATHP = "D:/48-2022FEB11-recom_prods/"
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

# READ from CSV FILE
data = pd.read_csv(PATHP + 'data/data1.csv',
    header = 0,
    sep = ",",
    dtype={'username': object}
)
len(data)
#Out[224]: 8894
data.drop(['primer_inscrip'], axis = 1, inplace = True)

# eliminate those with alphanumeric chars
data = data[[x.isnumeric() for x in data['username']]]
# eliminate teachers
data = data[~(data['username'].str.contains("^0198"))]
len(data)
# 8894
len(data.username.unique())
# 7818
#DIF = 14

#Process to clean date column:
tempList = []
for fecha in data['fecha']:
    if "-" in fecha:
        nva_fecha = fecha[5:7] + "/" + fecha[8:10] + "/" + fecha[2:4]
    else:
        nva_fecha = fecha
    tempList.append(nva_fecha)
data['fecha'] = tempList
data['fecha'] = pd.to_datetime(data['fecha'], format = '%d/%m/%y')

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




# TABLA Alianzas cruzadas
columnas = ["CIFAL", "COURSERA", "FB", "GOOGLE ADS", "IEBS", "ONU", \
    "UNICEF"]
a = data.groupby(['username', 'alsh']).count()['progmdesc']
a = a.to_frame()
a.reset_index(inplace = True)
a = a.pivot_table('username', 'username', 'alsh')
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
# Algoritmo p' limpiar y desmenuzar el archivo y obtener info de carrer
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

'''
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
'''

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

# AREA x ALIANZAS ***
a = data2.groupby(["area", "alsh"]).count()["username"]
'''
area            alsh      
ADMON           COURSERA       156
                GOOGLE ADS       1
                IEBS            11
                ONU            214
                UNICEF           3
AMBIENTE        COURSERA        10

'''

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

a = a.to_frame()
a.reset_index(inplace = True)
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



# PROGRAMAS (carreras)  ***
a = data2.groupby('progmlimpio').count()['username'].\
    sort_values(ascending = False)
a = a.to_frame()
a.reset_index(inplace = True)
a.columns = ['PROGRAMA', 'CANTIDAD']
a.to_csv(PATHP + "res/04_progs.csv", index = False)
# TOP 10
a[:10].to_csv(PATHP + "res/04_progs-top.csv", index = False)


# PROGRAMA x ALIANZA ***
a = data2.groupby(["progmlimpio", "alsh"]).count()["username"]
'''
progmlimpio                          alsh      
Admon                               COURSERA        31
                                    UNICEF           1
Admon Empresas Turist               COURSERA        16
Admon Finanzas                      COURSERA        35
Admon Instituc Educacion            COURSERA         2
                                    ONU              1
Admon Mercadotec Estrat             COURSERA         1
Admon Negocios                      COURSERA        34
...
'''
a = a.to_frame()
a.reset_index(inplace = True)
a['progmlimpio'] = limpia_reps(a['progmlimpio'])
a.columns = ['PROGRAMA', 'ALIANZA', 'CANTIDAD']
a.to_csv(PATHP + "res/05_progs_alianza.csv", index = False)


# PROGRAMA x ALIANZA X NIVEL*** - TABLA PIVOTE
a = data2.groupby(['nivel', "progmlimpio", "alsh"]).count()["username"]
a = a.to_frame()
a.reset_index(inplace = True)
a = a.pivot_table('username', ['progmlimpio', 'alsh'], 'nivel')
'''
nivel                                              LI      MA     MS
progmlimpio                         alsh                             
Admon                              COURSERA      31.0     NaN    NaN
                                   UNICEF         1.0     NaN    NaN
Admon Empresas Turist              COURSERA      16.0     NaN    NaN
Admon Finanzas                     COURSERA      35.0     NaN    NaN
Admon Instituc Educacion           COURSERA       NaN     1.0    1.0
                                   ONU            NaN     1.0    NaN
...
'''
# SE MODIFICA A MANO t6 (se convierte en tabla plana con sólo un header
a.reset_index(inplace = True)
a['progmlimpio'] = limpia_reps(a['progmlimpio'])
a.columns = ['PROGRAMA', 'ALIANZA', 'LIC', 'MAE', 'MAS']
a.to_csv(PATHP + "res/06_prog_alian_nivel.csv", index = False)





# Para tabla pivote usar:  'nivel', "area", 'progmlimpio', "alsh"
data3 = data2[['nivel', "area", 'progmlimpio', "alsh", 'etiqueta']]
data3.columns = ['NIVEL', 'AREA', 'PROGRAMA', 'ALIANZA', 'ETIQUETA']
data3.to_csv(PATHP + "res/data3.csv", index = False)
