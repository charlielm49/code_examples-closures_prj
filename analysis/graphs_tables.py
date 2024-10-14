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



st.set_page_config(page_title="Netflix Shows", layout="wide")

st.title("Tablas y gráficas análisis alianzas")


# -----------BEG - tabla fija con valores NA
st.header("Tabla de ALIANZAS")

t1 = pd.read_csv(PATHP + 'res/t1.csv',
    header = 0,
    sep = ','
)
labels = t1['ALIANZA']
values = t1['CANTIDAD']

# Use `hole` to create a donut-like pie chart
fig = go.Figure( data = [go.Pie(labels = labels, \
    values = values, hole=.5)])
fig.show()

# -----------END - tabla fija con valores NA


# -----------BEG - tabla fija con valores NA

st.header("Tabla de ÁREA y ALIANZAS")

dat = pd.read_csv(PATHP + 'res/area_alianzas.csv',
    header = 0,
    sep = ','
)
dat.replace(np.nan, '', regex = True) # all DF
dat['AREA'] = dat['AREA'].replace(np.nan, '') # only the column

st.table(dat)

# -----------END - tabla fija con valores NA



# -----------BEG - tabla pivote
st.header("Tablas PIVOTE: ÁREA, CARRERA y ALIANZAS")

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
