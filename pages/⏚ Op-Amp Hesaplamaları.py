import streamlit as st
import numpy as np
import plotly.graph_objects as go


TITLE = 'ElektroXLab'
st.set_page_config(page_title=TITLE, page_icon="⚡", layout="wide")
st.title("▶ Op-Amp Hesaplamaları")
''
''
''
with st.expander("AÇIKLAMA"):
    st.markdown(""" Op-amp (operasyonel yükselteç), girişine uygulanan küçük gerilim farkını çok yüksek kazançla yükselten, analog sinyalleri işlemek için kullanılan çok yönlü bir elektronik devre elemanıdır.
    - Toplam opamına tek bir giriş verirseniz sadece tersleme işlemi yapar. 
    - İşlem yapmak istediğiniz opamp devresini seçiniz ve giriş kutularını doldurunuz.
    """)
    st.caption("* NOT: 'M', 'k', 'm' ve 'n' SI birimlerini kullanabilirsiniz.")
    with st.expander("FORMÜLLER"):
        st.markdown("1. Tersleyen (Inverting) Kuvvetlendirici")
        st.latex(r"V_{out} = -\frac{R_f}{R_{in}} \cdot V_{in}")
        st.latex(r"A_v = -\frac{R_f}{R_{in}}")


        st.markdown("2. Terslemeyen (Non-inverting) Kuvvetlendirici")
        st.latex(r"V_{out} = \left(1 + \frac{R_f}{R_1}\right) \cdot V_{in}")
        st.latex(r"A_v = 1 + \frac{R_f}{R_1}")


        st.markdown("3. Toplayıcı (Summing Amplifier)")
        st.latex(r"V_{out} = -R_f \left(\frac{V_1}{R_1} + \frac{V_2}{R_2} + \cdots + \frac{V_n}{R_n}\right)")


        st.markdown("4. Fark Alıcı (Differential Amplifier)")
        st.latex(r"V_{out} = \frac{R_2}{R_1} (V_2 - V_1)")

        st.markdown("5. Diferansiyel Kuvvetlendirici (Instrumentation / Differential)")
        st.latex(r"V_{out} = \frac{R_f}{R_{in}} (V_2 - V_1)")


        st.markdown("6. İntegratör (Integrator)")
        st.latex(r"V_{out}(t) = -\frac{1}{R \, C} \int V_{in}(t) \, dt")

        st.markdown("7. Diferansiyel (Differentiator)")
        st.latex(r"V_{out}(t) = -R \, C \, \frac{dV_{in}(t)}{dt}")

        st.markdown("8. Alçak Geçiren (Low-pass) Aktif Filtre")
        st.latex(r"A_v = \frac{V_{out}}{V_{in}} = \frac{1}{1 + j \omega R C}")
        st.latex(r"f_c = \frac{1}{2 \pi R C}")

        st.markdown("9. Yüksek Geçiren (High-pass) Aktif Filtre")
        st.latex(r"A_v = \frac{V_{out}}{V_{in}} = \frac{j \omega R C}{1 + j \omega R C}")
        st.latex(r"f_c = \frac{1}{2 \pi R C}")

        st.markdown("10. Karşılaştırıcı (Comparator)")
        st.latex(r"""
        V_{out} =
        \begin{cases} 
        +V_{sat}, & \text{eğer } V_{in} > V_{ref} \\
        -V_{sat}, & \text{eğer } V_{in} < V_{ref}
        \end{cases}
        """)
''
''

error_box = st.empty()
try:
    #SI çarpanlarını için-------------------------------------
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

    # SI birim kontrol------------------------------------------
    def get_value_input_si(label, default="10k", min_val=None, max_val=None, forbid_zero=False):
        val_str = st.text_input(label, value=default)
        val = parse_input(val_str)
        if val is None:
            return None
        if forbid_zero and val == 0:
            st.error("⚠ Değer sıfır olamaz!")
            return None
        if min_val is not None and val < min_val:
            st.error(f"⚠ Değer {min_val} alt sınırının altında!")
            return None
        if max_val is not None and val > max_val:
            st.error(f"⚠ Değer {max_val} üst sınırının üstünde!")
            return None
        return val

    col1, col2 = st.columns(2)

    with col1:
        # Devre seçimi------------------------------------------------
        circuit_type = st.selectbox(
            "Devre Türü",
            ["Toplayıcı", "Fark Alıcı", "Filtre"]
        )

        #Kullanıcı girişleri------------------------------------------------------------
        valid = True
        if circuit_type == "Toplayıcı":
            num_inputs = st.number_input("Kaç giriş voltajı olacak?", min_value=1, max_value=5, value=2, step=1)
            V_ins, R_ins = [], []
            for i in range(num_inputs):
                V_val = get_value_input_si(f"Giriş V{i+1} (V)", default="1", min_val=0.001, max_val=100, forbid_zero=True)
                R_val = get_value_input_si(f"Direnç R{i+1} (Ω)", default="10k", min_val=1, max_val=1e6, forbid_zero=True)
                if V_val is None or R_val is None:
                    valid = False
                V_ins.append(V_val)
                R_ins.append(R_val)
            Rf_val = get_value_input_si("Geri Besleme Direnci Rf (Ω)", default="10k", min_val=1, max_val=1e6, forbid_zero=True)
            if Rf_val is None:
                valid = False

        elif circuit_type == "Fark Alıcı":
            V1 = get_value_input_si("Giriş V1 (V)", default="1", min_val=0.001, max_val=100, forbid_zero=True)
            V2 = get_value_input_si("Giriş V2 (V)", default="0.5", min_val=0.001, max_val=100, forbid_zero=True)
            R1 = get_value_input_si("Direnç R1 (Ω)", default="10k", min_val=1, max_val=1e6, forbid_zero=True)
            R2 = get_value_input_si("Direnç R2 (Ω)", default="10k", min_val=1, max_val=1e6, forbid_zero=True)
            R3 = get_value_input_si("Direnç R3 (Ω)", default="10k", min_val=1, max_val=1e6, forbid_zero=True)
            R4 = get_value_input_si("Direnç R4 (Ω)", default="10k", min_val=1, max_val=1e6, forbid_zero=True)
            if None in [V1, V2, R1, R2, R3, R4]:
                valid = False

        elif circuit_type == "Filtre":
            typee = st.selectbox("Filtre Tipi", ["Alçak Geçiren", "Yüksek Geçiren", "Bant Geçiren"])
            V_amp = get_value_input_si("Giriş Gerilimi Amplitüdü (V)", default="1", min_val=0.001, max_val=100, forbid_zero=True)
            R1_val = get_value_input_si("Direnç R1 (Ω)", default="10k", min_val=1, max_val=1e6, forbid_zero=True)
            C1 = get_value_input_si("Kapasitans C1 (F)", default="1u", min_val=1e-12, max_val=1, forbid_zero=True)
            K_gain = st.number_input("Op-Amp Kazancı (K)", value=1.0)  # Op-amp kazancı
            if typee == "Bant Geçiren":
                R2_val = get_value_input_si("Direnç R2 (Ω)", default="10k", min_val=1, max_val=1e6, forbid_zero=True)
                C2 = get_value_input_si("Kapasitans C2 (F)", default="1u", min_val=1e-12, max_val=1, forbid_zero=True)
                if None in [R2_val, C2]:
                    valid = False
            freq = st.number_input("Sinyal Frekansı (Hz)", value=50.0, min_value=0.01, max_value=1e6)

        #Zaman-----------------------------------
        t_end = st.number_input("Simülasyon Süresi (s)", min_value=0.01, max_value=5.0, value=0.1, step=0.01)
        samples = 1000
        t = np.linspace(0, t_end, samples)
        V_out = np.zeros_like(t)

        #Hesaplama----------------------------------------------------
        if valid:
            if circuit_type == "Toplayıcı":
                Vout_val = sum([-(Rf_val / R_ins[i]) * V_ins[i] for i in range(len(V_ins))])
                V_out[:] = Vout_val
                st.header("Sonuç")
                st.write(f"Çıkış Gerilimi (Vout): {Vout_val:.2f} V")

            elif circuit_type == "Fark Alıcı":
                Vout_val = (R2 / R1) * V2 - (R4 / R3) * V1
                st.header("Sonuç")
                st.write(f"Fark Alıcı Çıkışı (Vout): {Vout_val:.2f} V")
                V_out[:] = Vout_val

            elif circuit_type == "Filtre":
                V_in = V_amp * np.sin(2 * np.pi * freq * t)

                st.subheader("Sayısal Simülasyon (Euler Yöntemi)")

                if typee == "Alçak Geçiren":
                    tau = R1_val * C1
                    alpha = (t[1] - t[0]) / tau
                    for i in range(1, len(t)):
                        V_out[i] = V_out[i - 1] + alpha * (V_in[i] - V_out[i - 1])
                    V_out *= K_gain  # Op-amp kazancını uygula
                    st.write(f"Sayısal Çıkış (son değer): {V_out[-1]:.3f} V")

                elif typee == "Yüksek Geçiren":
                    tau = R1_val * C1
                    alpha = tau / (tau + (t[1] - t[0]))
                    for i in range(1, len(t)):
                        V_out[i] = alpha * (V_out[i - 1] + V_in[i] - V_in[i - 1])
                    V_out *= K_gain
                    st.write(f"Sayısal Çıkış (son değer): {V_out[-1]:.3f} V")

                elif typee == "Bant Geçiren":
                    tau_hp = R1_val * C1
                    alpha_hp = tau_hp / (tau_hp + (t[1] - t[0]))
                    V_hp = np.zeros_like(t)
                    for i in range(1, len(t)):
                        V_hp[i] = alpha_hp * (V_hp[i - 1] + V_in[i] - V_in[i - 1])
                    tau_lp = R2_val * C2
                    alpha_lp = (t[1] - t[0]) / tau_lp
                    V_out = np.zeros_like(t)
                    for i in range(1, len(t)):
                        V_out[i] = V_out[i - 1] + alpha_lp * (V_hp[i] - V_out[i - 1])
                    V_out *= K_gain
                    st.write(f"Sayısal Çıkış (son değer): {V_out[-1]:.3f} V")

                st.subheader("Analitik Steady-State AC Genliği")

                omega = 2 * np.pi * freq
                if typee == "Alçak Geçiren":
                    V_steady = V_amp / np.sqrt(1 + (omega * R1_val * C1) ** 2)
                    V_steady *= K_gain
                    st.write(f"Teorik Çıkış (steady-state): {V_steady:.3f} V")

                elif typee == "Yüksek Geçiren":
                    V_steady = V_amp * (omega * R1_val * C1) / np.sqrt(1 + (omega * R1_val * C1) ** 2)
                    V_steady *= K_gain
                    st.write(f"Teorik Çıkış (steady-state): {V_steady:.3f} V")

                elif typee == "Bant Geçiren":
                    V_hp_steady = V_amp * (omega * R1_val * C1) / np.sqrt(1 + (omega * R1_val * C1) ** 2)
                    V_out_steady = V_hp_steady / np.sqrt(1 + (omega * R2_val * C2) ** 2)
                    V_out_steady *= K_gain
                    st.write(f"Teorik Çıkış (steady-state): {V_out_steady:.3f} V")
        else:
            st.warning("⚠ Hesaplama yapılmadı. Lütfen tüm giriş değerlerini geçerli şekilde girin.")
            st.stop()
    with col2:
        fig = go.Figure()
        if circuit_type in ["Toplayıcı", "Fark Alıcı"]:
            fig.add_trace(go.Scatter(x=t, y=V_out, mode='lines', name='Vout'))
        else:
            if valid:
                fig.add_trace(go.Scatter(x=t, y=V_in, mode='lines', name='Vin'))
                fig.add_trace(go.Scatter(x=t, y=V_out, mode='lines', name='Vout'))
        fig.update_layout(
            title=f"{circuit_type} Devresi Çıkış Grafiği",
            xaxis_title="Zaman (s)",
            yaxis_title="Gerilim (V)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    #Çizimler-------------------------------------------------

        import io
        from PIL import Image
        import schemdraw
        import schemdraw.elements as elm


        if circuit_type== "Toplayıcı":
            d = schemdraw.Drawing()
            op = d.add(elm.Opamp(color='gray'))

            if num_inputs== 1:




                d += elm.Line().left().at(op.in1).length(0.7).color('gray')

                d += elm.Resistor().label('R1').color('gray')
                d += elm.Line().left().length(1).label('Vin').color('gray')
                d += elm.Line().right().length(4).color('gray')
                d += elm.Line().up().length(1).color('gray')
                d += elm.Line().right().length(1.87).color('gray')
                d += elm.Resistor().label('Rf').color('gray')
                d += elm.Line().left().length(4.85).color('gray')
                d += elm.Line().down().length(1).color('gray')


                d += elm.Line().left().at(op.in2).length(0.2).color('gray')
                d += elm.Ground(color='gray')

                # Çıkış
                d += elm.Line().right().at(op.out).length(2).label('Vout').color('gray')
                d += elm.Line().up().length(1.6).color('gray')

            if num_inputs == 2:




                d += elm.Line().left().at(op.in1).length(0.7).color('gray')

                d += elm.Resistor().label('R1').color('gray')
                d += elm.Line().left().length(1).label('Vin').color('gray')
                d += elm.Line().right().length(4).color('gray')
                d += elm.Line().up().length(1).color('gray')
                d += elm.Line().right().length(1.87).color('gray')
                d += elm.Resistor().label('Rf').color('gray')
                d += elm.Line().left().length(4.85).color('gray')
                d += elm.Line().down().length(1).color('gray')

                d += elm.Line().down().length(1).color('gray')
                d += elm.Line().left().length(0).color('gray')
                d += elm.Resistor().label('R2').color('gray')
                d += elm.Line().up().length(1).color('gray')



                d += elm.Line().left().at(op.in2).length(0.2).color('gray')
                d += elm.Ground(color='gray')

                # Çıkış
                d += elm.Line().right().at(op.out).length(2).label('Vout').color('gray')
                d += elm.Line().up().length(1.6).color('gray')

            if num_inputs == 3:




                d += elm.Line().left().at(op.in1).length(0.7).color('gray')

                d += elm.Resistor().label('R1').color('gray')
                d += elm.Line().left().length(1).label('Vin').color('gray')
                d += elm.Line().right().length(4).color('gray')
                d += elm.Line().up().length(1).color('gray')
                d += elm.Line().right().length(1.87).color('gray')
                d += elm.Resistor().label('Rf').color('gray')
                d += elm.Line().left().length(4.85).color('gray')
                d += elm.Line().down().length(1).color('gray')

                d += elm.Line().down().length(1).color('gray')
                d += elm.Line().left().length(0).color('gray')
                d += elm.Resistor().label('R2').color('gray')
                d += elm.Line().up().length(1).color('gray')
                d += elm.Line().down().length(2).color('gray')
                d += elm.Line().right().length(0).color('gray')
                d += elm.Resistor().label('R3').color('gray')
                d += elm.Line().up().length(1).color('gray')


                d += elm.Line().left().at(op.in2).length(0.2).color('gray')
                d += elm.Line().down().length(0.5).color('gray')
                d += elm.Ground(color='gray')


                d += elm.Line().right().at(op.out).length(2).label('Vout').color('gray')
                d += elm.Line().up().length(1.6).color('gray')

            if num_inputs == 4:




                d += elm.Line().left().at(op.in1).length(0.7).color('gray')

                d += elm.Resistor().label('R1').color('gray')
                d += elm.Line().left().length(1).label('Vin').color('gray')
                d += elm.Line().right().length(4).color('gray')
                d += elm.Line().up().length(1).color('gray')
                d += elm.Line().right().length(1.87).color('gray')
                d += elm.Resistor().label('Rf').color('gray')
                d += elm.Line().left().length(4.85).color('gray')
                d += elm.Line().down().length(1).color('gray')

                d += elm.Line().down().length(1).color('gray')
                d += elm.Line().left().length(0).color('gray')
                d += elm.Resistor().label('R2').color('gray')
                d += elm.Line().up().length(1).color('gray')
                d += elm.Line().down().length(2).color('gray')
                d += elm.Line().right().length(0).color('gray')
                d += elm.Resistor().label('R3').color('gray')
                d += elm.Line().up().length(1).color('gray')
                d += elm.Line().down().length(2).color('gray')
                d += elm.Line().left().length(0).color('gray')
                d += elm.Resistor().label('R4').color('gray')
                d += elm.Line().up().length(1).color('gray')


                d += elm.Line().left().at(op.in2).length(0.2).color('gray')
                d += elm.Line().down().length(0.5).color('gray')
                d += elm.Ground(color='gray')


                d += elm.Line().right().at(op.out).length(2).label('Vout').color('gray')
                d += elm.Line().up().length(1.6).color('gray')

            if num_inputs == 5:




                d += elm.Line().left().at(op.in1).length(0.7).color('gray')

                d += elm.Resistor().label('R1').color('gray')
                d += elm.Line().left().length(1).label('Vin').color('gray')
                d += elm.Line().right().length(4).color('gray')
                d += elm.Line().up().length(1).color('gray')
                d += elm.Line().right().length(1.87).color('gray')
                d += elm.Resistor().label('Rf').color('gray')
                d += elm.Line().left().length(4.85).color('gray')
                d += elm.Line().down().length(1).color('gray')

                d += elm.Line().down().length(1).color('gray')
                d += elm.Line().left().length(0).color('gray')
                d += elm.Resistor().label('R2').color('gray')
                d += elm.Line().up().length(1).color('gray')
                d += elm.Line().down().length(2).color('gray')
                d += elm.Line().right().length(0).color('gray')
                d += elm.Resistor().label('R3').color('gray')
                d += elm.Line().up().length(1).color('gray')
                d += elm.Line().down().length(2).color('gray')
                d += elm.Line().left().length(0).color('gray')
                d += elm.Resistor().label('R4').color('gray')
                d += elm.Line().up().length(1).color('gray')
                d += elm.Line().down().length(2).color('gray')
                d += elm.Line().right().length(0).color('gray')
                d += elm.Resistor().label('R5').color('gray')
                d += elm.Line().up().length(1).color('gray')


                d += elm.Line().left().at(op.in2).length(0.2).color('gray')
                d += elm.Line().down().length(0.5).color('gray')
                d += elm.Ground(color='gray')

                #
                d += elm.Line().right().at(op.out).length(2).label('Vout').color('gray')
                d += elm.Line().up().length(1.6).color('gray')

            #Görseli Streamlite aktar
            buf = io.BytesIO()
            d.draw()
            d.save(buf)
            buf.seek(0)
            img = Image.open(buf)
            st.image(img)














        if circuit_type== "Fark Alıcı":
            d = schemdraw.Drawing()


            op = d.add(elm.Opamp(color='gray'))


            d += elm.Line().left().at(op.in1).length(0.7).color('gray')

            d += elm.Resistor().label('R1').color('gray')
            d += elm.Line().left().length(3.3).color('gray')
            d += elm.Line().left().label('V1').length(0).color('gray')
            d += elm.Line().right().length(4).color('gray')
            d += elm.Line().up().length(1).color('gray')
            d += elm.Line().right().length(4.15).color('gray')
            d += elm.Resistor().label('R2').color('gray')



            d += elm.Line().left().at(op.in2).length(3).color('gray')
            d += elm.Line().down().length(1).color('gray')
            d += elm.Line().right().length(0).color('gray')
            d += elm.Resistor().label('R4').color('gray')
            d += elm.Ground(color='gray')
            d += elm.Line().left().length(3).color('gray')
            d += elm.Resistor().label('R3').color('gray')
            d += elm.Line().left().length(1).color('gray')
            d += elm.Line().left().label('V2').length(0).color('gray')



            d += elm.Line().right().at(op.out).length(2).label('Vout').color('gray')
            d += elm.Line().up().length(1.6).color('gray')

            # Görseli Streamlite aktar
            buf = io.BytesIO()
            d.draw()
            d.save(buf)
            buf.seek(0)
            img = Image.open(buf)
            st.image(img)
            #
except:
    error_box.error("Bir hata oluştu. Lütfen girdilerinizi kontrol edip tekrar deneyin.")
    st.stop()
