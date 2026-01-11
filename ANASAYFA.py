import streamlit as st
import os
import importlib.util

TITLE = 'ElektroXLab'
st.set_page_config(
    page_title=TITLE,
    page_icon="⚡",
    layout="wide",
)

# Başlık ve buton yan yana
col_title, col_button = st.columns([6, 1])
with col_title:
     st.title("⚡ ElektroXLab")
with col_button:
    if st.button("🏠 Ana Sayfa"):
        st.session_state.selected_page = None

# Ana container
main_container = st.container()


#ARAMA KODU --------------------------
def build_search_index(pages_folder="pages"):
    search_index = {}
    for filename in os.listdir(pages_folder):
        if filename.endswith(".py"):
            path = os.path.join(pages_folder, filename)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            title = filename.replace(".py", "").replace("_", " ")
            search_index[title] = {"filename": filename, "content": content.lower()}
    return search_index


search_index = build_search_index()

if "selected_page" not in st.session_state:
    st.session_state.selected_page = None

#Sayfa kategorilerini belirleme -----
page_categories = {
    "Devre Teorisi": [f for f in os.listdir("pages") if f.startswith("⏚") and f.endswith(".py")],
    "Elektronik": [f for f in os.listdir("pages") if f.startswith("𓐟") and f.endswith(".py")],
    "Sinyal ve Sistemler": [f for f in os.listdir("pages") if f.startswith("〰️") and f.endswith(".py")]
}

with st.sidebar:


    # Arama Çubuğu -----
    st.markdown("<h3>Arama Çubuğu 🔍</h3>", unsafe_allow_html=True)
    query = st.text_input("Aramak istediğiniz kelimeyi yazın:")

    if query:
        query_lower = query.lower()
        results = []
        for title, data in search_index.items():
            score = 0
            if query_lower in title.lower():
                score += 2
            if query_lower in data["content"]:
                score += 1
            if score > 0:
                results.append((score, title, data["filename"]))
        results.sort(reverse=True, key=lambda x: x[0])

        if results:
            st.subheader("Arama Sonuçları:")
            for score, title, filename in results:
                if st.button(f"{title} sayfasını aç", key=filename):
                    st.session_state.selected_page = filename
        else:
            st.warning("Aradığınız kelimeye uygun sonuç bulunamadı.")

    st.markdown("---")

    #Her kategori için ayrı selectbox -----
    st.markdown("### Sayfa Seçimi")
    for category, files in page_categories.items():
        # Diğer selectbox’ları sıfırlamak için callback fonksiyon
        def select_callback(cat=category, file_list=files):
            # Önce tüm kategorileri sıfırla
            for c in page_categories.keys():
                if c != cat:
                    st.session_state[c] = "Seçiniz"
            selected_file = st.session_state[cat]
            if selected_file != "Seçiniz":
                st.session_state.selected_page = selected_file


        # Selectbox oluştur
        st.selectbox(
            f"{category} sayfaları",
            ["Seçiniz"] + files,
            format_func=lambda x: x.replace(".py", "").replace("_", " ") if x != "Seçiniz" else "Seçiniz",
            key=category,
            on_change=select_callback
        )

#SAYFA YÜKLEME -----
with main_container:
    if st.session_state.selected_page:
        module_name = st.session_state.selected_page.replace(".py", "")
        module_path = os.path.join("pages", st.session_state.selected_page)
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

    if st.session_state.selected_page is None:

        #Ana Sayfa İçeriği -----
        import streamlit as st
        from streamlit.components.v1 import html

        with st.expander("Arka plandaki nedir?"):
            st.caption(
                "Buradan arka plandaki akım ve gerilim sinüzoidallerinin faz farkını ayarlayabileceğini biliyor muydun?")
            phase_deg = st.slider("Faz farkı (derece)", min_value=0, max_value=360, value=30, step=1)
            phase_rad = phase_deg * 3.14159 / 180  # dereceyi radyana çevir

        # HTML ve Canvas animasyonu
        html_code = f"""
        <div style="position:relative; width:100%; height:100vh; overflow:hidden;">
          <!-- Canvas arka plan -->
          <canvas id="waveCanvas" style="position:absolute; top:0; left:0; width:100%; height:100%; z-index:-1;"></canvas>

          <!-- İçerik -->
          <div style="position:relative; z-index:1; color:black; padding:50px; font-family:sans-serif;">

            <!-- Typewriter Başlık -->
            <h1 id="typewriter" style="color:black; font-size:28px; font-family:sans-serif;"></h1>

            <p>Sitenin içerikleri hakkında daha fazla bilgiye aşağıda ulaşabilirsiniz.</p>



            <!-- 3 kolonlu expander container -->
            <div style="display:flex; gap:50px; flex-wrap:wrap;">

              <!-- Sol kolon -->
              <div style="flex:1; min-width:250px; display:flex; flex-direction:column; gap:20px;">
                <details class="glow-expander">
                  <summary>⏚ Devre Teorisi</summary>
                  </p>ElektroXLab'da Devre Teorisi Dersi ile ilgili:</p>
                  </p>* Eşdeğer ve Bölücü Hesaplama</p>
                  </p>* Fazör İşlemleri</p>
                  </p>* Güç Hesaplayıcı ve Güç Faktörü Kompanzasyonu</p>
                  </p>* Op-Amp Hesaplamaları</p>
                  </p>* RC- RL- RLC Devresi Hesaplayıcı</p>
                  </p>* RLC Devre Cevapları </p>
                  </p>* Transformatör Hesaplayıcı</p>
                  </p>İçeriklerine ulaşabilirsiniz. Sayfalarda ayrıntılı açıklamalar bulunmaktadır. Ders bazında listelemelere ve arama çubuğuna yan çubuktan erişebilirsiniz.</p>
                </details>

                
              </div>
              
              <!-- ORTA kolon -->
              <div style="flex:1; min-width:250px; display:flex; flex-direction:column; gap:20px;">
                <details class="glow-expander">
                  <summary>𓐟 Elektronik</summary>
                  </p>ElektroXLab'da Elektronik Dersi ile ilgili:</p>
                  </p>* Mantık Devrelerinin Doğruluk Tablosu</p>
                  </p>* Minterm ve Maxtermler ile Karnough Haritası</p>
                  </p>* Transistor (BJT- MOSFET) Analizleri</p>
                  </p>* Yarıiletken Çalışma Noktaları</p>
                  </p>İçeriklerine ulaşabilirsiniz. Sayfalarda ayrıntılı açıklamalar bulunmaktadır. Ders bazında listelemelere ve arama çubuğuna yan çubuktan erişebilirsiniz.</p>
                </details>
              </div>  
              
              <!-- Sağ kolon -->
              <div style="flex:1; min-width:250px; display:flex; flex-direction:column; gap:20px;">
                <details class="glow-expander">
                  <summary>〰️ Sinyaller ve Sistemler</summary>
                  </p>ElektroXLab'da Sinyaller ve Sistemler Dersi ile ilgili:</p>
                  </p>* Doğrultucu Devreler</p>
                  </p>* FFT ve Enerji-Güç Hesaplayıcı</p>
                  </p>* Impulse, Step, Pole-Zero, Stabilite</p>
                  </p>* Konvolüsyon, Korelasyon ve Z-dönüşümü</p>
                  </p>* Modülasyon Karşılaştırma AM FM PM</p>
                  </p>* Sonlu (FIR) ve Sonsuz (IIR) Tepki Filtre İşlemleri </p>
                  </p>İçeriklerine ulaşabilirsiniz. Sayfalarda ayrıntılı açıklamalar bulunmaktadır. Ders bazında listelemelere ve arama çubuğuna yan çubuktan erişebilirsiniz.</p>
                </details>

                
              </div>

            </div>

            <!-- Expander CSS -->
            <style>
              .glow-expander {{
                background-color: rgba(255,255,255,0.08);
                border: 1px solid rgba(255,255,255,0.25);
                border-radius: 12px;
                padding: 10px 20px;
                color: black;
                font-family: sans-serif;
                box-shadow: 0 0 15px rgba(232, 78, 180, 0.6);
                transition: all 0.3s ease-in-out;
                overflow: hidden;
              }}

              .glow-expander:hover {{
                box-shadow: 0 0 25px rgba(0, 255, 255, 0.4);
                border-color: rgba(0,255,255,0.6);
              }}

              .glow-expander summary {{
                cursor: pointer;
                font-size:18px;
                font-weight:bold;
                list-style:none;
                user-select:none;
              }}

              .glow-expander summary::marker {{
                display: none;
              }}

              .glow-expander[open] {{
                background-color: rgba(255,255,255,0.12);
                box-shadow: 0 0 30px rgba(0,255,255,0.3);
                transition: all 0.3s ease-in-out;
              }}

              .glow-expander[open] p {{
                opacity: 1;
                max-height: 200px;
                transition: all 0.4s ease-in-out;
              }}

              .glow-expander p {{
                opacity: 0;
                max-height: 0;
                margin-top:10px;
                font-size:15px;
                line-height:1.5;
                transition: all 0.4s ease-in-out;
              }}
            </style>

            <!-- Typewriter Script -->
            <script>
              const text = "Bu sitede Elektrik-Elektronik Mühendisliği hakkında analizler ve hesaplamalar yapabileceğiniz sayfalar bulunmaktadır.";
              let i = 0;
              const speed = 10;

              function typeWriter() {{
                if (i < text.length) {{
                  document.getElementById("typewriter").innerHTML += text.charAt(i);
                  i++;
                  setTimeout(typeWriter, speed);
                }}
              }}

              typeWriter();
            </script>

          </div>
        </div>

        <script>
        const canvas = document.getElementById('waveCanvas');
        const ctx = canvas.getContext('2d');

        function resizeCanvas(){{
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }}
        resizeCanvas();

        // Dalga parametreleri
        const amplitudeV = 50;
        const amplitudeI = 50;
        const wavelengthV = 300;
        const wavelengthI = 300;
        const speedV = 0.01;
        const speedI = 0.01;
        const yOffsetV = 150;
        const yOffsetI = 300;
        const phase = {phase_rad};

        let t = 0;

        function drawWave(amplitude, wavelength, speed, yOffset, color, label, phaseShift=0){{
            ctx.beginPath();
            for(let x = 0; x < canvas.width; x++){{
                let y = amplitude * Math.sin((x + t*speed*1000)/wavelength - phaseShift) + yOffset;
                ctx.lineTo(x, y);
                if(x === canvas.width - 1){{
                    ctx.font = "16px sans-serif";
                    ctx.fillStyle = color;
                    ctx.fillText(label, x - 20, y - 10);
                }}
            }}
            ctx.strokeStyle = color;
            ctx.lineWidth = 2;
            ctx.shadowBlur = 15;
            ctx.shadowColor = color;
            ctx.stroke();
            ctx.shadowBlur = 0;
        }}

        function animate(){{
            ctx.fillStyle = '#CEE2CC';
            ctx.fillRect(0,0,canvas.width,canvas.height);

            drawWave(amplitudeV, wavelengthV, speedV, yOffsetV, '#E84EB4', 'V');
            drawWave(amplitudeI, wavelengthI, speedI, yOffsetI, '#21BBCB', 'I', phase);

            t += 1;
            requestAnimationFrame(animate);
        }}

        animate();
        window.addEventListener('resize', resizeCanvas);
        </script>
        """

        html(html_code, height=900)

