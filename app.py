import gradio as gr
from transformers import pipeline

# 1. Memanggil Model AI Buatanmu Sendiri!
detektor = pipeline("image-classification", model="umm-maybe/AI-image-detector")

def cek_gambar(foto):
    if foto is None:
        return "⚠️ Mohon unggah gambar terlebih dahulu.", {"Error": 1.0}
    
    try:
        # Melakukan prediksi menggunakan model
        hasil = detektor(foto)
        
        # Mengubah hasil ke format dictionary
        format_hasil = {item['label']: item['score'] for item in hasil}
        
# --- LOGIKA KESIMPULAN FLEKSIBEL ---
        label_tertinggi = max(format_hasil, key=format_hasil.get)
        persentase = format_hasil[label_tertinggi] * 100
        
        # Mengubah label ke huruf kecil semua agar gampang dicocokkan
        label_cek = label_tertinggi.lower()
        
        # Mengecek apakah label mengandung kata AI/Palsu
        if label_cek in ['aiartdata', 'artificial', 'fake', 'ai-generated', 'ai']:
            kesimpulan = f"🤖 KESIMPULAN: Gambar ini kemungkinan besar BUATAN AI ({persentase:.1f}%)"
        # Mengecek apakah label mengandung kata Asli/Manusia
        elif label_cek in ['realart', 'human', 'real', 'original']:
            kesimpulan = f"📸 KESIMPULAN: Gambar ini kemungkinan besar FOTO ASLI ({persentase:.1f}%)"
        else:
            kesimpulan = f"📌 KESIMPULAN: Terdeteksi sebagai '{label_tertinggi}' ({persentase:.1f}%)"

# --- TEMA "WEB 5.0" GRADIO ---
tema_web5 = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="cyan",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "sans-serif"]
).set(
    body_background_fill="#0b0f19",
    background_fill_primary="#111827",
    background_fill_secondary="#1f2937",
    border_color_primary="#374151",
    block_background_fill="#1f2937",
    block_border_width="1px",
    block_label_background_fill="#4f46e5",
    block_label_text_color="white",
    block_title_text_color="white",
    button_primary_background_fill="linear-gradient(90deg, #4f46e5, #06b6d4)",
    button_primary_background_fill_hover="linear-gradient(90deg, #4338ca, #0891b2)",
    button_primary_text_color="white",
)

# --- CSS KUSTOM VERSI BESAR & LEGA ---
css_kustom = """
/* Kanvas dilebarkan ke 1200px agar lega */
.gradio-container { max-width: 1200px !important; margin: auto; padding-top: 3rem !important; }

/* Ukuran Judul dibesarkan */
h1 { text-align: center; color: transparent; background-clip: text; -webkit-background-clip: text; background-image: linear-gradient(90deg, #60a5fa, #a78bfa); font-weight: 900; letter-spacing: -1px; margin-bottom: 0.2em; font-size: 3.5em !important; }
p.subtitle { text-align: center; color: #94a3b8; font-size: 1.3em; margin-bottom: 3em; }

/* Tombol lebih besar dan tebal */
.btn-grad { background-image: linear-gradient(90deg, #4f46e5, #06b6d4) !important; border: none !important; font-weight: bold !important; font-size: 1.3em !important; padding: 15px !important; margin-top: 20px !important; transition: all 0.3s ease !important; }
.btn-grad:hover { transform: translateY(-3px); box-shadow: 0 10px 25px rgba(6, 182, 212, 0.4) !important; }

/* Teks kesimpulan dibesarkan agar langsung jadi pusat perhatian */
.kesimpulan-teks textarea { font-size: 1.5em !important; font-weight: bold !important; text-align: center !important; color: #10b981 !important; line-height: 1.5 !important;}
"""

# --- MEMBANGUN UI SIMETRIS KIRI-KANAN ---
with gr.Blocks(theme=tema_web5, css=css_kustom) as web_app:
    gr.HTML("""
        <h1>🕵️‍♂️ DeepSight AI</h1>
        <p class='subtitle'>Detektor Gambar Asli vs AI-Generated</p>
    """)
    
    with gr.Row():
        
        # --- KOLOM KIRI (INPUT) ---
        # min_width dinaikkan agar tidak terlalu kurus, tapi tetap aman
        with gr.Column(scale=1, min_width=500):
            # Tinggi foto diubah dari 320 ke 420 agar terlihat besar dan jelas
            input_foto = gr.Image(type="pil", label="📸 1. Unggah Gambar yang Dicurigai", height=400)
            tombol_cek = gr.Button("Mulai Analisis 🚀", variant="primary", size="lg", elem_classes="btn-grad")
            
        # --- KOLOM KANAN (OUTPUT) ---
        with gr.Column(scale=1, min_width=500):
            # Output Kesimpulan
            output_kesimpulan = gr.Textbox(
                label="🎯 Keputusan AI", 
                interactive=False, 
                lines=2,
                elem_classes="kesimpulan-teks"
            )
            # Output Detail Grafik
            output_hasil = gr.Label(label="📊 Detail Persentase", num_top_classes=2)
            
    # Menghubungkan logika
    tombol_cek.click(
        fn=cek_gambar,
        inputs=input_foto,
        outputs=[output_kesimpulan, output_hasil]
    )

if __name__ == "__main__":
    web_app.launch()