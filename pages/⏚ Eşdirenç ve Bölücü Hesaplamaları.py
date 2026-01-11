import streamlit as st
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

st.title("♒︎ Eşdeğer Direnç ve Bölücü Hesaplamaları")
''
''
''
with st.expander("AÇIKLAMA"):
    st.markdown("""
    Bu sayfada:
    - Seri veya paralel dirençlerde eşdeğer direnç, akım ve güç hesaplayabilirsiniz.
    - Gerilim veya akım bölücü hesaplamaları yapabilirsiniz.
    - Değer girişlerini yaparken SI birimleri kullanabilirsiniz. (k,m,M,u).
    - Hesaplama yapmak için giriş kutularını doldurunuz, bölücü seçmek opsiyoneldir.
    - Seçilen bağlantı tipine göre girilen tüm dirençler aynı bağlantı tipinde kabul edilerek hesap yapılmaktadır. Bağlantı şekli sayfanın altında bir çizim halinde gösterilmektedir. 
    - **Eğer daha karmaşık bir topolojiniz varsa prompt yoluyla hesaplama yapınız, devrenizi sağdan sola doğru promptlaştırmayı tercih ediniz.**
    
    ---
    BİLGİLENDİRME:
    - Eş değer direnç, devredeki dirençlerin konumuna uygun olarak işleme alınıp  tek bir direnç değeri olarak özetlenmesine verilen isimdir.
    - Gerilim bölücü, toplam dirence kıyasla seçili bir direncin üzerine düşen gerilimin hesaplanmasında kullanılır, direnç değeriyle doğru orantılıdır. (Paralel kollardaki dirençlerin gerilimleri aynıdır.)
    - Akım bölücü, toplam dirence kıyasla seçili bir direncin üzerinden geçen akımın hesaplanmasında kullanılır, direnç değeriyle ters orantılıdır. (Seri koldaki dirençlerin akımı aynıdır.)
    
    """)
    with st.expander("Temel Formüller"):


        st.subheader("Dirençlerin Eşdeğerinin Alınması ")
        st.markdown("**Seri:**")
        st.latex(r"R_{eq} = R_1 + R_2 + \dots")
        st.markdown("**Paralel:**")
        st.latex(r"\frac{1}{R_{eq}} = \frac{1}{R_1} + \frac{1}{R_2} + \dots")
        '---'
        st.subheader("Gerilim Bölücü Formülü")

        st.latex(r"""
        V_{out} = V_{in} \times \frac{R_k}{R_1 + R_2 + \dots + R_n} = V_{in} \times \frac{R_k}{R_{eq}}
        """)
        '---'
        st.subheader("Akım Bölücü Formülü")
        st.latex(r"""
        I_k = I_{in} \times \frac{\frac{1}{R_k}}{\frac{1}{R_1} + \frac{1}{R_2} + \dots + \frac{1}{R_n}} 
            = I_{in} \times \frac{1/R_k}{R_{eq}}
        """)

error_box = st.empty()
try:
    with st.expander("Prompt yoluyla hesaplama"):

        import pandas as pd

        st.title("♒ Direnç Hesaplamaları")
        st.write("Promptları nasıl doğru yazacağınıza dair örnekler aşağıda verilmiştir. ***Yazımlarınızda parantezlerinize dikkat etmeyi unutmayın!***")
        st.write("**ÖRNEKLER**")
        st.write("* ((100 seri 200) paralel (300 seri 400)) seri 50")
        st.write("* (5472 paralel 217) seri 9")
        st.write("* (((843 paralel 267) paralel 905) seri 211) paralel 666")
        '---'
        # --- ID üretici ---
        _rid = {"n": 0}


        def new_id():
            _rid["n"] += 1
            return f"R{_rid['n']}"


        # --- Parser ---
        def parse_block(expr: str):
            expr = expr.strip().lower().replace("ohm", "")
            tokens = expr.replace("(", " ( ").replace(")", " ) ").split()

            def parse_number(tok):
                return float(tok)

            def helper(tokens):
                stack = []
                while tokens:
                    tok = tokens.pop(0)
                    if tok == "(":
                        stack.append(helper(tokens))
                    elif tok == ")":
                        break
                    elif tok.replace(".", "", 1).isdigit():
                        val = parse_number(tok)
                        stack.append({"type": "R", "id": new_id(), "value": val})
                    elif tok in ["seri", "paralel"]:
                        stack.append(tok)
                    else:
                        try:
                            val = parse_number(tok)
                            stack.append({"type": "R", "id": new_id(), "value": val})
                        except:
                            pass
                if len(stack) == 1 and isinstance(stack[0], dict) and stack[0].get("type") == "R":
                    return stack[0]
                else:
                    node = {"type": None, "children": []}
                    for item in stack:
                        if isinstance(item, dict):
                            node["children"].append(item)
                        elif item in ["seri", "paralel"]:
                            node["type"] = item
                    return node

            return helper(tokens)


        #Eşdeğer direnç---------------------------------------
        def calc_equiv(node):
            if node.get("type") == "R":
                return node["value"]
            if node["type"] == "seri":
                return sum(calc_equiv(c) for c in node["children"])
            elif node["type"] == "paralel":
                inv_sum = sum(1.0 / calc_equiv(c) for c in node["children"])
                return 1.0 / inv_sum


        # Gerilim bölücü-----------------------------------------------
        def voltage_divider(node, total_v):
            results = {}

            def walk(n, Vn):
                if n.get("type") == "R":
                    results[n["id"]] = {"R": n["value"], "V": Vn}
                    return
                if n["type"] == "seri":
                    R_eq = calc_equiv(n)
                    for c in n["children"]:
                        Rc = calc_equiv(c)
                        Vc = Vn * (Rc / R_eq)
                        walk(c, Vc)
                elif n["type"] == "paralel":
                    for c in n["children"]:
                        walk(c, Vn)

            walk(node, total_v)
            return results


        #Akım bölücü---------------------------------------
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
                    R_eq = calc_equiv(n)
                    for c in n["children"]:
                        Rc = calc_equiv(c)
                        Ic = In * (R_eq / Rc)
                        walk(c, Ic)

            walk(node, total_i)
            return results


        #Kullanıcı Input-------------------------------------------------------
        devre_input = st.text_input("Devreyi yazınız")
        mode = st.selectbox("Hesaplama Modu", ["Normal Hesaplama", "Gerilim Bölücü", "Akım Bölücü"])

        # Dinamik input kutuları
        if mode == "Gerilim Bölücü":
            value_input = st.number_input("Toplam Gerilim (V)", min_value=0.0, value=10.0, max_value=1e15)
        elif mode == "Akım Bölücü":
            value_input = st.number_input("Toplam Akım (A)", min_value=0.0, value=10.0, max_value=1e15)
        else:  # Normal Hesaplama
            choice = st.radio("Toplam değer türünü seçiniz:", ["Gerilim (V)", "Akım (A)"])
            if choice == "Gerilim (V)":
                value_input = st.number_input("Toplam Gerilim (V)", min_value=0.0, value=10.0, max_value=1e15)
                input_type = "V"
            else:
                value_input = st.number_input("Toplam Akım (A)", min_value=0.0, value=10.0, max_value=1e15)
                input_type = "I"

        if st.button("Hesapla"):
            tree = parse_block(devre_input)
            r_eq = calc_equiv(tree)
            st.success(f"Eşdeğer direnç: {r_eq:.6g} Ω")

            if mode == "Gerilim Bölücü":
                st.subheader("Gerilim / Akım / Güç Tablosu")
                voltages = voltage_divider(tree, value_input)
                data = []
                for rid, res in voltages.items():
                    r = res["R"];
                    v = res["V"]
                    i = v / r;
                    p = v * i
                    data.append({"ID": rid, "Direnç (Ω)": f"{r:.6g}", "Gerilim (V)": f"{v:.6g}",
                                 "Akım (A)": f"{i:.6g}", "Güç (W)": f"{p:.6g}"})
                df = pd.DataFrame(data)
                st.table(df)

            elif mode == "Akım Bölücü":
                st.subheader("Gerilim / Akım / Güç Tablosu")
                currents = current_divider(tree, value_input)
                data = []
                for rid, res in currents.items():
                    r = res["R"];
                    i = res["I"]
                    v = i * r;
                    p = v * i
                    data.append({"ID": rid, "Direnç (Ω)": f"{r:.6g}", "Gerilim (V)": f"{v:.6g}",
                                 "Akım (A)": f"{i:.6g}", "Güç (W)": f"{p:.6g}"})
                df = pd.DataFrame(data)
                st.table(df)

            else:  # Normal Hesaplama
                st.subheader("Toplam Güç")
                if input_type == "V":
                    total_power = (value_input ** 2) / r_eq
                else:  # Akım seçilmişse
                    total_power = (value_input ** 2) * r_eq
                st.write(f"Toplam güç: {total_power:.6g} W")

    import streamlit as st


    #Birim çevirici---------------------------------------------------------------
    def parse_input(value_str):
        try:
            value_str = value_str.strip().replace(',', '.').replace('V', '').replace('A', '')
            if value_str.endswith(('k', 'K')):
                return float(value_str[:-1]) * 1e3
            elif value_str.endswith('m'):
                return float(value_str[:-1]) * 1e-3
            elif value_str.endswith(('u', 'μ')):
                return float(value_str[:-1]) * 1e-6
            elif value_str.endswith('M'):
                return float(value_str[:-1]) * 1e6
            else:
                return float(value_str)
        except:
            return None


    col1, col2 = st.columns(2)


    #SI input kontrolü ----------
    def get_value_checked(label, default="1k", min_val=None, max_val=None, allow_zero=False):
        val_str = st.text_input(label, value=default)
        val = parse_input(val_str)
        if val is None:
            return None
        if not allow_zero and val <= 0:
            st.error("⚠ Değer sıfır veya negatif olamaz!")
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
        # ---------- Kullanıcı Girdileri ----------
        num_resistors = st.number_input("Direnç sayısı", min_value=2, max_value=10, value=2, step=1)
        connection_type = st.selectbox("Bağlantı tipi", ["Seri", "Paralel"])
        divider_type = st.selectbox("Bölücü tipi (opsiyonel)", ["Yok", "Gerilim Bölücü", "Akım Bölücü"])

        #Dirençleri al
        R_values = []
        for i in range(num_resistors):
            R_val = get_value_checked(f"R{i + 1} (Ω)", default=f"{1 * (i + 1)}k", min_val=0.000001, max_val=1e6)
            if R_val is None:
                st.stop()
            R_values.append(R_val)

        # Giriş gerilim/akım
        Vin = Iin = None
        if divider_type == "Gerilim Bölücü":
            Vin = get_value_checked("Giriş Gerilimi (Vin) [V]", default="10", min_val=0.00001, max_val=1e6)
            if Vin is None:
                st.stop()
        elif divider_type == "Akım Bölücü":
            Iin = get_value_checked("Giriş Akımı (Iin) [A]", default="0.01", min_val=0.000001, max_val=1e6)
            if Iin is None:
                st.stop()

        # Eğer bölücü seçildiyse hangi direnç baz alınacak
        if divider_type != "Yok":
            resistor_index = st.number_input(f"Çıkış hangi dirençten alınacak? (1-{num_resistors})", min_value=1,
                                             max_value=num_resistors, value=1) - 1

        #Hesaplama ----------
        # Eşdeğer direnç
        if connection_type == "Seri":
            Req = sum(R_values)
        else:  # Paralel
            Req = 1 / sum(1 / r for r in R_values)

        # ölücü hesaplaması
        Vout = Iout = None
        if divider_type == "Gerilim Bölücü":
            if connection_type == "Seri":
                Vout = Vin * (R_values[resistor_index] / Req)
        elif divider_type == "Akım Bölücü":
            if connection_type == "Paralel":
                G_total = sum(1 / r for r in R_values)  # toplam iletkenlik
                Ri = R_values[resistor_index]
                Iout = Iin * ((1 / Ri) / G_total)

        #Akım ve güç hesaplaması Req üzerinden
        if Vin is not None:
            I_total = Vin / Req
            P_total = Vin * I_total
        elif Iin is not None:
            V_total = Iin * Req
            P_total = V_total * Iin

    with col2:
        #Sonuçlar -------------------------------------
        st.subheader("Hesaplama Sonuçları")
        st.write(f"**Eşdeğer Direnç (Req):** {Req:.4f} Ω")
        if Vin is not None:
            st.write(f"**Toplam Akım (I):** {I_total:.6f} A")
            st.write(f"**Toplam Güç (P):** {P_total:.6f} W")
        elif Iin is not None:
            st.write(f"**Toplam Gerilim (V):** {V_total:.4f} V")
            st.write(f"**Toplam Güç (P):** {P_total:.6f} W")

        if Vout is not None:
            st.subheader("Gerilim Bölücü Çıkışı")
            st.write(f"**Vout:** {Vout:.4f} V")
            latex_str = (
                    r"V_{out} = V_{in} \times \frac{R_{" + str(resistor_index + 1) + r"}}{R_1 + \ldots + R_{"
                    + str(num_resistors) + r"}} = "
                    + f"{Vin} \\times \\frac{{{R_values[resistor_index]}}}{{{Req}}} = {Vout:.4f} \\, V"
            )
            st.latex(latex_str)

        if Iout is not None:
            st.subheader("Akım Bölücü Çıkışı")
            st.write(f"**Iout:** {Iout:.6f} A")

            # G_total: toplam iletkenlik
            G_total = sum(1 / r for r in R_values)
            Ri = R_values[resistor_index]

            latex_str = (
                    r"I_{out} = I_{in} \cdot \frac{1/R_i}{\sum 1/R} = "
                    + f"I_{{out}} = {Iin} \\times \\frac{{1/{Ri}}}{{{G_total:.6f}}} = {Iout:.6f} \\, A"
            )
            st.latex(latex_str)

        #Burdan sonrası çizim

        d = schemdraw.Drawing()

        if connection_type == "Seri":
            if num_resistors == 2:
                d += elm.SourceV().label('V_in').color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Resistor().label('R1').color('grey')
                d += elm.Resistor().label('R2').color('grey')
                d += elm.Line().right().length(1).color('grey')
                d += elm.Line().down().length(3).color('grey')
                d += elm.Line().left().length(7).color('grey')
                d += elm.Ground().color('grey')

            if num_resistors == 3:
                d += elm.SourceV().label('V_in').color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Resistor().label('R1').color('grey')
                d += elm.Resistor().label('R2').color('grey')
                d += elm.Resistor().label('R3').color('grey')
                d += elm.Line().right().length(1).color('grey')
                d += elm.Line().down().length(3).color('grey')
                d += elm.Line().left().length(10).color('grey')
                d += elm.Ground().color('grey')

            if num_resistors == 4:
                d += elm.SourceV().label('V_in').color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Resistor().label('R1').color('grey')
                d += elm.Resistor().label('R2').color('grey')
                d += elm.Resistor().label('R3').color('grey')
                d += elm.Resistor().label('R4').color('grey')
                d += elm.Line().right().length(1).color('grey')
                d += elm.Line().down().length(3).color('grey')
                d += elm.Line().left().length(13).color('grey')
                d += elm.Ground().color('grey')

            if num_resistors == 5:
                d += elm.SourceV().label('V_in').color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Resistor().label('R1').color('grey')
                d += elm.Resistor().label('R2').color('grey')
                d += elm.Resistor().label('R3').color('grey')
                d += elm.Resistor().label('R4').color('grey')
                d += elm.Resistor().label('R5').color('grey')
                d += elm.Line().right().length(1).color('grey')
                d += elm.Line().down().length(3).color('grey')
                d += elm.Line().left().length(16).color('grey')
                d += elm.Ground().color('grey')
            if num_resistors == 6:
                d += elm.SourceV().label('V_in').color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Resistor().label('R1').color('grey')
                d += elm.Resistor().label('R2').color('grey')
                d += elm.Resistor().label('R3').color('grey')
                d += elm.Resistor().label('R4').color('grey')
                d += elm.Resistor().label('R5').color('grey')
                d += elm.Resistor().label('R6').color('grey')
                d += elm.Line().right().length(1).color('grey')
                d += elm.Line().down().length(3).color('grey')
                d += elm.Line().left().length(19).color('grey')
                d += elm.Ground().color('grey')
            if num_resistors == 7:
                d += elm.SourceV().label('V_in').color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Resistor().label('R1').color('grey')
                d += elm.Resistor().label('R2').color('grey')
                d += elm.Resistor().label('R3').color('grey')
                d += elm.Resistor().label('R4').color('grey')
                d += elm.Resistor().label('R5').color('grey')
                d += elm.Resistor().label('R6').color('grey')
                d += elm.Resistor().label('R7').color('grey')
                d += elm.Line().right().length(1).color('grey')
                d += elm.Line().down().length(3).color('grey')
                d += elm.Line().left().length(22).color('grey')
                d += elm.Ground().color('grey')
            if num_resistors == 8:
                d += elm.SourceV().label('V_in').color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Resistor().label('R1').color('grey')
                d += elm.Resistor().label('R2').color('grey')
                d += elm.Resistor().label('R3').color('grey')
                d += elm.Resistor().label('R4').color('grey')
                d += elm.Resistor().label('R5').color('grey')
                d += elm.Resistor().label('R6').color('grey')
                d += elm.Resistor().label('R7').color('grey')
                d += elm.Resistor().label('R8').color('grey')
                d += elm.Line().right().length(1).color('grey')
                d += elm.Line().down().length(3).color('grey')
                d += elm.Line().left().length(25).color('grey')
                d += elm.Ground().color('grey')

            if num_resistors == 9:
                d += elm.SourceV().label('V_in').color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Resistor().label('R1').color('grey')
                d += elm.Resistor().label('R2').color('grey')
                d += elm.Resistor().label('R3').color('grey')
                d += elm.Resistor().label('R4').color('grey')
                d += elm.Resistor().label('R5').color('grey')
                d += elm.Resistor().label('R6').color('grey')
                d += elm.Resistor().label('R7').color('grey')
                d += elm.Resistor().label('R8').color('grey')
                d += elm.Resistor().label('R9').color('grey')
                d += elm.Line().right().length(1).color('grey')
                d += elm.Line().down().length(3).color('grey')
                d += elm.Line().left().length(28).color('grey')
                d += elm.Ground().color('grey')

            if num_resistors == 10:
                d += elm.SourceV().label('V_in').color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Resistor().label('R1').color('grey')
                d += elm.Resistor().label('R2').color('grey')
                d += elm.Resistor().label('R3').color('grey')
                d += elm.Resistor().label('R4').color('grey')
                d += elm.Resistor().label('R5').color('grey')
                d += elm.Resistor().label('R6').color('grey')
                d += elm.Resistor().label('R7').color('grey')
                d += elm.Resistor().label('R8').color('grey')
                d += elm.Resistor().label('R9').color('grey')
                d += elm.Resistor().label('R10').color('grey')
                d += elm.Line().right().length(1).color('grey')
                d += elm.Line().down().length(3).color('grey')
                d += elm.Line().left().length(31).color('grey')
                d += elm.Ground().color('grey')

        else:

            if num_resistors == 2:
                d += elm.SourceV().label('V_in').color('grey')
                d += elm.Line().right().length(2).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R1').color('grey')
                d += elm.Ground().color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R2').color('grey')
                d += elm.Line().left().length(2).color('grey')




            if num_resistors == 3:
                d += elm.SourceV().label('V_in').color('grey')
                d += elm.Line().right().length(2).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R1').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R2').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R3').color('grey')

                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Ground().color('grey')

            if num_resistors == 4:
                d += elm.SourceV().label('V_in').color('grey')
                d += elm.Line().right().length(2).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R1').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Ground().color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R2').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R3').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R4').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(2).color('grey')


            if num_resistors == 5:
                d += elm.SourceV().label('V_in').color('grey')
                d += elm.Line().right().length(2).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R1').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R2').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R3').color('grey')
                d += elm.Ground().color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R4').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R5').color('grey')
                d += elm.Line().left().length(2).color('grey')


            if num_resistors == 6:
                d += elm.SourceV().label('V_in').color('grey')
                d += elm.Line().right().length(2).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R1').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R2').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R3').color('grey')
                d += elm.Ground().color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R4').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R5').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R6').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(2).color('grey')


            if num_resistors == 7:
                d += elm.SourceV().label('V_in').color('grey')
                d += elm.Line().right().length(2).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R1').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R2').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R3').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Ground().color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R4').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R5').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R6').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R7').color('grey')
                d += elm.Line().left().length(2).color('grey')


            if num_resistors == 8:
                d += elm.SourceV().label('V_in').color('grey')
                d += elm.Line().right().length(2).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R1').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R2').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R3').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Ground().color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R4').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R5').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R6').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R7').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R8').color('grey')
                d += elm.Line().left().length(2).color('grey')

            if num_resistors == 9:
                d += elm.SourceV().label('V_in').color('grey')
                d += elm.Line().right().length(2).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R1').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R2').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R3').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R4').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R5').color('grey')
                d += elm.Ground().color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R6').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R7').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R8').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R9').color('grey')
                d += elm.Line().left().length(0).color('grey')
                d += elm.Line().left().length(2).color('grey')

            if num_resistors == 10:
                d += elm.SourceV().label('V_in').color('grey')
                d += elm.Line().right().length(2).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R1').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R2').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R3').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R4').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R5').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Ground().color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R6').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R7').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R8').color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().down().length(0).color('grey')
                d += elm.Resistor().label('R9').color('grey')
                d += elm.Line().left().length(0).color('grey')
                d += elm.Line().left().length(2).color('grey')
                d += elm.Line().right().length(0).color('grey')
                d += elm.Line().right().length(4).color('grey')
                d += elm.Line().up().length(0).color('grey')
                d += elm.Resistor().label('R10').color('grey')
                d += elm.Line().left().length(0).color('grey')
                d += elm.Line().left().length(2).color('grey')

        #Görseli Streamlite aktar
        buf = io.BytesIO()
        d.draw()
        d.save(buf)
        buf.seek(0)
        img = Image.open(buf)
        st.image(img)
except:
    error_box.error("Bir hata oluştu. Lütfen girdilerinizi kontrol edip tekrar deneyin.")
    st.stop()