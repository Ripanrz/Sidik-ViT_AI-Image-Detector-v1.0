import streamlit as st
from transformers import pipeline
from PIL import Image

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Sidik-ViT: AI Image Detector v1.0",
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
    
    /* =========================================
       SOLUSI ANTI-GETAR HUGGING FACE SPACES
       ========================================= */
    /* 1. Mengunci tinggi layar minimal agar iframe tidak kaget */
    .block-container {
        min-height: 100vh;
        padding-bottom: 5rem;
    }
    
    /* 2. Menstabilkan area gambar agar tidak membuat lompatan layout */
    [data-testid="stImage"] {
        min-height: 300px; 
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #0e1117; /* Sesuaikan dengan warna background tema kamu */
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. MEMANGGIL MODEL AI (SINGLE MODEL) ---
# WAJIB pakai st.cache_resource agar model tidak diload berulang kali
@st.cache_resource
def load_model():
    return pipeline("image-classification", model="Ripanrz/detektor-ai-v1.1")

detektor = load_model()

# --- 4. HEADER UI ---
st.markdown("<h1 class='title-text'>🕵️‍♂️ Sidik-ViT: AI Image Detector v1.0</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-text'>Sistem Identifikasi Gambar Asli vs AI-Generated</p>", unsafe_allow_html=True)

# --- 5. TATA LETAK KOLOM KIRI & KANAN ---
col1, col2 = st.columns([1, 1.2], gap="large")

# --- INISIALISASI SESSION STATE (MEMORI UI) ---
# Ini kunci agar layar tidak goyang dan hasil tidak hilang saat diklik hal lain
if 'hasil_analisis' not in st.session_state:
    st.session_state.hasil_analisis = None
if 'nama_gambar_terakhir' not in st.session_state:
    st.session_state.nama_gambar_terakhir = None

with col1:
    st.markdown("### 📥 Input Gambar")
    foto_upload = st.file_uploader("Pilih gambar...", type=['png', 'jpg', 'jpeg', 'webp'], label_visibility="collapsed")
    
    if foto_upload is not None:
        image = Image.open(foto_upload)
        st.image(image, use_container_width=True)
        
        # Jika user mengganti gambar, reset memori hasil analisis sebelumnya
        if st.session_state.nama_gambar_terakhir != foto_upload.name:
            st.session_state.hasil_analisis = None
            st.session_state.nama_gambar_terakhir = foto_upload.name
            
        tombol_cek = st.button("Mulai Analisis 🚀", use_container_width=True)
        
        # Pindahkan spinner ke kolom 1 di bawah tombol agar kolom 2 tidak "kaget" ukurannya
        if tombol_cek:
            with st.spinner("Model sedang mengevaluasi pola piksel gambar..."):
                try:
                    # Simpan hasil ke dalam session_state, bukan variabel biasa
                    st.session_state.hasil_analisis = detektor(image)
                except Exception as e:
                    st.error(f"❌ Terjadi kesalahan komputasi: {str(e)}")
    else:
        # Bersihkan memori jika gambar di-clear (silang ditekan)
        st.session_state.hasil_analisis = None
        st.session_state.nama_gambar_terakhir = None

with col2:
    st.markdown("### 📊 Hasil Analisis")
    
    # Bungkus hasil dalam wadah kosong untuk menstabilkan tinggi elemen
    wadah_hasil = st.container()
    
    with wadah_hasil:
        if foto_upload is None:
            st.info("👈 Silakan unggah gambar di kolom sebelah kiri untuk memulai eksekusi.")
            
        elif st.session_state.hasil_analisis is not None:
            # 1. Ambil hasil dari memori UI
            hasil = st.session_state.hasil_analisis
            
            # 2. Mengubah hasil ke format dictionary
            format_hasil = {item['label']: item['score'] for item in hasil}
            
            # 3. Menganalisis Label Tertinggi
            label_tertinggi = max(format_hasil, key=format_hasil.get)
            persentase = format_hasil[label_tertinggi] * 100
            label_cek = label_tertinggi.lower()
            
            # 4. Logika Kesimpulan Visual
            if label_cek in ['fake', 'aiartdata', 'artificial', 'ai-generated', 'ai']:
                keputusan_final = "🤖 GAMBAR INI BUATAN AI"
                warna_teks = "#ef4444" # Merah
            elif label_cek in ['realart', 'human', 'real', 'original']:
                keputusan_final = "📸 GAMBAR INI ASLI (MANUSIA/KAMERA)"
                warna_teks = "#10b981" # Hijau
            else:
                keputusan_final = f"📌 TERDETEKSI: {label_tertinggi.upper()}"
                warna_teks = "#f59e0b" # Kuning
            
            # 5. TAMPILKAN KESIMPULAN FINAL
            st.markdown(f"""
            <div class='result-box-final'>
                <span style='font-size: 0.5em; color: #9ca3af;'>KESIMPULAN MODEL ({persentase:.1f}%)</span><br>
                <span style='color: {warna_teks};'>{keputusan_final}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # 6. TAMPILKAN BREAKDOWN PERSENTASE
            st.markdown("#### Detail Tingkat Kepercayaan (*Confidence Score*):")
            st.markdown("<br>", unsafe_allow_html=True)
            
            for label, score in format_hasil.items():
                st.progress(float(score), text=f"Label: {label} ({score*100:.2f}%)")
