# Dashboard Analisis & Prediksi Churn Pelanggan Olist

Sebuah dashboard interaktif yang dibangun dengan Streamlit untuk menganalisis segmentasi pelanggan dan memprediksi risiko churn berdasarkan data dari dataset e-commerce Olist.

## 🚀 Demo Aplikasi

**[Link ke Aplikasi Live]**

![Screenshot Dashboard](URL_SCREENSHOT_DASHBOARDMU_DI_SINI)

## 📂 Struktur Proyek

Proyek ini menggunakan struktur yang sederhana dan efisien untuk aplikasi Streamlit:

```text

churn-dashboard-streamlit/
├── 📂 data/
│   └── 📄 final_customer_data.csv
│   └── 📄 main_df_for_app.csv
├── 📂 models/
│   └── 📄 final_rf_model_tuned.joblib
├── 📄 streamlit_app.py
├── 📄 requirements.txt
└── 📄 .gitignore

```

## ✨ Fitur Utama

- **Dashboard Analisis Interaktif:** Menampilkan KPI utama, distribusi segmen pelanggan, analisis geografis, kategori produk terlaris, dan penyebab kepuasan pelanggan.
- **Filter Berdasarkan Segmen:** Pengguna dapat memfilter seluruh dashboard untuk melihat data dari segmen pelanggan tertentu (misal: VIP, Loyal, dll.).
- **Alat Prediksi Churn:** Sebuah form interaktif untuk memprediksi risiko churn seorang pelanggan secara _real-time_ menggunakan model Random Forest yang sudah dioptimalkan.

## 💻 Tech Stack

- **Framework Aplikasi:** Streamlit
- **Analisis Data:** Pandas, NumPy
- **Visualisasi Data:** Plotly, Matplotlib, Seaborn
- **Machine Learning:** Scikit-learn, Joblib
