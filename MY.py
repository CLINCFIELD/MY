from datetime import datetime
from zoneinfo import ZoneInfo
import time
import streamlit as st

# Mengatur konfigurasi halaman web
st.set_page_config(page_title="Sistem Pakar Gabah", page_icon="🌾", layout="centered")

# --- TITEL & HEADER ---
st.title("🌾 Sistem Pakar Rekomendasi Penjemuran Gabah (Padi)")
st.caption("Metode Inferensi: Forward Chaining")
st.markdown("---")

# --- 1. INPUT FAKTA INTERNAL (KONDISI GABAH) ---
st.subheader("📋 Kondisi Fisik Gabah")
opsi_gabah = {
    "Gabah Basah / Baru Panen (Kadar Air > 20%)": 1,
    "Gabah Setengah Kering (Kadar Air ~ 17%)": 2,
    "Gabah Hampir Kering (Kadar Air ~ 15%)": 3
}
pilihan_gabah_teks = st.selectbox("Pilih kondisi fisik gabah saat ini:", list(opsi_gabah.keys()))
pilihan_gabah = opsi_gabah[pilihan_gabah_teks]

# --- 2. INPUT FAKTA EKSTERNAL (METEOROLOGI) ---
st.subheader("🌤️ Kondisi Cuaca & Lingkungan")
col1, col2 = st.columns(2)

with col1:
    suhu = st.number_input(
        "Masukkan Suhu Udara (°C):", 
        min_value=0, 
        max_value=50, 
        value=30°C, 
        step=1, 
        format="%d"
    )

with col2:
    kelembapan = st.number_input(
        "Masukkan Kelembapan Udara / RH (%):",
        min_value=0,
        max_value=100,
        value=10%,
        step=1,
        format="%d"
    )

opsi_langit = {
    "Cerah": 1,
    "Berawan": 2,
    "Mendung": 3,
    "Hujan": 4
}
langit = st.selectbox("Kondisi Visual Langit:", list(opsi_langit.keys()))

st.markdown("---")

# --- TOMBOL PROSES INFERENSI ---
if st.button("🔴 Jalankan Analisis Sistem Pakar", type="primary"):
    
    # Efek simulasi berpikir khas Streamlit
    with st.spinner("Mesin Inferensi sedang mencocokkan data dengan Basis Aturan..."):
        time.sleep(1.5) # Jeda animasi sebentar
        
    # --- 3. PROSES INFERENSI (FORWARD CHAINING) ---
    kesimpulan_cuaca = ""
    
    # Evaluasi Rule
    if kelembapan >= 75 or langit in ["Mendung", "Hujan"]:
        kesimpulan_cuaca = "BAHAYA / TIDAK LAYAK"
    elif suhu >= 30 and kelembapan < 75 and langit == "Cerah":
        kesimpulan_cuaca = "SANGAT OPTIMAL (TERIK)"
    elif suhu >= 26 and kelembapan < 75 and langit == "Berawan":
        kesimpulan_cuaca = "CUKUP OPTIMAL (BERAWAN)"
    else:
        kesimpulan_cuaca = "MODERAT (FLUKTUATIF)"

    # --- 4. HASIL ANALISIS & REKOMENDASI ---
    waktu_sekarang = datetime.now(ZoneInfo("Asia/Jakarta")).strftime("%Y-%m-%d %H:%M:%S")
    
    st.success(f"### 📊 Hasil Analisis Sistem Pakar ({waktu_sekarang})")
    
    # Menampilkan status dengan warna penanda
    if kesimpulan_cuaca == "BAHAYA / TIDAK LAYAK":
        st.error(f"**Status Kelayakan Cuaca:** {kesimpulan_cuaca}")
        st.markdown("##### 🚨 Rekomendasi Tindakan:")
        st.write("- **JANGAN LAKUKAN PENJEMURAN!**")
        st.write("- Jika gabah sedang dijemur, **SEGERA ANGKAT** atau tutup dengan terpal.")
        st.write("- Risiko jamur pembusuk sangat tinggi pada kelembapan ini.")
        
    elif kesimpulan_cuaca == "SANGAT OPTIMAL (TERIK)":
        st.info(f"**Status Kelayakan Cuaca:** {kesimpulan_cuaca}")
        st.markdown("##### 📋 Rekomendasi Tindakan:")
        st.write("- **SANGAT LAYAK DAN DIREKOMENDASIKAN UNTUK MENJEMUR GABAH.**")
        if pilihan_gabah == 1:
            st.write("- *Estimasi Penjemuran:* 4 - 6 Jam. Lakukan pembalikan gabah setiap 1-2 jam.")
        elif pilihan_gabah == 2:
            st.write("- *Estimasi Penjemuran:* 2 - 3 Jam untuk mencapai batas ideal SNI 14%.")
        elif pilihan_gabah == 3:
            st.write("- *Estimasi Penjemuran:* Cukup 1 - 2 Jam. Pantau agar tidak pecah saat digiling.")
            
    elif kesimpulan_cuaca == "CUKUP OPTIMAL (BERAWAN)":
        st.warning(f"**Status Kelayakan Cuaca:** {kesimpulan_cuaca}")
        st.markdown("##### 📋 Rekomendasi Tindakan:")
        st.write("- **PROSES PENJEMURAN BISA DILAKUKAN**, laju penguapan sedikit lambat.")
        st.write("- Wajib membalik gabah lebih sering agar panas merata.")
        
    elif kesimpulan_cuaca == "MODERAT (FLUKTUATIF)":
        st.warning(f"**Status Kelayakan Cuaca:** {kesimpulan_cuaca}")
        st.markdown("##### 📋 Rekomendasi Tindakan:")
        st.write("- **PENJEMURAN BERSYARAT.**")
        st.write("- Jemur gabah tidak jauh dari area tertutup agar cepat dievakuasi jika hujan mendadak.")
