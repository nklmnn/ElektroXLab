import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
from PIL import Image
import schemdraw
import schemdraw.elements as elm

TITLE = 'ElektroXLab'
st.set_page_config(
    page_title=TITLE,
    page_icon="⚡",
    layout="wide",
)
st.title("➰ RLC Devresi Hesaplayıcı")




with st.expander("AÇIKLAMA"):
    st.write("R, direnç, L bobin ve C kondansatör'ü temsil eder.")
    st.write(
        "Bu sayfada seri ve paralel bağlı RLC devreleri için empedans (Z), faz açısı (θ), akımı (I) ve gerilim(V) hesaplamalarına ulaşabilirsiniz. Eğer devrenizde birden fazla birbirine seri olan direnç, kondansatör veya bobin varsa, öncelikle bunların eş değer halini bulmalısınız."
    )

    st.write("Prompt yolunu kullanarak komponentleriniz eş değer halini elde edebilirsiniz.")

    with st.expander("Formüller"):
        st.subheader("Dirençler (R)")
        st.markdown("**Seri:**")
        st.latex(r"R_{eq} = R_1 + R_2 + \dots")
        st.markdown("**Paralel:**")
        st.latex(r"\frac{1}{R_{eq}} = \frac{1}{R_1} + \frac{1}{R_2} + \dots")
        '---'
        st.subheader("Kondansatörler (C)")
        st.markdown("**Seri:**")
        st.latex(r"\frac{1}{C_{eq}} = \frac{1}{C_1} + \frac{1}{C_2} + \dots")
        st.markdown("**Paralel:**")
        st.latex(r"C_{eq} = C_1 + C_2 + \dots")
        '---'
        st.subheader("Bobinler (L)")
        st.markdown("**Seri:**")
        st.latex(r"L_{eq} = L_1 + L_2 + \dots")
        st.markdown("**Paralel:**")
        st.latex(r"\frac{1}{L_{eq}} = \frac{1}{L_1} + \frac{1}{L_2} + \dots")
        '---'
        st.markdown("Empedans Dönüşümleri")

        # Direnç
        st.latex(r"Z_R = R")

        # Bobin / Endüktans
        st.latex(r"Z_L = j \, X_L = j \, 2 \pi f L")

        # Kondansatör / Kapasitans
        st.latex(r"Z_C = \frac{1}{j \, X_C} = \frac{1}{j \, 2 \pi f C} = -\frac{j}{2 \pi f C}")
        '---'

        # ---------- RC Devresi ----------

        RC_series = r"""
        Z = \sqrt{R^2 + X_C^2}, \quad X_C = \frac{1}{2 \pi f C} \\
        I = \frac{V}{Z}, \quad V_R = I R, \quad V_C = I X_C \\
        \theta = \arctan{\frac{-X_C}{R}}
        """

        RC_parallel = r"""
        Y = \sqrt{G^2 + B^2}, \quad G = \frac{1}{R}, \quad B = 2 \pi f C \\
        Z = \frac{1}{Y}, \quad I = \frac{V}{Z}, \quad I_R = V G, \quad I_C = V B \\
        \theta = \arctan{\frac{B}{G}}
        """

        # ---------- RL Devresi ----------

        RL_series = r"""
        Z = \sqrt{R^2 + X_L^2}, \quad X_L = 2 \pi f L \\
        I = \frac{V}{Z}, \quad V_R = I R, \quad V_L = I X_L \\
        \theta = \arctan{\frac{X_L}{R}}
        """

        RL_parallel = r"""
        Y = \sqrt{G^2 + B^2}, \quad G = \frac{1}{R}, \quad B = -\frac{1}{X_L} \\
        Z = \frac{1}{Y}, \quad I = \frac{V}{Z}, \quad I_R = V G, \quad I_L = V B \\
        \theta = \arctan{\frac{B}{G}}
        """

        # ---------- RLC Devresi ----------

        RLC_series = r"""
        Z = \sqrt{R^2 + (X_L - X_C)^2}, \quad X_L = 2 \pi f L, \quad X_C = \frac{1}{2 \pi f C} \\
        I = \frac{V}{Z}, \quad V_R = I R, \quad V_L = I X_L, \quad V_C = I X_C \\
        \theta = \arctan{\frac{X_L - X_C}{R}} \\
        f_0 = \frac{1}{2 \pi \sqrt{L C}} \quad \text{(Rezonans Frekansı)}
        """

        RLC_parallel = r"""
        Y = \sqrt{G^2 + B^2}, \quad G = \frac{1}{R}, \quad B = \frac{1}{X_C} - \frac{1}{X_L} \\
        Z = \frac{1}{Y}, \quad I = \frac{V}{Z}, \quad I_R = V G, \quad I_L = V / X_L, \quad I_C = V / X_C \\
        \theta = \arctan{\frac{B}{G}} \\
        """

        rezo = r"""
            f_0 = \frac{1}{2 \pi \sqrt{L C}}
            """

        # ---------- Örnek Kullanım ----------
        # import streamlit as st
        st.subheader("Seri RC Devresi Formülleri")
        st.latex(RC_series)
        st.markdown('---')
        st.subheader("Paralel RC Devresi Formülleri")
        st.latex(RC_parallel)
        st.markdown('---')
        st.subheader("Seri RL Devresi Formülleri")
        st.latex(RL_series)
        st.markdown('---')
        st.subheader("Paralel RL Devresi Formülleri")
        st.latex(RL_parallel)
        st.markdown('---')
        st.subheader("Seri RLC Devresi Formülleri")
        st.latex(RLC_series)
        st.markdown('---')
        st.subheader("Paralel RLC Devresi Formülleri")
        st.latex(RLC_parallel)
        st.markdown('---')
        st.subheader("RLC Devrelerindeki Rezonans Frekansı")
        st.latex(rezo)





error_box = st.empty()
try:
    with st.expander("Prompt Yoluyla Eşdeğer Komponent Hesaplama"):


        import pandas as pd

        st.title("Devre Hesaplamaları ⚡")

        # --- ID üretici ---
        _rid = {"n": 0}


        def new_id():
            _rid["n"] += 1
            return f"E{_rid['n']}"


        # --- Değer parser
        def parse_value(tok):
            tok = tok.strip().lower().replace("ohm", "")
            if tok.endswith("h"):  # Bobin
                return "L", float(tok[:-1])
            if tok.endswith("f"):  # Kondansatör
                return "C", float(tok[:-1])
            return "R", float(tok)  # Varsayılan direnç


        # --- Parser ağaç yapısı
        def parse_block(expr: str):
            expr = expr.strip().lower()
            tokens = expr.replace("(", " ( ").replace(")", " ) ").split()

            def helper(tokens):
                stack = []
                while tokens:
                    tok = tokens.pop(0)
                    if tok == "(":
                        stack.append(helper(tokens))
                    elif tok == ")":
                        break
                    elif tok in ["seri", "paralel"]:
                        stack.append(tok)
                    else:
                        try:
                            t, val = parse_value(tok)
                            stack.append({
                                "type": t,
                                "id": new_id(),
                                "value": val
                            })
                        except:
                            pass

                if len(stack) == 1 and isinstance(stack[0], dict):
                    return stack[0]

                node = {"type": None, "children": []}
                for item in stack:
                    if isinstance(item, dict):
                        node["children"].append(item)
                    elif item in ["seri", "paralel"]:
                        node["type"] = item
                return node

            return helper(tokens)


        # --- Eşdeğer hesaplama
        def calc_equiv(node, mode="R"):
            if node.get("type") in ["R", "L", "C"]:
                return node["value"]

            if node["type"] == "seri":
                if mode in ["R", "L"]:
                    return sum(calc_equiv(c, mode) for c in node["children"])
                elif mode == "C":
                    inv = sum(1.0 / calc_equiv(c, mode) for c in node["children"])
                    return 1.0 / inv

            elif node["type"] == "paralel":
                if mode in ["R", "L"]:
                    inv = sum(1.0 / calc_equiv(c, mode) for c in node["children"])
                    return 1.0 / inv
                elif mode == "C":
                    return sum(calc_equiv(c, mode) for c in node["children"])


        # --- Gerilim bölüşümü sadece R
        def voltage_divider(node, total_v):
            results = {}

            def walk(n, Vn):
                if n.get("type") == "R":
                    results[n["id"]] = {"R": n["value"], "V": Vn}
                    return
                if n["type"] == "seri":
                    R_eq = calc_equiv(n, "R")
                    for c in n["children"]:
                        Rc = calc_equiv(c, "R")
                        walk(c, Vn * (Rc / R_eq))
                elif n["type"] == "paralel":
                    for c in n["children"]:
                        walk(c, Vn)

            walk(node, total_v)
            return results


        # --- Akım bölüşümü sadece R
        def current_divider(node, total_i):
            results = {}

            def walk(n, In):
                if n.get("type") == "R":
                    results[n["id"]] = {"R": n["value"], "I": In}
                    return
                if n["type"] == "seri":
                    for c in n["children"]:
                        walk(c, In)
                elif n["type"] == "paralel":
                    R_eq = calc_equiv(n, "R")
                    for c in n["children"]:
                        Rc = calc_equiv(c, "R")
                        walk(c, In * (R_eq / Rc))

            walk(node, total_i)
            return results


        # --- Kullanıcı Girişi ---
        devre_input = st.text_input(
            "Devreyi yazınız (örn: ((100 seri 200) paralel (300 seri 400)) seri 50)"
        )

        element_type = st.selectbox(
            "Devre Elemanı Türü",
            ["Direnç (R)", "Bobin (L)", "Kondansatör (C)"]
        )

        mode_map = {
            "Direnç (R)": "R",
            "Bobin (L)": "L",
            "Kondansatör (C)": "C"
        }

        mode = st.selectbox(
            "Hesaplama Modu",
            ["Normal Hesaplama", "Gerilim Bölücü", "Akım Bölücü"]
        )

        value_input = st.number_input(
            "Toplam Gerilim (V) veya Akım (A)",
            min_value=0.0, value=10.0
        )

        if st.button("Hesapla"):
            tree = parse_block(devre_input)
            eq = calc_equiv(tree, mode_map[element_type])

            unit = {"R": "Ω", "L": "H", "C": "F"}[mode_map[element_type]]
            st.success(f"Eşdeğer değer: {eq:.6g} {unit}")

            if element_type == "Direnç (R)" and mode == "Gerilim Bölücü":
                st.subheader("Gerilim / Akım / Güç Tablosu")
                voltages = voltage_divider(tree, value_input)
                data = []
                for rid, res in voltages.items():
                    r = res["R"]
                    v = res["V"]
                    i = v / r
                    p = v * i
                    data.append({
                        "ID": rid,
                        "Direnç (Ω)": r,
                        "Gerilim (V)": v,
                        "Akım (A)": i,
                        "Güç (W)": p
                    })
                st.table(pd.DataFrame(data))

            elif element_type == "Direnç (R)" and mode == "Akım Bölücü":
                st.subheader("Gerilim / Akım / Güç Tablosu")
                currents = current_divider(tree, value_input)
                data = []
                for rid, res in currents.items():
                    r = res["R"]
                    i = res["I"]
                    v = i * r
                    p = v * i
                    data.append({
                        "ID": rid,
                        "Direnç (Ω)": r,
                        "Gerilim (V)": v,
                        "Akım (A)": i,
                        "Güç (W)": p
                    })
                st.table(pd.DataFrame(data))

            else:
                st.info("Bobin ve kondansatörler için bölücü tabloları DC’de anlamlı değildir.")


    # ---------- SI çarpanlarını algılamak için fonksiyon
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

    # ---------- SI birimi ile değer al, min/max ve sıfır kontrolü
    def get_value_input_si(label, default="10k", min_val=None, max_val=None, forbid_zero=True):
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

    with st.expander("Normal Eşdeğer Değer Hesaplayıcı"):
        st.header("Eşdeğer Değer Hesaplayıcı")

        element_type = st.selectbox("Hangi eleman tipi?", ["Direnç (R)", "Kondansatör (C)", "Bobin (L)"])
        num_elements = st.number_input(
            f"{element_type} sayısı (maks. 10):",
            min_value=1, max_value=10, value=3, step=1
        )
        connection_type = st.radio("Bağlantı tipi:", ["Seri", "Paralel"])

        values = []
        valid_inputs = True
        st.subheader(f"{element_type} değerlerini girin:")

        # ---------- Eleman değerlerini al
        for i in range(num_elements):
            if element_type == "Direnç (R)":
                val = get_value_input_si(f"R{i+1} (Ω)", default=f"{10*(i+1)}", min_val=1, max_val=1e6 )
            elif element_type == "Kondansatör (C)":
                val = get_value_input_si(f"C{i+1} (F)", default=f"{1e-6*(i+1)}", min_val=1e-12, max_val=1)
            else:  # Bobin (L)
                val = get_value_input_si(f"L{i+1} (H)", default=f"{0.1*(i+1)}", min_val=1e-6, max_val=1e3)

            if val is None:
                valid_inputs = False
            else:
                values.append(val)

        # ---------- Toplam hesap
        if valid_inputs and len(values) == num_elements:
            if element_type in ["Direnç (R)", "Bobin (L)"]:
                if connection_type == "Seri":
                    total = sum(values)
                else:  # Paralel
                    total = 1 / sum(1 / v for v in values)
            elif element_type == "Kondansatör (C)":
                if connection_type == "Seri":
                    total = 1 / sum(1 / v for v in values)
                else:  # Paralel
                    total = sum(values)

            unit = {"Direnç (R)": "Ω", "Kondansatör (C)": "F", "Bobin (L)": "H"}[element_type]
            st.markdown(f"**Toplam {element_type} ({connection_type} bağlantı):** {total:.6g} {unit}")
        else:
            st.warning("⚠ Hesaplama yapılmadı. Lütfen tüm değerleri geçerli şekilde girin.")
            st.stop()










    '---'
    # ---------- Devre tipi seç
    st.subheader("RLC Devre Hesaplayıcı")
    circuit_type = st.selectbox("Devre tipi:", ["RL", "RC", "RLC"])
    type_select = st.radio("Bağlantı tipi:", ["Seri", "Paralel"], key="rlc_type")

    col1, col2 = st.columns(2)
    with col1:
        # ---------- Kullanıcı girişleri
        V = get_value_input_si("Gerilim (V) [Volt]", default="230", min_val=0.1, max_val=10e3)
        f = get_value_input_si("Frekans (f) [Hz]", default="50", min_val=1, max_val=100)
        R = get_value_input_si("Direnç (R) [Ω]", default="10", min_val=1, max_val=1e6)

        L = None
        if circuit_type in ["RL", "RLC"]:
            L = get_value_input_si("Endüktans (L) [H]", default="0.1", min_val=1e-6, max_val=1e6)

        C = None
        if circuit_type in ["RC", "RLC"]:
            C = get_value_input_si("Kapasitans (C) [F]", default="50u", min_val=1e-12, max_val=1e3)

        # ---------- Hata kontrolü
        if None in [V, f, R] or (circuit_type in ["RL", "RLC"] and L is None) or (circuit_type in ["RC", "RLC"] and C is None):
            st.warning("⚠ Hesaplama yapılmadı. Lütfen tüm değerleri geçerli şekilde girin.")
            st.stop()
        else:
            # ---------- Empedans
            Z_R = R
            Z_L = 1j * 2 * np.pi * f * L if L is not None else 0
            Z_C = -1j / (2 * np.pi * f * C) if C is not None else 0

            if type_select == "Seri":
                Z_total = Z_R + Z_L + Z_C
                theta = np.angle(Z_total, deg=True)
                I_total = V / abs(Z_total) if abs(Z_total) != 0 else 0.0

                # Eleman gerilimleri seri
                V_R = I_total * abs(Z_R)
                V_L = I_total * abs(Z_L) if L is not None else None
                V_C = I_total * abs(Z_C) if C is not None else None

            else:  # Paralel
                Y_total = 0 + 0j
                if Z_R != 0:
                    Y_total += 1 / Z_R
                if Z_L != 0:
                    Y_total += 1 / Z_L
                if Z_C != 0:
                    Y_total += 1 / Z_C

                if Y_total == 0:
                    st.error("Toplam admittans 0 oldu; L veya C eksikliği ya da R sonsuz olabilir.")
                else:
                    Z_total = 1 / Y_total
                    theta = np.angle(Z_total, deg=True)
                    I_total = V / abs(Z_total)

                    # Eleman akımları paralel
                    I_R = V / abs(Z_R) if Z_R != 0 else None
                    I_L = V / abs(Z_L) if (L is not None and Z_L != 0) else None
                    I_C = V / abs(Z_C) if (C is not None and Z_C != 0) else None

            # ---------- Sonuçları göster
            st.markdown(f"**Toplam Empedans:** {abs(Z_total):.4g} Ω")
            st.markdown(f"**Faz Açısı (theta):** {theta:.2f}°")
            st.markdown(f"**Toplam Akım (I_total):** {I_total:.4g} A")
            if type_select == "Seri":
                st.markdown(f"V_R: {V_R:.4g} V")
                if V_L is not None: st.markdown(f"V_L: {V_L:.4g} V")
                if V_C is not None: st.markdown(f"V_C: {V_C:.4g} V")
            else:
                st.markdown(f"I_R: {I_R:.4g} A" if I_R is not None else "")
                st.markdown(f"I_L: {I_L:.4g} A" if I_L is not None else "")
                st.markdown(f"I_C: {I_C:.4g} A" if I_C is not None else "")

    with col2:
        d = schemdraw.Drawing()
        d += elm.SourceV().label('V_in').color('grey')

        if circuit_type== "RLC":

            if type_select == "Seri":

                d += elm.Line().right().length(0).color('grey')
                d += elm.Resistor().label(f'R={R}Ω').color('grey')
                d += elm.Inductor().label(f'L={L}H').color('grey')
                d += elm.Capacitor().label(f'C={C}F').color('grey')
                d += elm.Line().right().length(1).color('grey')
                d += elm.Line().down().length(3).color('grey')
                d += elm.Line().left().length(10).color('grey')
                d += elm.Ground().color('grey')
            else:

                d += elm.Line().right().length(3).color('grey')

                # R dalı
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label(f'R={R}Ω').color('grey')
                d += elm.Line().left().length(3).color('grey')

                # L dalı
                d += elm.Line().right().length(6).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Inductor().label(f'L={L}H').color('grey')
                d += elm.Line().left().length(3).color('grey')

                # C dalı
                d += elm.Line().right().length(6).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Capacitor().label(f'C={C}F').color('grey')
                d += elm.Line().left().length(3).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Ground().color('grey')

        if circuit_type == "RL":
            if type_select == "Seri":

                d += elm.Line().right().length(0).color('grey')
                d += elm.Resistor().label(f'R={R}Ω').color('grey')
                d += elm.Inductor().label(f'L={L}H').color('grey')
                d += elm.Line().right().length(1).color('grey')
                d += elm.Line().down().length(3).color('grey')
                d += elm.Line().left().length(7).color('grey')
                d += elm.Ground().color('grey')
            else:

                d += elm.Line().right().length(3).color('grey')

                # R dalı
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label(f'R={R}Ω').color('grey')
                d += elm.Line().left().length(3).color('grey')

                # L dalı
                d += elm.Line().right().length(6).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Inductor().label(f'L={L}H').color('grey')
                d += elm.Line().left().length(3).color('grey')
                d += elm.Line().down().length(3).color('grey')
                d += elm.Ground().color('grey')

        if circuit_type == "RC":
            if type_select == "Seri":

                d += elm.Line().right().length(0).color('grey')
                d += elm.Resistor().label(f'R={R}Ω').color('grey')
                d += elm.Capacitor().label(f'C={C}F').color('grey')
                d += elm.Line().right().length(1).color('grey')
                d += elm.Line().down().length(3).color('grey')
                d += elm.Line().left().length(7).color('grey')
                d += elm.Ground().color('grey')
            else:

                d += elm.Line().right().length(3).color('grey')

                # R dalı
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label(f'R={R}Ω').color('grey')
                d += elm.Line().left().length(3).color('grey')

                # L dalı
                d += elm.Line().right().length(6).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Capacitor().label(f'C={C}F').color('grey')
                d += elm.Line().left().length(3).color('grey')
                d += elm.Line().down().length(3).color('grey')
                d += elm.Ground().color('grey')



            # Görseli Streamlite aktar
        buf = io.BytesIO()
        d.draw()
        d.save(buf)
        buf.seek(0)
        img = Image.open(buf)
        st.image(img)
        #

    with st.expander("Ayrıntılı sonuçlar"):
            # ---------- Sonuçları göster
        st.markdown("---")
        st.subheader("***Sonuçlar***")

        if circuit_type == "RLC" and L is not None and C is not None:
            f_resonans = 1 / (2 * np.pi * np.sqrt(L * C))
            st.info(f"* Rezonans Frekansı (f₀): {f_resonans:.2f} Hz")

        st.write(f"Toplam Empedans (|Z|): {abs(Z_total):.4f} Ω")
        st.write(f"Faz Açısı (θ): {theta:.3f}°")
        st.write(f"Toplam Akım (I): {I_total:.4f} A")

        if type_select == "Seri":
            st.write("Seri Devre Eleman Gerilimleri:")
            st.write(f"VR = {V_R:.4f} V")
            if V_L is not None: st.write(f"VL = {V_L:.4f} V")
            if V_C is not None: st.write(f"VC = {V_C:.4f} V")
            st.write("Eleman Empedansları:")
            st.write(f"ZR = {abs(Z_R):.4f} Ω")
            if L is not None: st.write(f"ZL = {abs(Z_L):.4f} Ω")
            if C is not None: st.write(f"ZC = {abs(Z_C):.4f} Ω")
        else:
            st.write("Paralel Devre Eleman Akımları:")
            if I_R is not None: st.write(f"IR = {I_R:.4f} A")
            if I_L is not None: st.write(f"IL = {I_L:.4f} A")
            if I_C is not None: st.write(f"IC = {I_C:.4f} A")
            st.write("Eleman Empedansları:")
            st.write(f"ZR = {abs(Z_R):.4f} Ω")
            if L is not None: st.write(f"ZL = {abs(Z_L):.4f} Ω")
            if C is not None: st.write(f"ZC = {abs(Z_C):.4f} Ω")

        # Devre karakteri
        if theta > 0:
            st.info("Devre endüktif karakterdedir.")
        elif theta < 0:
            st.info("Devre kapasitif karakterdedir.")
        else:
            st.info("Devre resistif karakterdedir.")

        # ---------- Diyagramlar
        with st.expander("Diyagramlar"):
            st.markdown("---")
            st.markdown("Fazör Diyagramı")
            fig2, ax = plt.subplots(figsize=(5, 5))
            ax.set_xlim(-V * 1.2, V * 1.2)
            ax.set_ylim(-V * 1.2, V * 1.2)
            ax.set_aspect('equal')
            ax.grid(True)
            ax.arrow(0, 0, V, 0, head_width=V * 0.05, color='b', label='V (Volt)')
            theta_rad = np.radians(theta)
            I_vec = I_total * np.exp(1j * theta_rad)
            Ix, Iy = I_vec.real, I_vec.imag
            ax.arrow(0, 0, Ix, Iy, head_width=V * 0.05, color='r', label='I (A)')
            ax.set_xlabel("Re")
            ax.set_ylabel("Im")
            ax.legend()
            ax.set_title(f"θ = {theta:.2f}°")
            st.pyplot(fig2)

            # Frekans taraması grafiği
            freqs = np.linspace(1, 500, 500)
            XL_arr = 2 * np.pi * freqs * L if L is not None else np.zeros_like(freqs)
            XC_arr = 1 / (2 * np.pi * freqs * C) if C is not None else np.zeros_like(freqs)

            if type_select == "Seri":
                if circuit_type == "RLC":
                    Z_arr = np.sqrt(R ** 2 + (XL_arr - XC_arr) ** 2)
                    theta_arr = np.arctan2((XL_arr - XC_arr), R)
                elif circuit_type == "RL":
                    Z_arr = np.sqrt(R ** 2 + XL_arr ** 2)
                    theta_arr = np.arctan2(XL_arr, R)
                elif circuit_type == "RC":
                    Z_arr = np.sqrt(R ** 2 + XC_arr ** 2)
                    theta_arr = np.arctan2(-XC_arr, R)
            else:
                G = 1 / R
                inv_XC = np.zeros_like(freqs)
                inv_XL = np.zeros_like(freqs)
                if C is not None:
                    np.divide(1.0, XC_arr, out=inv_XC, where=XC_arr != 0)
                if L is not None:
                    np.divide(1.0, XL_arr, out=inv_XL, where=XL_arr != 0)
                if circuit_type == "RLC":
                    B_arr = inv_XC - inv_XL
                elif circuit_type == "RL":
                    B_arr = -inv_XL
                elif circuit_type == "RC":
                    B_arr = inv_XC
                Y_arr = np.sqrt(G ** 2 + B_arr ** 2)
                Y_arr_safe = np.where(Y_arr == 0, 1e-30, Y_arr)
                Z_arr = 1.0 / Y_arr_safe
                theta_arr = np.arctan2(B_arr, G)

            st.markdown("---")
            st.markdown("Faz Açısı ve Empedans vs Frekans")
            fig, ax1 = plt.subplots()
            ax1.plot(freqs, Z_arr, 'b-', label='Empedans (Z)')
            ax1.set_xlabel('Frekans (Hz)')
            ax1.set_ylabel('Empedans (Ω)', color='b')
            ax1.tick_params('y', colors='b')
            ax2 = ax1.twinx()
            ax2.plot(freqs, np.degrees(theta_arr), 'r--', label='Faz Açısı')
            ax2.set_ylabel('Faz Açısı (°)', color='r')
            ax2.tick_params('y', colors='r')
            if circuit_type == "RLC":
                ax1.axvline(f_resonans, color='g', linestyle='--', label='f₀ (Rezonans)')
                ax1.legend()
            fig.tight_layout()
            st.pyplot(fig)
except:
    error_box.error("Bir hata oluştu. Lütfen girdilerinizi kontrol edip tekrar deneyin.")
    st.stop()