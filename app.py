import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ===========================
# KONFIGURASI HALAMAN
# ===========================
st.set_page_config(page_title="Kriging Gold Estimation", layout="wide")

# ===========================
# SIDEBAR MENU CUSTOM
# ===========================
st.sidebar.markdown("<h2 style='text-align: center;'>MENU</h2>", unsafe_allow_html=True)

# Tombol navigasi manual
menu = None
if st.sidebar.button("DATASET"):
    menu = "Dataset"
if st.sidebar.button("PETA KRIGING"):
    menu = "Peta Hasil Kriging"
if st.sidebar.button("ESTIMASI CADANGAN"):
    menu = "Estimasi Cadangan"

if menu is None:
    menu = "Dataset"

# ===========================
# HALAMAN 1: DATASET
# ===========================
if menu == "Dataset":
    st.title("📊 DATASET")

    st.subheader("1️⃣ DATASET AWAL")
    tab1, tab2, tab3 = st.tabs(["Dataset Collar", "Dataset Sample", "Dataset Survey"])

    with tab1:
        st.write("Dataset Collar")
        df_collar = pd.read_excel(os.path.join("data", "collar_common.xlsx"))
        st.dataframe(df_collar, use_container_width=True)

    with tab2:
        st.write("Dataset Sample")
        df_sample = pd.read_excel(os.path.join("data", "sample_common.xlsx"))
        st.dataframe(df_sample, use_container_width=True)

    with tab3:
        st.write("Dataset Survey")
        df_survey = pd.read_excel(os.path.join("data", "survey_common.xlsx"))
        st.dataframe(df_survey, use_container_width=True)

    st.subheader("2️⃣ DATASET SETELAH PREPROCESSING")
    df_pre = pd.read_excel(os.path.join("data", "fix_data.xlsx"))
    st.dataframe(df_pre, use_container_width=True)

    st.subheader("3️⃣ DATASET HASIL KRIGING")
    tab1, tab2 = st.tabs(["Sebelum Optimasi", "Sesudah Optimasi"])

    with tab1:
        df_krig1 = pd.read_excel(os.path.join("data", "data_kriging.xlsx"))
        st.dataframe(df_krig1, use_container_width=True)

    with tab2:
        df_krig2 = pd.read_excel(os.path.join("data", "data_kriging_optimasi.xlsx"))
        st.dataframe(df_krig2, use_container_width=True)

# ===========================
# HALAMAN 2: PETA HASIL KRIGING
# ===========================
elif menu == "Peta Hasil Kriging":
    st.title("🗺️ PETA HASIL KRIGING")

    st.subheader("1️⃣ PETA DATASET SETELAH PREPROCESSING")
    df_map = pd.read_excel(os.path.join("data", "fix_data.xlsx"))
    tab1, tab2 = st.tabs(["Peta 2D", "Peta 3D"])
    with tab1:
        fig2d = px.scatter(df_map, x='X_sample', y='Y_sample', color='Au_composite', title="Peta 2D Au_composite")
        st.plotly_chart(fig2d, use_container_width=True)
    with tab2:
        fig3d = px.scatter_3d(df_map, x='X_sample', y='Y_sample', z='Z_sample', color='Au_composite', title="Peta 3D Au_composite")
        st.plotly_chart(fig3d, use_container_width=True)

    st.subheader("2️⃣ PETA KRIGING")
    tab1, tab2 = st.tabs(["Sebelum Optimasi", "Sesudah Optimasi"])

    with tab1:
        df_krig_before = pd.read_excel(os.path.join("data", "data_kriging.xlsx"))
        subtab1, subtab2 = st.tabs(["Peta 2D", "Peta 3D"])
        with subtab1:
            fig2d_before = px.scatter(df_krig_before, x='X', y='Y', color='Au', title="Peta 2D Sebelum Optimasi")
            st.plotly_chart(fig2d_before, use_container_width=True)
        with subtab2:
            fig3d_before = px.scatter_3d(df_krig_before, x='X', y='Y', z='Z', color='Au', title="Peta 3D Sebelum Optimasi")
            st.plotly_chart(fig3d_before, use_container_width=True)

    with tab2:
        df_krig_after = pd.read_excel(os.path.join("data", "data_kriging_optimasi.xlsx"))
        subtab1, subtab2 = st.tabs(["Peta 2D", "Peta 3D"])
        with subtab1:
            fig2d_after = px.scatter(df_krig_after, x='X', y='Y', color='Au', title="Peta 2D Sesudah Optimasi")
            st.plotly_chart(fig2d_after, use_container_width=True)
        with subtab2:
            fig3d_after = px.scatter_3d(df_krig_after, x='X', y='Y', z='Z', color='Au', title="Peta 3D Sesudah Optimasi")
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
    df_compare = pd.DataFrame({
        'Parameter': ['Volume', 'Tonase', 'Kadar Rata-rata'],
        'Sebelum': [192031250, 460875000.0, 0.8770],
        'Sesudah': [201218750, 482925000.0, 0.8946]
    })
    fig_bar = px.bar(df_compare, x='Parameter', y=['Sebelum', 'Sesudah'], barmode='group', title="Perbandingan Estimasi Cadangan")
    st.plotly_chart(fig_bar, use_container_width=True)
