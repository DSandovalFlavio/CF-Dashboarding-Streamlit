# ---- Creacion de Dashboard con Streamlit y Plotly ----

# Importacion de librerias
import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(
    page_title='Dashboard', # Titulo de la pagina
    page_icon='📊', # Icono de la pagina
    layout='wide', # Ancho de la pagina (wide, center)
    initial_sidebar_state='expanded', # Estado inicial del sidebar (expanded, collapsed)
    menu_items={'Get Help': 'https://twitter.com/DSandovalFlavio',
                'Report a bug': 'https://github.com/DSandovalFlavio/CF-Dashboarding-Streamlit',
                'About': 'Taller de Dashboarding con Streamlit para el Bootcamp de Ciencia de Datos de CodigoFacilito.'}
)

# sidebar saludo inicial y descripcion del proyecto
with st.sidebar:
    # Titulo
    st.title('Hola! este es mi primer dashboard')
    # descripcion
    st.markdown('Dashboard para analizar el desempeño de la tienda en las diferentes regiones.')
    # link dataset
    st.markdown('Dataset: [Superstore Sales](https://www.kaggle.com/datasets/flaviocesarsandoval/supertienda)')
    # link github
    st.markdown('Github: [DSandovalFlavio/CF-Dashboarding-Streamlit](https://github.com/DSandovalFlavio/CF-Dashboarding-Streamlit)')
    st.markdown('Twitter: [@DSandovalFlavio](https://twitter.com/DSandovalFlavio)')

# carga de datos
supertienda_raw = pd.read_csv('./data/Muestra - Supertienda.csv')
# quitar valores nulos
supertienda_raw = supertienda_raw[supertienda_raw['Fecha del pedido'].notna()]
supertienda_raw = supertienda_raw.drop(columns=['Unnamed: 20'])
# convertir a datetime y crear columnas de año y mes
supertienda_raw['Fecha del pedido'] = pd.to_datetime(supertienda_raw['Fecha del pedido'])
supertienda_raw['Año'] = (supertienda_raw['Fecha del pedido'].dt.year).astype(int)
supertienda_raw['Mes'] = (supertienda_raw['Fecha del pedido'].dt.month).astype(int)

# mostrar momentaneamente los datos
#st.write(supertienda_raw)

# Containner principal
with st.container():
    # Titulo
    st.title('Super Tienda Performance Dashboard')

# Containner para filtros por año, mes y region
with st.container():
    # creacion de columnas para filtros
    filtro_año, filtro_mes, filtro_region = st.columns(3)
    
    with filtro_año:
        # filtro por año
        list_años = supertienda_raw['Año'].unique()
        list_años.sort()
        año = st.multiselect('Año', list_años, list_años[0])
    with filtro_mes:
        # filtro por mes
        list_meses = supertienda_raw['Mes'].unique()
        list_meses.sort()
        mes = st.multiselect('Mes', list_meses, list_meses[0])
    with filtro_region:
        # filtro por region
        list_regiones = supertienda_raw['Región'].unique()
        list_regiones.sort()
        region = st.multiselect('Región', list_regiones, list_regiones[0])

# dataframe filtrado
supertienda_filter = supertienda_raw[
        (supertienda_raw['Año'].isin(año)) 
    &   (supertienda_raw['Mes'].isin(mes)) 
    &   (supertienda_raw['Región'].isin(region))
    ]

# Container para 2 KPI's
with st.container():
    # creacion de 2 columnas
    kpi1, kpi2 = st.columns(2)
    # Creacion de KPI's con st.metric
    with kpi1:
        st.metric(label='Total Ventas', value=f"${supertienda_filter['Ventas'].sum():,.0f}")
    with kpi2:
        st.metric(label='Total Productos Vendidos', value=f"{supertienda_filter['Cantidad'].sum():,.0f}")

# Container para nuestros dos primeros graficos
st.header('Tendencia de Ventas')
with st.container():
    # creacion de 2 columnas para el grafico de lineas y de pie
    line_chart_total, pie_chart_total = st.columns((2,1))
    with line_chart_total:
        # grafico de lineas
        data_line = supertienda_filter.groupby('Fecha del pedido')['Ventas'].sum().reset_index()
        line_chart = px.line(data_line, 
                            x='Fecha del pedido', 
                            y='Ventas', 
                            title='Tendencia de Ventas')
        line_chart.update_layout(height=600, 
                                width=1000)
        st.plotly_chart(line_chart)
    
    with pie_chart_total:
        # grafico de pie para ventas totales por pais
        data_pie = supertienda_filter.groupby('País/Región')['Ventas'].sum().reset_index()
        pie_chart = px.pie(data_pie, 
                            values='Ventas', 
                            names='País/Región', 
                            title='Ventas por País')
        # cambiar el tamaño del grafico
        pie_chart.update_traces(textposition='inside', 
                                textinfo='percent+label+value')
        pie_chart.update_layout(uniformtext_minsize=12, 
                                uniformtext_mode='hide',
                                showlegend=False,
                                height=600, 
                                width=600)
        st.plotly_chart(pie_chart)

# Container para nuestros dos ultimos graficos
with st.container():
    # creacion de 2 columnas para el grafico de barras horizontales y de barras verticales
    st.markdown('## Ventas por Categoría')
    bar_chart_total, bar_chart_total2 = st.columns((1,2))
    
    with bar_chart_total:
        # grafico de barras horizontales
        data_bar = supertienda_filter.groupby('Categoría')['Ventas'].sum().reset_index()
        bar_chart = px.bar(data_bar, 
                            y='Categoría', 
                            x='Ventas', 
                            title='Ventas por Categoría',
                            color='Categoría',
                            orientation='h',
                            text_auto='.2s')
        bar_chart.update_layout(height=600, 
                                width=600)
        st.plotly_chart(bar_chart)
    
    with bar_chart_total2:
        # grafico de barras verticales
        data_bar2 = supertienda_filter.groupby('Subcategoría')['Ventas'].sum().reset_index()
        bar_chart2 = px.bar(data_bar2, 
                            x='Subcategoría', 
                            y='Ventas', 
                            title='Ventas por Sub-Categoría',
                            color='Subcategoría',
                            text_auto='.2s')
        bar_chart2.update_layout(height=600, 
                                width=1000)
        st.plotly_chart(bar_chart2)