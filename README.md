# 🍽️ EDA interactivo 

Aplicación web interactiva desarrollada con **Streamlit** para realizar un análisis exploratorio (EDA) de una encuesta de 200 clientes de restaurantes en Nueva York.

La app permite filtrar los datos, explorar el perfil del cliente, analizar preferencias gastronómicas, comparar valoraciones de comida y servicio, y estudiar relaciones entre variables.

---

## 📁 Estructura del proyecto

```text
restaurant-eda-app/
├── app.py               # Aplicación Streamlit
├── restaurantes_eda.ipynb # Notebook de análisis exploratorio
├── DatasetP6.xlsx       # Dataset original
├── requirements.txt     # Dependencias
└── README.md            # Documentación
```

---

## 📊 Dataset

El archivo `DatasetP6.xlsx` contiene **200 registros** y **15 columnas**:

| Columna | Descripción |
|---|---|
| `User ID` | Identificador del cliente |
| `Area code` | Código de área |
| `Location` | Ubicación del cliente |
| `Gender` | Género |
| `YOB` | Año de nacimiento |
| `Marital Status` | Estado civil |
| `Activity` | Actividad u ocupación |
| `Budget` | Presupuesto declarado |
| `Cuisines` | Tipo de cocina preferida |
| `Alcohol` | Frecuencia de consumo de alcohol |
| `Smoker` | Hábito de fumar |
| `Food Rating` | Valoración de la comida |
| `Service Rating` | Valoración del servicio |
| `Overall Rating` | Valoración global |
| `Often A S` | Frecuencia de asistencia |

La aplicación crea además la variable derivada:

```python
Age = 2026 - YOB
```

---

## 🧹 Limpieza de datos

El análisis incluye:

- Eliminación de espacios en los nombres de columnas.
- Normalización de la columna `Location` con `strip()` y `title()`.
- Corrección de variantes de ubicación, por ejemplo:
  - `Market City, My` → `Market City, Ny`
  - `Central Park,Ny` → `Central Park, Ny`
- Creación de la columna `Age`.
- Detección de valores atípicos en `Overall Rating`.

En la versión original del dataset, `Overall Rating` contiene valores como `15`, `25`, `35` y `45`, además de la escala esperada de `1` a `5`. La app permite corregirlos opcionalmente dividiéndolos entre 10:

| Valor original | Valor corregido |
|---:|---:|
| 15 | 1 |
| 25 | 2 |
| 35 | 3 |
| 45 | 4 |

---

## 📈 Análisis incluidos

### Resumen general
- Número de clientes filtrados.
- Edad promedio.
- Valoración media de comida, servicio y valoración global.
- Presupuesto promedio.

### Perfil del cliente
- Distribución de edad.
- Distribución por género.
- Estado civil y actividad.

### Preferencias
- Tipos de cocina más elegidos.
- Frecuencia de consumo de alcohol.
- Hábito de fumar.

### Valoraciones
- Distribución de `Overall Rating`.
- Distribución de `Food Rating` y `Service Rating`.
- Valoración global promedio por cocina, ubicación, género, estado civil, alcohol y tabaco.

### Relaciones
- Boxplots de valoraciones y presupuesto según variables categóricas.
- Dispersión entre edad y valoración global.
- Matriz de correlación entre variables numéricas.

---

## 🚀 Instalación y ejecución

### 1. Clonar o descargar el proyecto

```bash
git clone <url-del-repositorio>
cd restaurant-eda-app
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
```

Activar el entorno:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá normalmente en:

```text
http://localhost:8501
```

---

## 📦 Dependencias

```txt
streamlit>=1.40.0
pandas>=2.2.0
numpy>=1.26.0
openpyxl>=3.1.0
matplotlib>=3.8.0
seaborn>=0.13.0
scipy>=1.13.0
```

Plotly no es obligatorio. La aplicación puede funcionar con gráficos nativos de Streamlit o con `matplotlib` y `seaborn`.

---

## 🧪 Notebook EDA

El notebook `restaurantes_eda.ipynb` documenta el análisis paso a paso:

1. Carga y exploración inicial del dataset.
2. Revisión de tipos de datos y valores nulos.
3. Limpieza de columnas y ubicaciones.
4. Creación de la variable `Age`.
5. Análisis univariado.
6. Análisis bivariado.
7. Correlaciones.
8. Conclusiones.

---

## 📌 Conclusiones principales

- El dataset contiene 200 clientes sin valores nulos en las columnas principales.
- La columna `Overall Rating` presenta valores inconsistentes respecto a la escala 1–5.
- Las correlaciones entre `Food Rating`, `Service Rating` y `Overall Rating` son bajas, por lo que no existe una relación lineal fuerte entre ellas.
- La valoración global varía según cocina, ubicación, consumo de alcohol y hábito de fumar.
- La app permite validar estos hallazgos de forma interactiva mediante filtros y visualizaciones.

---

## 📄 Licencia

Este proyecto se distribuye con fines educativos y de análisis de datos.
