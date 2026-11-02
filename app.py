import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="EDA Restaurantes", page_icon="🍽️", layout="wide")

st.title("🍽️ EDA interactivo — Encuesta de restaurantes")
st.caption("Versión sin Plotly, usando gráficos nativos de Streamlit.")

@st.cache_data
def load_data(file):
    df = pd.read_excel(file)
    df.columns = df.columns.str.strip()

    df["Location"] = (
        df["Location"]
        .astype(str)
        .str.strip()
        .str.title()
        .replace({
            "Market City, My": "Market City, Ny",
            "Central Park,Ny": "Central Park, Ny"
        })
    )

    df["Age"] = 2026 - df["YOB"]
    return df

uploaded = st.file_uploader("Sube DatasetP6.xlsx", type=["xlsx"])

if uploaded is None:
    st.info("Sube **DatasetP6.xlsx** para comenzar.")
    st.stop()

df = load_data(uploaded)
df = load_data(uploaded)

# ---------- LIMPIEZA OPCIONAL ----------
st.sidebar.header("🧹 Limpieza")

clean_ratings = st.sidebar.checkbox(
    "Corregir Overall Rating fuera de escala (15→1, 25→2, 35→3, 45→4)",
    value=False
)

if clean_ratings:
    invalid = ~df["Overall Rating"].isin([1, 2, 3, 4, 5])
    n_fixed = invalid.sum()

    df.loc[invalid, "Overall Rating"] = (
        df.loc[invalid, "Overall Rating"] // 10
    )

    st.sidebar.success(f"{n_fixed} valores corregidos.")
# ---------- Filtros ----------
st.sidebar.header("🎛️ Filtros")

def filter_multiselect(frame, column, label):
    options = sorted(frame[column].dropna().unique())
    selected = st.sidebar.multiselect(label, options, default=options)
    return frame[frame[column].isin(selected)] if selected else frame

for col, label in [
    ("Location", "Ubicación"),
    ("Gender", "Género"),
    ("Marital Status", "Estado civil"),
    ("Activity", "Actividad"),
    ("Cuisines", "Cocina"),
    ("Alcohol", "Alcohol"),
    ("Smoker", "Fumador"),
]:
    df = filter_multiselect(df, col, label)

st.sidebar.metric("Clientes filtrados", len(df))

# ---------- KPIs ----------
st.header("📌 Resumen")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Clientes", len(df))
c2.metric("Edad media", f"{df['Age'].mean():.1f}")
c3.metric("Food Rating", f"{df['Food Rating'].mean():.2f}")
c4.metric("Service Rating", f"{df['Service Rating'].mean():.2f}")
c5.metric("Overall Rating", f"{df['Overall Rating'].mean():.2f}")

# ---------- Valoraciones ----------
st.header("📊 Valoraciones")

tab1, tab2, tab3 = st.tabs(["Overall Rating", "Comida y servicio", "Por grupos"])

with tab1:
    counts = df["Overall Rating"].value_counts().sort_index()
    st.bar_chart(counts, use_container_width=True)
    st.caption("Frecuencia de cada valoración global.")

with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.bar_chart(df["Food Rating"].value_counts().sort_index())
        st.caption("Food Rating")

    with col2:
        st.bar_chart(df["Service Rating"].value_counts().sort_index())
        st.caption("Service Rating")

with tab3:
    group_col = st.selectbox(
        "Agrupar Overall Rating por:",
        ["Cuisines", "Location", "Gender", "Marital Status", "Alcohol", "Smoker"]
    )

    grouped = df.groupby(group_col)["Overall Rating"].mean().sort_values(ascending=False)
    st.bar_chart(grouped, use_container_width=True)
    st.caption(f"Overall Rating promedio por {group_col}.")

# ---------- Perfil ----------
st.header("👤 Perfil del cliente")

col1, col2 = st.columns(2)

with col1:
    st.bar_chart(df["Age"].value_counts().sort_index())
    st.caption("Distribución de edad.")

with col2:
    st.bar_chart(df["Gender"].value_counts())
    st.caption("Distribución por género.")

# ---------- Preferencias ----------
st.header("🍜 Preferencias")

col1, col2 = st.columns(2)

with col1:
    st.bar_chart(df["Cuisines"].value_counts())
    st.caption("Cocinas más elegidas.")

with col2:
    st.bar_chart(df["Alcohol"].value_counts())
    st.caption("Frecuencia de consumo de alcohol.")

# ---------- Relaciones ----------
st.header("🔗 Relaciones")

cat = st.selectbox(
    "Variable categórica",
    ["Alcohol", "Smoker", "Gender", "Activity", "Cuisines", "Location"]
)
num = st.selectbox(
    "Variable numérica",
    ["Food Rating", "Service Rating", "Overall Rating", "Budget", "Age"]
)

box_data = df[[cat, num]].copy()
box_data = box_data.reset_index(drop=True) # eliminé los nombres del índice y conservé los datos de las columnas.
# Alcohol aparece dos veces:
# 1. Como nombre de una columna.
# 2. Como nombre de un índice.
# Pandas no sabe cuál de los dos debe utilizar.
st.bar_chart(box_data.groupby(cat)[num].mean(), use_container_width=True)
st.caption(f"Promedio de {num} según {cat}. Para ver la dispersión completa, usa la tabla inferior.")

st.scatter_chart(
    df,
    x="Age",
    y="Overall Rating",
    size="Budget",
    color="Gender",
    use_container_width=True,
)

# ---------- Correlaciones ----------
st.header("🌡️ Correlaciones")

numeric_cols = ["Age", "Budget", "Food Rating", "Service Rating", "Overall Rating"]
corr = df[numeric_cols].corr()

st.dataframe(corr.round(2), use_container_width=True)
st.caption("Matriz de correlación entre variables numéricas.")

# ---------- Datos ----------
st.header("🗂️ Datos filtrados")
st.dataframe(df, use_container_width=True, height=420)

st.download_button(
    "⬇️ Descargar CSV filtrado",
    df.to_csv(index=False).encode("utf-8"),
    file_name="restaurantes_filtrados.csv",
    mime="text/csv",
)