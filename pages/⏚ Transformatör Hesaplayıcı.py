import numpy as np
import streamlit as st
import plotly.graph_objects as go

TITLE = 'ElektroXLab'
st.set_page_config(
    page_title=TITLE,
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ Transformatör Hesaplayıcı")

with st.expander("AÇIKLAMA"):
    st.markdown("""
    Transformatörler (trafolar), AC akım ile çalışan ve **manyetik indüksiyon prensibiyle**
    gerilim ve akımı **frekansı değiştirmeden** dönüştüren elektrik makineleridir.

    Bu sayfada **ideal trafoya yakın** hesaplamalar yapabilirsiniz:
    - **Sarım oranı**: a = Np / Ns  
    - **Gerilim dönüşümü**: Vp / Vs = a  
    - **Akım dönüşümü**: Is / Ip = a  
    - **Görünür güç (VA)**  
    - **Empedans yansıtma**: Z'ₚ = a² · Zₛ  
    - **Bakır kayıpları (opsiyonel)**  
    """)

error_box = st.empty()

try:

    # Yardımcı fonksiyonlar

    def safe_float(x):
        try:
            return float(x)
        except:
            return None

    def add_metric(label, value, unit=""):
        if value is None:
            st.metric(label, "—")
        else:
            st.metric(label, f"{value:.6g} {unit}")


    # Girdiler

    colL, colR = st.columns([1.2, 1])

    with colL:
        st.subheader("🔢 Temel Parametreler")
        Np = st.number_input("Primer Sarım Sayısı Np", min_value=1, value=1000, step=1)
        Ns = st.number_input("Sekonder Sarım Sayısı Ns", min_value=1, value=100, step=1)

        Vp = st.number_input("Primer Gerilimi Vp (V RMS)", min_value=0.0, value=230.0)
        Vs_in = st.text_input("Sekonder Gerilimi Vs (V RMS) — boşsa hesaplanır", "")
        Vs_given = safe_float(Vs_in)

        VA_in = st.text_input("Nominal Güç (VA) — opsiyonel", "")
        VA = safe_float(VA_in)

        eta = st.slider("Verim (η, %)", 50, 100, 95) / 100

    with colR:
        st.subheader("🔌 Yük & Kayıplar")
        Zs = safe_float(st.text_input("Sekonder Yük Empedansı Zₛ (Ω)", ""))

        Rp = safe_float(st.text_input("Primer Sargı Direnci Rp (Ω)", ""))
        Rs = safe_float(st.text_input("Sekonder Sargı Direnci Rs (Ω)", ""))

    st.divider()


    # Hesaplar

    a = Np / Ns

    Vs = Vs_given if Vs_given is not None else Vp * (Ns / Np)

    Ip = Is = Pin = Pout = None

    if VA is not None and Vp > 0:
        Is = VA / Vs
        Ip = VA / Vp
        Pin = VA
        Pout = VA * eta
    elif Zs is not None:
        Is = Vs / Zs
        Ip = Is / a
        VA = Vs * abs(Is)
        Pin = Vp * abs(Ip)
        Pout = Pin * eta

    Zp_ref = (a ** 2) * Zs if Zs is not None else None

    Pcu_p = (Ip ** 2) * Rp if (Ip is not None and Rp is not None) else None
    Pcu_s = (Is ** 2) * Rs if (Is is not None and Rs is not None) else None
    Pcu_total = (Pcu_p or 0) + (Pcu_s or 0) if (Pcu_p or Pcu_s) else None

    # Basit gerilim regülasyonu
    reg_percent = None
    if (Rp is not None or Rs is not None) and Is is not None:
        Req_sec = (Rp or 0) * (Ns / Np) ** 2 + (Rs or 0)
        Vdrop = Is * Req_sec
        reg_percent = (Vdrop / Vs) * 100 if Vs else None


    # Çıktılar

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        add_metric("Sarım Oranı a", a)
        add_metric("Primer Gerilim Vp", Vp, "V")
    with c2:
        add_metric("Sekonder Gerilim Vs", Vs, "V")
        add_metric("Nominal Güç", VA, "VA")
    with c3:
        add_metric("Primer Akım Ip", Ip, "A")
        add_metric("Sekonder Akım Is", Is, "A")
    with c4:
        add_metric("Yansıtılmış Empedans Z'ₚ", Zp_ref, "Ω")

    r1, r2, r3 = st.columns(3)
    with r1:
        add_metric("Bakır Kaybı (Primer)", Pcu_p, "W")
    with r2:
        add_metric("Bakır Kaybı (Sekonder)", Pcu_s, "W")
    with r3:
        add_metric("Toplam Bakır Kaybı", Pcu_total, "W")

    if reg_percent is not None:
        st.info(f"Basit gerilim regülasyonu ≈ **{reg_percent:.2f}%**")


    # Görsel: Gerilim dönüşümü

    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=Vs,
        delta={"reference": Vp, "relative": True},
        title={"text": "Gerilim Dönüşümü (Vs / Vp)"},
        domain={"x": [0, 1], "y": [0, 1]}
    ))
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    error_box.error(f"Hata oluştu: {e}")
    st.stop()
