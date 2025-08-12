# 🔥 Dashboard de Incendios de Cobertura Vegetal - Fénix Boyacá

## 📋 Descripción

Este dashboard interactivo desarrollado en Python y Streamlit analiza datos de incendios forestales en Boyacá, Colombia. Proporciona visualizaciones interactivas, análisis de patrones y mapas de calor para mejorar la toma de decisiones ambientales.

## 🚀 Características Principales

- **Mapa de Calor Interactivo**: Visualización de la frecuencia de incendios por municipio
- **Análisis de Cobertura Vegetal**: Distribución de áreas afectadas por tipo de cobertura
- **Análisis de Causas**: Identificación de las causas más frecuentes de incendios
- **Correlación Espacial**: Análisis de la relación entre número de incendios y hectáreas afectadas
- **Filtros Dinámicos**: Por departamento, fecha y tipo de cobertura
- **KPIs en Tiempo Real**: Indicadores clave de rendimiento

## 📦 Instalación

1. **Clonar o descargar el proyecto**
2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Asegurar que los archivos estén en el directorio**:
   - `app.py` (aplicación principal)
   - `coordenadas_municipios.csv` (coordenadas geográficas)
   - `BOYACA.png` (logo del proyecto)
   - `requirements.txt` (dependencias)

## 🎯 Uso

1. **Ejecutar la aplicación**:
   ```bash
   streamlit run app.py
   ```

2. **Abrir en el navegador**: La aplicación se abrirá automáticamente en `http://localhost:8501`

3. **Navegar por las secciones**:
   - **Inicio**: Información del proyecto y datos sin procesar
   - **Dashboard**: Visualizaciones interactivas y análisis

## 🗺️ Funcionalidades del Mapa de Calor

### Mapa de Plotly
- Visualización de densidad de incendios por municipio
- Escala de colores roja (mayor frecuencia = más intenso)
- Información detallada al hacer hover

### Mapa de Folium
- Marcadores circulares con radio proporcional a la frecuencia
- Colores por percentiles de frecuencia:
  - 🔴 Rojo: Alta frecuencia (80% superior)
  - 🟠 Naranja: Media-alta frecuencia (60-80%)
  - 🟡 Amarillo: Media frecuencia (40-60%)
  - 🟢 Verde: Baja frecuencia (<40%)
- Popups informativos con detalles del municipio

## 📊 Datos Utilizados

- **Fuente principal**: Datos abiertos de Colombia (datos.gov.co)
- **Dataset**: Incendios de cobertura vegetal
- **Coordenadas**: Archivo CSV con latitud y longitud de municipios de Boyacá

## 🛠️ Tecnologías Utilizadas

- **Streamlit**: Framework para aplicaciones web
- **Pandas**: Manipulación y análisis de datos
- **Plotly**: Visualizaciones interactivas
- **Folium**: Mapas interactivos
- **Matplotlib**: Gráficos estáticos
- **Sodapy**: Cliente para datos abiertos

## 📈 KPIs y Métricas

- Total de incendios por período
- Distribución por tipo de cobertura vegetal
- Municipios con mayor frecuencia de incendios
- Causas más frecuentes
- Correlación entre incendios y hectáreas afectadas

## 🔧 Personalización

### Agregar Nuevos Municipios
1. Editar `coordenadas_municipios.csv`
2. Agregar fila con: municipio, departamento, lat, lon, clave

### Modificar Visualizaciones
- Editar parámetros en `app.py`
- Cambiar colores, tamaños y estilos
- Agregar nuevas métricas o gráficos

## 📝 Notas Técnicas

- Los datos se cargan desde la API de datos.gov.co
- El procesamiento incluye limpieza y normalización de datos
- Los mapas se centran en Boyacá (lat: 5.5, lon: -73.5)
- La aplicación maneja errores de conexión y datos faltantes

## 🤝 Contribuciones

Para contribuir al proyecto:
1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Realizar cambios y pruebas
4. Enviar pull request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo LICENSE para más detalles.

## 👥 Autores

- **Paula Andrea Acuña Merlano**
- **Proyecto Fénix Boyacá**
- **Cohorte 6 - Talento Tech 2025 (MinTIC)**

## 📞 Contacto

Para preguntas o soporte técnico, contactar a través de los canales oficiales del proyecto. 