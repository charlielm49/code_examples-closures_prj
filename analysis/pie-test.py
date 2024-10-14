

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import subprocess

USB = "KING16-3"
#PATHP = "/home/admin/rec/"
PATHP = "/media/clm/" + USB + "/" + \
    "48-2022FEB11-recom_prods/"
PATHBIN = "/home/clm/bin/miniconda3/envs/work/bin/"

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
    data.to_csv(PATHP + "res/data1.csv", index = False)
    # Ejecutamos proceso de archivo
    #subprocess.call(PATHBIN + "python"  + )



# -----------BEG - tabla pivote
st.header("Tablas PIVOTE: ÁREA, PROGRAMA y ALIANZAS")

dat = pd.read_csv(PATHP + 'res/data1.csv',
    header = 0,
    sep = ',',
    dtype={'username': object},
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


#------------ BEG: BLOQUE GRÁFICAS 1

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


# PLOT 11  (row = 1, col = 1)
plot11 = (1, 1)
plotthis = plot11
row = plotthis[0]
col = plotthis[1]

dat = pd.read_csv(PATHP + 'res/t1.csv',
    header = 0,
    sep = ','
)

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

fig.update_layout(height = 600, width = 1200, 
    title = "Tabla Alianzas",
    title_font = dict(size = 32),
)

st.plotly_chart(fig)

#------------ END: BLOQUE GRÁFICAS 1




#------------ BEG: BLOQUE GRÁFICAS 2
labels = ["US", "China", "European Union", "Russian Federation", "Brazil", "India",
          "Rest of World"]

# Create subplots: use 'domain' type for Pie subplot
fig = make_subplots(rows=1, cols=2, 
    specs=[[{'type':'domain'}, {'type':'domain'}]])
fig.add_trace(
    go.Pie(labels=labels, values=[16, 15, 12, 6, 5, 4, 42], 
    name="GHG Emissions"),
    1, 1)
fig.add_trace(
    go.Pie(labels=labels, values=[27, 11, 25, 8, 1, 3, 25], 
    name="CO2 Emissions"),
    1, 2)

# Use `hole` to create a donut-like pie chart
fig.update_traces(hole=.4, hoverinfo="label+percent+name")

fig.update_layout(
    title_text="Global Emissions 1990-2011",
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='GHG', x=0.18, y=0.5, font_size=20, showarrow=False),
                 dict(text='CO2', x=0.82, y=0.5, font_size=20, showarrow=False)])

st.plotly_chart(fig)

#------------ END: BLOQUE GRÁFICAS 2
