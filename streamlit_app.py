import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestión y Control de Nómina Semanal", layout="wide")

# --- TÍTULO Y PRESENTACIÓN ---
st.title("📊 Consultor de Nómina")
st.caption("Periodo de Campaña: Desde el 21 de Septiembre hasta la actualidad")

# --- BARRA LATERAL: CARGA DE EXCEL Y FILTROS ---
st.sidebar.header("📁 Carga de Archivo")
archivo_excel = st.sidebar.file_uploader("Sube la planilla semanal (.xlsx)", type=["xlsx"])

st.sidebar.divider()
st.sidebar.header("🗓️ Filtros de Campaña")
opciones_semana = [
    "Toda la Campaña (Acumulado)",
    "Semana 39 (21 Sep - 27 Sep)",
    "Semana 40 (28 Sep - 04 Oct)",
    "Semana 41 (05 Oct - 11 Oct)",
    "Semana 42 (12 Oct - 18 Oct)",
    "Semana 43 (19 Oct - 25 Oct)",
    "Semana 44 (26 Oct - Actualidad)"
]
semana_sel = st.sidebar.selectbox("Selecciona Periodo / Semana:", opciones_semana)

# --- FUNCIÓN PARA PROCESAR LOS 5 BLOQUES ---
def procesar_planilla(file):
    df_raw = pd.read_excel(file, header=None)
    encabezados = [str(col).strip() for col in df_raw.iloc[0].tolist()]
    
    # Búsqueda de índices para los bloques
    indices_hb = [i for i, col in enumerate(encabezados) if col.upper() == "HABER BASICO"]
    idx_total_ing = encabezados.index("Total Ingresos") if "Total Ingresos" in encabezados else None
    idx_onp = encabezados.index("OFI. NOM. PREVIS.") if "OFI. NOM. PREVIS." in encabezados else None
    idx_total_dsc = encabezados.index("Total Dsctos") if "Total Dsctos" in encabezados else None
    
    df = df_raw.iloc[1:].copy()
    df.columns = encabezados
    return df

# --- ESTRUCTURA DE PESTAÑAS (LAS 4 CONSULTAS) ---
tab1, tab2, tab3, tab4 = st.tabs([
    "1. 👤 Neto por Trabajador",
    "2. 📈 Conceptos Consolidados",
    "3. 📉 Evolución Histórica",
    "4. ⚠️ Control de Alertas"
])

if archivo_excel is not None:
    df = procesar_planilla(archivo_excel)
    
    with tab1:
        st.subheader(f"Resumen de Pagos Netos — {semana_sel}")
        col_busqueda, col_banco = st.columns(2)
        with col_busqueda:
            busqueda = st.text_input("🔍 Buscar por Nombre o DNI:")
        with col_banco:
            banco_filtro = st.multiselect("Filtrar por Banco (Bloque 5):", df['Banco'].unique() if 'Banco' in df.columns else [])
            
        st.dataframe(df, use_container_width=True)

    with tab2:
        st.subheader(f"Desglose por Conceptos (Ingresos y Descuentos) — {semana_sel}")
        st.info("Aquí visualizaremos el consolidado general de los bloques 2 y 3.")

    with tab3:
        st.subheader("Evolución Semanal de la Planilla (Desde el 21 de Septiembre)")
        st.info("Aquí veremos la tendencia acumulada semana a semana.")

    with tab4:
        st.subheader(f"Top Variaciones y Control de Costos — {semana_sel}")
        st.info("Aquí revisaremos los principales conceptos de Horas Extras, Bonos y Descuentos.")

else:
    st.info("👈 Por favor, sube un archivo Excel de planilla en la barra lateral para comenzar.")
