
analysisv01.py [OK]
-- prog para leer datosy limpiar un poco
-- lee el archivo con lista de carreras limpiadas y estandarizadas a mano 'data/names2.csv' - el proceso posterior está pendiente (relaciones entre la info de carreras limpia y desmenuzada y alianzas)

analysisv02.py - parte de v01
-- prog para leer datosy limpiar un poco
-- Implementa el algoritmo para generar lista de carreras -names file (para no hacerlo a mano y que quede automatizado)
-- Usa closures para hacer el stemmer manual :-) está el proceso
-- Aquí hay mucho análisis, incluyendo el de alianzas cruzadas
-- Otro análisis y proceso de exploración: limpieza de carrera

analysisv03.py - parte de v02 [OK]
-- Igual que v02 pero esta versión es de producción, sin exploraciones
-- Toma archivo en ruta desde 'data/alianzas.xlsx' <- EXCEL depositado

analysisv03a.py - parte de v03
-- Igual que v03
-- Toma archivo en ruta desde 'data/data1.csv' <- archivo CSV leído y
parseado por streamlit, a partir del excel depositado en la página de streamlit (no importa el nombre del excel).

El archivo de EXCEL se lee tal cual en la página del reporte. Es decir, la columna de fecha ya NO se procesa
en la página del reporte. Se pasa tal cual a CSV y se hace la corrección en el archivo de procesamiento.

analysisv03a-win.py - parte de v03a-win PEND
-- Igual que v03a pero esta versión hace ajustes para nvo archivo XLS
-- Procesa columna de fecha y la corrige

analysisv04.py - parte de v03a-win OK
-- Igual que v03a pero esta versión hace ajustes para nvo archivo XLS
-- Procesa columna de fecha y la corrige
-- Se cambia el algoritmo de diagonal de tabla alianzas cruzadas: ahora en la diagonal va la cantidad de usuarios que sólo usan 1 alianza
-- Versión en sucio (tienen la exploración de algorit para alianz cruz)

analysisv04a.py - parte de v04 PEND
-- Igual que v04 pero esta versión es de producción (sin exploraciones)
-- Cambio a lectura automática de sheets de excel





graphs_tables.py [OK pero no muestra pie chart en misma page]
-- Tablas en streamlit + tabla pivote con aggrid

graphs_tablesv2.py [OK]
-- Tablas en streamlit + tabla pivote con aggrid
-- Usa layout para gráficas múltiples (tomado de msg_graphv04a)
-- Deja basura pero OK porque la toma como referencia

graphs_tablesv3.py - parte de v2 [OK]
-- Tablas en streamlit + tabla pivote con aggrid
-- Usa layout para gráficas múltiples (tomado de msg_graphv04a)
-- Usa layoput final para reporte

graphs_tablesv4.py - parte de v3
-- Tablas en streamlit + tabla pivote con aggrid
-- Usa layout para gráficas múltiples (tomado de msg_graphv04a)
-- SE fusionan tablas de bloque 2 y bloque 3 para formar un único bloque 2

graphs_tablesv4a.py - parte de v4
-- Se agrega upload file + llamado a proceso de el archivo
-- cambio de variable carrlimpia -> progmlimpio
-- se cambian los no,mbres de tablas:
t1.csv - 01_alianzas.csv <- # ALIANZAS ***
t2.csv - 02_alianzas_area.csv <- # AREA x ALIANZAS ***
t2-mod.csv (modificado a mano)
t3.csv - 03_alian_area_nivel.csv <- # AREA x ALIANZAS x NIVEL*** PV
t3-mod.csv (modificado a mano)
t4.csv - 04_progs.csv 
t5.csv - 05_progs_alianza.csv
t6.csv - 06_prog_alian_nivel.csv

graphs_tablesv4b-win.py - parte de v4a
-- Hace cambios para no leer columna de fechas, las guarda tal cual
-- se usa para windows, 

graphs_tablesv5.py - parte de v4b-win
-- Hace cambios para no leer columna de fechas, las guarda tal cual
-- Esta se ussará para linux

graphs_tablesv5a.py - parte de v5 [OK]
-- Igual que v5 , pero Cambio a lectura automática de sheets de excel





pie.py - archivo de prueba de internet para mostrar 2 pie charts en subplots

pie-test.py - parte de pie.py
-- Se agregan más gráficas y widget de drag and drop para subir el archivo

