import streamlit as st
import pandas as pd
import joblib
import plotly.express as px



# --- Konfigurasi Halaman & Pemuatan Data ---
st.set_page_config(
    page_title='Dashboard Analisis Pelanggan olist',
    page_icon='📊',
    layout='wide'

)

# Fungsi untuk me-load aset dengan cache Streamlit
@st.cache_resource
def load_model():
    model = joblib.load('models/final_rf_model_tuned.joblib')
    return model

@st.cache_resource
def load_data():
    rfm_data = pd.read_csv('data/final_customer_data.csv')
    main_df = pd.read_csv('data/main_df_for_app.csv')
    # Konversi tanggal
    main_df['order_purchase_timestamp'] = pd.to_datetime(main_df['order_purchase_timestamp'])
    main_df['order_delivered_customer_date'] = pd.to_datetime(main_df['order_delivered_customer_date'])
    return rfm_data, main_df

# Muat model dan data
rf_model = load_model()
rfm_df, main_df = load_data()

# Gabungkan segmen K-Means ke main_df untuk filtering
main_df_merged = pd.merge(main_df, rfm_df[['customer_unique_id', 'Cluster_Label']], on='customer_unique_id', how='left')

# --- Layout Utama & Sidebar Navigasi ---
st.sidebar.title('Navigasi')
page = st.sidebar.radio("Pilih Halaman", ["📊 Dashboard Analisis", "🔮 Alat Prediksi Churn"])

# --- Konten Halaman ---

if page == "📊 Dashboard Analisis":
    st.title('Dashboard Analisis Pelanggan Olist')
    
    # Filter
    segments = ['All'] + rfm_df['Cluster_Label'].unique().tolist()
    selected_segment = st.selectbox("Tampilkan Data untuk Segment:", segments)
    
    # Filter data berdasarkan pilihan
    if selected_segment == 'All':
        filtered_rfm = rfm_df
        filtered_main = main_df_merged
    else:
        filtered_rfm = rfm_df[rfm_df['Cluster_Label'] == selected_segment]
        filtered_main = main_df_merged[main_df_merged['Cluster_Label'] == selected_segment]
        
    # Menampilkan KPI Cards
    st.header("Ringkasan Bisnis")
    total_customers = filtered_rfm.shape[0]
    repeat_rate = (filtered_rfm['Frequency'] > 1).sum() / total_customers * 100 if total_customers > 0 else 0
    churn_rate = filtered_rfm['is_churn'].sum() / total_customers * 100 if total_customers > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pelanggan", f"{total_customers:,}")
    col2.metric("Repeat Buyer Rate", f"{repeat_rate:.1f}%")
    col3.metric("Churn Rate (Berisiko)", f"{churn_rate:.1f}%")
    
    st.markdown("---")
    
    # Menampilkan visualisasi
    st.header("Visualisasi Data")
    col1, col2 = st.columns(2)
    
    with col1:
        # Skala Masalah Retensi
        st.subheader("Skala Masalah Retensi")
        if 'customer_type' not in filtered_rfm.columns:
            filtered_rfm['customer_type'] = filtered_rfm['Frequency'].apply(lambda x: 'Pelanggan Berulang' if x > 1 else 'Pelanggan Sekali Beli')
        retention_counts = filtered_rfm['customer_type'].value_counts().reset_index()
        retention_counts.columns = ['customer_type', 'count']
        
        fig_pie = px.pie(retention_counts, names='customer_type', values='count', 
                         template='plotly_dark', hole=.4,
                         color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_pie, use_container_width=True)

        # Top 10 States
        st.subheader("Top 10 Negara Bagian")
        top_states = filtered_main.groupby('customer_state')['payment_value'].sum().nlargest(10).reset_index()
        
        # Buat figure Plotly
        fig_states_plotly = px.bar(
            top_states,
            x='payment_value',
            y='customer_state',
            orientation='h', # 'h' untuk horizontal
            title="Top 10 Negara Bagian berdasarkan Penjualan",
            labels={'payment_value': 'Total Penjualan (R$)', 'customer_state': 'Negara Bagian'},
            template='plotly_dark' # Template tema gelap
        )
        # Atur layout agar rapi
        fig_states_plotly.update_layout(
            yaxis={'categoryorder':'total ascending'}, # Urutkan dari terbesar ke terkecil
            margin=dict(l=20, r=20, t=40, b=20)
        )
    
        # Tampilkan di Streamlit
        st.plotly_chart(fig_states_plotly, use_container_width=True)
        
    with col2:
        # Distribusi Segmen
        st.subheader("Distribusi Segmen Pelanggan")
        segment_counts = filtered_rfm['Cluster_Label'].value_counts().reset_index()
        segment_counts.columns = ['Cluster_Label', 'count']
        fig_seg = px.bar(segment_counts, x='count', y='Cluster_Label', orientation='h',
                         template='plotly_dark', labels={'count': 'Jumlah Pelanggan', 'Cluster_Label': ''})
        fig_seg.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_seg, use_container_width=True)

        # Top 10 Categories
        st.subheader("Top 10 Kategori Produk")
        top_categories = filtered_main.groupby('product_category_name_english')['payment_value'].sum().nlargest(10).reset_index()
        fig_cat = px.bar(top_categories, x='payment_value', y='product_category_name_english', orientation='h',
                         template='plotly_dark', labels={'payment_value': 'Total Penjualan (R$)', 'product_category_name_english': ''})
        fig_cat.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_cat, use_container_width=True)
        
else: # Halaman "Alat Prediksi Churn"
    st.title("🔮 Alat Prediksi Churn")
    st.write("Masukkan data perilaku pelanggan untuk mendapatkan prediksi risiko churn.")
    
    with st.form("prediction_form"):
        frequency_input = st.number_input("Frequency (Jumlah total transaksi)", min_value=1, step=1, value=1)
        monetary_input = st.number_input("Monetary (Total belanja dalam R$)", min_value=0.0, format="%.2f")
        
        submit_button = st.form_submit_button(label="Jalankan Prediksi")

    if submit_button:
        # Buat prediksi berdasarkan input
        input_df = pd.DataFrame({
            'Frequency': [frequency_input],
            'Monetary': [monetary_input]
        })
        
        prediction = rf_model.predict(input_df)
        probability = rf_model.predict_proba(input_df)
        
        
        risk_probability = probability[0][1] * 100

        st.subheader("Hasil Prediksi")
        if prediction[0] == 1:
            st.error(f"Status: BERISIKO (Probabilitas Churn: {risk_probability:.2f}%)")
        else:
            st.success(f"Status: AMAN (Probabilitas Churn: {risk_probability:.2f}%)")
        
        st.progress(risk_probability / 100)
        st.info("Probabilitas di atas menunjukkan seberapa yakin model bahwa pelanggan ini akan churn.")
