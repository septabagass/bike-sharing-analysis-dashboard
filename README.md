# 🚲 Bike Sharing Analysis Dashboard

Proyek ini bertujuan untuk menganalisis pola penggunaan layanan **Bike Sharing** berdasarkan faktor waktu dan kondisi cuaca. Analisis dilakukan menggunakan pendekatan **Exploratory Data Analysis (EDA)** dan divisualisasikan melalui dashboard interaktif menggunakan **Streamlit**.

Proyek ini dibuat sebagai bagian dari submission pada kelas **Belajar Analisis Data dengan Python** yang diselenggarakan oleh **Dicoding**.

---

## 📌 Business Questions

Analisis ini dilakukan untuk menjawab pertanyaan bisnis berikut.

1. Bagaimana perbedaan rata-rata jumlah penyewa sepeda pengguna **registered** antara jam sibuk (*rush hour*) dan jam non-sibuk pada hari kerja selama tahun 2012?

2. Bagaimana pengaruh kondisi cuaca terhadap rata-rata jumlah penyewaan sepeda pada musim dingin (*winter*) selama periode 2011–2012?

---

## 🛠️ Setup Environment

### Menggunakan Anaconda

```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

### Menggunakan Virtual Environment (Shell/Terminal)

```bash
python -m venv venv
```

Aktivasi virtual environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

Install seluruh library yang dibutuhkan:

```bash
pip install -r requirements.txt
```

---

## ▶️ Menjalankan Dashboard

Masuk ke folder dashboard:

```bash
cd dashboard
```

Jalankan aplikasi Streamlit:

```bash
streamlit run dashboard.py
```

---

## 📂 Struktur Proyek

```text
bike-sharing-analysis-dashboard
│
├── dashboard
│   ├── dashboard.py
│   ├── day.csv
│   └── hour.csv
│
├── data
│   ├── day.csv
│   └── hour.csv
│
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```
