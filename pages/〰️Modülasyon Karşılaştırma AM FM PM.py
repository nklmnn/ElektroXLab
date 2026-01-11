import streamlit as st
import numpy as np
import plotly.graph_objects as go
TITLE = 'ElektroXLab'
st.set_page_config(
    page_title=TITLE,
    page_icon="⚡",
    layout="wide",
)

st.title(" Modülasyon Karşılaştırma (AM / FM / PM)")
with st.expander("AÇIKLAMA"):
    st.markdown("Modülasyon, bir bilginin (ses ya da analog işaret) iletilebilmesi için yüksek frekanslı bir taşıyıcı sinyalin **genlik, frekans veya fazının**, bilgi sinyaline bağlı olarak değiştirilmesi işlemidir. Bu işlem sinyalin daha uzak mesafelere taşınmasını, anten boyutlarının küçülmesini ve parazitin azaltılmasını sağlar. Analog haberleşmede başlıca **genlik modülasyonu (AM)**, **frekans modülasyonu (FM)** ve **faz modülasyonu (PM)** kullanılır; AM yapısal olarak basit ama gürültüye hassas, FM ve PM ise daha geniş bant karşılığında daha yüksek gürültü bağışıklığı sunar.")
error_box = st.empty()
try:
    # Kullanıcı giriş sinyali parametreleri
    amplitude = st.number_input("Mesaj Sinyal Genliği:", value=1.0, step=0.1)
    frequency = st.number_input("Mesaj Sinyal Frekansı (Hz):", value=5.0, step=0.1)
    phase = st.number_input("Mesaj Sinyal Fazı (radyan):", value=0.0, step=0.01)
    duration = st.number_input("Sinyal Süresi (saniye):", value=1.0, step=0.1)
    sampling_rate = st.number_input("Örnekleme Frekansı (Hz):", value=1000, step=10)

    t = np.arange(0, duration, 1/sampling_rate)
    message_signal = amplitude * np.sin(2*np.pi*frequency*t + phase)

    # Modülasyon parametreleri
    carrier_freq = st.number_input("Taşıyıcı Frekansı (Hz):", value=50.0, step=1.0)
    mod_index = st.number_input("Modülasyon İndeksi:", value=0.5, step=0.01)

    # Modülasyon sinyalleri
    am_signal = (1 + mod_index*message_signal) * np.sin(2*np.pi*carrier_freq*t)
    fm_signal = np.sin(2 * np.pi * carrier_freq * t + mod_index * np.cumsum(message_signal) / sampling_rate)
    pm_signal = np.sin(2*np.pi*carrier_freq*t + mod_index*message_signal)

    # Demodülasyonumsu
    demod_am = np.abs(am_signal) - 1
    demod_fm = np.diff(np.unwrap(np.angle(np.exp(1j*fm_signal))))
    demod_fm = np.append(demod_fm, demod_fm[-1])
    demod_pm = np.diff(np.unwrap(np.angle(np.exp(1j*pm_signal))))
    demod_pm = np.append(demod_pm, demod_pm[-1])

    # AM, FM, PM karşılaştırmalı grafik
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=message_signal, mode='lines', name='Mesaj Sinyali', line=dict(color='black')))
    fig.add_trace(go.Scatter(x=t, y=am_signal, mode='lines', name='AM Modüle'))
    fig.add_trace(go.Scatter(x=t, y=fm_signal, mode='lines', name='FM Modüle'))
    fig.add_trace(go.Scatter(x=t, y=pm_signal, mode='lines', name='PM Modüle'))
    fig.update_layout(title="AM / FM / PM Modülasyon Karşılaştırması", xaxis_title="Zaman (s)", yaxis_title="Genlik",
                      height=400, margin=dict(l=40, r=20, t=40, b=40))
    st.plotly_chart(fig, use_container_width=True)

    # Demodülasyon karşılaştırma grafiği
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=t, y=demod_am, mode='lines', name='AM Demodülasyonu'))
    fig2.add_trace(go.Scatter(x=t, y=demod_fm, mode='lines', name='FM Demodülasyonu'))
    fig2.add_trace(go.Scatter(x=t, y=demod_pm, mode='lines', name='PM Demodülasyonu'))
    fig2.update_layout(title="Basit Demodülasyon Karşılaştırması (Zarflanmış haller)", xaxis_title="Zaman (s)", yaxis_title="Genlik",
                       height=400, margin=dict(l=40, r=20, t=40, b=40))
    st.plotly_chart(fig2, use_container_width=True)

except:
    error_box.error("Bir hata oluştu. Lütfen girdilerinizi kontrol edip tekrar deneyin.")
    st.stop()