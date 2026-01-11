import streamlit as st
import numpy as np
import scipy.signal as signal
import plotly.graph_objects as go

TITLE = 'ElektroXLab'
st.set_page_config(
    page_title=TITLE,
    page_icon="⚡",
    layout="wide",
)

st.title("📈 Sistem Analizi: Impulse, Step, Pole-Zero & Stabilite")
with st.expander("AÇIKLAMA"):
    st.write("Bu kod, kullanıcının girdiği transfer fonksiyonuna ait temel kontrol ve sistem analizi grafiklerini etkileşimli olarak üreten bir Streamlit arayüzüdür; kullanıcı pay ve payda katsayılarını girerek sistemi tanımlar, ardından sistemin impuls yanıtı, basamak (step) yanıtı, kutup–sıfır haritası, Bode diyagramı (genlik ve faz) ve Nyquist diyagramı otomatik olarak hesaplanıp görselleştirilir. Böylece sistemin zaman domenindeki davranışı, frekans cevabı ve kararlılık özellikleri tek bir ekranda, sayısal hesap yükü kullanıcıya hissettirilmeden analiz edilebilir; kod esasen teorik kontrol kavramlarını somut grafiklere dönüştüren bir öğretici ve doğrulayıcı analiz aracı gibi çalışır.")
error_box = st.empty()
try:
    # Kullanıcı girişi
    numerator_input = st.text_input("Pay (katsayılar, en yüksek dereceden başlayarak, virgülle ayır):", "1")
    denominator_input = st.text_input("Payda (katsayılar, en yüksek dereceden başlayarak, virgülle ayır):", "1,1")

    # Katsayıları ayır
    num = [float(x.strip()) for x in numerator_input.split(",")]
    den = [float(x.strip()) for x in denominator_input.split(",")]

    # Transfer fonksiyonu oluştur
    sys = signal.TransferFunction(num, den)

    # Zaman vektörü
    t = np.linspace(0, 5, 1000)

    # Impulse yanıt
    t_imp, y_imp = signal.impulse(sys, T=t)
    fig_imp = go.Figure()
    fig_imp.add_trace(go.Scatter(x=t_imp, y=y_imp, mode='lines', name='Impulse Response'))
    fig_imp.update_layout(title="Impulse Response", xaxis_title="Zaman (s)", yaxis_title="Genlik", height=400)
    st.plotly_chart(fig_imp, use_container_width=True)

    # Step yanıt
    t_step, y_step = signal.step(sys, T=t)
    fig_step = go.Figure()
    fig_step.add_trace(go.Scatter(x=t_step, y=y_step, mode='lines', name='Step Response'))
    fig_step.update_layout(title="Step Response", xaxis_title="Zaman (s)", yaxis_title="Genlik", height=400)
    st.plotly_chart(fig_step, use_container_width=True)

    # Pole-Zero Analizi
    zeros = np.roots(num)
    poles = np.roots(den)
    fig_pz = go.Figure()
    fig_pz.add_trace(go.Scatter(x=np.real(zeros), y=np.imag(zeros), mode='markers',
                                marker=dict(symbol='circle', size=10, color='green'), name='Zeros'))
    fig_pz.add_trace(go.Scatter(x=np.real(poles), y=np.imag(poles), mode='markers',
                                marker=dict(symbol='x', size=10, color='red'), name='Poles'))
    fig_pz.update_layout(title="Pole-Zero Haritası", xaxis_title="Re", yaxis_title="Im", height=400)
    st.plotly_chart(fig_pz, use_container_width=True)

    # Bode Diyagramı (Magnitude ve Phase ayrı grafikler)
    w = np.logspace(-2, 4, 1000)  # 10^-2 ile 10^4 arası frekans
    w, mag, phase = signal.bode(sys, w=w)

    # Magnitude grafiği
    fig_mag = go.Figure()
    fig_mag.add_trace(go.Scatter(x=w, y=mag, mode='lines', name='Magnitude (dB)'))
    fig_mag.update_layout(
        title="Bode Grafiği - Magnitude",
        xaxis=dict(
            title="Frekans (rad/s)",
            type="log",
            tickvals=[0.1, 1, 10, 100, 1000, 10000],
            ticktext=["10⁻¹","10⁰","10¹","10²","10³","10⁴"]
        ),
        yaxis=dict(title="Magnitude (dB)"),
        height=400
    )
    st.plotly_chart(fig_mag, use_container_width=True)

    # Phase grafiği
    fig_phase = go.Figure()
    fig_phase.add_trace(go.Scatter(x=w, y=phase, mode='lines', name='Phase (deg)'))
    fig_phase.update_layout(
        title="Bode Grafiği - Phase",
        xaxis=dict(
            title="Frekans (rad/s)",
            type="log",
            tickvals=[0.1, 1, 10, 100, 1000, 10000],
            ticktext=["10⁻¹","10⁰","10¹","10²","10³","10⁴"]
        ),
        yaxis=dict(title="Phase (deg)"),
        height=400
    )
    st.plotly_chart(fig_phase, use_container_width=True)

    # Nyquist Grafiği
    w_nyq = np.logspace(-2, 4, 1000)  # 10^-2 ile 10^4 arası
    w, h = signal.freqresp(sys, w=w_nyq)
    fig_nyq = go.Figure()
    fig_nyq.add_trace(go.Scatter(x=np.real(h), y=np.imag(h), mode='lines', name='Nyquist'))
    fig_nyq.add_trace(go.Scatter(x=np.real(h), y=-np.imag(h), mode='lines', name='Mirror'))
    fig_nyq.update_layout(title="Nyquist Grafiği", xaxis_title="Re(G(s))", yaxis_title="Im(G(s))", height=400)
    st.plotly_chart(fig_nyq, use_container_width=True)

except Exception as e:
    error_box.error("Bir hata oluştu: Lütfen pay ve payda değerlerinizi kontrol ediniz.")
    st.stop()
