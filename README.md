# Dashboard Analisis & Prediksi Churn Pelanggan Olist

Sebuah dashboard interaktif yang dibangun dengan Streamlit untuk menganalisis segmentasi pelanggan dan memprediksi risiko churn berdasarkan data dari dataset e-commerce Olist.

## 🚀 Demo Aplikasi

🔗 **[Customer Churn Dashboard - Live Demo](https://customer-churn-dashboard-app-p3ecfvqtsr5dxwpebs2laf.streamlit.app/)**

<p align="center">
  <img src="https://github.com/user-attachments/assets/80d71cda-edaa-4491-8171-74c88660a684" width="80%">
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/d80ca84a-1dde-443b-9884-b2ab0d01c4df" width="80%">
</p>

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
