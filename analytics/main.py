import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from querys import (
    ciudad_mas_caliente,
    ciudad_mas_fria,
    top_ciudades_calientes,
    top_paises_por_temperatura,
    distribucion_condiciones_climaticas,
    resumen_completo_dia,
    ciudad_mas_humeda,
    ciudad_mas_seca,
    ciudad_vientos_mas_fuertes,
    ciudad_mayor_lluvia,
    ciudades_por_rango_temperatura,
    ciudades_mayor_variacion_termica,
    comparacion_sensacion_vs_temperatura
)
import querys
from utils import date_parts

# Configuración de la página
st.set_page_config(
    page_title="Weather Insights Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar para Filtros
st.sidebar.header("⚙️ Configuración")
hoy = datetime.utcnow() - timedelta(hours=5)
fecha_seleccionada = st.sidebar.date_input(
    "Selecciona la Fecha",
    value=hoy,
    max_value=hoy
)

# Actualizar la fecha directamente en el módulo querys usando date_parts
querys.year, querys.month, querys.day = date_parts(fecha_seleccionada)

# Estilo personalizado para un look premium
st.markdown("""
    <style>
    .stMetric {
        background-color: #161b22;
        padding: 15px;
        border-radius: 5px; 
        border: 1px solid #30363d;
        border-left: 5px solid #0078d4; 
    }
    .stMetric:hover {
        border-color: #58a6ff;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Global Weather Dashboard")
st.markdown(f"**Reporte del Clima** | {fecha_seleccionada.strftime('%d/%m/%Y')} (Capa Gold)")

try:
    # Cargar Resumen General
    df_resumen = resumen_completo_dia()
    
    if not df_resumen.empty and df_resumen.iloc[0]['total_ciudades'] > 0:
        resumen = df_resumen.iloc[0]
        
        # --- FILA 1: Métricas Principales ---
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Temp Promedio", f"{resumen['temp_promedio']}°C")
        with col2:
            st.metric("Humedad Promedio", f"{resumen['humedad_promedio']}%")
        with col3:
            st.metric("Total Ciudades", int(resumen['total_ciudades']))
        with col4:
            st.metric("Países", int(resumen['total_paises']))

        st.markdown("---")

        # --- FILA 2: Récords del Día (Nuevas Queries) ---
        st.subheader("🏆 Récords del Día")
        rec1, rec2, rec3, rec4 = st.columns(4)
        
        with rec1:
            try:
                hot = ciudad_mas_caliente().iloc[0]
                st.info(f"🔥 **Hottest**\n\n{hot['Name_City']}, {hot['Country_Name']}\n\n**{hot['temp']}°C**")
            except: st.info("Hottest: N/A")
            
        with rec2:
            try:
                cold = ciudad_mas_fria().iloc[0]
                st.info(f"❄️ **Coldest**\n\n{cold['Name_City']}, {cold['Country_Name']}\n\n**{cold['temp']}°C**")
            except: st.info("Coldest: N/A")

        with rec3:
            try:
                rain = ciudad_mayor_lluvia().iloc[0]
                st.info(f"🌧️ **Wettest**\n\n{rain['Name_City']}, {rain['Country_Name']}\n\n**{rain['rain_1h']} mm**")
            except: st.info("Wettest: No Rain")

        with rec4:
            try:
                wind = ciudad_vientos_mas_fuertes().iloc[0]
                st.info(f"💨 **Windiest**\n\n{wind['Name_City']}, {wind['Country_Name']}\n\n**{wind['velocidad_viento']} m/s**")
            except: st.info("Windiest: N/A")

        st.markdown("---")

        # --- FILA 3: Rankings y Clima ---
        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.subheader("🏙️ Top 10 Ciudades más Calientes")
            df_calientes = top_ciudades_calientes(10)
            if not df_calientes.empty:
                fig_hot = px.bar(
                    df_calientes, 
                    x='temperatura', 
                    y='Name_City', 
                    orientation='h',
                    color='temperatura',
                    color_continuous_scale='Reds',
                    labels={'temperatura': 'Temp (°C)', 'Name_City': 'Ciudad'},
                    text_auto='.1f',
                    template="plotly_dark"
                )
                fig_hot.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig_hot, use_container_width=True)

        with col_right:
            st.subheader("🌡️ Distribución por Rangos de Temperatura")
            df_rangos = ciudades_por_rango_temperatura()
            if not df_rangos.empty:
                fig_rangos = px.bar(
                    df_rangos,
                    x='rango_temperatura',
                    y='num_ciudades',
                    color='rango_temperatura',
                    color_discrete_sequence=px.colors.sequential.Oryel,
                    labels={'num_ciudades': 'N° Ciudades', 'rango_temperatura': 'Rango'},
                    template="plotly_dark",
                    text_auto=True
                )
                st.plotly_chart(fig_rangos, use_container_width=True)

        st.markdown("---")

        # --- FILA 4: Distribución y Países ---
        col_dist, col_country = st.columns([1, 1])

        with col_dist:
            st.subheader("☁️ Condiciones Climáticas")
            df_cond = distribucion_condiciones_climaticas()
            if not df_cond.empty:
                threshold = 4.0
                df_cond.loc[df_cond['porcentaje'] < threshold, 'condicion'] = 'Otros'
                df_cond = df_cond.groupby('condicion')['num_ciudades'].sum().reset_index()
                
                fig_pie = px.pie(
                    df_cond, 
                    values='num_ciudades', 
                    names='condicion',
                    hole=.4,
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    template="plotly_dark"
                )
                st.plotly_chart(fig_pie, use_container_width=True)

        with col_country:
            st.subheader("🌍 Países con Mayor Temperatura")
            df_paises = top_paises_por_temperatura(10)
            if not df_paises.empty:
                fig_country = px.bar(
                    df_paises,
                    x='Country_Name',
                    y='temp_promedio',
                    color='temp_promedio',
                    color_continuous_scale='Oranges',
                    labels={'temp_promedio': 'Temp Promedio (°C)', 'Country_Name': 'País'},
                    template="plotly_dark"
                )
                st.plotly_chart(fig_country, use_container_width=True)

        st.markdown("---")

        # --- FILA 5: Análisis de Variación y Humedad ---
        st.subheader("🔍 Análisis Detallado")
        tab_var, tab_sens, tab_hum = st.tabs(["🌡️ Variación Térmica", "🤔 Sensación vs Temp", "💧 Humedad Extrema"])
        
        with tab_var:
            st.markdown("Top 10 Ciudades con mayor variación térmica (Max vs Min)")
            df_var = ciudades_mayor_variacion_termica()
            if not df_var.empty:
                st.dataframe(df_var, use_container_width=True)
            else: st.info("Sin datos de variación.")

        with tab_sens:
            st.markdown("Top 10 Ciudades con mayor diferencia entre Sensación y Temperatura Real")
            df_sens = comparacion_sensacion_vs_temperatura()
            if not df_sens.empty:
                st.dataframe(df_sens, use_container_width=True)
            else: st.info("Sin datos de diferencia térmica.")

        with tab_hum:
            col_h1, col_h2 = st.columns(2)
            with col_h1:
                try:
                    hum_max = ciudad_mas_humeda().iloc[0]
                    st.metric("Ciudad más Húmeda", f"{hum_max['Name_City']}", f"{hum_max['humidity']}%")
                except: st.info("Sin datos de humedad.")
            with col_h2:
                try:
                    hum_min = ciudad_mas_seca().iloc[0]
                    st.metric("Ciudad más Seca", f"{hum_min['Name_City']}", f"{hum_min['humidity']}%")
                except: st.info("Sin datos de humedad.")

    else:
        st.warning(f"No hay datos disponibles para el dia {fecha_seleccionada.strftime('%d/%m/%Y')}.")
        st.info("Selecciona otra fecha en el panel lateral o asegúrate de que el pipeline ETL haya procesado datos para este día.")

except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.info("Verifica la conexión con MinIO y que los archivos Parquet existan en la zona Gold.")
