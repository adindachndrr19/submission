import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Mengatur tema tampilan menggunakan Seaborn
sns.set_theme(style='darkgrid')

# Membaca dataset dari URL
data_url = 'https://raw.githubusercontent.com/adindachndrr19/submission/refs/heads/main/data/hour.csv'
bike_data = pd.read_csv(data_url)

# Mengubah kolom 'dteday' menjadi tipe datetime
bike_data['dteday'] = pd.to_datetime(bike_data['dteday'])
date_range_start = bike_data['dteday'].min()
date_range_end = bike_data['dteday'].max()

# Sidebar untuk memilih rentang waktu
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.header("Filter Rentang Waktu")
    selected_start_date, selected_end_date = st.date_input(
        "Pilih Rentang Waktu",
        min_value=date_range_start,
        max_value=date_range_end,
        value=[date_range_start, date_range_end]
    )

# Filter dataset berdasarkan rentang waktu
filtered_data = bike_data[
    (bike_data['dteday'] >= pd.Timestamp(selected_start_date)) &
    (bike_data['dteday'] <= pd.Timestamp(selected_end_date))
]

# Mapping kategori 'season' dan 'weathersit'
season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
weather_labels = {1: "Sunny", 2: "Cloudy", 3: "Rainy"}
filtered_data['season'] = filtered_data['season'].map(season_labels)
filtered_data['weathersit'] = filtered_data['weathersit'].map(weather_labels)

# Fungsi untuk menampilkan deskripsi data
def generate_summary_with_date(df):
    numeric_summary = df.describe().T.reset_index()
    numeric_summary.columns = [
        "Kolom", "Count", "Mean", "Std Dev", "Min",
        "25%", "Median", "75%", "Max"
    ]
    date_summary = pd.DataFrame({
        "Kolom": ["dteday"],
        "Count": [df['dteday'].notnull().sum()],
        "Mean": [None],
        "Std Dev": [None],
        "Min": [df['dteday'].min().strftime('%Y-%m-%d')],
        "25%": [None],
        "Median": [None],
        "75%": [None],
        "Max": [df['dteday'].max().strftime('%Y-%m-%d')]
    })
    combined_summary = pd.concat([date_summary, numeric_summary], ignore_index=True)
    return combined_summary

# Menampilkan tabel deskripsi dataset
st.title("📊 Analisis Data Rental Sepeda")
st.subheader("Ringkasan Dataset")
summary_table = generate_summary_with_date(filtered_data)
st.dataframe(summary_table)

# Fungsi untuk membuat visualisasi penyewaan berdasarkan musim
def visualize_rentals_by_season(data):
    plt.figure(figsize=(8, 5))
    sns.barplot(data=data, x='season', y='cnt', estimator=np.mean, palette='coolwarm')
    plt.xlabel("Musim")
    plt.ylabel("Rata-rata Penyewaan")
    plt.title("Rata-rata Penyewaan Sepeda per Musim")
    st.pyplot(plt)

st.subheader("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
visualize_rentals_by_season(filtered_data)

# Fungsi untuk membuat visualisasi pengaruh cuaca terhadap penyewaan
def visualize_weather_effect(data):
    plt.figure(figsize=(8, 5))
    sns.barplot(data=data, x='weathersit', y='cnt', palette='magma')
    plt.xlabel("Kondisi Cuaca")
    plt.ylabel("Jumlah Penyewaan")
    plt.title("Dampak Kondisi Cuaca terhadap Penyewaan Sepeda")
    st.pyplot(plt)

st.subheader("Dampak Kondisi Cuaca terhadap Penyewaan Sepeda")
visualize_weather_effect(filtered_data)

# Menampilkan Insight
st.subheader("📌 Insight Penting")
st.markdown("""
1. **Pola Musim**: Tingkat penyewaan sepeda tertinggi terjadi pada (fall), dan tingkat penyewaan sepeda terendah terjadi pada (winter). Cuaca yang tidak stabil dengan suhu yang lebih rendah memungkinkan hujan terjadi lebih besar sehingga (Spring) memliki tingkat penyewaan yang rendah.
2. **Pengaruh Cuaca**: Ketika Cuaca mendukung orang akan lebih suka bersepeda sehingga membuat tingkat penyewaan sepeda menjadi tinggi pada saat cuaca sedang cerah(Sunny).Tingkat penyewaan sepeda sedikit turun dibandingkan dengan cuaca cerah (sunny) jika cuaca sedang mendung(rainy).Kondisi jalan yang basah membuat bersepeda kurang nyaman sehingga menurunkan tingkat penyewaan sepeda secara signifikan.Hasil analisis ini menunjukkan bahwa cuaca sangat memengaruhi keputusan pelanggan untuk menyewa sepeda
3. **Strategi Pengelolaan**: Hujan adalah sebagai faktor utama dalam penurunan tingkat penyewaan sepeda secara signifikan, sehingga faktor cuaca(season) sangat memengaruhi keputusan pelanggan.Peningkatan pada musim panas dan gugur dan penurunan pada musim dingin dan semi menunjukkan bahwa musim-musim menentukan tingkat penyewaan sepeda.Selain musim dan cuaca, ada pola harian dan jam tertentu di mana penyewaan meningkat, terutama pada pagi dan sore hari, ketika kemungkinan besar penyewaan akan berkurang.

Berdasarkan analisis ini, pengelola layanan penyewaan sepeda dapat merancang strategi yang lebih efektif untuk menghadapi perubahan musim dan kondisi cuaca. Misalnya, mereka dapat mengintensifkan promosi selama musim semi untuk mendorong peningkatan penyewaan, atau menyediakan fasilitas tambahan seperti jas hujan dan jalur khusus untuk memberikan kenyamanan lebih bagi pengguna saat cuaca mendung atau hujan ringan.
""")
