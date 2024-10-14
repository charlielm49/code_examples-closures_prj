#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Manual imports
#import csv
import datetime
#import math
#import matplotlib.pyplot as plt
#import nltk
import numpy as np
import openpyxl
import pandas as pd
#import pprint
#import pymysql.cursors
#import re
#import seaborn as sns
#import statsmodels.api as sm
import subprocess
#import sys

# Manual imports
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
from plotly.subplots import make_subplots
import plotly.graph_objects as go
#from nltk.corpus import stopwords

#stop_words_sp = set(stopwords.words('spanish'))

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
#PATHP = "/home/admin/rec/"
PATHP = "/media/clm/" + USB + "/" + \
    "48-2022FEB11-recom_prods/"
#PATHBIN = "/home/admin/bin/miniconda3/envs/work/bin/"
PATHBIN = "/home/clm/bin/miniconda3/envs/work/bin/"
#_______________________________________________________________________
#_______________________________________________________________________

# CONFIGURATION

# To display more rows in the shell:

#pd.set_option('display.max_rows', 500)
#pd.set_option('display.max_columns', 500)

#_______________________________________________________________________
#_______________________________________________________________________

# FILE READING



st.set_page_config(page_title="Análisis Alianzas", layout="wide")
st.title("Tablas y gráficas análisis alianzas")


upload = st.file_uploader("SUBIR ARCHIVO PARA ACTUALIZACIÓN")
if upload is not None:
    archList = ["IEBS", "COURSERA", "UNICEF", "ONU", "GOOGLE ADS", "FB", \
    "CIFAL"]
    tmpList = []
    for archivo in archList:
        print("ciclo for:", archivo)
        arcDF = pd.read_excel(upload,
            header = 0,
            usecols = ['MATRICULA', 'FECHA_ESTATUS', 'PRIMER_INSCRIPCION',\
            'NIVEL', 'PROGRAMA', 'ALIANZA', 'MODALIDAD'],
            sheet_name = archivo
        )
        arcDF['ALSH'] = archivo
        print(arcDF.head())
        tmpList.append(arcDF)
    data = pd.concat(tmpList)
    print("todos concat ANTES de:\n", data)
    # No funciona el object con matrícula porque viene como int de source
    #, y se tiene que hacer conversion a str explicit
    data["MATRICULA"] = data["MATRICULA"].astype(str).str.zfill(9)
    # Convert from excel date to python date
    data['date'] = pd.to_datetime(data['FECHA_ESTATUS'], unit='D', \
        origin='1899-12-30')
    data.drop('FECHA_ESTATUS', axis = 1, inplace = True)
    data.columns = ['username', 'primer_inscrip', \
        'nivel', 'proglong', 'etiqueta', 'modal', 'alsh', 'date']
    print("todos concat DESPUES:\n", data)
    # Guardamos archivo
    data.to_csv(PATHP + "data/data1.csv", index = False)
    # Ejecutamos proceso de archivo
    subprocess.call(PATHBIN+"python "+PATHP+"analysis/analysisv03a.py", \
        shell = True)


# --------------------------BEG - BLOQUE 1------------------------------

fig = make_subplots(rows = 1, cols = 2,
    subplot_titles = (
        "Tabla",
        "Gráfica de Pie"
    ),
    specs=[[
        {'type':'table'}, 
        {'type':'pie'}
    ]]
)

# -----------BEG - tabla fija con valores NA
#st.header("Tabla de ÁREA y ALIANZAS")

# PLOT 11  (row = 1, col = 1)
plot11 = (1, 1)
plotthis = plot11
row = plotthis[0]
col = plotthis[1]

dat = pd.read_csv(PATHP + 'res/01_alianzas.csv',
    header = 0,
    sep = ','
)
#dat.replace(np.nan, '', regex = True) # all DF
#dat['AREA'] = dat['AREA'].replace(np.nan, '') # only the column

fig.add_trace(
    go.Table(
        #columnwidth = [100, 80],
        header = dict(
            values = dat.columns,
            align = ['center', 'center'],
            font = dict(size = 20),
            height = 40
        ),
        cells = dict(
            values = [dat[k].tolist() for k in dat.columns],
            format = [None] + [","] + [',.1%'],
            align = ['center'],
            font = dict(size = 16),
            height = 30
        )
    ),
    row = plotthis[0], col = plotthis[1]
)

# -----------END - tabla fija con valores NA



# -----------BEG - tabla fija con valores NA

# PLOT 12 (row = 1, col = 2)
plot12 = (1, 2)
plotthis = plot12
row = plotthis[0]
col = plotthis[1]

t1 = pd.read_csv(PATHP + 'res/01_alianzas.csv',
    header = 0,
    sep = ','
)
labels = t1['ALIANZA']
values = t1['CANTIDAD']

# Use `hole` to create a donut-like pie chart
fig.add_trace(
    go.Pie(labels = labels, values = values, hole=.5),
    row = row, col = col
)

# -----------END - tabla fija con valores NA

fig.update_layout(height = 600, width = 1200, 
    title = "Tabla Alianzas",
    title_font = dict(size = 32),
)

st.plotly_chart(fig)









# --------------------------BEG - BLOQUE 2------------------------------
fig = make_subplots(rows = 1, cols = 2,
    subplot_titles = (
        "Tabla Alianzas por Área",
        "Tabla Alianzas por Área por Nivel"
    ),
    specs=[[
        {'type':'table'}, 
        {'type':'table'}
    ]]
)

# -----------BEG - tabla fija con valores NA
#st.header("Tabla de ÁREA y ALIANZAS")

# PLOT 11  (row = 1, col = 1)
plot11 = (1, 1)
plotthis = plot11
row = plotthis[0]
col = plotthis[1]

dat = pd.read_csv(PATHP + 'res/02_alianzas_area.csv',
    header = 0,
    sep = ','
)

# only the column
cols = dat.columns
for colname in cols:
    dat[colname] = dat[colname].replace(np.nan, '')

fig.add_trace(
    go.Table(
        columnwidth = [140, 120, 80],
        header = dict(
            values = dat.columns,
            align = ['center', 'center'],
            font = dict(size = 20),
            height = 40
        ),
        cells = dict(
            values = [dat[k].tolist() for k in dat.columns],
            #format = [None] + [","] + [',.1%'],
            align = ['left', 'center'],
            font = dict(size = 16),
            height = 30
        )
    ),
    row = plotthis[0], col = plotthis[1]
)
#fig.update_layout(height = 600, width = 1200, 
#    title = "Tabla Alianzas por Área",
#    title_font = dict(size = 32),
#)


# -----------BEG - tabla fija con valores NA
#st.header("Tabla de ÁREA y ALIANZAS")

# PLOT 12  (row = 1, col = 2)
plot12 = (1, 2)
plotthis = plot12
row = plotthis[0]
col = plotthis[1]
    
dat = pd.read_csv(PATHP + 'res/03_alian_area_nivel.csv',
    header = 0,
    sep = ','
)

# only the column
cols = dat.columns
for colname in cols:
    dat[colname] = dat[colname].replace(np.nan, '')

fig.add_trace(
    go.Table(
        columnwidth = [140, 120, 80],
        header = dict(
            values = dat.columns,
            align = ['center', 'center'],
            font = dict(size = 20),
            height = 40
        ),
        cells = dict(
            values = [dat[k].tolist() for k in dat.columns],
            #format = [None] + [","] + [',.1%'],
            align = ['left', 'center'],
            font = dict(size = 16),
            height = 30
        )
    ),
    row = plotthis[0], col = plotthis[1]
)

fig.update_layout(height = 600, width = 1200, 
    title = "Tabla Alianzas por Área & Tabla Alianzas por Área por Nivel",
    title_font = dict(size = 32),
)

st.plotly_chart(fig)





# --------------------------BEG - BLOQUE 3------------------------------

fig = make_subplots(rows = 1, cols = 2,
    subplot_titles = (
        "Tabla (Todos los programas)",
        "Gráfica de Pie (TOP 10)"
    ),
    specs=[[
        {'type':'table'}, 
        {'type':'pie'}
    ]]
)

# -----------BEG - tabla fija con valores NA
#st.header("Tabla de ÁREA y ALIANZAS")

# PLOT 11  (row = 1, col = 1)
plot11 = (1, 1)
plotthis = plot11
row = plotthis[0]
col = plotthis[1]

dat = pd.read_csv(PATHP + 'res/04_progs.csv',
    header = 0,
    sep = ','
)
#dat.replace(np.nan, '', regex = True) # all DF
#dat['AREA'] = dat['AREA'].replace(np.nan, '') # only the column

fig.add_trace(
    go.Table(
        columnwidth = [150, 80],
        header = dict(
            values = dat.columns,
            align = ['center', 'center'],
            font = dict(size = 20),
            height = 40
        ),
        cells = dict(
            values = [dat[k].tolist() for k in dat.columns],
            format = [None] + [","] + [',.1%'],
            align = ['left', 'center'],
            font = dict(size = 16),
            height = 30
        )
    ),
    row = plotthis[0], col = plotthis[1]
)

# -----------

# PLOT 12 (row = 1, col = 2)
plot12 = (1, 2)
plotthis = plot12
row = plotthis[0]
col = plotthis[1]

t1 = pd.read_csv(PATHP + 'res/04_progs-top.csv',
    header = 0,
    sep = ','
)
labels = t1['PROGRAMA']
values = t1['CANTIDAD']

# Use `hole` to create a donut-like pie chart
fig.add_trace(
    go.Pie(labels = labels, values = values, hole=.5),
    row = row, col = col
)

# -----------END - PIE fija con valores NA

fig.update_layout(height = 600, width = 1200, 
    title = "Tabla Programas",
    title_font = dict(size = 32),
)

st.plotly_chart(fig)





# --------------------------BEG - BLOQUE 4------------------------------
fig = make_subplots(rows = 1, cols = 2,
    subplot_titles = (
        "Tabla Alianzas por Programa",
        "Tabla Alianzas por Programa por Nivel"
    ),
    specs=[[
        {'type':'table'}, 
        {'type':'table'}
    ]]
)

# -----------BEG - tabla fija con valores NA
#st.header("Tabla de ÁREA y ALIANZAS")

# PLOT 11  (row = 1, col = 1)
plot11 = (1, 1)
plotthis = plot11
row = plotthis[0]
col = plotthis[1]

dat = pd.read_csv(PATHP + 'res/05_progs_alianza.csv',
    header = 0,
    sep = ','
)

# only the column
cols = dat.columns
for colname in cols:
    dat[colname] = dat[colname].replace(np.nan, '')

fig.add_trace(
    go.Table(
        columnwidth = [140, 120, 80],
        header = dict(
            values = dat.columns,
            align = ['center', 'center'],
            font = dict(size = 20),
            height = 40
        ),
        cells = dict(
            values = [dat[k].tolist() for k in dat.columns],
            #format = [None] + [","] + [',.1%'],
            align = ['left', 'center'],
            font = dict(size = 16),
            height = 30
        )
    ),
    row = plotthis[0], col = plotthis[1]
)
#fig.update_layout(height = 600, width = 1200, 
#    title = "Tabla Alianzas por Área",
#    title_font = dict(size = 32),
#)

# -----------

# PLOT 12  (row = 1, col = 2)
plot12 = (1, 2)
plotthis = plot12
row = plotthis[0]
col = plotthis[1]
    
dat = pd.read_csv(PATHP + 'res/06_prog_alian_nivel.csv',
    header = 0,
    sep = ','
)

# only the column
cols = dat.columns
for colname in cols:
    dat[colname] = dat[colname].replace(np.nan, '')

fig.add_trace(
    go.Table(
        columnwidth = [140, 120, 80],
        header = dict(
            values = dat.columns,
            align = ['center', 'center'],
            font = dict(size = 20),
            height = 40
        ),
        cells = dict(
            values = [dat[k].tolist() for k in dat.columns],
            #format = [None] + [","] + [',.1%'],
            align = ['left', 'center'],
            font = dict(size = 16),
            height = 30
        )
    ),
    row = plotthis[0], col = plotthis[1]
)

fig.update_layout(height = 600, width = 1200, 
    title = "Tabla Alianzas por Programa &\
 Tabla Alianzas por Programa por Nivel",
    title_font = dict(size = 32),
)

st.plotly_chart(fig)




# --------------------------BEG - BLOQUE 5------------------------------

# -----------BEG - tabla desglose alianzas mezcladas
st.header("Tabla desglosada ALIANZAS CRUZADAS")

dat = pd.read_csv(PATHP + 'res/07_tablacruz.csv',
    header = 0,
    sep = ','
)

#selection = aggrid_interactive_table(df = dat)
st.table(dat)


go.Table(
     columnwidth = [140, 120, 80],
     header = dict(
         values = dat.columns,
         align = ['center', 'center'],
         font = dict(size = 20),
         height = 40
     ),
     cells = dict(
         values = [dat[k].tolist() for k in dat.columns],
         #format = [None] + [","] + [',.1%'],
         align = ['left', 'center'],
         font = dict(size = 16),
         height = 30
     )
)


# -----------END - tabla desglose alianzas mezcladas




# --------------------------BEG - BLOQUE 6------------------------------

# -----------BEG - tabla pivote
st.header("Tablas PIVOTE: ÁREA, PROGRAMA y ALIANZAS")

dat = pd.read_csv(PATHP + 'res/data3.csv',
    header = 0,
    sep = ','
)

def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df (pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection

#selection = aggrid_interactive_table(df = dat)
aggrid_interactive_table(df = dat)

# -----------END - tabla pivote









