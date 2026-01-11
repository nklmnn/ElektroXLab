

import streamlit as st
import numpy as np
import plotly.graph_objects as go


TITLE = 'ElektroXLab'
st.set_page_config(
    page_title=TITLE,
    page_icon="⚡",
    layout="wide",
)
st.title("〰️Doğrultucu Devreler")

with st.expander("AÇIKLAMA"):
    st.markdown("""
    Bu sayfa, farklı doğrultucu devrelerini simüle eder. AC giriş sinyali verilerek çıkış geriliminin dalga formu, RMS ve Ortalama değerleri hesaplanır.
    * Dalga doğrultucular, AC sinyallerde grafiğin eksende eksi kısma düştüğü noktaları doğrultarak verimli bir sinyal elde etmeyi amaçlar. Yarım dalga doğrultucu bunu yarı yarıya yaparken tam dalga doğrultucu ise dalganın hepsini grafiğin pozitif tarafına doğrultur.
    * Köprü doğrutucu ve tam dalga doğrultucu grafiksel olarak benzer sonuç verir ama topoloji olarak farklıdırlar.
    * Köprü doğrultucu, 4 diyot kullanır, transformatörün merkez tapasına gerek yoktur. Daha yaygın ve pratiktir.
    * Tam dalga doğrultucu: 2 diyot kullanır ama transformatörün ortadan çıkış vermesi gerekir.
    * Yarım dalga doğrultucu ise tek diyot kullanır.
    """)
    st.markdown("Gözlemlemek istediğiniz doğrultucu tipini seçip giriş kutularını doldurunuz.")

error_box = st.empty()
try:
    def parse_si(value_str):
        multipliers = {
            "k": 1e3,
            "m": 1e-3, "": 1
        }
        if value_str is None or value_str.strip() == "":
            return 0.0
        value_str = value_str.strip()

        # Önce uzun prefix’leri dene (ör: "µ" > "m" > "")
        for prefix, factor in sorted(multipliers.items(), key=lambda x: -len(x[0])):
            if prefix != "" and value_str.endswith(prefix):
                try:
                    return float(value_str.replace(prefix, "")) * factor
                except:
                    return 0.0

        # Hiçbir prefix yoksa, direkt float çevir
        try:
            return float(value_str)
        except:
            return 0.0


    # Parametreler -----------------------------------------------------------------------
    rect_type = st.selectbox("Doğrultucu Türü", ["Yarım Dalga", "Tam Dalga", "Köprü Doğrultucu"])
    V_peak = parse_si(st.text_input("Gerilim (V) [Volt]", "10", key="V_peak", max_chars=10))
    freq = parse_si(st.text_input("AC Frekansı (Hz)", "50", key="V1", max_chars=10))

    t = np.linspace(0, 0.1, 1000)  # 0.1 s örnek

    V_in = V_peak * np.sin(2 * np.pi * freq * t)

    # Doğrultma ----------------------------------------------------------------------------
    if rect_type == "Yarım Dalga":
        V_out = np.maximum(V_in, 0)
    elif rect_type == "Tam Dalga":
        V_out = np.abs(V_in)
    elif rect_type == "Köprü Doğrultucu":
        V_out = np.abs(V_in)

    # RMS ve Ortalama --------------------------------------------------------------------------
    V_rms = np.sqrt(np.mean(V_out**2))
    V_avg = np.mean(V_out)
    st.markdown(f"**RMS Gerilim:** {V_rms:.2f} V")
    st.markdown(f"**Ortalama Gerilim:** {V_avg:.2f} V")

    # Grafik ------------------------------------------------------------------------------------
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=V_in, mode='lines', name='AC Giriş'))
    fig.add_trace(go.Scatter(x=t, y=V_out, mode='lines', name='Doğrultulmuş Çıkış'))
    fig.update_layout(title=f"{rect_type} Doğrultucu Çıkış Dalga Formu",
                      xaxis_title="Zaman (s)", yaxis_title="Gerilim (V)", height=400)
    st.plotly_chart(fig, use_container_width=True)

except:
    error_box.error("Bir hata oluştu. Lütfen girdilerinizi kontrol edip tekrar deneyin.")
    st.stop()