import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

TITLE = 'ElektroXLab'
st.set_page_config(
    page_title=TITLE,
    page_icon="⚡",
    layout="wide",
)
st.title("2–3–4 Değişken Karnaugh Sadeleştirici")
with st.expander("AÇIKLAMA"):
    st.markdown("Bu sayfada 2-3 veya 4 değişkenli ifadelerinizin maxterm veya minterm olduğu bitleri girerek SOP sonucunu ve karnough haritası çizimini elde edebilirsiniz.")
    st.markdown("* Fonskiyonun 1 olduğu durumlar minterm, 0 olduğu durumlar ise maxtermlerdir.")
    st.markdown("* SOP, çarpımların toplamı anlamına gelirken, POS ise toplamların çarpımı anlamına gelmektedir.")
    st.markdown("Tanımları hatırlayalım:")
    st.markdown("SOP (Sum of Products)	1 olan mintermleri AND’leyip OR’la birleştirirsin.")
    st.markdown("POS (Product of Sums)	0 olan maxtermleri OR’layıp AND ile birleştirirsin.")
    st.markdown("-----Dönüşüm mantığı------")
    st.markdown("")
    st.markdown("SOP → POS")
    st.markdown("")
    st.markdown("SOP’teki her minterm 1 olduğu durumu temsil eder.")
    st.markdown("")
    st.markdown("Fonksiyonun 0 olduğu durumları bul (yani minterm olmayan durumlar).")
    st.markdown("")
    st.markdown("Bu 0’lar maxterm olur.")
    st.markdown("")
    st.markdown("Maxtermleri OR’layıp hepsini AND ile birleştir → POS elde edilir.")
    st.markdown("----")
    st.markdown("POS → SOP")
    st.markdown("")
    st.markdown("POS’teki her maxterm fonksiyonun 0 olduğu durumu gösterir.")
    st.markdown("")
    st.markdown("1 olan durumları bul (maxterm olmayanlar).")
    st.markdown("")
    st.markdown("Mintermleri AND’leyip hepsini OR’la → SOP elde edilir.")
    '---'
    st.markdown("Değişken sayınızı, minterm veya maxterm seçeneğini ve ilgili bit sayılarını giriniz.")
error_box = st.empty()

try:

    # Gray Kodu---------------

    def gray_code(n):
        if n == 0:
            return [""]
        if n == 1:
            return ["0", "1"]
        prev = gray_code(n - 1)
        return ["0" + x for x in prev] + ["1" + x for x in reversed(prev)]


    # K-map-----------

    def build_kmap(minterms, num_vars):
        if num_vars == 2:
            rows, cols = 2, 2
        elif num_vars == 3:
            rows, cols = 2, 4
        elif num_vars == 4:
            rows, cols = 4, 4
        else:
            raise ValueError("Sadece 2, 3 veya 4 değişken desteklenir.")

        row_bits = num_vars // 2
        col_bits = num_vars - row_bits

        ROW = gray_code(row_bits)
        COL = gray_code(col_bits)

        kmap = [[0]*cols for _ in range(rows)]
        for m in minterms:
            if m < 0 or m >= 2**num_vars:
                raise ValueError("Minterm aralık dışında.")
            bits = f"{m:0{num_vars}b}"
            r = ROW.index(bits[:row_bits])
            c = COL.index(bits[row_bits:])
            kmap[r][c] = 1

        return kmap, ROW, COL


    # Gruplar---------------------

    def get_group_cells(r, c, h, w, rows, cols):
        return [((r+i) % rows, (c+j) % cols) for i in range(h) for j in range(w)]

    def power_of_two_sizes(limit):
        sizes = []
        p = 1
        while p <= limit:
            sizes.append(p)
            p *= 2
        return sizes

    def all_possible_groups(kmap):
        rows, cols = len(kmap), len(kmap[0])
        groups = set()
        h_sizes = power_of_two_sizes(rows)
        w_sizes = power_of_two_sizes(cols)

        for h in h_sizes:
            for w in w_sizes:
                for r in range(rows):
                    for c in range(cols):
                        cells = get_group_cells(r, c, h, w, rows, cols)
                        if all(kmap[rr][cc] == 1 for rr, cc in cells):
                            groups.add(frozenset(cells))
        return list(groups)

    def maximal_groups(groups):
        # Sadece başka hiçbir grubun alt kümesi olmayan grupları tut.
        groups_list = list(groups)
        maximal = []
        for i, g in enumerate(groups_list):
            is_subset = False
            for j, h in enumerate(groups_list):
                if i != j and g.issubset(h) and g != h:
                    is_subset = True
                    break
            if not is_subset:
                maximal.append(g)
        return maximal


    # Grup → Boolean-------------------

    def group_to_term(group, variables, ROW, COL):
        bits = []
        for (r, c) in group:
            bits.append(ROW[r] + COL[c])

        term = []
        for i, var in enumerate(variables):
            vals = {b[i] for b in bits}
            if len(vals) == 1:
                v = next(iter(vals))
                term.append(var if v == "1" else var + "'")
        return "".join(term)


    #--------------------------------------

    def kmap_simplify(minterms, variables):
        kmap, ROW, COL = build_kmap(minterms, len(variables))
        rows, cols = len(kmap), len(kmap[0])

        # Map minterm yerleşimi
        all_one_cells = {(r, c) for r in range(rows) for c in range(cols) if kmap[r][c] == 1}

        # maximal gruplar
        candidate_groups = all_possible_groups(kmap)
        prime_groups = maximal_groups(candidate_groups)

        # Map
        cover_map = {g: set(g) for g in prime_groups}
        cell_to_groups = {cell: [] for cell in all_one_cells}
        for g in prime_groups:
            for cell in cover_map[g]:
                if cell in cell_to_groups:
                    cell_to_groups[cell].append(g)

        # ------------------------
        essential = set()
        for cell, glist in cell_to_groups.items():
            if len(glist) == 1:
                essential.add(glist[0])

        selected = set(essential)
        covered = set().union(*[cover_map[g] for g in selected]) if selected else set()

        # Greedy cover for remaining cells
        remaining = all_one_cells - covered
        # Helper: tie-break by fewer literals (shorter term)
        def group_score(g):
            new_cover = len(cover_map[g] & remaining)
            literals = len(group_to_term(g, variables, ROW, COL))
            return (new_cover, -literals)  # max new_cover, then min literals

        while remaining:
            # Diğer hücreleri kaplayan en iyi grup
            best = None
            best_score = (-1, 0)
            for g in prime_groups:
                score = group_score(g)
                if score > best_score:
                    best = g
                    best_score = score
            if best is None or best_score[0] == 0:
                # Fallback
                singletons = [frozenset([cell]) for cell in remaining]
                for s in singletons:
                    selected.add(s)
                break
            selected.add(best)
            covered |= cover_map[best]
            remaining = all_one_cells - covered

        # SOP yapma
        terms = sorted(set(group_to_term(g, variables, ROW, COL) for g in selected if group_to_term(g, variables, ROW, COL)))
        result = " + ".join(terms) if terms else "0"  # if no terms, function is 0

        # For plotting, show only selected groups
        return result, kmap, list(selected), ROW, COL


    # Plot kısmı

    def plot_kmap(kmap, groups, ROW, COL, variables):
        rows, cols = len(kmap), len(kmap[0])
        fig, ax = plt.subplots(figsize=(max(6, cols+2), max(4, rows+2)))

        ax.imshow(kmap, cmap="Greys", vmin=0, vmax=1)

        # Grid
        for i in range(rows + 1):
            ax.axhline(i - 0.5, color="black", linewidth=1)
        for j in range(cols + 1):
            ax.axvline(j - 0.5, color="black", linewidth=1)

        # hücreler
        for r in range(rows):
            for c in range(cols):
                ax.text(c, r, str(kmap[r][c]),
                        ha="center", va="center", fontsize=14, color="red")

        # grup renklendirme
        for group in groups:
            color = (random.random(), random.random(), random.random(), 0.25)
            # Gruptaki her hücrenin üzerine yarı saydam bir örtü çiz
            for (r, c) in group:
                rect = plt.Rectangle((c-0.5, r-0.5), 1, 1, color=color)
                ax.add_patch(rect)

        # Axis
        ax.set_xticks(range(cols))
        ax.set_yticks(range(rows))
        ax.set_xticklabels(COL, fontsize=12)
        ax.set_yticklabels(ROW, fontsize=12)

        # Etiketler
        row_bits = len(ROW[0])
        col_bits = len(COL[0])
        row_vars = variables[:row_bits]
        col_vars = variables[row_bits:]
        ax.set_xlabel("Kolon: " + "".join(col_vars) + " Gray=" + " ".join(COL), fontsize=12)
        ax.set_ylabel("Satır: " + "".join(row_vars) + " Gray=" + " ".join(ROW), fontsize=12)

        ax.invert_yaxis()
        ax.set_title("Karnaugh Haritası", fontsize=14)
        plt.tight_layout()
        st.pyplot(fig)


    # Streamlit tarafı



    num_vars = st.selectbox("Değişken sayısı", [2, 3, 4])
    variables = [chr(ord("A")+i) for i in range(num_vars)]

    mode = st.radio("Girdi tipi", [
        "Minterm (fonksiyon 1 olduğu durumlar)",
        "Maxterm (fonksiyon 0 olduğu durumlar)"
    ])

    expr = st.text_input("Listeyi gir (örn: 1,2,3)")

    if st.button("Sadeleştir ve Görselleştir"):
        try:
            if expr.strip() == "":
                st.warning("Lütfen en az bir indeks giriniz (örn: 0,1,2).")
                st.stop()

            raw_parts = [x.strip() for x in expr.split(",")]
            if any(p == "" for p in raw_parts):
                raise ValueError("Girdi biçimi hatalı: boş eleman bulundu.")

            indices = [int(x) for x in raw_parts]
            if any(i < 0 or i >= 2**num_vars for i in indices):
                raise ValueError(f"İndeksler 0–{2**num_vars - 1} aralığında olmalıdır.")

            all_indices = set(range(2**num_vars))

            if mode.startswith("Min"):
                minterms = sorted(set(indices))
            else:
                minterms = sorted(all_indices - set(indices))

            # Edge cases
            if len(minterms) == 0:
                st.subheader("Minimal SOP")
                st.code("0")
                st.subheader("Karnaugh Haritası")
                kmap, ROW, COL = build_kmap(minterms, len(variables))
                plot_kmap(kmap, [], ROW, COL, variables)
                st.stop()

            if len(minterms) == 2**num_vars:
                st.subheader("Minimal SOP")
                st.code("1")
                st.subheader("Karnaugh Haritası")
                kmap, ROW, COL = build_kmap(minterms, len(variables))
                plot_kmap(kmap, [frozenset([(r, c) for r in range(len(kmap)) for c in range(len(kmap[0]))])], ROW, COL, variables)
                st.stop()

            result, kmap, groups, ROW, COL = kmap_simplify(minterms, variables)

            st.subheader("Minimal SOP")
            st.code(result if result else "0")

            st.subheader("Karnaugh Haritası")
            plot_kmap(kmap, groups, ROW, COL, variables)

        except Exception as e:
            error_box.error(f"Hata: {e}")
            st.stop()

except Exception as e:
    error_box.error(f"Hata: {e}")
    st.stop()
