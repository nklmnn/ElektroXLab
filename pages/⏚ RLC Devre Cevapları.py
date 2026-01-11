import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.signal import TransferFunction, step, impulse, bode

TITLE = 'ElektroXLab'
st.set_page_config(
    page_title=TITLE,
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ RLC Devre Cevapları")
with st.expander ("AÇIKLAMA"):
    st.markdown(""""Devre Tipi Seçimi: Açılır menüden Seri RLC veya Paralel RLC seçiniz.

Eleman Değerleri: Direnç (R), İndüktör (L) ve Kondansatör (C) değerlerini giriniz.

Zaman Parametreleri: Simülasyon süresi ve örnekleme frekansını ayarlayınız.

Çıktılar:
Step & Impulse Response: Devrenin zaman alanındaki basamak ve darbe girişlerine verdiği cevaptır.

Magnitude Response: Frekans cevabının genlik grafiği (dB).

Phase Response: Frekans cevabının faz grafiği (derece).

Zaman Sabiti & Sönümleme Katsayısı: Hesaplanan ω₀, ζ ve τ değerleri.

Sönümlü Salınım Grafiği: Devrenin doğal frekans ve sönümleme katsayısına göre salınım davranışı.""")
error_box = st.empty()
try:
    # Devre tipi seçimi
    circuit_type = st.selectbox("Devre Tipi:", ["Seri RLC", "Paralel RLC"])

    # Eleman değerleri
    R = st.number_input("Direnç R (Ω):",  min_value=0.000001, value=10.0)
    L = st.number_input("İndüktör L (H):",  min_value=0.000001, value=0.01)
    C = st.number_input("Kondansatör C (F):", min_value=0.000001, value=0.01)

    # Zaman parametreleri
    duration = st.number_input("Simülasyon Süresi (s):", value=0.05)
    sampling_rate = st.number_input("Örnekleme Frekansı (Hz):", value=10000)
    t = np.linspace(0, duration, int(duration*sampling_rate))


    # Transfer Fonksiyonu
    if circuit_type == "Seri RLC":
        num = [1]
        den = [L*C, R*C, 1]
    else:  # Paralel RLC
        num = [R*C, 1]
        den = [L*C, R*C, 1]

    sys = TransferFunction(num, den)


    # Step ve Impulse Yanıtı

    t_step, y_step = step(sys, T=t)
    t_imp, y_imp = impulse(sys, T=t)

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=t_step, y=y_step, mode='lines', name='Step Response'))
    fig1.add_trace(go.Scatter(x=t_imp, y=y_imp, mode='lines', name='Impulse Response'))
    fig1.update_layout(title=f"{circuit_type} - Step & Impulse Response",
                       xaxis_title="Zaman (s)", yaxis_title="Genlik", height=400)
    st.plotly_chart(fig1, use_container_width=True)


    # Frekans cevabı Magnitude ve Phase ayrı grafikler

    w = np.logspace(1, 5, 1000)  # 10^1 ile 10^5 arası
    w, mag, phase = bode(sys, w=w)

    # Magnitude grafiği
    fig_mag = go.Figure()
    fig_mag.add_trace(go.Scatter(x=w, y=mag, mode='lines', name='Magnitude (dB)'))
    fig_mag.update_layout(
        title=f"{circuit_type} - Frekans Cevabı (Magnitude)",
        xaxis=dict(title="Frekans (rad/s)", type="log",
                   tickvals=[10, 100, 1000, 10000, 100000],
                   ticktext=["10", "10²", "10³", "10⁴", "10⁵"]),
        yaxis=dict(title="Magnitude (dB)"),
        height=400
    )
    st.plotly_chart(fig_mag, use_container_width=True)

    # Phase grafiği
    fig_phase = go.Figure()
    fig_phase.add_trace(go.Scatter(x=w, y=phase, mode='lines', name='Phase (deg)'))
    fig_phase.update_layout(
        title=f"{circuit_type} - Frekans Cevabı (Phase)",
        xaxis=dict(title="Frekans (rad/s)", type="log",
                   tickvals=[10, 100, 1000, 10000, 100000],
                   ticktext=["10", "10²", "10³", "10⁴", "10⁵"]),
        yaxis=dict(title="Phase (deg)"),
        height=400
    )
    st.plotly_chart(fig_phase, use_container_width=True)


    # Zaman sabiti ve sönümleme katsayısı

    st.subheader("Zaman Sabiti & Sönümleme Katsayısı")

    omega_0 = 1/np.sqrt(L*C)
    zeta = R/(2*np.sqrt(L/C))
    tau = 1/(zeta*omega_0)

    st.write(f"🔹 Doğal Frekans ω₀: {omega_0:.2f} rad/s")
    st.write(f"🔹 Sönümleme Katsayısı ζ: {zeta:.2f}")
    st.write(f"🔹 Zaman Sabiti τ: {tau:.4f} s")

    # Sönümlü salınım grafiği
    t_damped = np.linspace(0, 5*tau, 500)

    if zeta < 1:  # Underdamped
        y_damped = np.exp(-zeta*omega_0*t_damped) * np.sin(omega_0*np.sqrt(1 - zeta**2) * t_damped)
    elif zeta == 1:  # Critically damped
        y_damped = t_damped * np.exp(-omega_0 * t_damped)
    else:  # Overdamped
        s1 = -omega_0 * (zeta - np.sqrt(zeta**2 - 1))
        s2 = -omega_0 * (zeta + np.sqrt(zeta**2 - 1))
        y_damped = np.exp(s1 * t_damped) - np.exp(s2 * t_damped)

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=t_damped, y=y_damped, mode='lines', name='Damped Oscillation'))
    fig3.update_layout(title=f"{circuit_type} - Sönümlü Salınım",
                       xaxis_title="Zaman (s)", yaxis_title="Genlik", height=400)
    st.plotly_chart(fig3, use_container_width=True)

except Exception as e:
    error_box.error(f"Bir hata oluştu: {str(e)}")
    st.stop()
