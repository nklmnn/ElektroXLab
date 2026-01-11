import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

TITLE = 'ElektroXLab'
st.set_page_config(
    page_title=TITLE,
    page_icon="⚡",
    layout="wide",
)

st.title("📐Fazör Hesaplayıcı")

with st.expander("AÇIKLAMA"):
    st.markdown("""
        
        - Fazörler, karmaşık sayılardır. Gerçek ve sanal kısımdan oluşurlar.
        - Sanal kısım bize açıyı verir, x-y koordinat sisteminde y eksenini belirler. Gerçek kısım ise x ekseninde gösterilir.
        - ***Bu sayfada fazörlerle ilgili dönüşüm, toplama, çıkarma, çarpma, bölme veya ortalama alma işlemleri yapabilirsiniz. Sanal kısım için 'i' veya 'j' yazmaya gerek yoktur.***
        - ***Ondalık sayı girerken '    ,   ' kullanınız!***
""")
    with st. expander("Formüller"):
        st.subheader("Fazör Dönüşüm Formülleri")
        st.latex(r"v(t) = V_m \cos(\omega t + \theta) \rightarrow \mathbf{V} = V_m \angle \theta")
        st.latex(r"i(t) = I_m \cos(\omega t + \phi) \rightarrow \mathbf{I} = I_m \angle \phi")
        st.latex(r"\mathbf{V} = V_m \angle \theta \rightarrow v(t) = V_m \cos(\omega t + \theta)")
        st.latex(r"\mathbf{I} = I_m \angle \phi \rightarrow i(t) = I_m \cos(\omega t + \phi)")
        st.latex(r"\mathbf{V} = V_m \cos\theta + j V_m \sin\theta")
        st.latex(
            r"V_{\text{polar}} = \sqrt{(\text{Re}\{V\})^2 + (\text{Im}\{V\})^2}, \quad \theta = \arctan{\frac{\text{Im}\{V\}}{\text{Re}\{V\}}}")

error_box = st.empty()
try:

    #FAZÖR DÖNÜŞÜM FONKSİYONLARI ----------------
    def polar_to_rect(mag, angle_deg):
        angle_rad = np.radians(angle_deg)
        return mag * np.cos(angle_rad) + 1j * mag * np.sin(angle_rad)

    def rect_to_polar(c):
        mag = np.abs(c)
        angle_deg = np.degrees(np.angle(c))
        return mag, angle_deg

    #LIMITLER ----------------
    MAG_MIN, MAG_MAX = 0.0, 1e6
    ANGLE_MIN, ANGLE_MAX = -360.0, 360.0
    REAL_MIN, REAL_MAX = -1e6, 1e6
    IMAG_MIN, IMAG_MAX = -1e6, 1e6

    # SEÇİMLER------------------------------------
    operation = st.selectbox("İşlem Türünü Seçin", ["Dönüşüm", "Fazör İşlemleri"])


    #DÖNÜŞÜM----------------------------------------------------

    if operation == "Dönüşüm":
        mode = st.radio("Girdi Türü", ["Kutupsal → Kartezyan", "Kartezyan → Kutupsal"])

        # ---- KUTUPSAL → KARTEZYAN ----
        if mode == "Kutupsal → Kartezyan":
            mag = st.number_input("Genlik (|Z|)", value=10.0, min_value=MAG_MIN, max_value=MAG_MAX)
            angle_deg = st.number_input("Açı (°)", value=30.0, min_value=ANGLE_MIN, max_value=ANGLE_MAX)

            # limit kontrolü
            if not (MAG_MIN <= mag <= MAG_MAX and ANGLE_MIN <= angle_deg <= ANGLE_MAX):
                st.error("⚠ Limit dışında giriş var. Hesaplama durduruldu.")
                st.stop()

            z = polar_to_rect(mag, angle_deg)

            st.header("Sonuç (Kartezyan)")
            st.write(f"Gerçek Kısım: {z.real:.6g}")
            st.write(f"Sanal Kısım: {z.imag:.6g}j")
            st.latex(f"Z = {z.real:.6g} + {z.imag:.6g}j")

        #KARTEZYAN DAN KUTUPSALA---------------------
        else:
            real = st.number_input("Gerçek Kısım", value=8.0, min_value=REAL_MIN, max_value=REAL_MAX)
            imag = st.number_input("Sanal Kısım (j)", value=4.0, min_value=IMAG_MIN, max_value=IMAG_MAX)

            if not (REAL_MIN <= real <= REAL_MAX and IMAG_MIN <= imag <= IMAG_MAX):
                st.error("⚠ Limit dışında giriş var. Hesaplama durduruldu.")
                st.stop()

            z = real + 1j * imag
            mag, angle_deg = rect_to_polar(z)

            st.header("Sonuç (Kutupsal)")
            st.write(f"Genlik: {mag:.6g}")
            st.write(f"Açı: {angle_deg:.2f}°")
            st.latex(f"Z = {mag:.6g} \\angle {angle_deg:.2f}^\circ")

        #Fazör diyagramı-----
        with st.expander("Fazör diyagramı"):
            fig, ax = plt.subplots(figsize=(5,5))
            mag_z = np.abs(z)
            arrow = FancyArrowPatch((0,0),(z.real,z.imag), color='b', arrowstyle='-|>', mutation_scale=20)
            ax.add_patch(arrow)

            ax.set_xlim(-1.2*mag_z, 1.2*mag_z)
            ax.set_ylim(-1.2*mag_z, 1.2*mag_z)
            ax.set_aspect('equal')
            ax.grid(alpha=0.3)
            ax.set_xlabel("Re")
            ax.set_ylabel("Im")
            ax.set_title("Fazör Diyagramı")
            st.pyplot(fig)


    #FAZÖR İŞLEMLERİ-------------------------------------------------

    else:
        st.subheader("➕ Fazör İşlemleri")

        operation_type = st.selectbox(
            "Hangi işlemi yapmak istiyorsunuz?",
            ["Toplama", "Çıkarma", "Çarpma", "Ortalama", "İki Fazörü Böl (Z1 / Z2)"]
        )

        # ---- Fazör sayısı ----
        if operation_type == "İki Fazörü Böl (Z1 / Z2)":
            n = 2
            st.info(" Bu işlem için yalnızca 2 fazör girilir.")
        else:
            n = st.number_input(
                "Kaç fazör gireceksiniz?",
                min_value=2, max_value=10, value=2
            )

        fazors = []
        labels = []
        colors = plt.cm.tab10.colors

        #FAZÖRLERİN ALINMASI------------------------------------------
        for i in range(n):
            st.markdown(f"**Fazör {i + 1}**")
            input_type = st.radio(
                f"Giriş Türü Fazör {i + 1}",
                ["Kutupsal", "Kartezyan"],
                key=f"type_{i}"
            )

            #Kutupsal giriş---------------------------------
            if input_type == "Kutupsal":
                mag = st.number_input(
                    f"Genlik {i + 1}",
                    value=10.0,
                    min_value=MAG_MIN,
                    max_value=MAG_MAX,
                    key=f"mag_{i}"
                )
                angle_deg = st.number_input(
                    f"Açı (°) {i + 1}",
                    value=0.0,
                    min_value=ANGLE_MIN,
                    max_value=ANGLE_MAX,
                    key=f"angle_{i}"
                )

                if not (MAG_MIN <= mag <= MAG_MAX and ANGLE_MIN <= angle_deg <= ANGLE_MAX):
                    st.error(f"⚠ Fazör {i + 1} limit dışında.")
                    st.stop()

                z = polar_to_rect(mag, angle_deg)

            #Kartezyan giriş ----------------------------------
            else:
                real = st.number_input(
                    f"Gerçek Kısım {i + 1}",
                    value=0.0,
                    min_value=REAL_MIN,
                    max_value=REAL_MAX,
                    key=f"real_{i}"
                )
                imag = st.number_input(
                    f"Sanal Kısım (j) {i + 1}",
                    value=0.0,
                    min_value=IMAG_MIN,
                    max_value=IMAG_MAX,
                    key=f"imag_{i}"
                )

                if not (REAL_MIN <= real <= REAL_MAX and IMAG_MIN <= imag <= IMAG_MAX):
                    st.error(f"⚠ Fazör {i + 1} limit dışında.")
                    st.stop()

                z = real + 1j * imag

            fazors.append(z)
            labels.append(f"Z{i + 1}")

        # HESAPLAMA-----------------------------
        if operation_type == "Toplama":
            result = sum(fazors)

        elif operation_type == "Çıkarma":
            result = fazors[0]
            for z in fazors[1:]:
                result -= z

        elif operation_type == "Çarpma":
            result = fazors[0]
            for z in fazors[1:]:
                result *= z

        elif operation_type == "Ortalama":
            result = sum(fazors) / len(fazors)

        elif operation_type == "İki Fazörü Böl (Z1 / Z2)":
            if fazors[1] == 0:
                st.error("⚠ Sıfır fazöre bölme yapılamaz.")
                st.stop()
            result = fazors[0] / fazors[1]

        #SONUÇ-------------------------
        st.header("Sonuç:")

        st.write("Kartezyan Hali:")
        st.write(f"Gerçek Kısım: {result.real:.6g}")
        st.write(f"Sanal Kısım: {result.imag:.6g}j")
        st.latex(f"Z = {result.real:.6g} + {result.imag:.6g}j")

        mag, angle_deg = rect_to_polar(result)
        st.write("Kutupsal Hali:")
        st.write(f"Genlik: {mag:.6g}")
        st.write(f"Açı: {angle_deg:.2f}°")
        st.latex(f"Z = {mag:.6g} \\angle {angle_deg:.2f}^\circ")

        # --------- Fazör diyagramı ---------
        with st.expander("Fazör diyagramı"):
            fig, ax = plt.subplots(figsize=(6, 6))

            for i, z in enumerate(fazors):
                arrow = FancyArrowPatch(
                    (0, 0),
                    (z.real, z.imag),
                    color=colors[i % 10],
                    arrowstyle='-|>',
                    mutation_scale=20,
                    label=labels[i]
                )
                ax.add_patch(arrow)

            #Sonuç fazörü kırmızı
            arrow_r = FancyArrowPatch(
                (0, 0),
                (result.real, result.imag),
                color='r',
                arrowstyle='-|>',
                mutation_scale=25,
                label='Sonuç'
            )
            ax.add_patch(arrow_r)

            max_mag = max([np.abs(z) for z in fazors] + [np.abs(result)])

            ax.set_xlim(-1.2 * max_mag, 1.2 * max_mag)
            ax.set_ylim(-1.2 * max_mag, 1.2 * max_mag)
            ax.set_aspect('equal')
            ax.grid(alpha=0.3)
            ax.set_xlabel("Re")
            ax.set_ylabel("Im")
            ax.set_title("Fazör Diyagramı")
            ax.legend()

            st.pyplot(fig)
except:
    error_box.error("Bir hata oluştu. Lütfen girdilerinizi kontrol edip tekrar deneyin.")
st.stop()