import streamlit as st
from transformers import pipeline
from PIL import Image

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Detektor AI - V1.0",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS KUSTOM (TEMA WEB 5.0 LEGASI) ---
st.markdown("""
<style>
    /* Ukuran Judul dengan Gradien */
    .title-text {
        text-align: center;
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 4em;
        font-weight: 900;
        margin-bottom: 0px;
        padding-top: 10px;
    }
    .subtitle-text {
        text-align: center;
        color: #94a3b8;
        font-size: 1.3em;
        margin-top: -10px;
        margin-bottom: 40px;
    }
    
    /* Kotak Hasil Kesimpulan Final */
    .result-box-final {
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
        color: white;
        padding: 30px;
        border-radius: 12px;
        background: linear-gradient(135deg, #1e3a8a, #312e81);
        border: 2px solid #4f46e5;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
    }
    
    /* Tombol Kustom */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #4f46e5, #06b6d4);
        color: white;
        border: none;
        font-weight: bold;
        font-size: 1.2em;
        padding: 10px 24px;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(6, 182, 212, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. MEMANGGIL MODEL AI (SINGLE MODEL) ---
# WAJIB pakai st.cache_resource agar model tidak diload berulang kali
@st.cache_resource
def load_model():
    return pipeline("image-classification", model="Ripanrz/detektor-ai-v1.0")

detektor = load_model()

# --- 4. HEADER UI ---
st.markdown("<h1 class='title-text'>🕵️‍♂️ Detektor AI - V1.0</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-text'>Sistem Identifikasi Gambar Asli vs AI-Generated</p>", unsafe_allow_html=True)

# --- 5. TATA LETAK KOLOM KIRI & KANAN ---
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("### 📥 Input Gambar")
    foto_upload = st.file_uploader("Pilih gambar...", type=['png', 'jpg', 'jpeg', 'webp'], label_visibility="collapsed")
    
    if foto_upload is not None:
        image = Image.open(foto_upload)
        st.image(image, use_container_width=True)
        tombol_cek = st.button("Mulai Analisis 🚀", use_container_width=True)
    else:
        tombol_cek = False

with col2:
    st.markdown("### 📊 Hasil Analisis")
    
    if foto_upload is None:
        st.info("👈 Silakan unggah gambar di kolom sebelah kiri untuk memulai eksekusi.")
        
    elif tombol_cek:
        with st.spinner("Model sedang mengevaluasi pola piksel gambar..."):
            try:
                # 1. Melakukan prediksi 
                hasil = detektor(image)
                
                # 2. Mengubah hasil ke format dictionary
                format_hasil = {item['label']: item['score'] for item in hasil}
                
                # 3. Menganalisis Label Tertinggi
                label_tertinggi = max(format_hasil, key=format_hasil.get)
                persentase = format_hasil[label_tertinggi] * 100
                label_cek = label_tertinggi.lower()
                
                # 4. Logika Kesimpulan Visual
                if label_cek in ['FAKE', 'aiartdata', 'artificial', 'fake', 'ai-generated', 'ai']:
                    keputusan_final = "🤖 GAMBAR INI BUATAN AI"
                    warna_teks = "#ef4444" # Merah
                elif label_cek in ['realart', 'human', 'real', 'original', 'REAL']:
                    keputusan_final = "📸 GAMBAR INI ASLI (MANUSIA/KAMERA)"
                    warna_teks = "#10b981" # Hijau
                else:
                    keputusan_final = f"📌 TERDETEKSI: {label_tertinggi.upper()}"
                    warna_teks = "#f59e0b" # Kuning
                
                # 5. TAMPILKAN KESIMPULAN FINAL (KOTAK BESAR)
                st.markdown(f"""
                <div class='result-box-final'>
                    <span style='font-size: 0.5em; color: #9ca3af;'>KESIMPULAN MODEL ({persentase:.1f}%)</span><br>
                    <span style='color: {warna_teks};'>{keputusan_final}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # 6. TAMPILKAN BREAKDOWN PERSENTASE
                st.markdown("#### Detail Tingkat Kepercayaan (*Confidence Score*):")
                st.markdown("<br>", unsafe_allow_html=True) # Tambah sedikit spasi
                
                for label, score in format_hasil.items():
                    # Progress bar untuk setiap label yang dikembalikan model
                    st.progress(float(score), text=f"Label: {label} ({score*100:.2f}%)")
                    
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan komputasi: {str(e)}")