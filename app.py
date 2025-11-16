import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ===========================
# KONFIGURASI HALAMAN
# ===========================
st.set_page_config(page_title="Kriging Gold Estimation", layout="wide")

# ===========================
# CACHE DATA
# ===========================
@st.cache_data
def load_excel(file_path):
    return pd.read_excel(file_path)

# Load semua dataset sekaligus
df_collar = load_excel(os.path.join("data", "collar_common.xlsx"))
df_sample = load_excel(os.path.join("data", "sample_common.xlsx"))
df_survey = load_excel(os.path.join("data", "survey_common.xlsx"))
df_pre = load_excel(os.path.join("data", "fix_data.xlsx"))
df_krig1 = load_excel(os.path.join("data", "data_kriging.xlsx"))
df_krig2 = load_excel(os.path.join("data", "data_kriging_optimasi.xlsx"))

# ===========================
# SIDEBAR MENU CUSTOM (FULL WIDTH)
# ===========================
st.sidebar.markdown("<h2 style='text-align: center;'>MENU</h2>", unsafe_allow_html=True)

# Tombol vertikal full width
menu = "Dataset"  # default
with st.sidebar:
    if st.button("DATASET", key="btn_dataset"):
        menu = "Dataset"
    if st.button("PETA KRIGING", key="btn_peta"):
        menu = "Peta Hasil Kriging"
    if st.button("ESTIMASI CADANGAN", key="btn_estimasi"):
        menu = "Estimasi Cadangan"

# ===========================
# HALAMAN 1: DATASET
# ===========================
if menu == "Dataset":
    st.title("📊 DATASET (Preview 1000 baris)")

    st.subheader("1️⃣ DATASET AWAL")
    tab1, tab2, tab3 = st.tabs(["Dataset Collar", "Dataset Sample", "Dataset Survey"])

    with tab1:
        st.write("Dataset Collar")
        st.dataframe(df_collar.head(1000), use_container_width=True)

    with tab2:
        st.write("Dataset Sample")
        st.dataframe(df_sample.head(1000), use_container_width=True)

    with tab3:
        st.write("Dataset Survey")
        st.dataframe(df_survey.head(1000), use_container_width=True)

    st.subheader("2️⃣ DATASET SETELAH PREPROCESSING")
    st.dataframe(df_pre.head(1000), use_container_width=True)

    st.subheader("3️⃣ DATASET HASIL KRIGING")
    tab1, tab2 = st.tabs(["Sebelum Optimasi", "Sesudah Optimasi"])

    with tab1:
        st.dataframe(df_krig1.head(1000), use_container_width=True)

    with tab2:
        st.dataframe(df_krig2.head(1000), use_container_width=True)

# ===========================
# HALAMAN 2: PETA HASIL KRIGING
# ===========================
elif menu == "Peta Hasil Kriging":
    st.title("🗺️ PETA HASIL KRIGING")

    st.subheader("1️⃣ PETA DATASET SETELAH PREPROCESSING")
    tab1, tab2 = st.tabs(["Peta 2D", "Peta 3D"])
    with tab1:
        df_map_sample = df_pre.sample(min(5000, len(df_pre)))  # Ambil sample maksimal 5000 titik
        fig2d = px.scatter(df_map_sample, x='X_sample', y='Y_sample', color='Au_composite', title="Peta 2D Au_composite")
        st.plotly_chart(fig2d, use_container_width=True)
    with tab2:
        df_map_sample3d = df_pre.sample(min(5000, len(df_pre)))
        fig3d = px.scatter_3d(df_map_sample3d, x='X_sample', y='Y_sample', z='Z_sample', color='Au_composite', title="Peta 3D Au_composite")
        st.plotly_chart(fig3d, use_container_width=True)

    st.subheader("2️⃣ PETA KRIGING")
    tab1, tab2 = st.tabs(["Sebelum Optimasi", "Sesudah Optimasi"])

    with tab1:
        subtab1, subtab2 = st.tabs(["Peta 2D", "Peta 3D"])
        df_plot2d = df_krig1.sample(min(5000, len(df_krig1)))
        df_plot3d = df_krig1.sample(min(5000, len(df_krig1)))
        with subtab1:
            fig2d_before = px.scatter(df_plot2d, x='X', y='Y', color='Au', title="Peta 2D Sebelum Optimasi")
            st.plotly_chart(fig2d_before, use_container_width=True)
        with subtab2:
            fig3d_before = px.scatter_3d(df_plot3d, x='X', y='Y', z='Z', color='Au', title="Peta 3D Sebelum Optimasi")
            st.plotly_chart(fig3d_before, use_container_width=True)

    with tab2:
        subtab1, subtab2 = st.tabs(["Peta 2D", "Peta 3D"])
        df_plot2d_after = df_krig2.sample(min(5000, len(df_krig2)))
        df_plot3d_after = df_krig2.sample(min(5000, len(df_krig2)))
        with subtab1:
            fig2d_after = px.scatter(df_plot2d_after, x='X', y='Y', color='Au', title="Peta 2D Sesudah Optimasi")
            st.plotly_chart(fig2d_after, use_container_width=True)
        with subtab2:
            fig3d_after = px.scatter_3d(df_plot3d_after, x='X', y='Y', z='Z', color='Au', title="Peta 3D Sesudah Optimasi")
            st.plotly_chart(fig3d_after, use_container_width=True)

# ===========================
# HALAMAN 3: ESTIMASI CADANGAN
# ===========================
elif menu == "Estimasi Cadangan":
    st.title("⛏️ ESTIMASI CADANGAN EMAS")

    st.subheader("TABEL RINGKASAN VOLUME, TONASE, DAN KADAR RATA-RATA AU")
    tab1, tab2 = st.tabs(["Sebelum Optimasi", "Sesudah Optimasi"])

    with tab1:
        df_est_before = pd.DataFrame({
            'Parameter': ['Volume total ore (m³)', 'Tonase total ore (t)', 'Rata-rata kadar Au ore (g/t)'],
            'Nilai': [192031250, 460875000.0, 0.8770]
        })
        st.table(df_est_before)

    with tab2:
        df_est_after = pd.DataFrame({
            'Parameter': ['Volume total ore (m³)', 'Tonase total ore (t)', 'Rata-rata kadar Au ore (g/t)'],
            'Nilai': [201218750, 482925000.0, 0.8946]
        })
        st.table(df_est_after)

    st.subheader("📈 PERBANDINGAN SEBELUM DAN SESUDAH OPTIMASI")
    # Buat bar chart per parameter, supaya beda bar chart terlihat
    df_compare = pd.DataFrame({
        'Parameter': ['Volume', 'Tonase', 'Kadar Rata-rata'],
        'Sebelum': [192031250, 460875000.0, 0.8770],
        'Sesudah': [201218750, 482925000.0, 0.8946]
    })
    # Ubah ke format long untuk Plotly supaya tiap parameter terlihat jelas
    df_long = df_compare.melt(id_vars='Parameter', value_vars=['Sebelum', 'Sesudah'], var_name='Status', value_name='Nilai')
    fig_bar = px.bar(df_long, x='Parameter', y='Nilai', color='Status', barmode='group', title="Perbandingan Estimasi Cadangan")
    st.plotly_chart(fig_bar, use_container_width=True)
