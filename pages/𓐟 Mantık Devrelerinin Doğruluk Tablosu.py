import streamlit as st
import itertools
import pandas as pd
import re
TITLE = 'ElektroXLab'
st.set_page_config(
    page_title=TITLE,
    page_icon="⚡",
    layout="wide",
)

error_box = st.empty()
try:
    #Mantık kapıları
    def AND(a,b): return a & b
    def OR(a,b): return a | b
    def NOT(a): return ~a & 1
    def NAND(a,b): return NOT(AND(a,b))
    def NOR(a,b): return NOT(OR(a,b))
    def XOR(a,b): return a ^ b
    def XNOR(a,b): return NOT(XOR(a,b))

    OPERATORS = {
        "NOT":  (4, "unary"),
        "AND":  (3, "binary"),
        "NAND": (3, "binary"),
        "OR":   (2, "binary"),
        "NOR":  (2, "binary"),
        "XOR":  (1, "binary"),
        "XNOR": (1, "binary"),
    }


    #TOKENIZE YAPILAN YER
    def tokenize(expr):
        expr = expr.upper().replace(" ", "")
        pattern = r"NOT|NAND|NOR|AND|OR|XOR|XNOR|\(|\)|[A-Z]"
        return re.findall(pattern, expr)

    # -------------------------

    def to_rpn(tokens):
        output = []
        stack = []

        for t in tokens:
            if re.fullmatch(r"[A-Z]", t):
                output.append(t)

            elif t in OPERATORS:
                prec, typ = OPERATORS[t]
                while stack and stack[-1] in OPERATORS:
                    p2, _ = OPERATORS[stack[-1]]
                    if p2 >= prec:
                        output.append(stack.pop())
                    else:
                        break
                stack.append(t)

            elif t == "(":
                stack.append(t)

            elif t == ")":
                while stack and stack[-1] != "(":
                    output.append(stack.pop())
                stack.pop()  # '('

        while stack:
            output.append(stack.pop())

        return output

    # -------------------------

    class Node:
        def __init__(self, op, left=None, right=None):
            self.op = op
            self.left = left
            self.right = right

    def rpn_to_ast(rpn):
        stack = []
        for t in rpn:
            if t in OPERATORS:
                prec, typ = OPERATORS[t]
                if typ == "unary":
                    a = stack.pop()
                    stack.append(Node(t, a))
                else:
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(Node(t, a, b))
            else:
                stack.append(t)
        return stack[0]

    # -------------------------

    def evaluate(node, values):
        if isinstance(node, str):
            return values[node]

        if OPERATORS[node.op][1] == "unary":
            return NOT(evaluate(node.left, values))

        left = evaluate(node.left, values)
        right = evaluate(node.right, values)
        return globals()[node.op](left, right)

    #STREAMLİT TARAFI-------------------------

    st.title("𝄜 Doğruluk Tablosu")
    with st.expander("AÇIKLAMA"):
        st.write("Bu sayfada girdiğiniz lojik ifadelerin doğruluk tablosuna ulaşabilirsiniz. ")
        st.write("- Doğruluk tablosu sadece değişkenlerin farklı değerlerine göre son output sütununu verir, ara işlem değerlerini yazdırmaz.")
        st.write( "- ***Lütfen parantez kullanımlarınıza dikkat ediniz ve örneklere göz atınız!***")
        st.write( "**Örnek:** ")
        st.write("* (A AND NOT B) OR (B XOR C)")
        st.write( "* ((A AND B) OR (NOT A AND C)) XOR (B OR NOT C)")
        st.write("* ((A AND NOT B) OR (C XOR D)) AND ((B OR C) XOR (NOT A AND D))")


    expression = st.text_input("Mantıksal ifade:")

    if expression:
        tokens = tokenize(expression)
        rpn = to_rpn(tokens)
        ast = rpn_to_ast(rpn)

        variables = sorted({t for t in tokens if re.fullmatch(r"[A-Z]", t)})

        combos = list(itertools.product([0,1], repeat=len(variables)))
        results = []

        for combo in combos:
            val_dict = dict(zip(variables, combo))
            out = evaluate(ast, val_dict)
            results.append(list(combo) + [out])

        df = pd.DataFrame(results, columns=variables + ["Output"])
        st.dataframe(df)
except:
    error_box.error("Bir hata oluştu. Lütfen girdilerinizi kontrol edip tekrar deneyin.")
    st.stop()