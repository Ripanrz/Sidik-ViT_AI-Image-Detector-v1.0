import streamlit as st
from transformers import pipeline
from PIL import Image

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Detektor AI - V1",
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
    
    /* Kotak Hasil Kesimpulan */
    .result-box {
        text-align: center;
        font-size: 2.2em;
        font-weight: bold;
        color: #10b981;
        padding: 20px;
        border-radius: 10px;
        background-color: #1f2937;
        border: 1px solid #374151;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
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

# --- 3. MEMANGGIL MODEL AI DENGAN CACHE ---
# WAJIB pakai st.cache_resource agar model tidak diload berulang kali
@st.cache_resource
def load_model():
    return pipeline("image-classification", model="Ripanrz/detektor-ai-v1")

detektor = load_model()

# --- 4. HEADER UI ---
st.markdown("<h1 class='title-text'>🕵️‍♂️ Detektor AI - V1</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-text'>Detektor Gambar Asli vs AI-Generated</p>", unsafe_allow_html=True)

# --- 5. TATA LETAK KOLOM KIRI & KANAN ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📥 Input Gambar")
    # Widget Upload Foto
    foto_upload = st.file_uploader("Pilih gambar...", type=['png', 'jpg', 'jpeg', 'webp'], label_visibility="collapsed")
    
    if foto_upload is not None:
        # Menampilkan Preview Gambar
        image = Image.open(foto_upload)
        st.image(image, use_container_width=True)
        
        # Tombol Eksekusi
        tombol_cek = st.button("Mulai Analisis 🚀", use_container_width=True)
    else:
        tombol_cek = False

with col2:
    st.markdown("### 📊 Hasil Analisis")
    
    if foto_upload is None:
        st.info("👈 Silakan unggah gambar di kolom sebelah kiri untuk memulai.")
        
    elif tombol_cek:
        with st.spinner("Menganalisis gambar dengan teliti..."):
            try:
                # 1. Melakukan prediksi menggunakan model
                hasil = detektor(image)
                
                # 2. Mengubah hasil ke format dictionary
                format_hasil = {item['label']: item['score'] for item in hasil}
                
                # 3. Logika Kesimpulan Fleksibel
                label_tertinggi = max(format_hasil, key=format_hasil.get)
                persentase = format_hasil[label_tertinggi] * 100
                label_cek = label_tertinggi.lower()
                
                if label_cek in ['aiartdata', 'artificial', 'fake', 'ai-generated', 'ai']:
                    kesimpulan = f"🤖 AI ({persentase:.1f}%)"
                elif label_cek in ['realart', 'human', 'real', 'original']:
                    kesimpulan = f"📸 ASLI ({persentase:.1f}%)"
                else:
                    kesimpulan = f"📌 '{label_tertinggi}' ({persentase:.1f}%)"

                # 4. Menampilkan Kesimpulan Utama
                st.markdown(f"<div class='result-box'>{kesimpulan}</div>", unsafe_allow_html=True)
                
                # 5. Menampilkan Breakdown Persentase (Pengganti gr.Label)
                st.markdown("#### Detail Kepercayaan Model:")
                for label, score in format_hasil.items():
                    # Streamlit progress bar menerima nilai 0.0 - 1.0
                    st.progress(float(score), text=f"{label} ({score*100:.1f}%)")
                    
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan: {str(e)}")