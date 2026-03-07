import streamlit as st
from transformers import pipeline
from PIL import Image

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Detektor AI - V1 (Ensemble)",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS KUSTOM (TEMA WEB 5.0 LEGASI) ---
st.markdown("""
<style>
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
        padding: 25px;
        border-radius: 12px;
        background: linear-gradient(135deg, #1e3a8a, #312e81);
        border: 2px solid #4f46e5;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
    }
    
    /* Kotak Hasil Individual */
    .result-box-mini {
        text-align: center;
        font-size: 1.5em;
        font-weight: bold;
        padding: 15px;
        border-radius: 8px;
        background-color: #1f2937;
        border: 1px solid #374151;
        margin-bottom: 15px;
    }
    
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

# --- 3. MEMANGGIL 2 MODEL AI SEKALIGUS (ENSEMBLE) ---
@st.cache_resource
def load_models():
    # Model Layer 1: Buatanmu
    mod1 = pipeline("image-classification", model="Ripanrz/detektor-ai-v1")
    # Model Layer 2: Model Global (Robust ViT)
    mod2 = pipeline("image-classification", model="umm-maybe/AI-image-detector")
    return mod1, mod2

detektor_lokal, detektor_global = load_models()

# --- FUNGSI BANTUAN: MENGURAI HASIL ---
def proses_hasil_model(hasil):
    format_hasil = {item['label']: item['score'] for item in hasil}
    label_tertinggi = max(format_hasil, key=format_hasil.get)
    persentase = format_hasil[label_tertinggi] * 100
    label_cek = label_tertinggi.lower()
    
    # Menghitung probabilitas mutlak bahwa gambar ini adalah AI (0.0 - 1.0)
    prob_ai = 0.0
    if label_cek in ['aiartdata', 'artificial', 'fake', 'ai-generated', 'ai']:
        teks = f"🤖 AI ({persentase:.1f}%)"
        prob_ai = format_hasil[label_tertinggi]
    elif label_cek in ['realart', 'human', 'real', 'original']:
        teks = f"📸 ASLI ({persentase:.1f}%)"
        prob_ai = 1.0 - format_hasil[label_tertinggi]
    else:
        teks = f"📌 {label_tertinggi} ({persentase:.1f}%)"
        prob_ai = 0.5 # Ragu-ragu
        
    return teks, format_hasil, prob_ai

# --- 4. HEADER UI ---
st.markdown("<h1 class='title-text'>🕵️‍♂️ Detektor AI - V2</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle-text'>Sistem Keamanan Ganda: Model V1 + Global Robust Model</p>", unsafe_allow_html=True)

# --- 5. TATA LETAK KOLOM ---
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("### 📥 Input Gambar")
    foto_upload = st.file_uploader("Pilih gambar...", type=['png', 'jpg', 'jpeg', 'webp'], label_visibility="collapsed")
    
    if foto_upload is not None:
        image = Image.open(foto_upload)
        st.image(image, use_container_width=True)
        tombol_cek = st.button("Mulai Analisis Ganda 🚀", use_container_width=True)
    else:
        tombol_cek = False

with col2:
    st.markdown("### 📊 Hasil Analisis")
    
    if foto_upload is None:
        st.info("👈 Silakan unggah gambar di kolom sebelah kiri untuk memulai.")
        
    elif tombol_cek:
        with st.spinner("Mengaktifkan dua model AI secara bersamaan..."):
            try:
                # 1. Melakukan prediksi dari kedua model
                hasil_1 = detektor_lokal(image)
                hasil_2 = detektor_global(image)
                
                # 2. Memproses hasil masing-masing
                teks_1, format_1, prob_ai_1 = proses_hasil_model(hasil_1)
                teks_2, format_2, prob_ai_2 = proses_hasil_model(hasil_2)
                
                # 3. MENGHITUNG CONSENSUS (KESIMPULAN GABUNGAN)
                rata_rata_ai = (prob_ai_1 + prob_ai_2) / 2
                
                if rata_rata_ai >= 0.60:
                    keputusan_final = "🤖 GAMBAR INI BUATAN AI"
                    warna_teks = "#ef4444" # Merah
                elif rata_rata_ai <= 0.40:
                    keputusan_final = "📸 GAMBAR INI ASLI (MANUSIA/KAMERA)"
                    warna_teks = "#10b981" # Hijau
                else:
                    keputusan_final = "⚠️ HASIL MERAGUKAN (50/50)"
                    warna_teks = "#f59e0b" # Kuning
                
                # 4. TAMPILKAN KESIMPULAN FINAL
                st.markdown(f"""
                <div class='result-box-final'>
                    <span style='font-size: 0.5em; color: #9ca3af;'>KESIMPULAN GABUNGAN ({rata_rata_ai*100:.1f}%)</span><br>
                    <span style='color: {warna_teks};'>{keputusan_final}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # 5. TAMPILKAN BREAKDOWN 2 MODEL (Bersebelahan)
                col_mod1, col_mod2 = st.columns(2)
                
                with col_mod1:
                    st.markdown("#### Layer 1: Model Kamu")
                    st.markdown(f"<div class='result-box-mini' style='color: #60a5fa;'>{teks_1}</div>", unsafe_allow_html=True)
                    for label, score in format_1.items():
                        st.progress(float(score), text=f"{label} ({score*100:.1f}%)")
                        
                with col_mod2:
                    st.markdown("#### Layer 2: Global Model")
                    st.markdown(f"<div class='result-box-mini' style='color: #a78bfa;'>{teks_2}</div>", unsafe_allow_html=True)
                    for label, score in format_2.items():
                        st.progress(float(score), text=f"{label} ({score*100:.1f}%)")
                    
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan komputasi: {str(e)}")