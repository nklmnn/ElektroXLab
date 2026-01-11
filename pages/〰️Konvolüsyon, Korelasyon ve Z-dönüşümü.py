
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.signal import convolve, correlate


# Sayfa ayarı

TITLE = 'ElektroXLab'
st.set_page_config(
    page_title=TITLE,
    page_icon="⚡",
    layout="wide",
)
st.title("Konvolüsyon • Korelasyon • Z-Dönüşümü")
with st.expander("AÇIKLAMA"):
    st.write("Bu sayfa ayrık zamanlı sinyaller üzerinde yapılan üç temel işlemi gösterir. Konvolüsyon bölümünde x[n] ve h[n] dizileri kullanıcı tarafından seçilir veya elle girilir, ardından bu iki dizinin konvolüsyonu hesaplanarak bir LTI sistemin çıkışının nasıl oluştuğu zaman ekseninde gösterilir. Korelasyon bölümünde iki sinyal arasındaki benzerlik, kayma miktarına bağlı olarak hesaplanır ve sinyallerin birbirine ne kadar ve hangi gecikmede benzediği gözlemlenir. Z-dönüşümü bölümünde ise bir dizinin Z-düzlemindeki sıfırları birim çemberle birlikte çizilir ve aynı dizinin DTFT’si hesaplanarak frekans domenindeki genlik ve faz davranışı incelenir; böylece zaman alanı, z-düzlemi ve frekans alanı arasındaki ilişki doğrudan görülür.")

# Yardımcılar

def make_signal(kind, N, f=0.1, amp=1.0, duty=0.5, seed=0):
    n = np.arange(N)
    if kind == "Dizin (elle)":
        return None
    if kind == "Darbe (rect)":
        L = max(1, int(N * duty))
        x = np.zeros(N)
        x[:L] = amp
        return x
    if kind == "Sinüs":
        return amp * np.sin(2 * np.pi * f * n)
    if kind == "Üçgen":
        saw = (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * f * n))
        return amp * saw
    if kind == "Rastgele":
        rng = np.random.default_rng(seed)
        return amp * (2 * rng.random(N) - 1)
    return np.zeros(N)

def as_array_from_text(txt):
    if not txt.strip():
        return None
    try:
        vals = [float(v.strip()) for v in txt.split(",")]
        return np.array(vals, dtype=float)
    except Exception:
        return None

def zplane_plot(zeros, poles):
    fig = go.Figure()
    theta = np.linspace(0, 2 * np.pi, 512)
    fig.add_trace(go.Scatter(x=np.cos(theta), y=np.sin(theta),
                             mode="lines", name="|z|=1"))
    if zeros is not None and len(zeros) > 0:
        fig.add_trace(go.Scatter(x=zeros.real, y=zeros.imag,
                                 mode="markers",
                                 marker=dict(symbol="circle", size=10),
                                 name="Sıfırlar"))
    if poles is not None and len(poles) > 0:
        fig.add_trace(go.Scatter(x=poles.real, y=poles.imag,
                                 mode="markers",
                                 marker=dict(symbol="x", size=11),
                                 name="Kutup(lar)"))
    fig.update_layout(title="Z-Düzlemi (Birim Çember dâhil)",
                      xaxis_title="Re{z}", yaxis_title="Im{z}",
                      xaxis=dict(scaleanchor="y", scaleratio=1),
                      height=420)
    return fig

def dtft_on_unit_circle(x, nfft=2048):
    w = np.linspace(0, np.pi, nfft)
    ejw = np.exp(-1j * np.outer(w, np.arange(len(x))))
    X = ejw @ x
    return w, X


# Tabs

tab1, tab2, tab3 = st.tabs([
    "🔁 Konvolüsyon",
    "🎯 Korelasyon",
    "🌀 Z-Dönüşümü"
])


# 1 KONVOLÜSYON

with tab1:
    st.subheader("🔁 x[n] * h[n]")

    colA, colB = st.columns([1.2, 1.2])

    with colA:
        N_x = st.slider("x[n] uzunluğu", 4, 64, 16, key="Nx_conv")
        kind_x = st.selectbox("x[n] tipi",
                              ["Darbe (rect)", "Sinüs", "Üçgen", "Rastgele", "Dizin"],
                              key="kx_conv")
        x_text = st.text_input("x[n] (elle)", "1, 2, 1, 0, -1", key="xtext_conv")
        fx = st.slider("x[n] frekansı", 0.02, 0.45, 0.1, 0.01, key="fx_conv")
        ax = st.slider("x[n] genlik", 0.1, 3.0, 1.0, 0.1, key="ax_conv")
        dx = st.slider("x[n] darbe doluluk", 0.1, 1.0, 0.5, 0.05, key="dx_conv")

        x = make_signal(kind_x, N_x, f=fx, amp=ax, duty=dx)
        if kind_x == "Dizin":
            x = as_array_from_text(x_text)
        if x is None:
            st.warning("x[n] geçersiz. Sıfır dizi kullanıldı.")
            x = np.zeros(N_x)

    with colB:
        N_h = st.slider("h[n] uzunluğu", 3, 64, 8, key="Nh_conv")
        kind_h = st.selectbox("h[n] tipi",
                              ["Darbe (rect)", "Sinüs", "Üçgen", "Rastgele", "Dizin"],
                              key="kh_conv")
        h_text = st.text_input("h[n] (elle)", "1, -1, 1", key="htext_conv")
        fh = st.slider("h[n] frekansı", 0.02, 0.45, 0.2, 0.01, key="fh_conv")
        ah = st.slider("h[n] genlik", 0.1, 3.0, 1.0, 0.1, key="ah_conv")
        dh = st.slider("h[n] darbe doluluk", 0.1, 1.0, 0.5, 0.05, key="dh_conv")

        h = make_signal(kind_h, N_h, f=fh, amp=ah, duty=dh)
        if kind_h == "Dizin (elle)":
            h = as_array_from_text(h_text)
        if h is None:
            st.warning("h[n] geçersiz. Sıfır dizi kullanıldı.")
            h = np.zeros(N_h)

    y = convolve(x, h, mode="full")
    n_x, n_h, n_y = np.arange(len(x)), np.arange(len(h)), np.arange(len(y))

    fig_x = go.Figure().add_trace(go.Scatter(x=n_x, y=x, mode="lines+markers", name="x[n]"))
    fig_x.update_layout(title="x[n]", height=250)
    st.plotly_chart(fig_x, use_container_width=True)

    fig_h = go.Figure().add_trace(go.Scatter(x=n_h, y=h, mode="lines+markers", name="h[n]"))
    fig_h.update_layout(title="h[n]", height=250)
    st.plotly_chart(fig_h, use_container_width=True)

    fig_y = go.Figure().add_trace(go.Scatter(x=n_y, y=y, mode="lines+markers", name="y[n]"))
    fig_y.update_layout(title="Konvolüsyon Sonucu", height=320)
    st.plotly_chart(fig_y, use_container_width=True)


    # 2 KORELASYON

with tab2:
    st.subheader("🎯 x[n] ⊗ h[n]")

    N1 = st.slider("x[n] uzunluğu", 4, 64, 16, key="Nx_corr")
    kx2 = st.selectbox("x[n] tipi",
                       ["Darbe (rect)", "Sinüs", "Üçgen", "Rastgele", "Dizin"],
                       key="kx_corr")
    x2_text = st.text_input("x[n]", "1, 2, 1, 0, -1", key="xtext_corr")
    fx2 = st.slider("x[n] frekansı", 0.02, 0.45, 0.15, 0.01, key="fx_corr")
    ax2 = st.slider("x[n] genlik", 0.1, 3.0, 1.0, 0.1, key="ax_corr")
    dx2 = st.slider("x[n] darbe doluluk", 0.1, 1.0, 0.5, 0.05, key="dx_corr")

    x2 = make_signal(kx2, N1, f=fx2, amp=ax2, duty=dx2)
    if kx2 == "Dizin":
        x2 = as_array_from_text(x2_text)
    if x2 is None:
        x2 = np.zeros(N1)

    N2 = st.slider("h[n] uzunluğu", 3, 64, 8, key="Nh_corr")
    kh2 = st.selectbox("h[n] tipi",
                       ["Darbe (rect)", "Sinüs", "Üçgen", "Rastgele", "Dizin"],
                       key="kh_corr")
    h2_text = st.text_input("h[n]", "1, -1, 1", key="htext_corr")
    fh2 = st.slider("h[n] frekansı", 0.02, 0.45, 0.2, 0.01, key="fh_corr")
    ah2 = st.slider("h[n] genlik", 0.1, 3.0, 1.0, 0.1, key="ah_corr")
    dh2 = st.slider("h[n] darbe doluluk", 0.1, 1.0, 0.5, 0.05, key="dh_corr")

    h2 = make_signal(kh2, N2, f=fh2, amp=ah2, duty=dh2)
    if kh2 == "Dizin":
        h2 = as_array_from_text(h2_text)
    if h2 is None:
        h2 = np.zeros(N2)

    r = correlate(x2, h2, mode="full")
    n_r = np.arange(-(len(h2)-1), len(x2))

    fig_r = go.Figure().add_trace(go.Scatter(x=n_r, y=r, mode="lines+markers"))
    fig_r.update_layout(title="Korelasyon Sonucu", height=320)
    st.plotly_chart(fig_r, use_container_width=True)


    # 3) Z-DÖNÜŞÜMÜ

with tab3:
    st.subheader("🌀 Z-Dönüşümü: Sıfırlar / DTFT")

    c1, c2 = st.columns([1.4, 1])

    with c1:
        N_z = st.slider("Dizi uzunluğu", 2, 128, 16, key="Nz")
        kind_z = st.selectbox("x[n] tipi",
                              ["Darbe (rect)", "Sinüs", "Üçgen", "Rastgele", "Dizin"],
                              key="kz")
        xz_text = st.text_input("x[n]", "1, 0.5, 0, -0.25", key="xztext")
        fz = st.slider("Frekans", 0.02, 0.45, 0.12, 0.01, key="fz")
        az = st.slider("Genlik", 0.1, 3.0, 1.0, 0.1, key="az")
        dz = st.slider("Darbe doluluk", 0.1, 1.0, 0.5, 0.05, key="dz")

    with c2:
        causal = st.radio("Kısmi nedensellik", ["0 (başlangıç)", "Pozitif ofset"], key="z_causal")
        n0 = st.number_input("n₀ gecikmesi", value=0, min_value=0, step=1, key="z_n0")
        show_phase = st.checkbox("Fazı göster", True, key="z_phase")
        norm_mag = st.checkbox("Magnitude normalize", True, key="z_norm")

    xz = make_signal(kind_z, N_z, f=fz, amp=az, duty=dz)
    if kind_z == "Dizin":
        xz = as_array_from_text(xz_text)
        if xz is None:
            xz = np.zeros(N_z)

    if causal == "Pozitif ofset" and n0 > 0:
        xz = np.concatenate([np.zeros(n0), xz])

    coeff_q = xz.astype(float)
    zeros = np.array([])
    if np.any(coeff_q):
        nz = np.trim_zeros(coeff_q, 'b')
        if len(nz) >= 2:
            roots = np.roots(nz)
            zeros = np.array([1/r for r in roots if abs(r) > 1e-12])

    fig_z = zplane_plot(zeros, [])
    st.plotly_chart(fig_z, use_container_width=True)

    w, X = dtft_on_unit_circle(xz)
    mag, pha = np.abs(X), np.angle(X)

    if norm_mag and np.max(mag) > 0:
        mag /= np.max(mag)

    fig_mag = go.Figure().add_trace(go.Scatter(x=w/np.pi,
                                               y=20*np.log10(np.maximum(mag, 1e-8)),
                                               mode="lines"))
    fig_mag.update_layout(title="DTFT Magnitude", height=320)
    st.plotly_chart(fig_mag, use_container_width=True)

    if show_phase:
        fig_ph = go.Figure().add_trace(go.Scatter(x=w/np.pi, y=np.unwrap(pha), mode="lines"))
        fig_ph.update_layout(title="DTFT Faz", height=320)
        st.plotly_chart(fig_ph, use_container_width=True)
