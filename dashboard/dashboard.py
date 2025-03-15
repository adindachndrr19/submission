import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Mengkonfigurasi tampilan Seaborn
sns.set(style='dark')

# Memuat dataset yang dibutuhkan
all_data_df = pd.read_csv('https://raw.githubusercontent.com/adindachndrr19/submission/refs/heads/main/data/hour.csv')

# Mengkonversi tipe data "dteday" menjadi datetime
all_data_df['dteday'] = pd.to_datetime(all_data_df['dteday'])
min_date = all_data_df['dteday'].min()
max_date = all_data_df['dteday'].max()

# Membuat Sidebar untuk memfilter rentang waktu
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date, max_value=max_date, value=[min_date, max_date]
    )

# Filter data berdasarkan rentang waktu
filtered_df = all_data_df[(all_data_df['dteday'] >= str(start_date)) & (all_data_df['dteday'] <= str(end_date))]

# Melakukan Mapping nama "weather" dan "season"
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
weather_mapping = {1: "Sunny", 2: "Cloudy", 3: "Rainy"}
filtered_df['season'] = filtered_df['season'].map(season_mapping)
filtered_df['weathersit'] = filtered_df['weathersit'].map(weather_mapping)

# Informasi dataset
# Menampilkan deskripsi dataset dengan styling, termasuk kolom 'dteday'
def styled_dataframe_with_date(df):
    # Statistik untuk kolom numerik
    numeric_description = df.describe().T  # Transpose untuk format vertikal
    numeric_description.reset_index(inplace=True)  # Mengubah index menjadi kolom
    numeric_description.rename(columns={
        "index": "Kolom",
        "count": "Count",
        "mean": "Mean",
        "std": "Std Dev",
        "min": "Min",
        "25%": "25th Percentile",
        "50%": "Median",
        "75%": "75th Percentile",
        "max": "Max"
    }, inplace=True)

    # Tambahkan statistik khusus untuk kolom 'dteday'
    date_stats = {
        "Kolom": ["dteday"],
        "Count": [len(df['dteday'].dropna())],
        "Mean": [None],  # Tidak relevan untuk datetime
        "Std Dev": [None],  # Tidak relevan untuk datetime
        "Min": [df['dteday'].min().strftime('%Y-%m-%d %H:%M:%S')],  # Format datetime ke string
        "25th Percentile": [None],  # Tidak relevan untuk datetime
        "Median": [None],  # Tidak relevan untuk datetime
        "75th Percentile": [None],  # Tidak relevan untuk datetime
        "Max": [df['dteday'].max().strftime('%Y-%m-%d %H:%M:%S')]  # Format datetime ke string
    }
    date_stats_df = pd.DataFrame(date_stats)

    # Gabungkan statistik datetime dengan statistik numerik
    combined_df = pd.concat([date_stats_df, numeric_description], ignore_index=True)
    return combined_df

# Tampilkan tabel statistik deskriptif termasuk 'dteday'
st.header('📊 Analisis Rental Sepeda 🚴‍♂️')
st.subheader('Informasi Gabungan Dataset day dan hour.csv')
styled_df = styled_dataframe_with_date(filtered_df)
st.dataframe(styled_df)

# Fungsi untuk plot penyewaan berdasarkan musim
def plot_rentals_by_season(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='season', y='cnt', data=df, estimator=np.mean, palette='viridis', ax=ax)
    ax.set_xlabel('Musim(Season)')
    ax.set_ylabel('Rata-rata Penyewaan Sepeda')
    ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Musim(Season)')
    st.pyplot(fig)

st.subheader('Penyewaan Sepeda Berdasarkan Musim(Season)')
plot_rentals_by_season(filtered_df)

# Fungsi untuk plot pengaruh cuaca terhadap penyewaan sepeda
def plot_weather_effect(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='weathersit', y='cnt', data=df, palette='Set2', ax=ax)
    ax.set_xlabel('Weather Situation')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.set_title('Pengaruh Kondisi Cuaca(Weather Situation) terhadap Penyewaan Sepeda')
    st.pyplot(fig)

st.subheader('Pengaruh Cuaca(Weather) terhadap Penyewaan Sepeda')
plot_weather_effect(filtered_df)

# Insight
st.subheader('📌 Insight')
st.write("1. Pola Penyewaan Sepeda Musiman \nTingkat penyewaan sepeda tertinggi terjadi pada (fall), dan tingkat penyewaan sepeda terendah terjadi pada (winter). \nCuaca yang tidak stabil dengan suhu yang lebih rendah memungkinkan hujan terjadi lebih besar sehingga (Spring) memliki tingkat penyewaan yang rendah.")
st.write("2. Pengaruh Cuaca terhadap Penyewaan Sepeda \nKetika Cuaca mendukung orang akan lebih suka bersepeda sehingga membuat tingkat penyewaan sepeda menjadi tinggi pada saat cuaca sedang cerah(Sunny).\nTingkat penyewaan sepeda sedikit turun dibandingkan dengan cuaca cerah (sunny) jika cuaca sedang mendung(rainy).\nKondisi jalan yang basah membuat bersepeda kurang nyaman sehingga menurunkan tingkat penyewaan sepeda secara signifikan.\nHasil analisis ini menunjukkan bahwa cuaca sangat memengaruhi keputusan pelanggan untuk menyewa sepeda")
st.write("3. Pola Umum Penggunaan Sepeda:\nHujan adalah sebagai faktor utama dalam penurunan tingkat penyewaan sepeda secara signifikan, sehingga faktor cuaca(season) sangat memengaruhi keputusan pelanggan.\nPeningkatan pada musim panas dan gugur dan penurunan pada musim dingin dan semi menunjukkan bahwa musim-musim menentukan tingkat penyewaan sepeda.\nSelain musim dan cuaca, ada pola harian dan jam tertentu di mana penyewaan meningkat, terutama pada pagi dan sore hari, ketika kemungkinan besar penyewaan akan berkurang.")
st.write("Berdasarkan analisis ini, pengelola layanan penyewaan sepeda dapat merancang strategi yang lebih efektif untuk menghadapi perubahan musim dan kondisi cuaca. Misalnya, mereka dapat mengintensifkan promosi selama musim semi untuk mendorong peningkatan penyewaan, atau menyediakan fasilitas tambahan seperti jas hujan dan jalur khusus untuk memberikan kenyamanan lebih bagi pengguna saat cuaca mendung atau hujan ringan.")
