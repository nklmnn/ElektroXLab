import streamlit as st
import numpy as np
import plotly.graph_objs as go
import math

TITLE = 'ElektroXLab'
st.set_page_config(
    page_title=TITLE,
    page_icon="⚡",
    layout="wide",
)
st.title("𓐟 Transistor Analizleri")

with st.expander("AÇIKLAMA"):

    st.write('Bu sayfada üzerinde analizler yapmak istediğiniz transistör çeşidini seçip öğrenim amaçlı ölçümler alabilirsiniz. BJT=NPN BJT ve MOSFET=N-kanal MOSFET tir.')
    st.write('* Transistör, küçük bir elektrik sinyaliyle daha büyük bir akımı kontrol eden ve bu byüzden anahtar ya da yükselteç gibi davranabilen yarı iletken bir devre elemanıdır.')
    st.write('* BJT (Bipolar Junction Transistor), akım kontrollü çalışan ve küçük base akımıyla collector-emitter arasındaki daha büyük akımı yöneten transistör türüdür. ')
    st.write('* MOSFET (Metal-Oxide-Semiconductor Field-Effect Transistor), kapısına (gate) uygulanan gerilimle drain-source arasındaki akımı kontrol eden, gerilim kontrollü bir alan etkili transistördür.')
    st.write('DC çalışma noktası, devrede AC bir sinyal yokken akım ve gerilimlerin aldığı sabit değerlerdir. Doğru bölgede çalışmayı ve küçük işaret analizinin sağlam bir zemine oturmasını mümkün kılar.')
    st.write('Küçük işaret analizi, bir devrenin çalışma noktası etrafındaki küçük değişimlere nasıl tepki verdiğini inceleyip kazanç, giriş-çıkış direnci ve frekans davranışı gibi özellikleri hesaplamak için kullanılır.')




    with st.expander("BJT ve MOSFET Temel Formülleri"):

        st.header("BJT Formülleri")

        st.subheader("Akım İlişkileri")
        st.latex(r"I_C = \beta I_B")
        st.latex(r"I_E = I_C + I_B")
        st.latex(r"I_E \approx (\beta + 1) I_B")

        st.subheader("Gerilim İlişkileri")
        st.latex(r"V_{BE} \approx 0.7 \text{ V}")
        st.latex(r"V_{CE} > V_{CE(sat)}")
        st.latex(r"V_{CE(sat)} \approx 0.1 - 0.3 \text{ V}")

        st.subheader("Küçük İşaret Parametreleri")
        st.latex(r"g_m = \frac{I_C}{V_T}")
        st.latex(r"r_{\pi} = \frac{\beta}{g_m}")
        st.latex(r"r_o = \frac{V_A}{I_C}")

        st.subheader("Kolektör Akımı (Asıl Denklem)")
        st.latex(r"I_C = I_S e^{\frac{V_{BE}}{V_T}}")

        st.header("MOSFET Formülleri")

        st.subheader("Kesim Bölgesi (Cutoff)")
        st.latex(r"V_{GS} < V_{th}")
        st.latex(r"I_D = 0")

        st.subheader("Lineer Bölge")
        st.latex(r"""
        I_D = \mu_n C_{ox} \frac{W}{L}
        \left[
        (V_{GS}-V_{th})V_{DS} - \frac{V_{DS}^2}{2}
        \right]
        """)

        st.subheader("Doyum (Saturation) Bölgesi")
        st.latex(r"""
        I_D = \frac{1}{2} \mu_n C_{ox} \frac{W}{L}
        (V_{GS}-V_{th})^2 (1 + \lambda V_{DS})
        """)

        st.subheader("Küçük İşaret Parametreleri")
        st.latex(r"g_m = \frac{2I_D}{V_{GS}-V_{th}}")
        st.latex(r"r_o = \frac{1}{\lambda I_D}")


# Sayfada üst kısım
device = st.selectbox("Transistör çeşidi seçimi", ["BJT", "MOSFET"], key="device_select")
st.caption("Not: SI birimlerini harf olarak sonuna ekleyebilirsiniz.")

error_box = st.empty()
try:
    # SI çarpanlarını algılamak için fonksiyon ----------
    def parse_input(value_str, default_unit=1.0):
        multipliers = {
            'n': 1e-9,
            'u': 1e-6,
            'µ': 1e-6,
            'm': 1e-3,
            'k': 1e3,
            'M': 1e6,
            'G': 1e9
        }
        try:
            value_str = value_str.strip()
            if value_str[-1] in multipliers:
                return float(value_str[:-1]) * multipliers[value_str[-1]]
            else:
                return float(value_str) * default_unit
        except:
            st.error(f"⚠ Hatalı giriş: {value_str}")
            return None

    # Min/Max ve sıfır kontrolü ----------
    def parse_input_checked(label, default="1", min_val=None, max_val=None, allow_zero=True, key=None):
        val_str = st.text_input(label, value=default, key=key)
        val = parse_input(val_str)
        if val is None:
            st.stop()
        if val < 0:
            st.error(f"⚠ {label} negatif olamaz!")
            st.stop()
        if min_val is not None and val < min_val:
            st.error(f"⚠ {label} min değeri {min_val} aşılamaz!")
            st.stop()
        if max_val is not None and val > max_val:
            st.error(f"⚠ {label} max değeri {max_val} aşamaz!")
            st.stop()
        return val



    # Small-signal

    Vt = 25.85e-3

    def gm_bjt(Ic):
        return Ic / Vt if Ic>0 else 0.0

    def rpi_bjt(beta, gm):
        return beta / gm if gm>0 else np.inf

    def ro_bjt(Va, Ic):
        return Va / Ic if Ic>0 else np.inf

    def gm_mos(Id, Vov):
        return 2*Id / Vov if Vov>0 else 0.0

    def ro_mos(lambda_, Id):
        return 1.0 / (lambda_*Id) if (lambda_>0 and Id>0) else np.inf


    # Tabs

    tabs = st.tabs([
        "DC Çalışma Noktası",
        "Küçük İşaret Parametreleri",
        "I–V eğrileri",
        "Güç ve termal analiz",
        "Anahtarlama kayıpları",
        "Frekans / Miller etkisi",
        "Gürültü hesapları",
    ])


    # Tab 1

    with tabs[0]:
        st.header("1) DC Çalışma Noktası")
        col1, col2 = st.columns(2)
        with col1:
            Vcc = parse_input_checked("Vcc (V)", default="200", min_val=0.1, max_val=1e6, key="t1_Vcc")
            if device=="BJT":
                Rc = parse_input_checked("Rc (Ω)", default="1k", min_val=0, max_val=1e6, key="t1_Rc")
                Re = parse_input_checked("Re (Ω)", default="1k", min_val=0, max_val=1e6, key="t1_Re")
                beta = st.number_input("β", value=100.0, min_value=1.0, max_value=1000.0, key="t1_beta")
                Ib = parse_input_checked("I_B (A veya mA)", default="1m", min_val=0, max_val=1, key="t1_Ib")
                Ic = beta * Ib
                Vce = Vcc - Ic * (Rc + Re)
                st.write(f"DC Ic ≈ {Ic:.6g} A")
                st.write(f"DC Vce ≈ {Vce:.6g} V")
            else:
                Vth = parse_input_checked("Vth (V)", default="2", min_val=0, max_val=1000, key="t8_Vth")
                Rd = parse_input_checked("Rd (Ω)", default="1k", min_val=0, max_val=1e6, key="t1_Rd")
                Vds = parse_input_checked("V_DS Q-nokta (V)", default="6", min_val=0, max_val=1e3, key="t1_Vds")
                Vgs = parse_input_checked("V_GS (V)", default="3", min_val=0, max_val=1000, key="t1_Vgs")
                Id = (Vcc - Vds) / Rd if Rd > 0 else 0
                Vov = Vgs - Vth
                st.write(f"DC Id ≈ {Id:.6g} A")
                st.write(f"Overdrive voltage Vov ≈ {Vov:.3f} V")

        with col2:
            fig = go.Figure()
            if device=="BJT":
                VCE_range = np.linspace(0, max(10, Vcc), 300)
                Ib_vals = np.array([Ib*0.2, Ib*0.5, Ib, Ib*2]) if Ib>0 else np.array([1e-6,1e-5,1e-4])
                for i, ib in enumerate(Ib_vals):
                    ic_curve = beta*ib*(1 - np.exp(-VCE_range/5))
                    fig.add_trace(go.Scatter(x=VCE_range, y=ic_curve, mode='lines', name=f"Ib={ib:.3g} A"))
                if Rc>0:
                    I_load = (Vcc - VCE_range)/Rc
                    fig.add_trace(go.Scatter(x=VCE_range, y=I_load, mode='lines', name="Load line", line=dict(dash='dash', color='black')))
                if 'Ic' in locals():
                    fig.add_trace(go.Scatter(x=[Vce], y=[Ic], mode='markers', name='Q point', marker=dict(size=10, color='red')))
            else:
                VDS_range = np.linspace(0, max(10, Vds), 300)
                Vgs_list = [Vgs-1, Vgs, Vgs+1]
                for i, vg in enumerate(Vgs_list):
                    Id = np.where(vg<=0, 0, 0.5*1e-3*(max(0,vg-0.7))**2*np.ones_like(VDS_range))
                    fig.add_trace(go.Scatter(x=VDS_range, y=Id, mode='lines', name=f"Vgs={vg}V"))
            st.plotly_chart(fig, use_container_width=True, key="t1_fig")


    # Tab 2

    with tabs[1]:
        st.header("2) Küçük İşaret Parametreleri")
        if device=="BJT":
            Ic = parse_input_checked("DC Ic [A]", default="5m", min_val=1e-6, max_val=1.0, allow_zero=True, key="t2_Ic")
            beta = st.number_input("β", value=100.0, min_value=1.0, max_value=1000.0, key="t2_beta")
            Va = parse_input_checked("Early Va [V]", default="100", min_val=0.1, max_val=1e5, allow_zero=True, key="t2_Va")
            gm = gm_bjt(Ic)
            r_pi = rpi_bjt(beta, gm)
            r_o = ro_bjt(Va, Ic)
            st.write(f"g_m = {gm:.6g} S, r_π = {r_pi:.6g} Ω, r_o ≈ {r_o:.6g} Ω")
        else:
            Id = parse_input_checked("DC Id [A]", default="10m", min_val=1e-6, max_val=1.0, allow_zero=True, key="t2_Id")
            Vov = parse_input_checked("Vov (Vgs-Vth) [V]", default="2", min_val=0.01, max_val=100.0, allow_zero=True, key="t2_Vov")
            lam = float(st.number_input("λ", value=0.01, min_value=0.0, max_value=1.0, key="t2_lambda"))
            gm = gm_mos(Id,Vov)
            ro = ro_mos(lam, Id)
            st.write(f"gm ≈ {gm:.6g} S, ro ≈ {ro:.6g} Ω")


    # Tab 3

    with tabs[2]:
        st.header("3) I–V Eğrileri")
        fig = go.Figure()
        if device=="BJT":
            beta = st.number_input("β (BJT)", value=100.0, min_value=1.0, max_value=1000.0, key="t3_beta")
            # VBE aralığı kontrolü
            VBE_start = parse_input_checked("VBE start (V)", default="0.55", min_val=0.0, max_val=1.5, allow_zero=False, key="t3_VBE_start")
            VBE_end   = parse_input_checked("VBE end (V)", default="0.9", min_val=VBE_start, max_val=2.0, allow_zero=False, key="t3_VBE_end")
            num_points = st.number_input("Num of points", min_value=10, max_value=1000, value=200, key="t3_points")

            VBE_range = np.linspace(VBE_start, VBE_end, num_points)
            Is = 1e-15
            Ic_vs_Vbe = Is * np.exp(VBE_range / Vt)
            fig.add_trace(go.Scatter(x=VBE_range, y=Ic_vs_Vbe, mode='lines', name='I_C(V_BE)'))
        else:
            Vth = parse_input_checked("Vth (V)", default="2", min_val=0.0, max_val=100.0, allow_zero=False, key="t3_Vth")
            k = parse_input_checked("k (A/V^2)", default="1e-3", min_val=1e-9, max_val=10.0, allow_zero=False, key="t3_k")
            VGS_offset = st.number_input("VGS offset (V)", value=0.5, min_value=0.01, max_value=10.0, key="t3_VGS_offset")
            VGS_vals = [Vth + VGS_offset, Vth + 2*VGS_offset, Vth + 3*VGS_offset, Vth + 4*VGS_offset]
            VDS = np.linspace(0,10,300)
            for i, vg in enumerate(VGS_vals):
                Id = np.where(vg<=Vth, 0, np.where(VDS<(vg-Vth), k*((vg-Vth)*VDS-0.5*VDS**2), 0.5*k*(vg-Vth)**2))
                fig.add_trace(go.Scatter(x=VDS, y=Id, mode='lines', name=f"Vgs={vg:.2f}V"))
        st.plotly_chart(fig, use_container_width=True, key="t3_fig")


    # Tab 4

    with tabs[3]:
        st.header("4) Güç ve Termal Analiz")

        Vd = parse_input_checked("V_DS veya V_CE (V)", default="10", min_val=0.0, max_val=1000.0, allow_zero=True, key="t4_Vd")
        Id = parse_input_checked("I_D veya I_C (A)", default="0.1", min_val=0.0, max_val=100.0, allow_zero=True, key="t4_Id")
        theta_JA = parse_input_checked("θ_JA (°C/W)", default="50", min_val=0.0, max_val=500.0, allow_zero=True, key="t4_theta")
        Tamb = parse_input_checked("T_ambient (°C)", default="25", min_val=-50.0, max_val=150.0, allow_zero=True, key="t4_Tamb")

        # Hesaplama
        P = Vd * Id
        Tj = Tamb + theta_JA * P

        st.write(f"P ≈ {P:.6g} W, Tj ≈ {Tj:.2f} °C")


    # Tab 5

    with tabs[4]:
        st.header("5) Anahtarlama Kayıpları (MOSFET)")

        I_load = parse_input_checked("I_load (A)", default="10", min_val=0.0, max_val=100.0, allow_zero=True, key="t5_Il")
        Vds_on = parse_input_checked("Vds_on (V)", default="24", min_val=0.0, max_val=1000.0, allow_zero=True, key="t5_Vds")
        Rds_on = parse_input_checked("Rds_on (Ω)", default="0.05", min_val=1e-6, max_val=10.0, allow_zero=True, key="t5_Rds")
        Qg = parse_input_checked("Gate charge Qg (nC)", default="20n", min_val=1e-9, max_val=1.0, allow_zero=True, key="t5_Qg")
        fs = float(st.number_input("Switch freq (Hz)", value=20000.0, min_value=1.0, max_value=1e6, step=1.0, key="t5_fs"))
        tr = parse_input_checked("Rise time (s)", default="100n", min_val=1e-9, max_val=1.0, allow_zero=True, key="t5_tr")
        tf = parse_input_checked("Fall time (s)", default="100n", min_val=1e-9, max_val=1.0, allow_zero=True, key="t5_tf")

        # Hesaplamalar
        P_cond = I_load**2 * Rds_on
        P_sw = 0.5 * Vds_on * I_load * (tr + tf) * fs
        Idrv = Qg * fs

        st.write(f"P_cond ≈ {P_cond:.6g} W")
        st.write(f"P_sw ≈ {P_sw:.6g} W")
        st.write(f"I_drv ≈ {Idrv:.6g} A")



    # Tab 6

    with tabs[5]:
        st.header("6) Frekans / Miller Etkisi")

        Cgs = parse_input_checked("C_gs (F)", default="10n", min_val=1e-12, max_val=1.0, allow_zero=True, key="t6_Cgs")
        Cgd = parse_input_checked("C_gd (F)", default="2n", min_val=1e-12, max_val=1.0, allow_zero=True, key="t6_Cgd")
        Av = float(st.number_input("A_v", value=-10.0, min_value=-1e3, max_value=1e3, key="t6_Av"))

        Cin_approx = Cgs + Cgd * (1 + abs(Av))
        st.write(f"C_in ≈ {Cin_approx:.6g} F")


    # Tab 7

    with tabs[6]:
        st.header("7) Gürültü Hesapları & İleri Analiz")
        if device=="BJT":
            Ic = parse_input_checked("Ic (A)", default="1m", min_val=1e-9, max_val=10.0, allow_zero=True, key="t7_Ic")
            in_rms = math.sqrt(2*1.602e-19*Ic) if Ic > 0 else 0.0
            st.write(f"Shot noise i_n_rms ≈ {in_rms:.6g} A/√Hz")
        else:
            Id = parse_input_checked("Id (A)", default="10m", min_val=1e-9, max_val=10.0, allow_zero=True, key="t7_Id")
            st.write("MOSFET termal gürültü approx datasheet bağlıdır")



    st.markdown("---")
    st.caption(
        "Not: Bu araç eğitim/öğretim amaçlıdır. Gerçek devre tasarımlarında datasheet değerleri ve güvenlik faktörleri mutlaka kontrol edilmelidir."
    )

except:
    error_box.error("Bir hata oluştu. Lütfen girdilerinizi kontrol edip ytekrar deneyin.")
    st.stop()