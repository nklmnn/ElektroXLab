import streamlit as st
import numpy as np
import math
import matplotlib.pyplot as plt


# SI
TITLE = 'ElektroXLab'
st.set_page_config(
    page_title=TITLE,
    page_icon="⚡",
    layout="wide",
)
def parse_si(value_str):
    multipliers = {
        "M": 1e6, "k": 1e3,
        "m": 1e-3, "": 1
    }
    if value_str is None or value_str.strip() == "":
        return 0.0
    value_str = value_str.strip()

    # Önce multipliers
    for prefix, factor in sorted(multipliers.items(), key=lambda x: -len(x[0])):
        if prefix != "" and value_str.endswith(prefix):
            try:
                return float(value_str.replace(prefix, "")) * factor
            except:
                return 0.0

    # Hiçbiri yoksa
    try:
        return float(value_str)
    except:
        return 0.0



# AC Güç Hesaplayıcı

st.title("🏭 Güç Hesaplayıcı ve Güç Faktörü Kompanzasyonu")
''
with st.expander("AÇIKLAMA"):
    st.markdown("Her elektrik sistemi belirli bir miktar güç üretir veya tüketir. Rezistif (yalnızca direnç içeren) devrelerde bu güç tamamen gerçek güç (P) şeklinde ifade edilir. Ancak devrede endüktif veya kapasitif elemanlar da bulunuyorsa, bu durumda reaktif güç (Q) devreye girer. Gerçek ve reaktif güç birlikte sistemin görünür gücünü (S) oluşturur. Elektrik üretim ve dağıtım sistemlerinde, enerji kalitesi ve verimlilik açısından reaktif gücün belirli sınırlar içinde tutulması zorunludur. Bu nedenle, reaktif gücü üreten endüktif yükleri dengelemek için devreye paralel bağlanan kapasitif yükler kullanılır. Böylece sistemin toplam reaktif gücü istenen seviyeye düşürülür. Bu dengeleme işlemine kompanzasyon denir.")
    st.markdown("Giriş olarak gerilim, akım ve faz açısı bilgilerinizi girerek güç vektörlerini, buradan aldığınız sonuçları kullanarak da hedef güç faktörünüz için gerekli kapasitör değerini bulabilirsiniz.")
    st.caption("* NOT: 'M', 'k' ve 'm' SI birimlerini kullanabilirsiniz.")
    with st.expander("Formüller"):
        st.header("Güç Formülleri")

        # Temel formüller
        st.latex(r"P = V I \cos\varphi\text{ (aktif güç, birimi watt)}")
        st.latex(r"Q = V I \sin\varphi\text{ (reaktif güç, birimi VAR)}")
        st.latex(r"S = V I \quad\text{ (görünür güç, birimi VA)}")
        st.latex(r"S = P + jQ")
        st.latex(r"|S| = \sqrt{P^2 + Q^2}")

        # Güç faktörü
        st.latex(r"\text{PF} = \cos\varphi = \frac{P}{|S|}\text{ (güç faktörü)}")

        # pf için
        st.latex(r"\varphi = \arccos(\text{PF})\text{ (güç faktörü açısı)}")
        st.latex(r"\tan\varphi = \frac{Q}{P}")

        # Kompanzasyon
        st.subheader("Kompanzasyon (hedef PF'e getirmek için gerekli $Q_C$)")
        st.latex(r"Q_{C} = Q_{\text{mevcut}} - Q_{\text{hedef}}")
        st.latex(r"Q_{\text{mevcut}} = P \tan\varphi_{1}")
        st.latex(r"Q_{\text{hedef}} = P \tan\varphi_{2}")
        st.latex(r"\Rightarrow \; Q_{C} = P\left(\tan\varphi_{1} - \tan\varphi_{2}\right)")

        # Kondansatör değeri
        st.subheader("Kondansatörün değeri (C) — sabit gerilim varsayımıyla")
        st.latex(r"Q_{C} = V^2 \omega C \quad\text{(kapasitif reaktif güç, } \omega = 2\pi f)")
        st.latex(r"\Rightarrow \; C = \frac{Q_{C}}{V^2 \omega} = \frac{Q_{C}}{V^2 2\pi f}")


        st.write("Not: Kapasitif reaktif güç Qc genelde negatif işaret taşır (reaktif güç üretir).")
''
''
''

error_box = st.empty()
try:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(" Güç Hesaplayıcısı")
        # Girdiler
        V = parse_si(st.text_input("Gerilim (V) [Volt]", "230", key="V1", max_chars=30))
        I = parse_si(st.text_input("Akım (I) [Amper]", "5", key="I1", max_chars=30))
        phi_deg = parse_si(st.text_input("Faz Açısı (φ) [°] (Akıma göre)", "30", key="phi1", max_chars=30))
        phi_rad = np.radians(phi_deg)

        # Sıfır veya negatif değer uyarısı
        if V <= 0:
            st.warning("⚠️ Gerilim değeri hatalıdır.")
        if I <= 0:
            st.warning("⚠️ Akım değeri hatalıdır.")

        # Hesaplamalar
        S = V * I
        P = V * I * np.cos(phi_rad)
        Q = V * I * np.sin(phi_rad)

        # Sonuçlar
        st.subheader("Hesaplanan Güçler")
        st.write(f" ♢ Görünür Güç (S): {S:.2f} VA")
        st.write(f"🔸 Aktif Güç (P): {P:.2f} W")
        st.write(f"🔹 Reaktif Güç (Q): {Q:.2f} VAR")
        st.markdown("")
        st.latex(f"\\vec{{S}} = {P:.2f} + j{Q:.2f}\\;VA")


#---------------------------------------------------------------------------------------------------

    with col2:
        st.subheader(" Güç Faktörü Kompanzasyon Hesaplayıcısı")


        #Kullanıcı giriş
        P2 = parse_si(st.text_input("Aktif Güç (P) [W]", str(round(P, 2)), key="P2", max_chars=30))
        QL = parse_si(st.text_input("Endüktif Reaktif Güç (Q_L) [VAR]", str(round(Q, 2)), key="QL", max_chars=30))
        V2 = parse_si(st.text_input("Gerilim (V) [V]", str(round(V, 2)), key="V2", max_chars=30))
        f = parse_si(st.text_input("Frekans (f) [Hz]", "50", key="f", max_chars=10))
        PF_hedef = st.slider("Hedef Güç Faktörü (PF)", min_value=0.6, max_value=1.0, value=0.8, key="PF_hedef")

        #Uyarılar
        if P2 <= 0:
            st.warning("⚠️ Aktif güç değeri hatalıdır.")
        if QL < 0:
            st.warning("⚠️ Reaktif güç değeri hatalıdır.")
        if V2 <= 0:
            st.warning("⚠️ Gerilim değeri hatalıdır.")
        if f <= 0:
            st.warning("⚠️ Frekans değeri hatalıdır.")

        # Hesaplamalar
        S2 = math.sqrt(P2 ** 2 + QL ** 2)
        PF_mevcut = P2 / S2 if S2 != 0 else 0
        phi_hedef = math.acos(PF_hedef)
        QC = QL - P2 * math.tan(phi_hedef)

        # kontrol ve uyarılar
        if QC > 0 and f > 0 and V2 > 0:
            C = QC / (2 * math.pi * f * V2 ** 2)
        else:
            C = 0

        st.subheader("Hesaplama Sonuçları")
        st.write(f"**Önceki Güç Faktörü:** {PF_mevcut:.3f}")
        st.write(f"**Kompanzasyon için gereken kapasitif reaktif güç (Q_C):** {QC:.2f} VAR")
        st.write(f"**Gerekli Kapasitör Değeri (C):** {C * 1e6:.2f} μF" if C > 0 else "Kompanzasyona gerek yok.")

    with st.expander("AC Güç Üçgeni"):

        # AC Güç Üçgeni çiz


        fig, ax = plt.subplots(figsize=(6,6))
        scale = max(P2, QL, 1) * 0.05  # ok boyutu ölçeklendirme

        # Mevcut güç üçgeni
        ax.arrow(0, 0, P2, QL, head_width=scale, head_length=scale, fc='blue', ec='blue', label='Önceki S')
        ax.text(P2*0.5, QL*0.5, 'S_önceki', color='blue')

        # Kompanzasyon sonrası
        Q_after = QL - QC if QC>0 else QL
        ax.arrow(0, 0, P2, Q_after, head_width=scale, head_length=scale, fc='green', ec='green', label='Kompanzasyonlu S')
        ax.text(P2*0.5, Q_after*1.05, 'S_kompanzasyon', color='green')

        # Aktif ve reaktif bileşenler
        ax.plot([0,P2],[0,0], '--', label='P (aktif)')
        ax.plot([P2,P2],[0,Q_after], 'r--', label='Q (reaktif)')

        ax.set_xlabel('Aktif Güç P [W]')
        ax.set_ylabel('Reaktif Güç Q [VAR]')
        ax.set_title('AC Güç Üçgeni (Önceki ve Kompanzasyon Sonrası)')
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)
except:
    error_box.error("Bir hata oluştu. Lütfen girdilerinizi kontrol edip tekrar deneyin.")
    st.stop()