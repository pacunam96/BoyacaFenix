# =============================================================================
# IMPORTS Y CONFIGURACIÓN
# =============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from sodapy import Socrata
from datetime import datetime
from PIL import Image
import folium
from streamlit_folium import folium_static
import os

# =============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# =============================================================================

st.set_page_config(
    page_title="Bienvenidos aFénix Boyacá",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# ESTILOS CSS PERSONALIZADOS
# =============================================================================

def load_custom_css():
    """Carga los estilos CSS personalizados para la aplicación."""
    
    # Estilos para el encabezado
    header_css = """
        .header-container {
            display: flex;
            justify-content: center;
            background-color: #ffffff;
            border-bottom: 1px solid #e0e0e0;
            padding: 0;
        }
        .header-img {
            width: 100%;
            height: auto;
        }
    """
    
    # Estilos para el tema minimalista
    theme_css = """
        /* Fondo principal y panel lateral */
        .main, .stApp, .stSidebar {
            background-color: #ffffff !important;
            color: #000000 !important;
        }

        /* Panel lateral con línea divisoria */
        .stSidebar {
            border-right: 1px solid #e0e0e0;
        }

        /* Componentes principales */
        .stMetric, .stDataFrame, .stPlotlyChart {
            background-color: #ffffff !important;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            color: #000000 !important;
            box-shadow: none;
        }

        /* Tipografía */
        .stSubheader, .stTitle, h1, h2, h3, h4, h5, h6, p, label, span {
            color: #000000 !important;
        }

        /* Elementos internos de Streamlit */
        .css-1d391kg, .css-1v0mbdj, .css-18e3th9 {
            background-color: #ffffff !important;
            color: #000000 !important;
        }

        /* Botones */
        .stButton>button {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #000000;
            border-radius: 5px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #000000;
            color: #ffffff;
        }
    """
    
    # Aplicar estilos
    st.markdown(f"<style>{header_css}{theme_css}</style>", unsafe_allow_html=True)

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

@st.cache_data
def load_data():
    """
    Carga datos desde la API de datos.gov.co
    
    Returns:
        pd.DataFrame: DataFrame con los datos de incendios forestales
    """
    try:
        cliente = Socrata("www.datos.gov.co", None)
        resultados = cliente.get("ryr5-rs2a", limit=5000)
        df = pd.DataFrame.from_records(resultados)

        # Convertir fechas si la columna existe
        if "fecha_reporte" in df.columns:
            df["fecha_reporte"] = pd.to_datetime(df["fecha_reporte"], errors="coerce")

        # Verificar columnas clave
        columnas_clave = ["departamento", "municipio", "fecha_reporte"]
        columnas_presentes = [col for col in columnas_clave if col in df.columns]

        # Limpiar datos faltantes
        if columnas_presentes:
            df = df.dropna(subset=columnas_presentes)

        return df
    
    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        return pd.DataFrame()

def create_filters(df):
    """
    Crea los filtros de la aplicación
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        
    Returns:
        tuple: (df_filtrado, depto_seleccionado, rango_fechas)
    """
    st.sidebar.header("🔍 Filtros")

    # Filtro por departamento
    departamentos = sorted(df["departamento"].dropna().unique())
    depto_seleccionado = st.sidebar.multiselect(
        "Departamento", 
        departamentos, 
        default=departamentos
    )

    # Filtro por fecha
    rango_fechas = None
    if "fecha_reporte" in df.columns:
        fecha_min = df["fecha_reporte"].min()
        fecha_max = df["fecha_reporte"].max()
        rango_fechas = st.sidebar.date_input(
            "Rango de Fechas", 
            [fecha_min, fecha_max]
        )

        # Aplicar filtros
        df_filtrado = df[
            (df["departamento"].isin(depto_seleccionado)) &
            (df["fecha_reporte"] >= pd.to_datetime(rango_fechas[0])) &
            (df["fecha_reporte"] <= pd.to_datetime(rango_fechas[1]))
        ]
    else:
        df_filtrado = df[df["departamento"].isin(depto_seleccionado)]

    return df_filtrado, depto_seleccionado, rango_fechas

# =============================================================================
# FUNCIONES DE PÁGINAS
# =============================================================================

def render_inicio_page():
    """Renderiza la página de inicio con información del proyecto."""
    
    # Título principal
    st.title("🔥 Fénix Boyacá - Dashboard de Incendios Forestales")
    st.markdown("---")
    
    # Información del proyecto y contexto
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="section-header">
            <h3>📋 Información del Proyecto</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        **Área de aplicación:** Ambiental  
        **Modalidad:** Virtual  
        **Nivel:** Integrador  
        **Ubicación:** Bogotá, Cundinamarca
        """)
        
        st.markdown("**👨‍🏫 Tutores:**")
        st.markdown("""
        • Abel Fernando Becerra Carrillo  
        • Ronal Francisco Coral Prado  
        • Omar Camilo Quesada Carreño
        """)
        
        st.markdown("**👩‍💻 Autora:** Paula Andrea Acuña Merlano")
    
    with col2:
        st.markdown("""
        <div class="section-header">
            <h3>🌿 Contexto del Problema</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        En Boyacá, los incendios forestales destruyen **miles de hectáreas** de cobertura vegetal cada año. 
        
        Aunque existen datos en entidades como **Corpoboyacá**, la información está:
        • Dispersa
        • Poco visualizada  
        • Difícil de analizar
        
        Esto impide una **toma de decisiones rápida y efectiva**.
        """)
    
    # Solución Propuesta
    st.markdown("""
    <div class="section-header">
        <h3>💡 Solución Propuesta</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    **Fénix Boyacá** es una aplicación web interactiva desarrollada en **Python y Streamlit** que integra datos abiertos de incendios forestales para ofrecer:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        🔍 **Visualizaciones Interactivas**
        • Por municipio
        • Por fecha
        • Por tipo de cobertura afectada
        """)
    
    with col2:
        st.markdown("""
        📊 **Indicadores Clave (KPI)**
        • Gestión del riesgo
        • Análisis de patrones
        • Zonas críticas
        """)
    
    with col3:
        st.markdown("""
        🎯 **Centralización de Datos**
        • Datos dispersos en un solo dashboard
        • Accesible y fácil de interpretar
        • Toma de decisiones informada
        """)
    
    # Beneficios del Proyecto
    st.markdown("""
    <div class="section-header">
        <h3>✅ Beneficios del Proyecto</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ✅ **Mejora la toma de decisiones** basada en evidencia  
        ✅ **Facilita la rendición de cuentas** con visualizaciones claras  
        ✅ **Identifica puntos críticos** y tendencias históricas  
        ✅ **Optimiza la planeación territorial** y la prevención de riesgos
        """)
    
    with col2:
        st.markdown("""
        🚀 **Fénix Boyacá** no solo será una herramienta de análisis, sino un **aliado estratégico** para la gestión ambiental, fortaleciendo:
        
        • La **prevención** de incendios
        • La **respuesta** efectiva
        • La **transparencia** en la administración pública
        • La **participación ciudadana**
        """)
    
    # Documentación del Proyecto
    st.markdown("""
    <div class="section-header">
        <h3>📚 Documentación del Proyecto</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FF6B35 0%, #FF8C00 100%); padding: 15px; border-radius: 10px; margin: 10px 0;">
            <h4 style="color: white; text-align: center; margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
                📊 Presentación del Proyecto
            </h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        **🎯 Presentación en Canva:**
        
        [Ver Presentación PPT](https://www.canva.com/design/DAGvz0aK4Tw/_VW9040Su3BI-FttTMwr5g/edit?utm_content=DAGvz0aK4Tw&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
        
        Incluye:
        • Resumen ejecutivo del proyecto
        • Metodología y cronograma
        • Análisis de estado del arte
        • Beneficios y resultados esperados
        """)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FF8C00 0%, #FFA500 100%); padding: 15px; border-radius: 10px; margin: 10px 0;">
            <h4 style="color: white; text-align: center; margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
                📄 Informe Técnico
            </h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        **📋 Informe Detallado:**
        
        [Ver Informe Completo](https://docs.google.com/document/d/1BvTtdorHL_o2Ynl1i74C6GqnKlAQCbgd/edit?usp=sharing&ouid=101862213845686051579&rtpof=true&sd=true)
        
        Contiene:
        • Análisis técnico completo
        • Metodología detallada
        • Resultados y conclusiones
        • Recomendaciones específicas
        """)
    
    # Estado del Arte
    st.markdown("""
    <div class="section-header">
        <h3>📚 Estado del Arte</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Se analizaron **3 herramientas** existentes para la gestión de incendios forestales:
    """)
    
    estado_arte_data = {
        'Herramienta': [
            'FIRMS (NASA)',
            'EFFIS (Comisión Europea)'
        ],
        'Características': [
            'Detección satelital global',
            'Monitoreo europeo'
        ],
        'Tipo': ['Indirecto', 'Indirecto']
    }
    
    df_estado_arte = pd.DataFrame(estado_arte_data)
    st.dataframe(df_estado_arte, use_container_width=True)
    
    # Riesgos e Impacto
    st.markdown("""
    <div class="section-header">
        <h3>⚠️ Riesgos e Impacto</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="subsection-header">
            <h4>🚨 Riesgos Identificados</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ⚠️ **Datos incompletos** o desactualizados  
        ⚠️ **Cambios en requerimientos** del cliente  
        ⚠️ **Procesos manuales** que puedan generar retrasos  
        ⚠️ **Problemas técnicos** de software o conexión
        """)
    
    with col2:
        st.markdown("""
        <div class="subsection-header">
            <h4>🎯 Impacto Esperado</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        🚀 **Fénix Boyacá** no solo será una herramienta de análisis, sino un **aliado estratégico** para la gestión ambiental, fortaleciendo:
        
        • La **prevención** de incendios
        • La **respuesta** efectiva
        • La **transparencia** en la administración pública
        • La **participación ciudadana**
        """)

def render_tablas_page():
    """Renderiza la página de tablas con datos procesados."""
    
    st.title("📊 Tablas de Datos")
    st.markdown("---")
    
    # Cargar datos
    df = load_data()
    
    if df.empty:
        st.warning("No se encontraron datos.")
        return
    
    # Crear filtros
    df_filtrado, depto_seleccionado, rango_fechas = create_filters(df)
    
    # Procesar datos
    df_processed = process_data_types(df)
    
    # Mostrar tablas
    st.subheader("📄 Datos filtrados sin valores nulos")
    st.dataframe(df_filtrado)
    
    st.subheader("📄 Datos finales procesados")
    st.dataframe(df_processed)
    
    # Tabla resumen por tipo de cobertura vegetal
    df_resumen = create_coverage_summary(df_processed)
    
    st.markdown("""
    <div class="section-header">
        <h3>🔥 Tabla Resumen por Tipo de Cobertura Vegetal 🔥</h3>
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(df_resumen)
    
    # Tabla de causas de incendios
    if "causa_del_incendio" in df_filtrado.columns:
        causas_incendio = df_filtrado["causa_del_incendio"].value_counts().head(10).reset_index()
        causas_incendio.columns = ["Causa del Incendio", "Frecuencia"]
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FF6B35 0%, #FF8C00 100%); padding: 10px; border-radius: 8px; margin: 15px 0;">
            <h4 style="color: white; text-align: center; margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
                🔥 Tabla de Causas de Incendios 🔥
            </h4>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(causas_incendio)
    
    # Datos del análisis de correlación
    if "municipio" in df_filtrado.columns and "rea_total_afectada_ha" in df_filtrado.columns:
        datos_municipio = create_correlation_data(df_filtrado)
        
        if not datos_municipio.empty:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #FF6B35 0%, #FF8C00 100%); padding: 10px; border-radius: 8px; margin: 15px 0;">
                <h4 style="color: white; text-align: center; margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
                    🔥 Datos del Análisis de Correlación 🔥
                </h4>
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(datos_municipio)

def process_data_types(df):
    """Procesa los tipos de datos del DataFrame."""
    
    # Conversión de fechas
    date_columns = ['fecha_del_reporte', 'fecha_de_inicio', 'fecha_de_finalizaci_n']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Conversión de horas
    time_columns = ['hora_de_inicio', 'hora_de_finalizaci_n']
    for col in time_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format='%H:%M', errors='coerce').dt.time
    
    # Conversión de strings
    string_columns = ['municipio', 'tipo_de_incendio', 'causa_del_incendio', 'estado']
    for col in string_columns:
        if col in df.columns:
            df[col] = df[col].astype(str)
    
    # Conversión de booleanos
    if 'localizado_dentro_de_rea' in df.columns:
        df['localizado_dentro_de_rea'] = df['localizado_dentro_de_rea'].astype(bool)
    
    # Conversión de numéricos
    numeric_columns = [
        'tejido_urbano_contin_o_ha', 'tejido_urbano_discontinuo', 'zonas_industriales_o',
        'red_vial_ferroviaria_y', 'zonas_portuarias_ha', 'aeropuertos_ha',
        'obras_hidr_ulicas_ha', 'zonas_de_extracci_n_minera', 'zonas_de_disposici_n_de',
        'zonas_verdes_urbanas_y_o', 'instalaciones_recreativas', 'otros_cultivos_transitorios',
        'cereales_ha', 'oleaginosas_y_leguminosas', 'hortalizas_ha', 'tub_rculos_ha',
        'otros_cultivos_permanentes', 'ca_a_ha', 'pl_tano_y_banano_ha', 'tabaco_ha',
        'papaya_ha', 'amapola_ha', 'otros_cultivos_permanentes_1', 'caf_ha', 'cacao_ha',
        'vi_edos_ha', 'otros_cultivos_permanentes_2', 'palma_de_aceite_ha', 'c_tricos_ha',
        'mango_ha', 'cultivos_agroforestales_ha', 'cultivos_confinados_ha',
        'pastos_limpios_ha', 'pastos_arbolados_ha', 'pastos_enmalezados_ha',
        'mosaico_de_cultivos_ha', 'mosaico_de_pastos_y_cultivos', 'mosaico_de_cultivos_pastos',
        'mosaico_de_pastos_con_espacios', 'mosaico_de_cultivos_con', 'bosque_denso_alto_de_tierra',
        'bosque_denso_alto_inundable', 'bosque_denso_bajo_de_tierra', 'bosque_denso_bajo_inundable',
        'bosque_abierto_alto_de_tierra', 'bosque_abierto_alto_inundable', 'bosque_abierto_bajo_de_tierra',
        'bosque_abierto_bajo_inundable', 'bosque_fragmentado_ha', 'bosque_de_galer_a_o_ripario',
        'acacia_ha', 'araucaria_ha', 'caucho_ha', 'ceiba_ha', 'cipr_s_ha', 'eucalipto_ha',
        'flormorado_ha', 'guadua_plantada_ha', 'melina_ha', 'nogal_ha', 'pino_ha', 'teca_ha',
        'herbazal_denso_de_tierra', 'herbazal_denso_de_tierra_1', 'herbazal_denso_de_tierra_2',
        'herbazal_denso_inundable', 'herbazal_denso_inundable_1', 'arracachal_ha', 'helechal_ha',
        'herbazal_abierto_arenoso', 'herbazal_abierto_rocoso_ha', 'arbustal_denso_ha', 'arbustal_abierto_ha',
        'vegetaci_n_secundaria_o_en', 'zonas_arenosas_naturales', 'afloramientos_rocosos_ha',
        'tierras_desnudas_y_degradadas', 'zonas_quemadas_ha', 'zonas_glaciares_y_nivales',
        'zonas_pantanosas_ha', 'turberas_ha', 'vegetaci_n_acu_tica_sobre', 'pantanos_costeros_ha',
        'salitral_ha', 'sedimentos_expuestos_en_baja', 'bosque_natural_denso_ha', 'bosque_intervenido_ha',
        'bosque_plantado_ha', 'bosque_seco_ha', 'cultivos_ha', 'paramos_ha', 'sabanas_y_pastizales_ha',
        'pastos_mejorados_ha', 'rastrojos_ha', 'vegetaci_n_seca_ha', 'sabanas_pastizales_ha',
        'pastos_manejados_ha', 'coberturas_sin_determinar', 'rea_total_afectada_ha',
        'altura_minima_en_m_s_n_m', 'altura_maxima_en_m_s_n_m'
    ]
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Eliminar columnas innecesarias
    columnas_a_eliminar = ['observaciones', 'consecutivo', 'entidad', 'departamento']
    df = df.drop(columns=[col for col in columnas_a_eliminar if col in df.columns])
    
    return df

def create_coverage_summary(df):
    """Crea el resumen por tipo de cobertura vegetal."""
    
    resumen = {
        "Bosques": df[[
            'bosque_denso_alto_de_tierra', 'bosque_denso_alto_inundable', 'bosque_denso_bajo_de_tierra',
            'bosque_denso_bajo_inundable', 'bosque_abierto_alto_de_tierra', 'bosque_abierto_alto_inundable',
            'bosque_abierto_bajo_de_tierra', 'bosque_abierto_bajo_inundable', 'bosque_fragmentado_ha',
            'bosque_de_galer_a_o_ripario', 'bosque_natural_denso_ha', 'bosque_intervenido_ha',
            'bosque_plantado_ha', 'bosque_seco_ha'
        ]].sum().sum(),

        "Cultivos": df[[
            'cultivos_ha', 'otros_cultivos_transitorios', 'cereales_ha', 'oleaginosas_y_leguminosas',
            'hortalizas_ha', 'tub_rculos_ha', 'otros_cultivos_permanentes', 'caf_ha', 'cacao_ha',
            'ca_a_ha', 'pl_tano_y_banano_ha', 'tabaco_ha', 'palma_de_aceite_ha', 'papaya_ha',
            'mango_ha', 'cultivos_agroforestales_ha', 'cultivos_confinados_ha'
        ]].sum().sum(),

        "Pastos": df[[
            'pastos_limpios_ha', 'pastos_arbolados_ha', 'pastos_enmalezados_ha',
            'mosaico_de_pastos_y_cultivos', 'mosaico_de_cultivos_pastos', 'mosaico_de_pastos_con_espacios',
            'pastos_mejorados_ha', 'pastos_manejados_ha', 'sabanas_y_pastizales_ha', 'sabanas_pastizales_ha'
        ]].sum().sum(),

        "Zonas urbanas": df[[
            'tejido_urbano_contin_o_ha', 'tejido_urbano_discontinuo', 'zonas_industriales_o',
            'zonas_portuarias_ha', 'aeropuertos_ha', 'zonas_de_disposici_n_de',
            'zonas_verdes_urbanas_y_o', 'instalaciones_recreativas'
        ]].sum().sum(),

        "Otras coberturas": df[[
            'zonas_quemadas_ha', 'paramos_ha', 'vegetaci_n_seca_ha', 'vegetaci_n_acu_tica_sobre',
            'tierras_desnudas_y_degradadas', 'afloramientos_rocosos_ha'
        ]].sum().sum()
    }
    
    return pd.DataFrame(list(resumen.items()), columns=['tipo_de_cobertura', 'area_total_ha'])

def create_correlation_data(df):
    """Crea los datos para el análisis de correlación."""
    
    # Asegurar que la columna de hectáreas sea numérica
    df["rea_total_afectada_ha"] = pd.to_numeric(df["rea_total_afectada_ha"], errors="coerce")
    
    # Filtrar solo registros con datos válidos de hectáreas
    df_validos = df.dropna(subset=["rea_total_afectada_ha"])
    
    if df_validos.empty:
        return pd.DataFrame()
    
    # Agregar datos por municipio
    datos_municipio = df_validos.groupby("municipio").agg({
        "rea_total_afectada_ha": ["sum", "mean", "count"],
        "causa_del_incendio": lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else "No especificada"
    }).reset_index()
    
    # Renombrar columnas
    datos_municipio.columns = ["Municipio", "Total_Hectareas", "Promedio_Hectareas", "Numero_Incendios", "Causa_Mas_Frecuente"]
    
    # Filtrar municipios con al menos 1 incendio y datos válidos
    datos_municipio = datos_municipio[
        (datos_municipio["Numero_Incendios"] > 0) & 
        (datos_municipio["Total_Hectareas"] > 0)
    ].sort_values("Numero_Incendios", ascending=False)
    
    return datos_municipio

def render_dashboard_page():
    """Renderiza la página del dashboard con visualizaciones."""
    
    st.title("📊 Dashboard de Incendios Forestales")
    st.markdown("---")
    
    # Cargar datos
    df = load_data()
    
    if df.empty:
        st.warning("No se encontraron datos.")
        return
    
    # Crear filtros
    df_filtrado, depto_seleccionado, rango_fechas = create_filters(df)
    
    # Procesar datos
    df_processed = process_data_types(df)
    
    # Crear resumen para gráficos
    df_resumen = create_coverage_summary(df_processed)
    
    # KPIs principales
    render_kpis(df_filtrado)
    
    # Layout principal - Mapa en la parte superior
    st.markdown("---")
    
    # Mapa de calor - Ocupa toda la parte superior
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FF4500 0%, #FF6B35 100%); padding: 15px; border-radius: 10px; margin: 20px 0;">
        <h3 style="color: white; text-align: center; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
            🗺️ Mapa de Calor: Frecuencia de Incendios por Municipio
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Renderizar mapa
    render_heatmap(df_filtrado)
    

    # Cuadrícula 2x2 para los gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        render_coverage_chart(df_resumen)
    
    with col2:
        render_top_municipios_chart(df_filtrado)
    
    # Segunda fila de la cuadrícula
    col3, col4 = st.columns(2)
    
    with col3:
        render_causes_chart(df_filtrado)
    
    with col4:
        render_correlation_chart(df_filtrado)

def render_kpis(df_filtrado):
    """Renderiza los KPIs principales."""
    
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    
    with col_kpi1:
        total_incendios = len(df_filtrado)
        st.metric(
            label="🔥 Total Incendios",
            value=f"{total_incendios:,}",
            delta="registros"
        )
    
    with col_kpi2:
        if 'rea_total_afectada_ha' in df_filtrado.columns:
            # Convertir a numérico y sumar
            total_hectareas = pd.to_numeric(df_filtrado['rea_total_afectada_ha'], errors='coerce').sum()
            # Verificar si es NaN y convertir a 0
            if pd.isna(total_hectareas):
                total_hectareas = 0
            value_display = f"{total_hectareas:,.0f}"
        else:
            total_hectareas = 0
            value_display = "0"
        
        st.metric(
            label="🌿 Hectáreas Afectadas",
            value=value_display,
            delta="hectáreas totales"
        )
    
    with col_kpi3:
        if 'departamento' in df_filtrado.columns:
            deptos_unicos = df_filtrado['departamento'].nunique()
            st.metric(
                label="🏛️ Departamentos",
                value=deptos_unicos,
                delta="afectados"
            )
        else:
            st.metric(
                label="🏛️ Departamentos",
                value="No disponible",
                delta="sin datos"
            )
    
    with col_kpi4:
        if 'municipio' in df_filtrado.columns:
            municipio_max = df_filtrado['municipio'].mode().iloc[0] if len(df_filtrado['municipio'].mode()) > 0 else "No especificado"
            st.metric(
                label="📍 Municipio Crítico",
                value=municipio_max,
                delta="más afectado"
            )
        else:
            st.metric(
                label="📍 Municipio Crítico",
                value="No disponible",
                delta="sin datos"
            )

def render_heatmap(df_filtrado):
    """Renderiza el mapa de calor."""
    
    try:
        coordenadas_df = pd.read_csv("coordenadas_municipios.csv")
        
        # Contar incendios por municipio
        if "municipio" in df_filtrado.columns:
            incendios_por_municipio = df_filtrado["municipio"].value_counts().reset_index()
            incendios_por_municipio.columns = ["municipio", "frecuencia_incendios"]
            
            # Normalizar nombres de municipios para hacer el merge
            incendios_por_municipio["municipio_normalizado"] = incendios_por_municipio["municipio"].str.upper().str.strip()
            coordenadas_df["municipio_normalizado"] = coordenadas_df["municipio"].str.upper().str.strip()
            
            # Hacer merge con las coordenadas
            mapa_data = pd.merge(
                incendios_por_municipio, 
                coordenadas_df, 
                on="municipio_normalizado", 
                how="inner"
            )
            
            if not mapa_data.empty:
                # Renombrar columnas después del merge para evitar conflictos
                if 'municipio_x' in mapa_data.columns:
                    mapa_data = mapa_data.rename(columns={'municipio_x': 'municipio'})
                if 'municipio_y' in mapa_data.columns:
                    mapa_data = mapa_data.drop(columns=['municipio_y'])
                
                # Verificar que todas las columnas necesarias existan
                columnas_requeridas = ["municipio", "lat", "lon", "frecuencia_incendios", "departamento"]
                columnas_faltantes = [col for col in columnas_requeridas if col not in mapa_data.columns]
                
                if columnas_faltantes:
                    st.error(f"❌ Faltan columnas necesarias: {columnas_faltantes}")
                    st.write("Columnas disponibles:", list(mapa_data.columns))
                else:
                    # Crear mapa de calor con Plotly
                    fig_mapa = px.density_map(
                        mapa_data,
                        lat="lat",
                        lon="lon",
                        z="frecuencia_incendios",
                        hover_name="municipio",
                        hover_data=["frecuencia_incendios", "departamento"],
                        zoom=7,
                        center={"lat": 5.5, "lon": -73.5},
                        map_style="carto-darkmatter",
                        title="🔥 Frecuencia de Incendios por Municipio",
                        color_continuous_scale="Reds",
                        range_color=[0, mapa_data["frecuencia_incendios"].max()]
                    )
                    
                    fig_mapa.update_layout(
                        height=500,
                        margin={"r": 0, "t": 50, "l": 0, "b": 0},
                        title_x=0.5,
                        title_font_size=16
                    )
                    
                    st.plotly_chart(fig_mapa, use_container_width=True)
                    
                    # Estadísticas del mapa en columnas
                    col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
                    
                    with col_stats1:
                        st.metric(
                            label="Municipios Mapeados",
                            value=len(mapa_data),
                            delta=f"de {len(incendios_por_municipio)} totales"
                        )
                    
                    with col_stats2:
                        st.metric(
                            label="Mayor Frecuencia",
                            value=mapa_data['frecuencia_incendios'].max(),
                            delta="incendios"
                        )
                    
                    with col_stats3:
                        promedio_frecuencia = mapa_data['frecuencia_incendios'].mean()
                        if pd.isna(promedio_frecuencia):
                            st.metric(
                                label="Promedio",
                                value="N/A",
                                delta="incendios/municipio"
                            )
                        else:
                            st.metric(
                                label="Promedio",
                                value=f"{promedio_frecuencia:.1f}",
                                delta="incendios/municipio"
                            )
                    
                    with col_stats4:
                        municipio_max = mapa_data.loc[mapa_data['frecuencia_incendios'].idxmax(), 'municipio']
                        st.metric(
                            label="Municipio Crítico",
                            value=municipio_max,
                            delta="más afectado"
                        )
            else:
                st.info("No hay datos de coordenadas disponibles para el mapa")
        else:
            st.info("No hay datos de municipios para crear el mapa")
            
    except FileNotFoundError:
        st.info("📁 Archivo de coordenadas no encontrado")
    except Exception as e:
        st.error(f"❌ Error al cargar el mapa: {str(e)}")

def render_coverage_chart(df_resumen):
    """Renderiza el gráfico de cobertura vegetal."""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FF6B35 0%, #FF8C00 100%); padding: 10px; border-radius: 8px; margin: 10px 0;">
        <h4 style="color: white; text-align: center; margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
            🌿 Distribución de Cobertura Vegetal
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Paleta de colores temática de fuego
    colores = ['#FF4500', '#FF6B35', '#FF8C00', '#FFA500', '#FF6347', '#DC143C', '#B22222']

    # Crear figura con mejor proporción y resolución
    fig, ax = plt.subplots(figsize=(10, 8), dpi=100)
    
    # Calcular porcentajes para mostrar solo los más relevantes
    total = df_resumen['area_total_ha'].sum()
    porcentajes = (df_resumen['area_total_ha'] / total * 100).round(1)
    
    # Filtrar solo categorías con más del 1% del total
    df_filtrado_grafico = df_resumen[porcentajes > 1].copy()
    if len(df_filtrado_grafico) == 0:
        df_filtrado_grafico = df_resumen.head(5)

    # Graficar pastel tipo dona mejorado
    wedges, texts, autotexts = ax.pie(
        df_filtrado_grafico['area_total_ha'],
        labels=df_filtrado_grafico['tipo_de_cobertura'],
        colors=colores[:len(df_filtrado_grafico)],
        startangle=90,
        wedgeprops=dict(width=0.6, edgecolor='white', linewidth=2),
        textprops=dict(color="black", fontsize=11, fontweight='bold'),
        autopct='%1.1f%%',
        pctdistance=0.85
    )

    # Mejorar la apariencia de los textos
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)

    # Centrar el gráfico
    ax.axis('equal')
    ax.set_title("Distribución de Cobertura Vegetal Afectada", fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    
    st.pyplot(fig, use_container_width=True)

def render_top_municipios_chart(df_filtrado):
    """Renderiza el gráfico de top municipios."""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FF8C00 0%, #FFA500 100%); padding: 10px; border-radius: 8px; margin: 10px 0;">
        <h4 style="color: white; text-align: center; margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
            📈 Top 10 Municipios con Más Incendios
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Crear gráfica de barras para municipios
    if "municipio" in df_filtrado.columns:
        top_municipios = df_filtrado["municipio"].value_counts().head(10).reset_index()
        top_municipios.columns = ["Municipio", "Cantidad de Incendios"]
        
        fig_barras = px.bar(
            top_municipios, 
            x="Municipio", 
            y="Cantidad de Incendios",
            color="Cantidad de Incendios",
            color_continuous_scale="Reds",
            title="🔥 Top 10 Municipios"
        )
        
        fig_barras.update_layout(
            xaxis_tickangle=-45,
            height=400,
            showlegend=False,
            title_font_size=14
        )
        
        st.plotly_chart(fig_barras, use_container_width=True)
    else:
        st.info("No hay datos de municipios disponibles")

def render_causes_chart(df_filtrado):
    """Renderiza el gráfico de causas de incendios."""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FF4500 0%, #FF6B35 100%); padding: 10px; border-radius: 8px; margin: 10px 0;">
        <h4 style="color: white; text-align: center; margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
            🔥 Top 8 Causas de Incendios
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    if "causa_del_incendio" in df_filtrado.columns:
        # Contar las causas más frecuentes
        causas_incendio = df_filtrado["causa_del_incendio"].value_counts().head(8).reset_index()
        causas_incendio.columns = ["Causa del Incendio", "Frecuencia"]
        
        # Crear gráfica de barras para causas
        fig_causas = px.bar(
            causas_incendio, 
            x="Causa del Incendio", 
            y="Frecuencia",
            color="Frecuencia",
            color_continuous_scale="Reds",
            title="🔥 Top 8 Causas"
        )
        
        fig_causas.update_layout(
            xaxis_tickangle=-45,
            height=400,
            showlegend=False,
            title_font_size=14
        )
        
        st.plotly_chart(fig_causas, use_container_width=True)
    else:
        st.info("No hay datos de causas disponibles")

def render_correlation_chart(df_filtrado):
    """Renderiza el gráfico de correlación."""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FF6B35 0%, #FF8C00 100%); padding: 10px; border-radius: 8px; margin: 10px 0;">
        <h4 style="color: white; text-align: center; margin: 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
            📊 Correlación: Incendios vs Hectáreas
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    if "municipio" in df_filtrado.columns and "rea_total_afectada_ha" in df_filtrado.columns:
        # Asegurar que la columna de hectáreas sea numérica
        df_filtrado["rea_total_afectada_ha"] = pd.to_numeric(df_filtrado["rea_total_afectada_ha"], errors="coerce")
        
        # Filtrar solo registros con datos válidos de hectáreas
        df_validos = df_filtrado.dropna(subset=["rea_total_afectada_ha"])
        
        if not df_validos.empty:
            # Agregar datos por municipio
            datos_municipio = df_validos.groupby("municipio").agg({
                "rea_total_afectada_ha": ["sum", "mean", "count"],
                "causa_del_incendio": lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else "No especificada"
            }).reset_index()
        
            # Renombrar columnas
            datos_municipio.columns = ["Municipio", "Total_Hectareas", "Promedio_Hectareas", "Numero_Incendios", "Causa_Mas_Frecuente"]
            
            # Filtrar municipios con al menos 1 incendio y datos válidos
            datos_municipio = datos_municipio[
                (datos_municipio["Numero_Incendios"] > 0) & 
                (datos_municipio["Total_Hectareas"] > 0)
            ].sort_values("Numero_Incendios", ascending=False)
            
            if not datos_municipio.empty and len(datos_municipio) > 1:
                # Crear diagrama de dispersión simplificado
                fig_dispersion = px.scatter(
                    datos_municipio.head(15),  # Solo top 15 para mejor visualización
                    x="Numero_Incendios",
                    y="Total_Hectareas",
                    size="Promedio_Hectareas",
                    color="Causa_Mas_Frecuente",
                    hover_name="Municipio",
                    title="🔥 Correlación: Incendios vs Hectáreas",
                    color_discrete_sequence=px.colors.sequential.Reds
                )
                
                fig_dispersion.update_layout(
                    height=400,
                    title_font_size=14,
                    showlegend=False
                )
                
                st.plotly_chart(fig_dispersion, use_container_width=True)
                
                # Calcular correlación
                correlacion = datos_municipio["Numero_Incendios"].corr(datos_municipio["Total_Hectareas"])
                
                # Métricas de correlación
                st.markdown("**📊 Métricas de Correlación:**")
                st.markdown(f"• **Coeficiente:** {correlacion:.3f}")
                st.markdown(f"• **Municipios analizados:** {len(datos_municipio)}")
                
                # Interpretación rápida
                if correlacion > 0.5:
                    st.success("🔴 Correlación positiva fuerte")
                elif correlacion > 0.2:
                    st.warning("🟡 Correlación positiva moderada")
                else:
                    st.info("🟢 Correlación débil")
            else:
                st.info("Datos insuficientes para correlación")
        else:
            st.info("No hay datos válidos para análisis")
    else:
        st.info("Faltan datos para análisis de correlación")

def render_analisis_page():
    """Renderiza la página de análisis avanzado."""
    
    st.title("📈 Análisis Avanzado")
    st.markdown("---")
    
    # Análisis de los datos del dashboard
    st.markdown("""
    <div class="section-header">
        <h3>📊 Análisis de los Datos del Dashboard</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    A continuación se presenta un análisis detallado de los principales hallazgos obtenidos de la visualización de datos de incendios forestales en Boyacá:
    """)
    
    # Análisis 1: Distribución de Cobertura Vegetal
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FF6B35 0%, #FF8C00 100%); padding: 15px; border-radius: 10px; margin: 20px 0;">
        <h4 style="color: white; text-align: center; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
            🌿 1. Distribución de Cobertura Vegetal Afectada
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    La gráfica de dona muestra que el **92,6%** de las áreas afectadas corresponden a **pastos**, lo que evidencia que la mayoría de los incendios impactan zonas abiertas utilizadas probablemente para ganadería o agricultura. 
    
    Las **zonas urbanas** representan un **4,5%** y los **bosques** un **2,8%**, lo que, aunque menor, sigue siendo preocupante por su valor ambiental.
    """)
    
    # Análisis 2: Top Municipios
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FF8C00 0%, #FFA500 100%); padding: 15px; border-radius: 10px; margin: 20px 0;">
        <h4 style="color: white; text-align: center; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
            📍 2. Top 10 Municipios con Más Incendios
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    En este ranking, el municipio con más casos registrados lidera con una diferencia notable frente a los demás. **Sogamoso, Samacá** y otros municipios del centro de Boyacá aparecen en los primeros lugares, lo que indica que hay **zonas específicas con mayor recurrencia de incendios** y podrían requerir estrategias de prevención más focalizadas.
    """)
    
    # Análisis 3: Causas de Incendios
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FF4500 0%, #FF6B35 100%); padding: 15px; border-radius: 10px; margin: 20px 0;">
        <h4 style="color: white; text-align: center; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
            🔥 3. Top 8 Causas de Incendios
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    La **quema de cobertura vegetal** es la causa más común, superando ampliamente a las demás, lo que sugiere un origen mayormente **humano** y posiblemente ligado a prácticas agropecuarias. Le siguen los incendios **intencionales** y **accidentales**, y en menor medida causas como descuido y origen desconocido.
    """)
    
    # Análisis 4: Correlación
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FF6B35 0%, #FF8C00 100%); padding: 15px; border-radius: 10px; margin: 20px 0;">
        <h4 style="color: white; text-align: center; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
            📊 4. Correlación: Incendios vs Hectáreas
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    El diagrama de dispersión refleja que, en general, a mayor número de incendios se incrementa el área afectada, aunque hay casos puntuales con **pocos incendios pero gran cantidad de hectáreas quemadas**. Esto sugiere que no solo importa la cantidad de eventos, sino también su **magnitud e intensidad**.
    """)
    
    # Conclusiones y recomendaciones
    st.markdown("""
    <div class="section-header">
        <h3>💡 Conclusiones y Recomendaciones</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎯 Principales Hallazgos:**
        
        • Los incendios afectan principalmente zonas de pastos (92,6%)
        • Hay municipios específicos con mayor recurrencia
        • La causa principal es la quema de cobertura vegetal
        • Existe correlación entre número de incendios y área afectada
        """)
    
    with col2:
        st.markdown("""
        **🚨 Recomendaciones:**
        
        • Implementar estrategias focalizadas en municipios críticos
        • Fortalecer controles sobre prácticas agropecuarias
        • Desarrollar campañas de prevención específicas
        • Mejorar sistemas de detección temprana
        """)
    
    # Funcionalidades futuras
    st.markdown("""
    <div class="section-header">
        <h3>🔮 Funcionalidades Futuras</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📈 Análisis Avanzado:**
        • Análisis de tendencias temporales
        • Predicción de incendios
        • Análisis de clusters geográficos
        • Modelos de machine learning
        • Análisis de patrones estacionales
        • Correlación con variables climáticas
        """)
    
    with col2:
        st.markdown("""
        **📊 Métricas Avanzadas:**
        • Índice de riesgo por municipio
        • Análisis de vulnerabilidad
        • Predicción de áreas críticas
        • Análisis de impacto económico
        • Modelos de propagación
        • Análisis de eficiencia de respuesta
        """)

# =============================================================================
# INICIALIZACIÓN DE LA APLICACIÓN
# =============================================================================

# Cargar estilos CSS
load_custom_css()

# Cargar logo
try:
    logo = Image.open("BOYACA.png")
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    st.image(logo, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("⚠️ No se encontró el archivo BOYACA.png")

# Menú de navegación
menu = st.sidebar.radio(
    "Navegación", 
    ["Inicio", "Dashboard", "Tablas", "Análisis"]
)

# =============================================================================
# NAVEGACIÓN PRINCIPAL
# =============================================================================

if menu == "Inicio":
    render_inicio_page()

elif menu == "Tablas":
    render_tablas_page()

elif menu == "Dashboard":
    render_dashboard_page()

elif menu == "Análisis":
    render_analisis_page()

        

        

