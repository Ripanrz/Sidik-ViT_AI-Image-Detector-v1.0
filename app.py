import gradio as gr
from transformers import pipeline

# 1. Memanggil Model AI Kelas Dunia
detektor = pipeline("image-classification", model="Ripanrz/detektor-ai-v1")

def cek_gambar(foto):
    if foto is None:
        return "⚠️ Unggah gambar.", {"Error": 1.0}
    
    try:
        # Melakukan prediksi menggunakan model
        hasil = detektor(foto)
        
        # Mengubah hasil ke format dictionary
        format_hasil = {item['label']: item['score'] for item in hasil}
        
        # --- LOGIKA KESIMPULAN FLEKSIBEL ---
        label_tertinggi = max(format_hasil, key=format_hasil.get)
        persentase = format_hasil[label_tertinggi] * 100
        label_cek = label_tertinggi.lower()
        
        if label_cek in ['aiartdata', 'artificial', 'fake', 'ai-generated', 'ai']:
            kesimpulan = f"🤖 AI ({persentase:.1f}%)"
        elif label_cek in ['realart', 'human', 'real', 'original']:
            kesimpulan = f"📸 ASLI ({persentase:.1f}%)"
        else:
            kesimpulan = f"📌 '{label_tertinggi}' ({persentase:.1f}%)"

        return kesimpulan, format_hasil
        
    except Exception as e:
        return f"❌ Error: {str(e)}", {"Error": 1.0}

# --- TEMA "WEB 5.0 LEGASI" GRADIO ---
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
    block_padding="12px", 
    block_radius="10px",
)

# --- CSS KUSTOM REVISI ANTI-KEPOTONG ---
css_kustom = """
/* Kanvas dibatasi max 1100px dan width 95% agar ada margin aman di kiri-kanan */
.gradio-container { width: 95% !important; max-width: 1100px !important; margin: auto; padding-top: 2rem !important; }

/* Ukuran Judul */
h1 { text-align: center; color: transparent; background-clip: text; -webkit-background-clip: text; background-image: linear-gradient(90deg, #60a5fa, #a78bfa); font-weight: 900; letter-spacing: -1.5px; margin-bottom: 0em; font-size: 4em !important; }
p.subtitle { text-align: center; color: #94a3b8; font-size: 1.3em; margin-bottom: 2em; margin-top: -5px;}

/* Tombol */
.btn-grad { background-image: linear-gradient(90deg, #4f46e5, #06b6d4) !important; border: none !important; font-weight: bold !important; font-size: 1.3em !important; padding: 12px !important; margin-top: 15px !important; transition: all 0.3s ease !important; }
.btn-grad:hover { transform: translateY(-4px); box-shadow: 0 10px 25px rgba(6, 182, 212, 0.4) !important; }

/* Teks Kesimpulan */
.kesimpulan-teks textarea { font-size: 1.8em !important; font-weight: bold !important; text-align: center !important; color: #10b981 !important; line-height: 1.4 !important; padding: 10px !important;}

/* Hapus label yang tumpuk di atas input_foto agar clean */
#input_foto label { display: none !important; }

/* Padatkan spasi antara tombol dan kotak hasil */
.output-col { gap: 1rem !important; }
"""

# --- MEMBANGUN UI KIRI-KANAN LEGASI ---
with gr.Blocks(theme=tema_web5, css=css_kustom) as web_app:
    gr.HTML("""
        <h1>🕵️‍♂️ Detektor AI — V1</h1>
        <p class='subtitle'>Detektor Gambar Asli vs AI-Generated</p>
    """)
    
    # KUNCI: Menghapus force-row yang bikin kepotong, biarkan Gradio atur sejajarnya
    with gr.Row():
        
        # --- KOLOM KIRI (INPUT) ---
        # min_width diatur ke 320 agar proporsional
        with gr.Column(scale=1, min_width=320):
            input_foto = gr.Image(type="pil", height=400, show_label=False, elem_id="input_foto")
            tombol_cek = gr.Button("Mulai Analisis 🚀", variant="primary", size="lg", elem_classes="btn-grad")
            
        # --- KOLOM KANAN (OUTPUT) ---
        with gr.Column(scale=1, min_width=320, elem_classes="output-col"):
            output_kesimpulan = gr.Textbox(
                show_label=False,
                interactive=False, 
                lines=2,
                elem_classes="kesimpulan-teks",
                placeholder="Keputusan AI"
            )
            output_hasil = gr.Label(show_label=False, num_top_classes=2)
            
    # Menghubungkan logika
    tombol_cek.click(
        fn=cek_gambar,
        inputs=input_foto,
        outputs=[output_kesimpulan, output_hasil]
    )

if __name__ == "__main__":
    web_app.launch()