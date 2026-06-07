import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Menggunakan cache agar data tidak diload ulang setiap kali ada interaksi
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")

    day_df['dteday'] = pd.to_datetime(day_df['dteday'])

    # Mapping
    season_mapping = {1: 'spring', 2: 'summer', 3: 'fall', 4: 'winter'}
    day_df['season_label'] = day_df['season'].map(season_mapping)

    weathersit_mapping = {1: 'Clear', 2: 'Mist', 3: 'Light Rain', 4: 'Heavy Rain'}
    day_df['weathersit_label'] = day_df['weathersit'].map(weathersit_mapping)

    day_df['yr_label'] = day_df['yr'].map({0: 2011, 1: 2012})
    hour_df['yr_label'] = hour_df['yr'].map({0: 2011, 1: 2012})
    
    return day_df, hour_df

# Load data
day_df, hour_df = load_data()

# Header
st.title("🚲 Bike Sharing Dashboard")

# Sidebar Filter 
with st.sidebar:
    st.header("Filter Tanggal")

    min_date = day_df['dteday'].min().date()
    max_date = day_df['dteday'].max().date()

    # Mengambil input tanggal
    date_range = st.date_input(
        label='Pilih Rentang Tanggal',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    # Handling error jika user baru memilih satu tanggal di kalender
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range[0]

    st.write("Tanggal dipilih:", start_date, "sampai", end_date)


# Filter dataframe berdasarkan input
filtered_df = day_df[
    (day_df['dteday'] >= pd.to_datetime(start_date)) &
    (day_df['dteday'] <= pd.to_datetime(end_date))
]

# Metrics
col1, col2, col3 = st.columns(3)

total = int(filtered_df['cnt'].sum()) if not filtered_df.empty else 0
avg = int(filtered_df['cnt'].mean()) if not filtered_df.empty else 0
max_val = int(filtered_df['cnt'].max()) if not filtered_df.empty else 0

with col1:
    st.metric("Total Rental", f"{total:,}")
with col2:
    st.metric("Average Rental", f"{avg:,}")
with col3:
    st.metric("Max Rental", f"{max_val:,}")

st.markdown("---")

# 1. RUSH HOUR
st.subheader("Insight 1: Rush Hour vs Non-Rush Hour")

data_2012 = hour_df[
    (hour_df['yr_label'] == 2012) & 
    (hour_df['workingday'] == 1)
].copy()

def kategori_jam(jam):
    if (7 <= jam <= 9) or (17 <= jam <= 19):
        return 'Rush Hour'
    else:
        return 'Non Rush Hour'

data_2012['kategori_jam'] = data_2012['hr'].apply(kategori_jam)
rata2_jam = data_2012.groupby('kategori_jam')['registered'].mean()

rush = rata2_jam.get('Rush Hour', 0)
non_rush = rata2_jam.get('Non Rush Hour', 0)
persentase = ((rush - non_rush) / non_rush) * 100 if non_rush != 0 else 0

st.metric("Perbedaan Penggunaan (%)", f"{persentase:.2f}%")

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(rata2_jam.index, rata2_jam.values, color=['#90CAF9','#1976D2'])

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 5, f'{yval:.0f}', ha='center')

ax.set_title("Registered Users Comparison (2012 Working Days)")
ax.set_ylabel("Average Registered Users")
st.pyplot(fig)

st.caption("Penggunaan sepeda meningkat secara signifikan saat jam commuting (pagi & sore).")

st.markdown("---")

# 2. CUACA
st.subheader("Insight 2: Dampak Cuaca pada Musim Dingin (Winter)")

winter = day_df[day_df['season_label'] == 'winter']
weather = winter[winter['weathersit_label'].isin(['Clear', 'Light Rain'])]
rata2_cuaca = weather.groupby('weathersit_label')['cnt'].mean()

clear = rata2_cuaca.get('Clear', 0)
rain = rata2_cuaca.get('Light Rain', 0)
penurunan = ((clear - rain) / clear) * 100 if clear != 0 else 0

st.metric("Penurunan Penggunaan karena Hujan (%)", f"{penurunan:.2f}%")

fig2, ax2 = plt.subplots(figsize=(8, 5))
bars2 = ax2.bar(rata2_cuaca.index, rata2_cuaca.values, color=['#90CAF9','#EF5350'])

for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, yval + 50, f'{yval:.0f}', ha='center')

ax2.set_title("Weather Impact on Bike Rentals (Winter)")
ax2.set_ylabel("Average Total Rentals")
st.pyplot(fig2)

st.caption("Cuaca buruk (hujan ringan) menurunkan minat penggunaan sepeda secara signifikan di musim dingin.")
