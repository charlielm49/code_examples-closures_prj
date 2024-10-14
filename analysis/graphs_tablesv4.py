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

dat = pd.read_csv(PATHP + 'res/t1.csv',
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

t1 = pd.read_csv(PATHP + 'res/t1.csv',
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

dat = pd.read_csv(PATHP + 'res/t2-mod.csv',
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
    
dat = pd.read_csv(PATHP + 'res/t3-mod.csv',
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
    title = "Tabla Alianzas por Área & Tabla Alianza por Área por Nivel",
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

dat = pd.read_csv(PATHP + 'res/t4.csv',
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

# -----------END - tabla fija con valores NA



# -----------BEG - tabla fija con valores NA

# PLOT 12 (row = 1, col = 2)
plot12 = (1, 2)
plotthis = plot12
row = plotthis[0]
col = plotthis[1]

t1 = pd.read_csv(PATHP + 'res/t4-top10.csv',
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

# -----------END - tabla fija con valores NA

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

dat = pd.read_csv(PATHP + 'res/t5-mod.csv',
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
    
dat = pd.read_csv(PATHP + 'res/t6-mod.csv',
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









