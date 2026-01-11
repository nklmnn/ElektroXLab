import streamlit as st
import numpy as np
import plotly.graph_objects as go

TITLE = 'ElektroXLab'
st.set_page_config(
    page_title=TITLE,
    page_icon="⚡",
    layout="wide",
)

st.title("〰️ Sinyal Üretici")
with st.expander("AÇIKLAMA"):
    st.markdown("""
    Bu araç ile farklı dalga tiplerini oluşturabilir, zaman ve frekans domeninde görselleştirebilir,
    ve aynı sinyalin enerji ve ortalama gücünü hesaplayabilirsiniz.
    """)

error_box = st.empty()
try:
    # ---------- Kullanıcı Girdileri ----------
    wave_type = st.selectbox("Dalga Tipi Seç:", ["Sinüs", "Kare", "Üçgen", "Testere Dişi", "Rastgele"])
    amplitude = st.number_input("Genlik (V veya A):", value=1.0, step=0.1)
    frequency = st.number_input("Frekans (Hz):", value=50.0, step=1.0)
    phase_deg = st.number_input("Faz (°):", value=0.0, step=1.0)
    duration = st.number_input("Sinyal Süresi (s):", value=0.1, step=0.01)
    sampling_rate = st.number_input("Örnekleme Frekansı (Hz):", value=1000, step=10)

    t = np.linspace(0, duration, int(duration * sampling_rate))
    phase_rad = np.deg2rad(phase_deg)

    # ---------- Dalga Üretimi ----------
    if wave_type == "Sinüs":
        y = amplitude * np.sin(2 * np.pi * frequency * t + phase_rad)
    elif wave_type == "Kare":
        y = amplitude * np.sign(np.sin(2 * np.pi * frequency * t + phase_rad))
    elif wave_type == "Üçgen":
        y = amplitude * 2*np.abs(2*((t*frequency - np.floor(t*frequency + 0.5)))) - amplitude
    elif wave_type == "Testere Dişi":
        y = amplitude * (2*(t*frequency - np.floor(t*frequency)))
    elif wave_type == "Rastgele":
        y = amplitude * np.random.randn(len(t))
    else:
        y = amplitude * np.sin(2 * np.pi * frequency * t + phase_rad)

    # ---------- Zaman Domeni Grafiği ----------
    st.subheader("📈 Zaman Domeni")
    fig_time = go.Figure()
    fig_time.add_trace(go.Scatter(x=t, y=y, mode='lines', name='Sinyal'))
    fig_time.update_layout(xaxis_title="Zaman (s)", yaxis_title="Genlik", height=400)
    st.plotly_chart(fig_time, use_container_width=True)

    # ---------- FFT Frekans Spektrumu ----------
    if st.checkbox("Frekans Spektrumu Göster"):
        st.subheader("📊 Frekans Spektrumu")
        Y_fft = np.fft.fft(y)
        f = np.fft.fftfreq(len(t), 1/sampling_rate)
        fig_fft = go.Figure()
        fig_fft.add_trace(go.Scatter(
            x=f[:len(f)//2], y=2/len(t)*np.abs(Y_fft[:len(f)//2]),
            mode='lines', name='FFT'
        ))
        fig_fft.update_layout(xaxis_title="Frekans (Hz)", yaxis_title="Genlik", height=400)
        st.plotly_chart(fig_fft, use_container_width=True)

    # ---------- Enerji ve Güç Hesaplama ----------
    st.subheader("⚡ Sinyal Enerjisi ve Ortalama Güç")
    signal_energy = np.sum(np.abs(y)**2) * (1/sampling_rate)
    signal_power = signal_energy / duration

    st.write(f"🔹 Sinyal Enerjisi: {signal_energy:.6f} V²·s")
    st.write(f"🔹 Ortalama Güç: {signal_power:.6f} V²")

except:
    error_box.error("Bir hata oluştu. Lütfen girdilerinizi kontrol edip ytekrar deneyin.")
    st.stop()