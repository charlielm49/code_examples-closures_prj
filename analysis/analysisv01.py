#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Manual imports
#import csv
import datetime
#import math
#import matplotlib.pyplot as plt
#import numpy as np
import openpyxl
import pandas as pd
#import pprint
#import pymysql.cursors
#import re
#import seaborn as sns
#import statsmodels.api as sm
#import sys

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
    'nivel', 'proglong', 'alianza', 'modal', 'alsh', 'date']

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
data['carreraid'] = tempList3
data['carreradesc'] = tempList4

# -----------BEG - bloque exploración # Frequencies
data['alsh'].value_counts()

UNICEF        3669
COURSERA       929
ONU            217
IEBS            25
GOOGLE_ADS       9
FB               7
CIFAL            1

data['alianza'].value_counts()

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

dat2 = data.groupby(["alsh", "alianza"], sort = False)\
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



names = pd.read_csv(PATHP + 'data/names2.csv',
    header = 0,
    sep = ","
    )
nivel,descmia,ejec,desclongori,area,carrid,carridori
LI,ADMON,,LICENCIATURA ADMINISTRACION,ADMON,AA,AA
LI,ADMON EMPRESA TURISTI,,LlCEN ADMON DE EMPRESA TURISTI,ADMON,TU,TU
LI,ADMON FINANZAS,,LIC ADMINISTRACION Y FINANZAS,ADMON,AF,AF
MA,ADMON INSTITUC EDUCA,,MA ADMINISTRACI INSTITUC EDUCA,ADMON,AI,AI

antes de merge:
1. desduplicar names por:  nivel, descmia, ejec

names.drop_duplicates(['nivel', 'descmia', 'ejec'], inplace = True)

2. hacer variable qu eservirá como ID de la materia: desclongmia
comparar con el id original formado por 1. nivle 2. carrid
compoarar a ver si coincide, si no, usar el mio

PEND

data2 = pd.merge(data, names, left_on = ['carreradesc'],
right_on = ['desclongori'], how = "left"
)



data4.groupby(["area", "alsh"]).count()["username"]


data4.groupby(["descmia", "alsh"]).count()["username"]


