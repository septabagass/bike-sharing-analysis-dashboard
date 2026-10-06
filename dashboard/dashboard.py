import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="Bike Sharing Analytics",
    page_icon="🚲",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Background utama */
    .stApp {
        background-color: var(--background-color);
    }

    /* Judul */
    .main-title {
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 0px;
        color: var(--text-color);
    }

    /* Subtitle */
    .subtitle {
        color: var(--text-color);
        opacity: 0.7;
        font-size: 15px;
        margin-top: 0px;
    }

    /* KPI */
    div[data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        padding: 18px;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: 0px 2px 8px rgba(0,0,0,0.04);
    }

    /* Label KPI */
    div[data-testid="stMetricLabel"] {
        color: var(--text-color) !important;
    }

    /* Nilai KPI */
    div[data-testid="stMetricValue"] {
        color: var(--text-color) !important;
    }

    /* Delta KPI */
    div[data-testid="stMetricDelta"] {
        color: var(--text-color) !important;
    }

    /* Section */
    .section-title {
        font-size: 21px;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 10px;
        color: var(--text-color);
    }

    /* Insight box */
    .insight-box {
        background-color: var(--secondary-background-color);
        padding: 18px;
        border-radius: 12px;
        border-left: 5px solid #2563EB;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.04);
        color: var(--text-color);
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv("hour_bersih.csv")

    df["dteday"] = pd.to_datetime(df["dteday"])

    return df


df = load_data()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    # Logo
    try:
        st.image(
            "assets/logo.png",
            width=100
        )
    except:
        st.markdown("### 🚲")

    st.markdown("## Bike Sharing")
    st.caption("Analytics Dashboard")

    st.divider()

    st.markdown("### Filter Data")

    # Tahun
    years = sorted(df["dteday"].dt.year.unique())

    selected_year = st.selectbox(
        "Tahun",
        ["Semua"] + years
    )

    # Musim
    season_options = sorted(df["season"].unique())

    selected_season = st.multiselect(
        "Musim",
        season_options,
        default=season_options
    )

    # Working day
    working_options = {
        "Semua": "Semua",
        "Hari Kerja": 1,
        "Hari Libur": 0
    }

    selected_working = st.selectbox(
        "Jenis Hari",
        list(working_options.keys())
    )


# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df.copy()


# Filter tahun
if selected_year != "Semua":

    filtered_df = filtered_df[
        filtered_df["dteday"].dt.year == selected_year
    ]


# Filter musim
filtered_df = filtered_df[
    filtered_df["season"].isin(selected_season)
]


# Filter working day
if selected_working != "Semua":

    filtered_df = filtered_df[
        filtered_df["workingday"] ==
        working_options[selected_working]
    ]


# =========================================================
# HEADER
# =========================================================

try:
        st.image(
        "assets/logo.png",
        width=100
    )
except:
    st.markdown("## 🚲")


st.markdown(
    '<p class="main-title">Bike Sharing Analytics Dashboard</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">'
    'Dashboard analisis pola penyewaan sepeda berdasarkan '
    'waktu, musim, dan kondisi cuaca.'
    '</p>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# KPI
# =========================================================

total_rental = filtered_df["cnt"].sum()

average_rental = filtered_df["cnt"].mean()

total_registered = filtered_df["registered"].sum()

total_casual = filtered_df["casual"].sum()


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Penyewaan",
        f"{total_rental:,.0f}"
    )


with col2:

    st.metric(
        "Rata-rata Penyewaan",
        f"{average_rental:,.0f}"
    )


with col3:

    st.metric(
        "Registered User",
        f"{total_registered:,.0f}"
    )


with col4:

    st.metric(
        "Casual User",
        f"{total_casual:,.0f}"
    )


# =========================================================
# TREND PENYEWAAN
# =========================================================

st.markdown(
    '<p class="section-title">📈 Tren Penyewaan Sepeda</p>',
    unsafe_allow_html=True
)


daily = (
    filtered_df
    .groupby("dteday", as_index=False)["cnt"]
    .sum()
)


fig_trend = px.line(
    daily,
    x="dteday",
    y="cnt",
    markers=True,
    labels={
        "dteday": "Tanggal",
        "cnt": "Jumlah Penyewaan"
    }
)


fig_trend.update_layout(
    height=400,
    hovermode="x unified",
    margin=dict(l=20, r=20, t=20, b=20)
)


st.plotly_chart(
    fig_trend,
    use_container_width=True
)


# =========================================================
# JAM & MUSIM
# =========================================================

col1, col2 = st.columns(2)


# ---------------------------------------------------------
# PENYEWAAN BERDASARKAN JAM
# ---------------------------------------------------------

with col1:

    st.markdown(
        '<p class="section-title">🕐 Penyewaan Berdasarkan Jam</p>',
        unsafe_allow_html=True
    )

    # Kalau dataset yang digunakan adalah hourly,
    # bagian ini dapat digunakan ketika kolom hr tersedia.

    if "hr" in filtered_df.columns:

        hourly = (
            filtered_df
            .groupby("hr", as_index=False)["cnt"]
            .mean()
        )

        fig_hour = px.line(
            hourly,
            x="hr",
            y="cnt",
            markers=True,
            labels={
                "hr": "Jam",
                "cnt": "Rata-rata Penyewaan"
            }
        )

        fig_hour.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(
            fig_hour,
            use_container_width=True
        )

    else:

        st.info(
            "Kolom 'hr' tidak tersedia pada dataset harian."
        )


# ---------------------------------------------------------
# PENYEWAAN BERDASARKAN MUSIM
# ---------------------------------------------------------

with col2:

    st.markdown(
        '<p class="section-title">🌤️ Penyewaan Berdasarkan Musim</p>',
        unsafe_allow_html=True
    )

    seasonal = (
        filtered_df
        .groupby("season", as_index=False)["cnt"]
        .mean()
    )

    fig_season = px.bar(
        seasonal,
        x="season",
        y="cnt",
        labels={
            "season": "Musim",
            "cnt": "Rata-rata Penyewaan"
        }
    )

    fig_season.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig_season,
        use_container_width=True
    )


# =========================================================
# REGISTERED VS CASUAL
# =========================================================

st.markdown(
    '<p class="section-title">👥 Registered vs Casual User</p>',
    unsafe_allow_html=True
)


user_type = pd.DataFrame({
    "Tipe User": [
        "Registered",
        "Casual"
    ],
    "Jumlah": [
        filtered_df["registered"].sum(),
        filtered_df["casual"].sum()
    ]
})


fig_user = px.bar(
    user_type,
    x="Tipe User",
    y="Jumlah",
    text="Jumlah",
    labels={
        "Jumlah": "Total User"
    }
)


fig_user.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)


fig_user.update_layout(
    height=350,
    margin=dict(l=20, r=20, t=20, b=20)
)


st.plotly_chart(
    fig_user,
    use_container_width=True
)


# =========================================================
# RUSH HOUR ANALYSIS
# =========================================================

st.markdown(
    '<p class="section-title">🚦 Rush Hour Analysis</p>',
    unsafe_allow_html=True
)


if "hr" in filtered_df.columns:

    rush_df = filtered_df.copy()

    rush_df["hour_category"] = rush_df["hr"].apply(
        lambda x:
        "Rush Hour"
        if (7 <= x <= 9) or (16 <= x <= 19)
        else "Non-Rush Hour"
    )


    avg_registered = (
        rush_df
        .groupby("hour_category")["registered"]
        .mean()
        .reset_index()
    )


    rush_avg = avg_registered.loc[
        avg_registered["hour_category"] == "Rush Hour",
        "registered"
    ].iloc[0]


    non_rush_avg = avg_registered.loc[
        avg_registered["hour_category"] == "Non-Rush Hour",
        "registered"
    ].iloc[0]


    percentage_difference = (
        (rush_avg - non_rush_avg)
        / non_rush_avg
    ) * 100


    col1, col2 = st.columns([2, 1])


    with col1:

        fig_rush = px.bar(
            avg_registered,
            x="hour_category",
            y="registered",
            text="registered",
            labels={
                "hour_category": "Kategori Jam",
                "registered": "Rata-rata Registered User"
            }
        )


        fig_rush.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside"
        )


        fig_rush.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=20, b=20)
        )


        st.plotly_chart(
            fig_rush,
            use_container_width=True
        )


    with col2:

        st.metric(
            "Selisih Rush Hour",
            f"{percentage_difference:.2f}%"
        )


        st.markdown(
            f"""
            <div class="insight-box">

            <b>💡 Insight</b>

            <p>
            Rata-rata registered user pada
            <b>Rush Hour</b> mencapai
            <b>{rush_avg:.2f}</b> pengguna.
            </p>

            <p>
            Sedangkan pada
            <b>Non-Rush Hour</b> sebesar
            <b>{non_rush_avg:.2f}</b> pengguna.
            </p>

            <p>
            Artinya, penggunaan pada Rush Hour
            sekitar <b>{percentage_difference:.2f}%</b>
            lebih tinggi.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# DATA PREVIEW
# =========================================================

with st.expander("🔎 Lihat Data yang Digunakan"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Bike Sharing Analytics Dashboard • "
    "Developed for Data Analysis Project"
)
