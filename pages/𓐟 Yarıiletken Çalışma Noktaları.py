import streamlit as st
import numpy as np
import plotly.graph_objs as go
TITLE = 'ElektroXLab'
st.set_page_config(
    page_title=TITLE,
    page_icon="⚡",
    layout="wide",
)



error_box = st.empty()
try:

    # SI birimleri
    def parse_input(value_str):
        try:
            if value_str is None or value_str.strip() == "":
                return 0.0
            value_str = value_str.replace(",", ".").strip()
            units = {
                "n": 1e-9,
                "m": 1e-3,
                "u": 1e-6,
                "k": 1e3,
                "M": 1e6,
                "G": 1e9,
            }
            for unit, factor in units.items():
                if value_str.endswith(unit):
                    return float(value_str[:-1]) * factor
            return float(value_str)
        except:
            return 0.0

    # Başlık ---
    st.title("𓐟 Yarıiletken Çalışma Bölgeleri (BJT & MOSFET & Diyot)")
    with st.expander("AÇIKLAMA"):
        st.write("Bu sayfada transistörlerin ilgili akımlarını ve çalıştıkları bölgeyi görebilirsiniz.")
        st.subheader("Diyot (PN Diyot) Formülleri")

        st.latex(r"""
        I_D = I_S \left( e^{\frac{V_D}{n V_T}} - 1 \right)
        """)
        st.latex(r"""
        V_T = \frac{k T}{q} \approx 25.85 \text{ mV (300 K)}
        """)
        st.latex(r"""
        r_d = \frac{n V_T}{I_D}
         """)
        st.latex(r"""
        \begin{cases}
        V_D > 0 \Rightarrow \text{İletimde} \\
        V_D < 0 \Rightarrow \text{Kesimde}
        \end{cases}
        """)
        st.subheader("BJT Formülleri")

        st.latex(r"""
        I_C = \beta I_B
        """)

        st.latex(r"""
        I_E = I_C + I_B
        """)
        st.latex(r"""
        V_{BE} \approx 0.7 \text{ V}, \quad V_{CE} > V_{CE(sat)}
        """)
        st.latex(r"""
        V_{CE} = V_{CC} - I_C R_C - I_E R_E
        """)
        st.latex(r"""
        \begin{cases}
        \text{Kesim: } I_B = 0 \\
        \text{Aktif: } V_{BE} > 0,\; V_{BC} < 0 \\
        \text{Doyum: } V_{CE} \approx 0.2 \text{ V}
        \end{cases}
        """)
        st.subheader("MOSFET Formülleri")

        st.latex(r"""
        \begin{cases}
        \text{Kesim: } V_{GS} < V_T \\
        \text{Triyot: } V_{GS} > V_T,\; V_{DS} < V_{GS}-V_T \\
        \text{Doyum: } V_{GS} > V_T,\; V_{DS} \ge V_{GS}-V_T
        \end{cases}
        """)
        st.latex(r"""
        I_D = k_n \left[ (V_{GS} - V_T)V_{DS} - \frac{V_{DS}^2}{2} \right]
        """)
        st.latex(r"""
        I_D = \frac{1}{2} k_n (V_{GS} - V_T)^2
        """)


    device_type = st.radio("Transistör tipi seçiniz:", ["BJT", "MOSFET", "Diyot"])

    # BJT ---
    if device_type == "BJT":
        st.markdown("BJT Parametreleri")

        transistor_type = st.radio("Tip:", ["NPN", "PNP"])
        beta = st.number_input("Kazanç (β)", 10, 500, 100)

        V_CE = parse_input(st.text_input("Kollektör-Emiter Gerilimi, VCE (V)", "5"))
        I_B  = parse_input(st.text_input("Baz Akımı, IB (A veya mA)", "1m"))

        V_CE_sat = 0.2  # doyum gerilimi

        # Kesim - Aktif - Doyum
        if I_B <= 1e-9:
            region = "Kesim (Cutoff)"
            color = "blue"
        elif V_CE > V_CE_sat:
            region = "Aktif (Active)"
            color = "green"
        else:
            region = "Doyum (Saturation)"
            color = "red"

        # Akım hesapları
        I_C_mag = beta * I_B
        I_C = I_C_mag if transistor_type == "NPN" else -I_C_mag

        st.write(f" Çalışma Bölgesi: **{region}**")
        st.latex(rf"I_{{C}} \approx {I_C:.4f}\;A")

        # Çıkış karakteristiği
        V_CE_range = np.linspace(0, max(10, V_CE*1.5), 500)
        I_C_range_mag = beta * I_B * (1 - np.exp(-V_CE_range / 10))
        I_C_range = I_C_range_mag if transistor_type == "NPN" else -I_C_range_mag

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=V_CE_range, y=I_C_range,
                                 mode="lines", name="IC- VCE Karakteristiği"))
        fig.add_trace(go.Scatter(x=[V_CE], y=[I_C],
                                 mode="markers", name="Çalışma Noktası",
                                 marker=dict(color=color, size=10)))
        fig.update_layout(title="BJT Çıkış Karakteristiği",
                          xaxis_title="VCE (V)", yaxis_title="IC (A)")
        st.plotly_chart(fig, use_container_width=True)

    # MOSFET ---
    elif device_type == "MOSFET":
        st.markdown(" MOSFET Parametreleri")
        mosfet_type = st.radio("Tip:", ["N-Kanal", "P-Kanal"])
        V_GS = parse_input(st.text_input("Kapı-Source Gerilimi VGS (V)", "5"))
        V_DS = parse_input(st.text_input("Drain-Source Gerilimi VDS (V)", "5"))
        Vth = parse_input(st.text_input("Eşik Gerilimi Vth (V)", "2"))
        k = st.number_input("Kazanç Katsayısı (k)", 1, 1000, 100)

        is_n = (mosfet_type == "N-Kanal")

        # Bölge tespiti
        if is_n:
            if V_GS < Vth:
                region = "Kesim (Cutoff)"
                I_D = 0.0
            elif V_DS < (V_GS - Vth):
                region = "Direnç (Ohmik/Triode)"
                I_D = k * ((V_GS - Vth) * V_DS - 0.5 * V_DS**2)
            else:
                region = "Doyum (Saturation)"
                I_D = 0.5 * k * (V_GS - Vth)**2
        else:
            # P-kanal iletim için V_GS <= -Vth beklenir.
            if V_GS > -Vth:
                region = "Kesim (Cutoff)"
                I_D = 0.0
            elif V_DS < -(V_GS - Vth):  # |V_DS| < |V_GS - Vth|  → triode
                region = "Direnç (Ohmik/Triode)"
                Id_mag = k * ((-(V_GS) - Vth) * V_DS - 0.5 * V_DS**2)
                I_D = -abs(Id_mag)  # negatif akım konvansiyonu
            else:
                region = "Doyum (Saturation)"
                I_D = -0.5 * k * (max(0.0, (-(V_GS) - Vth)))**2  # negatif

        st.write(f" Çalışma Bölgesi: **{region}**")
        st.latex(rf"I_{{D}} \approx {I_D:.4f}\;A")

        # Eğri
        V_DS_range = np.linspace(0, max(10, V_DS*1.5), 500)

        if is_n:
            triode_mask = (V_GS >= Vth) & (V_DS_range < (V_GS - Vth))
            sat_mask    = (V_GS >= Vth) & (~triode_mask)

            I_D_range = np.zeros_like(V_DS_range)
            I_D_range[triode_mask] = k * ((V_GS - Vth) * V_DS_range[triode_mask] - 0.5 * V_DS_range[triode_mask]**2)
            I_D_range[sat_mask]    = 0.5 * k * (max(0.0, V_GS - Vth))**2
        else:
            # P-kanal
            Vov_abs = max(0.0, (-(V_GS) - Vth))  # |V_GS| - Vth
            triode_mask = (V_GS <= -Vth) & (V_DS_range < Vov_abs)
            sat_mask    = (V_GS <= -Vth) & (~triode_mask)

            I_D_range = np.zeros_like(V_DS_range)
            # Triode büyüklüğü, pozitif hesapla sonra eksi işaretle
            Id_tri_mag = k * (Vov_abs * V_DS_range - 0.5 * V_DS_range**2)
            I_D_range[triode_mask] = -Id_tri_mag[triode_mask]
            I_D_range[sat_mask]    = -0.5 * k * (Vov_abs**2)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=V_DS_range, y=I_D_range,
                                 mode="lines", name="ID - VDS Karakteristiği"))
        fig.add_trace(go.Scatter(x=[V_DS], y=[I_D],
                                 mode="markers", name="Çalışma Noktası",
                                 marker=dict(color="red", size=10)))
        fig.update_layout(title="MOSFET Çıkış Karakteristiği",
                          xaxis_title="VDS (V)", yaxis_title="ID (A)")
        st.plotly_chart(fig, use_container_width=True)

    # DİYOT ---
    else:
        st.markdown(" Diyot Parametreleri")

        diode_type = st.radio("Diyot Tipi:", ["Normal Diyot", "Zener Diyot"])
        Vd = parse_input(st.text_input("Diyot Gerilimi Vd (V)", "0.7"))
        Is = parse_input(st.text_input("Doyma Akımı Is (A)", "1e-12"))
        n = 1.0
        Vt = 0.02585  # Termal gerilim

        if diode_type == "Normal Diyot":
            # Shockley denklemi
            Id = Is * (np.exp(Vd / (n * Vt)) - 1)

            st.write(f" Anlık Diyot Akımı: **{Id:.4e} A**")
            st.latex(rf"I_{{D}} = I_S \left(e^{{\frac{{V_D}}{{n V_T}}}} - 1\right)")

            # IV karakteristiği
            Vd_range = np.linspace(-0.5, 1.0, 500)
            Id_range = Is * (np.exp(Vd_range / (n * Vt)) - 1)

        else:
            # Zener modeli
            Vz = parse_input(st.text_input("Zener Kırılma Gerilimi Vz (V)", "5.1"))
            Rz = parse_input(st.text_input("Dinamik Direnç Rz (Ω)", "10"))

            def zener_current(v):
                if v >= 0:
                    return Is * (np.exp(v / (n * Vt)) - 1)  # normal yönde
                elif v <= -Vz:
                    return -(v + Vz) / Rz  # ters kırılma
                else:
                    return -Is  # ters yönde küçük akım

            Id = zener_current(Vd)
            st.write(f" Anlık Zener Akımı: **{Id:.4e} A**")

            # Eğri
            Vd_range = np.linspace(-10, 1.0, 800)
            Id_range = np.array([zener_current(v) for v in Vd_range])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=Vd_range, y=Id_range,
                                 mode="lines", name="I-V Karakteristiği"))
        fig.add_trace(go.Scatter(x=[Vd], y=[Id],
                                 mode="markers", name="Çalışma Noktası",
                                 marker=dict(color="red", size=10)))
        fig.update_layout(title=f"{diode_type} I-V Karakteristiği",
                          xaxis_title="Vd (V)", yaxis_title="Id (A)")
        st.plotly_chart(fig, use_container_width=True)

except:
    error_box.error("Bir hata oluştu. Lütfen girdilerinizi kontrol edip tekrar deneyin.")
    st.stop()