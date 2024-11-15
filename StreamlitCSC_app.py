import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

## Configuración inicial de la página
st.set_page_config(
    page_title="Dashboard por Equipo CSC",
    page_icon=":bar_chart:",
    layout="wide"
)

st.markdown(
    """
    <div style="
        background-color: #E0E0E0;
        padding: 1px 10px;
        border-radius: 5px;
        display: flex;
        align-items: center;">
        <img src="https://www.nibol.com.bo/wp-content/uploads/2022/06/logo-nibol-negro-ok1.png" width="250" style="margin-right: 100px;"/>
        <h1 style="color: #000000; margin: 0; font-size: 42px;">
            Reporte Seguimiento CSC
        </h1>
    </div>
    <hr style="border: none; border-top: 3px solid #000000; margin: 5px 0;">
    """,
    unsafe_allow_html=True
)
st.markdown("")
st.markdown("")
# Cargar los datos con caching para evitar recargar el archivo si no es necesario
@st.cache_data
def load_data(file):
    if file is not None:
        data = pd.read_csv(file)
        return data
    return None

##st.sidebar.image("https://cdn.worldvectorlogo.com/logos/john-deere-6.svg", width=150)
st.sidebar.header("Carga de Archivos")
uploaded_file1 = st.sidebar.file_uploader("Archivo Semana Consolidada", key="file1")
uploaded_file2 = st.sidebar.file_uploader("Archivo Horas de trabajo Motor", key="file2")
uploaded_file3 = st.sidebar.file_uploader("Archivo Horas de Funcionamiento", key="file3")

# Verificar si se han cargado los tres archivos
if not all([uploaded_file1, uploaded_file2, uploaded_file3]):
    st.info("Se requiere cargar los tres archivos", icon="ℹ")
    st.stop()

df = load_data(uploaded_file1).drop_duplicates()
df['Serie'] = df['Serie'].replace('En reposo', 'Ralentí')
df2 = load_data(uploaded_file2).drop_duplicates()
df3 = load_data(uploaded_file3).drop_duplicates()


# Obtener valores clave para mostrar en la interfaz
FechaInicio = df['Fecha de inicio'].max()
FechaTerminación = df['Fecha de terminación'].max()
Chasis = df['Número de serie de la máquina'].max()
st.markdown("")
st.markdown(
    """
    <div style="
        background-color: #E0E0E0;
        padding: 1px 10px;
        border-radius: 5px;
        display: flex;
        ">
        <h2 style="
            color: #000000;
            margin: 0;
            font-size: 22px;
            font-weight: bold;
            text-align: center;
            ">
            Datos Generales
        </h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Crear un diccionario con los nombres de los meses abreviados en español
meses_abreviados = {
    1: "ene", 2: "feb", 3: "mar", 4: "abr", 5: "may", 6: "jun",
    7: "jul", 8: "ago", 9: "sep", 10: "oct", 11: "nov", 12: "dic"
}

# Obtener la fecha actual
hoy = datetime.now()
dia = hoy.day
mes = meses_abreviados[hoy.month]  # Obtener la abreviatura del mes
año = hoy.year

# Crear la fecha en el formato deseado
fecha_actual = f"{dia} {mes} {año}"

st.text_input("", placeholder="Escriba el nombre del cliente aquí")
st.markdown(f"**Fecha del Reporte:** {fecha_actual}")
st.markdown(f"**PIN:** {Chasis}")
st.markdown(f"**Periodo de Análisis:** Del {FechaInicio} al {FechaTerminación}")

# Expander para mostrar los datos cargados
with st.expander("Vista de datos Cargados"):
    tab1, tab2, tab3 = st.tabs(["Semana Consolidada", "Horas de trabajo Motor", "Horas de Funcionamiento"])

    with tab1:
        st.dataframe(df, use_container_width=True)

    with tab2:
        st.dataframe(df2, use_container_width=True)

    with tab3:
        st.dataframe(df3, use_container_width=True)

# Función para graficar barras
def graficar_barras(df, categoria_seleccionada):
    df_filtrado = df[df['Categoría'] == categoria_seleccionada].sort_values(['Valor'],ascending=False)
    valor_unidades = df_filtrado['Unidades de medida'].max()

    fig = px.bar(
        df_filtrado, 
        x='Serie', 
        y='Valor', 
        title=f'Categoría: {categoria_seleccionada} - {valor_unidades}',
        labels={'Valor':f'Valor ({valor_unidades})', 'Serie':''},
        template='plotly_white',
        color_discrete_sequence=['#367C2B', '#FFCC00', '#A2B5A1', '#556B2F', '#8B4513']
    )

    fig.update_layout(
        title_font_size=20,
        xaxis_title_font_size=16,
        yaxis_title_font_size=16,
        margin=dict(l=50, r=50, t=50, b=50),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, zeroline=False),
        font=dict(family="Arial", size=12),
    )
    fig.update_traces(text=df_filtrado['Valor'], textposition='outside')

    return fig

import plotly.express as px

def graficar_pie(df, categoria_seleccionada):
    df_filtrado = df[df['Categoría'] == categoria_seleccionada]
    valor_unidades = df_filtrado['Unidades de medida'].max()
    fig = px.pie(
        df_filtrado,
        names='Serie',
        values='Valor',
        title=f'Categoría: {categoria_seleccionada} - {valor_unidades}',
        template='plotly_white',
        color_discrete_sequence=['#367C2B', '#FFCC00', '#A2B5A1', '#556B2F', '#8B4513']
    )
    fig.update_traces(
        textinfo='label+percent+value',  # Muestra el nombre, el porcentaje y el valor
        texttemplate='%{label}: %{value} (%{percent})',  # Personaliza el formato de la etiqueta
        textposition='inside',  # Coloca el texto dentro de cada porción
    )
    fig.update_layout(
        title_font_size=20,
        margin=dict(l=50, r=50, t=50, b=50),
        font=dict(family="Arial", size=12),
    )
    return fig

st.markdown(
    """
    <div style="
        background-color: #E0E0E0;
        padding: 1px 10px;
        border-radius: 5px;
        display: flex;
        ">
        <h2 style="
            color: #000000;
            margin: 0;
            font-size: 22px;
            font-weight: bold;
            text-align: left;
            ">
            Información de operación diaria
        </h2>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("")
st.markdown("")
# Mostrar gráficos en la misma fila
col1, col2 = st.columns([1, 1])

with col1:
    table1 = df2.groupby('Fecha').agg(
    Horas_Motor_Inicio=('Horas de trabajo del motor', 'min'),
    Horas_Motor_Fin=('Horas de trabajo del motor', 'max'))
    table1['Horas Trabajadas'] = table1['Horas_Motor_Fin'] - table1['Horas_Motor_Inicio']
    table1=table1.sort_values(by='Fecha',ascending=False)
    st.markdown("##### Horas de trabajo del motor") 
    st.dataframe(table1)

with col2:
        # Convertir la columna 'Duración' a formato de timedelta, calcular los segundos, y luego a horas
    df3['Duración_horas'] = pd.to_timedelta(df3['Duración']).dt.total_seconds() / 60 / 60

    # Agrupar por 'Fecha' y 'Estado de máquina' y sumar las horas
    df_agrupada = df3.groupby(['Fecha', 'Estado de máquina'])['Duración_horas'].sum().reset_index()

    # Paleta de colores de John Deere
    colores = {'Activado': '#367C2B',  # Verde John Deere
            'Apag.': '#CDCDCD'}  # Gris John Deere

    # Redondear la columna de duración a 2 decimales
    df_agrupada['Duración_horas'] = df_agrupada['Duración_horas'].round(2)

    # Calcular el porcentaje de cada duración por estado y fecha
    total_por_fecha = df_agrupada.groupby('Fecha')['Duración_horas'].transform('sum')
    df_agrupada['Porcentaje'] = (df_agrupada['Duración_horas'] / total_por_fecha) * 100

    # Crear un texto que contenga tanto las horas como el porcentaje
    df_agrupada['Texto'] = df_agrupada['Duración_horas'].astype(str) + ' hrs<br>' + df_agrupada['Porcentaje'].round(1).astype(str) + '%'

    # Crear el gráfico con Plotly Express
    fig_Funcionamiento = px.bar(df_agrupada, 
                                x='Duración_horas', 
                                y='Fecha', 
                                color='Estado de máquina', 
                                color_discrete_map=colores, 
                                orientation='h', 
                                text='Texto',  # Mostrar tanto horas como porcentaje
                                )

    # Configuración de la apariencia
    fig_Funcionamiento.update_traces(texttemplate='%{text}', textposition='inside', marker=dict(line=dict(color='black', width=1)))

    # Ajustar el diseño del gráfico
    fig_Funcionamiento.update_layout(
        xaxis_title='Duración en Horas',
        yaxis_title='Fecha',
        legend_title='Estado de Máquina',
        template='plotly_white',
        margin=dict(l=50, r=50, t=50, b=50)
    )

    # Mostrar el gráfico
    st.markdown("##### Horas de Funcionamiento") 
    st.plotly_chart(fig_Funcionamiento, use_container_width=True)


st.markdown(
    """
    <div style="
        background-color: #E0E0E0;
        padding: 1px 10px;
        border-radius: 5px;
        display: flex;
        ">
        <h2 style="
            color: #000000;
            margin: 0;
            font-size: 22px;
            font-weight: bold;
            text-align: left;
            ">
            Información sobre el consumo de combustible
        </h2>
    </div>
    """,
    unsafe_allow_html=True
)


# Asegurar que la columna 'Valor' sea numérica
df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')

# Filtrar la columna 'Categoría'
categorias = df['Categoría'].unique()

Combustible_consumido=df.loc[df['Categoría']=="Combustible consumido en período"]['Valor'].max()
st.markdown("")
st.markdown(f"<div style='font-size: 22px;'>El total de consumible consumido en el periodo es de {Combustible_consumido} l </div>", unsafe_allow_html=True)
st.markdown("")
# Mostrar gráficos en la misma fila
col1, col2 = st.columns([1, 1])

with col1:
    # Selección de categorías
    # Establecer el índice predeterminado para "Consumo promedio combustible"
    index_default = list(categorias).index("Combustible consumido") if "Combustible consumido" in categorias else 0
    categoria_seleccionada = "Combustible consumido" #st.selectbox('Selecciona una categoría', categorias, index=index_default)
    fig1 = graficar_barras(df, categoria_seleccionada)
    st.plotly_chart(fig1)

with col2:
    index_default2 = list(categorias).index("Consumo promedio combustible") if "Consumo promedio combustible" in categorias else 0
    categoria_seleccionada2 = "Consumo promedio combustible" #st.selectbox('Selecciona una categoría', categorias, index=index_default2,key='2')
    fig2 = graficar_barras(df, categoria_seleccionada2)
    st.plotly_chart(fig2)

st.markdown(
    """
    <div style="
        background-color: #E0E0E0;
        padding: 1px 10px;
        border-radius: 5px;
        display: flex;
        ">
        <h2 style="
            color: #000000;
            margin: 0;
            font-size: 22px;
            font-weight: bold;
            text-align: left;
            ">
            Información sobre el funcionamiento del motor
        </h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Corregir ralenti y filtros reporte
df_Motor=df
df_Motor=df_Motor.loc[df_Motor['Serie'].isin(['Ralentí', 'Cosecha', 'Trabajando'])]

# Mostrar gráficos en la misma fila
col1, col2 = st.columns([1, 1])

with col1:
    fig2_1 = graficar_barras(df_Motor,"Factor de carga prom del motor")
    st.plotly_chart(fig2_1)

with col2:
    fig2_2 = graficar_barras(df_Motor, "Régimen de motor promedio")
    st.plotly_chart(fig2_2)

st.markdown(
    """
    <div style="
        background-color: #E0E0E0;
        padding: 1px 10px;
        border-radius: 5px;
        display: flex;
        ">
        <h2 style="
            color: #000000;
            margin: 0;
            font-size: 22px;
            font-weight: bold;
            text-align: left;
            ">
           Información temperaturas de funcionamiento
        </h2>
    </div>
    """,
    unsafe_allow_html=True
)
TiempoRalenti=df.loc[df['Categoría']=="Tiempo a ralentí"]['Valor'].max()
TiempoCosecha=df.loc[df['Categoría']=="Tiempo de cosecha"]['Valor'].max()
TiempoManiobra=df.loc[df['Categoría']=="Tiempo de maniobra"]['Valor'].max()
TiempoTransporte=df.loc[df['Categoría']=="Tiempo de transporte"]['Valor'].max()
Temperaturaref_prom=df.loc[df['Categoría']=="Temp de refrigerante promedio"]['Valor'].max()
Temperaturamax_hidr=df.loc[df['Categoría']=="Temp máx de aceite hidráulico"]['Valor'].max()
Temperaturamax_ref=df.loc[df['Categoría']=="Temp máx refrigerante"]['Valor'].max()
TemperaturaProm_hidr=df.loc[df['Categoría']=="Temp promedio de aceite hidráulico"]['Valor'].max()
st.markdown("")

st.markdown(f"<div style='font-size: 18px;font-weight: bold;'>Temperaturas: </div>", unsafe_allow_html=True)
st.markdown(f"<div style='font-size: 18px;padding: 1px 20px'>Promedio Refrigerante      ={Temperaturaref_prom} °C </div>", unsafe_allow_html=True)
st.markdown(f"<div style='font-size: 18px;padding: 1px 20px'>Max Refrigerante           ={Temperaturamax_ref} °C </div>", unsafe_allow_html=True)
st.markdown(f"<div style='font-size: 18px;padding: 1px 20px'>Promedio Aceite Hidráulico ={TemperaturaProm_hidr} °C </div>", unsafe_allow_html=True)
st.markdown(f"<div style='font-size: 18px;padding: 1px 20px'>Max Aceite Hidráulico      ={Temperaturamax_hidr} °C </div>", unsafe_allow_html=True)
st.markdown("")
st.markdown(
    """
    <div style="
        background-color: #E0E0E0;
        padding: 1px 10px;
        border-radius: 5px;
        display: flex;
        ">
        <h2 style="
            color: #000000;
            margin: 0;
            font-size: 22px;
            font-weight: bold;
            text-align: left;
            ">
           Información sobre la Utilización de tecnología
        </h2>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("")

col1, col2,col3 = st.columns([1,1,1])

with col1:
        fig4_1 = graficar_pie(df,"Harvest Monitor System")
        st.plotly_chart(fig4_1)
with col2:
        fig4_2 = graficar_pie(df, "AutoTrac™")
        st.plotly_chart(fig4_2)
with col3:
        fig4_3 = graficar_pie(df, "SmartClean System Hours")
        st.plotly_chart(fig4_3)

st.markdown(
    """
    <div style="
        background-color: #E0E0E0;
        padding: 1px 10px;
        border-radius: 5px;
        display: flex;
        ">
        <h2 style="
            color: #000000;
            margin: 0;
            font-size: 22px;
            font-weight: bold;
            text-align: left;
            ">
           Información sobre el extractor primario y presión de cuchillas
        </h2>
    </div>
    """,
    unsafe_allow_html=True
)
Presiondecuchillainferiormaxima=df.loc[df['Categoría']=="Presión de cuchilla inferior máxima"]['Valor'].max()
Presióndepicadormaxima=df.loc[df['Categoría']=="Presión de picador máxima"]['Valor'].max()
PrimaryExtractorFanSpeed=df.loc[df['Categoría']=="Primary Extractor Fan Speed"]['Valor'].max()
PrimaryExtractorLossTarget=df.loc[df['Categoría']=="Primary Extractor Loss Target"]['Valor'].max()
st.markdown("")

col1, col2 = st.columns([1,1])

with col1:
        st.markdown(f"<div style='font-size: 18px;font-weight: bold;'>Presión de Cuchillas: </div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 18px;padding: 1px 20px'>Presión maxima de cuchilla inferior    ={Presiondecuchillainferiormaxima} kPa </div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 18px;padding: 1px 20px'>Presión máxima Picador                 ={Presióndepicadormaxima} kPa </div>", unsafe_allow_html=True)
        
        st.markdown("")
        st.markdown(f"<div style='font-size: 18px;font-weight: bold;'>Extractor primario: </div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 18px;padding: 1px 20px'>Velocidad del ventilador extractor primario={PrimaryExtractorFanSpeed} RPM </div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 18px;padding: 1px 20px'>Límite pérdida extractor primario          ={PrimaryExtractorLossTarget} ton/hec </div>", unsafe_allow_html=True)
        

with col2:
        fig5_1 = graficar_pie(df, "Primary Extractor Loss")
        st.plotly_chart(fig5_1)

st.markdown(
    """
    <div style="
        background-color: #E0E0E0;
        padding: 1px 10px;
        border-radius: 5px;
        display: flex;
        ">
        <h2 style="
            color: #000000;
            margin: 0;
            font-size: 22px;
            font-weight: bold;
            text-align: left;
            ">
           Información sobre la Utilización de la máquina y velocidad
        </h2>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("")

col1, col2 = st.columns([1,1])

with col1:
        fig6_1 = graficar_barras(df,"Utilización de la máquina")
        st.plotly_chart(fig6_1)
with col2:
        fig6_2 = graficar_barras(df, "Velocidad de avance prom")
        st.plotly_chart(fig6_2)

# Verifica si el campo "Precisión del receptor StarFire™ de la máquina" existe en el DataFrame
if "Precisión del receptor StarFire™ de la máquina" in df.columns:
    st.markdown(
        """
        <div style="
            background-color: #E0E0E0;
            padding: 1px 10px;
            border-radius: 5px;
            display: flex;
            ">
            <h2 style="
                color: #000000;
                margin: 0;
                font-size: 22px;
                font-weight: bold;
                text-align: left;
                ">
            Precision señal piloto automatico
            </h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("")

    # Llama a la función personalizada para graficar
    fig6_1 = graficar_barras(df, "Precisión del receptor StarFire™ de la máquina")
    # Muestra el gráfico con Streamlit
    st.plotly_chart(fig6_1)
else:
   ""

st.markdown("")

fig6_1 = graficar_barras(df,"Precisión del receptor StarFire™ de la máquina")
st.plotly_chart(fig6_1)
