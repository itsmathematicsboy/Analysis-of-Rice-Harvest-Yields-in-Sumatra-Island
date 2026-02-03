import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

st.set_page_config(page_title = 'Hasil Panen di Sumatra', layout = 'wide')
# Backend
link = r'https://raw.githubusercontent.com/itsmathematicsboy/Analysis-of-Rice-Harvest-Yields-in-Sumatra-Island/main/Data%20Tanaman%20Padi%20Sumatera.csv'

@st.cache_data
def load_data(data):
    df = pd.read_csv(data)
    return df

df = load_data(link)

def calculate_metrics(data):
    metrics = {}

    # Produksi
    metrics['total_produksi'] = data['Produksi'].sum()

    # Produktivitas (ton/ha)
    produktivitas = data['Produksi'] / data['Luas Panen']
    metrics['produktivitas_rata2'] = produktivitas.mean()

    # Iklim
    metrics['curah_hujan_median'] = data['Curah hujan'].median()   # mm/tahun
    metrics['kelembapan_rata2'] = data['Kelembapan'].mean()        # %
    metrics['suhu_rata2'] = data['Suhu rata-rata'].mean()          # °C

    # Luas panen
    metrics['luas_panen_rata2'] = data['Luas Panen'].mean()        # ha

    # Pertumbuhan produksi tahunan (%)
    produksi_tahunan = data.groupby('Tahun')['Produksi'].sum()
    metrics['growth_produksi'] = produksi_tahunan.pct_change().mean() * 100

    # Stabilitas produksi (opsional tapi bagus)
    metrics['std_produksi'] = produksi_tahunan.std()

    return metrics

def line_plot(data, col_x, col_y):
    line = px.line(data, x = col_x, y = col_y)
    line.update_layout(dragmode=False)
    return line

def bar_plot(data, col_x, col_y):
    bar = px.bar(data, x = col_x, y = col_y)
    bar.update_layout(dragmode=False)
    return bar

#Front end
with st.sidebar:
    province_list = ['Semua'] + sorted(df['Provinsi'].unique().tolist())
    province = st.radio('Provinsi', province_list, key = 'Provinsi')

if st.session_state['Provinsi'] == 'Semua':

    # Data Tambahan
    diff_date = df['Tahun'].max() - df['Tahun'].min() # Selisih Tahun
    metrics = calculate_metrics(df) # Metrik Tambahan
    # groupby dataset tahun dan produksi
    jumlah_produksi_per_tahun = df.groupby('Tahun')['Produksi'].sum().reset_index()
    # groupby dataset provinsi dan produksi
    jumlah_produksi_per_provinsi = df.groupby('Provinsi')['Produksi'].sum().reset_index().sort_values(by = 'Produksi')

    st.header(f'Grafik Hasil Panen Dalam {diff_date} Tahun')
    with st.container():
        # Metrik Curah hujan, Kelembapan dan Suhu
        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Produksi",
            f"{metrics['total_produksi']:,.0f} ton"
        )

        col2.metric(
            "Produktivitas Rata-rata",
            f"{metrics['produktivitas_rata2']:.2f} ton/ha"
        )

        col3.metric(
            "Curah Hujan (Median)",
            f"{metrics['curah_hujan_median']:.0f} mm"
        )

        col4.metric(
            "Suhu Rata-rata",
            f"{metrics['suhu_rata2']:.2f} °C"
        )

        # Visualisasi Grafik
        col5, col6 = st.columns([2, 2])
        with col5:
            st.plotly_chart(line_plot(jumlah_produksi_per_tahun, 'Tahun', 'Produksi')) # Line Plot
        with col6:
            st.plotly_chart(bar_plot(jumlah_produksi_per_provinsi.iloc[:3, :], 'Provinsi', 'Produksi')) # Bar Plot
else:
    df = df[df['Provinsi'] == province]
    # Data Tambahan
    diff_date = df['Tahun'].max() - df['Tahun'].min() # Selisih Tahun
    metrics = calculate_metrics(df) # Metrik Tambahan
    # groupby dataset tahun dan produksi
    jumlah_produksi_per_tahun = df.groupby('Tahun')['Produksi'].sum().reset_index()

    st.header(f'Grafik Hasil Panen Dalam {diff_date} Tahun Pada Provinsi {province}')
    with st.container():
        # Metrik Curah hujan, Kelembapan dan Suhu
        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Produksi",
            f"{metrics['total_produksi']:,.0f} ton"
        )

        col2.metric(
            "Produktivitas Rata-rata",
            f"{metrics['produktivitas_rata2']:.2f} ton/ha"
        )

        col3.metric(
            "Curah Hujan (Median)",
            f"{metrics['curah_hujan_median']:.0f} mm"
        )

        col4.metric(
            "Suhu Rata-rata",
            f"{metrics['suhu_rata2']:.2f} °C"
        )
        col5, col6 = st.columns(2)
        with col5:
            st.plotly_chart(line_plot(jumlah_produksi_per_tahun, 'Tahun', 'Produksi'))
        with col6:
            st.plotly_chart(bar_plot(df, 'Tahun', 'Luas Panen'))
    