import gradio as gr
from transformers import pipeline

# 1. Memanggil Model AI Buatanmu Sendiri!
# pipeline otomatis mengunduh model "Ripanrz/detektor-ai-v1" dari Hugging Face Hub
detektor = pipeline("image-classification", model="Ripanrz/detektor-ai-v1")

def cek_gambar(foto):
    if foto is None:
        return {"Mohon unggah gambar": 1.0}
    
    try:
        # Melakukan prediksi menggunakan model
        hasil = detektor(foto)
        
        # Mengubah hasil ke format dictionary agar bisa dibaca oleh gr.Label()
        # Contoh output: {'AiArtData': 0.98, 'RealArt': 0.02}
        format_hasil = {item['label']: item['score'] for item in hasil}
        return format_hasil
        
    except Exception as e:
        return {f"Error: {str(e)}": 1.0}

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

# --- CSS KUSTOM MEMAKSA SIMETRIS ---
css_kustom = """
.gradio-container { max-width: 1000px !important; margin: auto; }
h1 { text-align: center; color: transparent; background-clip: text; -webkit-background-clip: text; background-image: linear-gradient(90deg, #60a5fa, #a78bfa); font-weight: 900; letter-spacing: -1px; margin-bottom: 0.2em; }
p.subtitle { text-align: center; color: #94a3b8; font-size: 1.1em; margin-bottom: 2em; }
.force-row { flex-wrap: nowrap !important; }
"""

# --- MEMBANGUN UI SIMETRIS KIRI-KANAN ---
with gr.Blocks(theme=tema_web5, css=css_kustom) as web_app:
    gr.HTML("""
        <h1>🕵️‍♂️ DeepSight AI</h1>
        <p class='subtitle'>Detektor Gambar Asli vs AI-Generated</p>
    """)
    
    with gr.Row(equal_height=True, elem_classes="force-row"):
        
        # --- KOLOM KIRI (INPUT) ---
        with gr.Column(scale=1, min_width=300):
            # Tipe diubah ke "pil" karena pipeline transformers lebih suka format PIL Image
            input_foto = gr.Image(type="pil", label="📸 1. Unggah Gambar yang Dicurigai", height=300)
            tombol_cek = gr.Button("Mulai Analisis 🚀", variant="primary", size="lg")
            
        # --- KOLOM KANAN (OUTPUT) ---
        with gr.Column(scale=1, min_width=300):
            # Menggunakan gr.Label agar hasil klasifikasi terlihat seperti grafik batang persentase
            output_hasil = gr.Label(label="📊 Hasil Analisis AI", num_top_classes=2)
            
    # Menghubungkan logika
    tombol_cek.click(
        fn=cek_gambar,
        inputs=input_foto,
        outputs=output_hasil
    )

if __name__ == "__main__":
    web_app.launch()