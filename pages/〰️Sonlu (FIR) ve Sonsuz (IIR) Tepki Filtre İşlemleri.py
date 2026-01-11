
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.signal import lfilter, butter, firwin, freqz, square, sawtooth

TITLE = 'ElektroXLab'
st.set_page_config(
    page_title=TITLE,
    page_icon="⚡",
    layout="wide",
)

st.title("〰️Sonlu (FIR) ve Sonsuz (IIR) Tepki Filtre İşlemleri")

with st.expander("AÇIKLAMA"):
    st.caption("Bilgilendirme:")
    st.caption("Dijital dünyada sürekli sinyal yoktur. Biz onu küçük noktalara bölerek saklarız. Buna örnekleme denir.")
    st.caption("FIR (Sonlu Tepki): [a]=[1]'dir yani geri besleme yoktur. Hep kararlıdır, lineer faz tasarlanabilir. Filtre derecesi büyük seçilmelidir.")
    st.caption("IIR (Sonsuz Tepki): Geri besleme vardır. Daha az derece ile daha keskin filtre yapılabilir, ama faz cevabı bozulur ve kararlılık problemi çıkabilir.")
    st.caption("Lowpass → düşük frekans geçer, yüksekler kesilir.")
    st.caption("Highpass → yüksek frekans geçer, düşükler kesilir.")
    st.caption("Bandpass → belirli bir aralık geçer.")
    st.caption("Bandstop → belirli bir aralık kesilir.")
    st.caption("FFT spektrum analizi, sinyalde baskın olan frekansları görmenizi sağlar.")
    st.caption("Frekans cevabı, filtrenin giriş sinyalindeki frekansların ne kadarının geçişine izin verdiğini gösterir.")

error_box = st.empty()
try:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sinyal Parametreleri")
        signal_type = st.selectbox("Sinyal Tipi:", ["Sinüs", "Kare", "Üçgen", "Kombinasyon"])
        phase = st.slider("Faz (radyan):", -np.pi, np.pi, 0.0, step=0.1)
        st.caption("-pi ile +pi aralığında.")

        if signal_type == "Kombinasyon":
            st.markdown("**Kombinasyon için 2 farklı sinüs dalgası seçin**")
            freq1 = st.number_input("Frekans 1 (Hz):", 1, 100, 5)
            amp1 = st.number_input("Genlik 1:", value=1.0, step=0.1)
            freq2 = st.number_input("Frekans 2 (Hz):", 1, 100, 10)
            amp2 = st.number_input("Genlik 2:", value=0.5, step=0.1)
        else:
            freq1 = st.number_input("Frekans (Hz):", 1, 100, 5)
            amp1 = st.number_input("Genlik:", value=1.0, step=0.1)
            freq2 = amp2 = 0

    duration = st.number_input("Sinyal Süresi (s):", value=2.0, step=0.1)
    sampling_rate = st.number_input("Örnekleme Frekansı (Hz):", value=500, step=10)
    t = np.linspace(0, duration, int(duration * sampling_rate))

    # Filtre Parametreleri
    st.subheader("⚙️ Filtre Parametreleri")
    filter_type = st.selectbox("Filtre Türü:", ["FIR", "IIR"])
    filter_design = st.selectbox("Filtre Tasarımı:", ["Lowpass", "Highpass", "Bandpass", "Bandstop"])
    cutoff_input = st.text_input("Kesme Frekansı(ları) [Hz] (Örn: 50 veya 50,150):", "50")
    order = st.number_input("Filtre Derecesi:", min_value=1, max_value=50, value=5)

    try:
        cutoff_values = [float(x.strip()) for x in cutoff_input.split(",") if x.strip() != ""]
    except ValueError:
        st.error("⚠️ Kesme frekansını sayısal değer olarak girin (örn: 50 veya 50,150).")
        cutoff_values = [50.0]

    nyq = 0.5 * sampling_rate
    normal_cutoff = [f / nyq for f in cutoff_values]

    # Cutoff kontrolü
    if (filter_design in ["Bandpass", "Bandstop"]) and len(normal_cutoff) != 2:
        st.warning("⚠️ Bandpass/Bandstop için 2 cutoff değeri girilmelidir. (örn: 30,80)")
        normal_cutoff = [0.2, 0.4]
    elif (filter_design in ["Lowpass", "Highpass"]) and len(normal_cutoff) != 1:
        st.warning("⚠️ Lowpass/Highpass için tek cutoff değeri girilmelidir.")
        normal_cutoff = [0.2]

    # Sinyal oluşturma
    if signal_type == "Sinüs":
        signal_vals = amp1 * np.sin(2 * np.pi * freq1 * t + phase)
    elif signal_type == "Kare":
        signal_vals = amp1 * square(2 * np.pi * freq1 * t + phase)
    elif signal_type == "Üçgen":
        signal_vals = amp1 * sawtooth(2 * np.pi * freq1 * t + phase, width=0.5)
    else:
        s1 = amp1 * np.sin(2 * np.pi * freq1 * t + phase)
        s2 = amp2 * np.sin(2 * np.pi * freq2 * t + phase)
        signal_vals = s1 + s2

    # Filtreleme
    if filter_type == "FIR":
        pass_zero = True if filter_design.lower() in ['lowpass', 'bandstop'] else False
        b = firwin(order + 1, cutoff=normal_cutoff, pass_zero=pass_zero)
        a = [1]
        filtered_vals = lfilter(b, a, signal_vals)
    else:
        if order > 12:
            st.warning("⚠️ Yüksek dereceli IIR filtreler kararsız olabilir. 12 üstüne çıkmayın.")
        b, a = butter(order, Wn=normal_cutoff, btype=filter_design.lower())
        filtered_vals = lfilter(b, a, signal_vals)

    w, h = freqz(b, a, worN=8000)

    # FFT
    N = len(t)
    freq_axis = np.fft.fftfreq(N, 1 / sampling_rate)
    fft_input = np.fft.fft(signal_vals)
    fft_output = np.fft.fft(filtered_vals)
    mask = freq_axis >= 0
    freq_axis = freq_axis[mask]
    fft_input = np.abs(fft_input[mask]) / N
    fft_output = np.abs(fft_output[mask]) / N

    with col2:
        col3, col4 = st.columns(2)

        with col3:
            fig_signal = go.Figure()
            fig_signal.add_trace(go.Scatter(x=t, y=signal_vals, mode='lines', name='Orijinal Sinyal'))
            fig_signal.update_layout(title="Orijinal Sinyal", xaxis_title="Zaman (s)", yaxis_title="Genlik", height=300)
            st.plotly_chart(fig_signal, use_container_width=True)

            fig_filtered = go.Figure()
            fig_filtered.add_trace(go.Scatter(x=t, y=signal_vals, mode='lines', name='Orijinal'))
            fig_filtered.add_trace(go.Scatter(x=t, y=filtered_vals, mode='lines', name='Filtrelenmiş'))
            fig_filtered.update_layout(title=f"{filter_type} Filtrelenmiş Sinyal", xaxis_title="Zaman (s)", yaxis_title="Genlik", height=300)
            st.plotly_chart(fig_filtered, use_container_width=True)

        with col4:
            fig_freq = go.Figure()
            fig_freq.add_trace(go.Scatter(x=w * sampling_rate / (2 * np.pi),
                                          y=20 * np.log10(np.maximum(abs(h), 1e-8)),
                                          mode='lines', name='Magnitude (dB)'))
            fig_freq.add_trace(go.Scatter(x=w * sampling_rate / (2 * np.pi),
                                          y=np.angle(h, deg=True),
                                          mode='lines', name='Phase (deg)', yaxis='y2'))
            fig_freq.update_layout(
                title=f"{filter_type} Frekans Cevabı",
                xaxis_title="Frekans (Hz)",
                yaxis=dict(title="Magnitude (dB)"),
                yaxis2=dict(title="Phase (deg)", overlaying='y', side='right'),
                height=300
            )
            st.plotly_chart(fig_freq, use_container_width=True)

            fig_fft = go.Figure()
            fig_fft.add_trace(go.Scatter(x=freq_axis, y=fft_input, mode='lines', name="Orijinal FFT"))
            fig_fft.add_trace(go.Scatter(x=freq_axis, y=fft_output, mode='lines', name="Filtrelenmiş FFT"))
            fig_fft.update_layout(title="FFT Spektrum Analizi", xaxis_title="Frekans (Hz)", yaxis_title="Genlik", height=300)
            st.plotly_chart(fig_fft, use_container_width=True)

except:
    error_box.error("Bir hata oluştu. Lütfen girdilerinizi kontrol edip tekrar deneyin.")
    st.stop()