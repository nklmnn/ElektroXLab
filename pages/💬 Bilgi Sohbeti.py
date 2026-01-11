import pandas as pd


data = {
    "soru": [
        "Site",

        "Merhaba",
        "selam",
        "nasılsın, naber",
        "İyiyim",
        "Kötüyüm",
        "fazör nedir",
        "kompanzasyon nedir",
        "direnç nedir",
        "endüktans nedir",
        "kapasitör nedir",
        "transistör nedir",
        "diyot nedir",
        "ohm kanunu nedir",
        "ac nedir",
        "dc nedir",
        "voltaj nedir",
        "akım nedir",
        "güç nedir",
        "frekans nedir",
        "görüşürüz",
        "topraklama nedir",
        "kısa devre nedir",
        "açık devre nedir",
        "rezistans nedir",
        "indüktör nedir",
        "seri bağlantı nedir",
        "paralel bağlantı nedir",
        "ampermetre nedir",
        "volmetre nedir",
        "multimetre nedir",
        "enerji nedir",
        "bobin nedir",
        "trafonun görevi nedir",
        "kapasitans nedir",
        "empedans nedir",
        "faz farkı nedir",
        "aktif güç nedir",
        "reaktif güç nedir",
        "güç faktörü nedir",
        "eşdeğer direnç nedir",
        "eşdeğer endüktans nedir",
        "eşdeğer kapasitans nedir",
        "topraklama önemi nedir",
        "sigorta nedir",
        "devre kesici nedir",
        "voltaj düşümü nedir",
        "yük nedir",
        "kaynak nedir",
        "kondansatör nedir",
        "indüktans ölçümü nasıl yapılır",
        "rezistans ölçümü nasıl yapılır",
        "paralel devre özellikleri nelerdir",
        "seri devre özellikleri nelerdir",
        "kapasitör şarjı nasıl olur",
        "indüktör şarjı nasıl olur",
        "transistör tipi nedir",
        "pn diyot nedir",
        "led nedir",
        "fotosel nedir",
        "potansiyometre nedir",
        "röle nedir",
        "transformer nedir",
        "elektrik motoru nedir",
        "generatör nedir",
        "alternatör nedir",
        "topraklama türleri nelerdir",
        "faz nedir",
        "nötr nedir",
        "aktif nedir",
        "reaktif nedir",
        "empedans ölçümü nasıl yapılır",
        "kapasitör bağlama şekilleri nelerdir",
        "endüktör bağlama şekilleri nelerdir",
        "devre analizi nasıl yapılır",
        "kirchoff kanunları nelerdir",
        "voltaj kaynağı nedir",
        "akım kaynağı nedir",
        "ohmmetre nedir",
        "osiloskop nedir",
        "multimetre kullanımı nasıl olur",
        "akım yönü nasıl belirlenir",
        "gerilim yönü nasıl belirlenir",
        "seri paralel karışık devre nedir",
        "fazör diyagramı nedir",
        "rezonans nedir",
        "rezonans frekansı nedir",
        "gerilim bölücü nedir",
        "akım bölücü nedir",
        "yük dengelemesi nedir",
        "faz değişimi nedir",
        "kaynak empedansı nedir",
        "ara direnç nedir",
        "topraklama hatası nedir",
        "şebeke nedir",
        "enerji kaynağı nedir",
        "elektriksel güvenlik nedir",
        "isolasyon nedir",
        "sigorta seçimi nasıl yapılır",
        "devre elemanı nedir",
        "elektriksel direnç ölçümü nedir",
        "akım ölçümü nedir",
        "voltaj ölçümü nedir",
        "reaktif güç ölçümü nedir",
        "aktif güç ölçümü nedir",
        "güç ölçümü nasıl yapılır",
        "faz akımı nedir",
        "faz gerilimi nedir",
        "üç fazlı sistem nedir",
        "monofaz nedir",
        "tristör nedir",
        "triak nedir",
        "kontrol rölesi nedir",
        "termistör nedir",
        "fototransistör nedir",
        "sensör nedir",
        "anahtar nedir",
        "dijital multimetre nedir",
        "analog multimetre nedir",
        "osiloskop nedir",
        "gerçek güç nedir",
        "görünür güç nedir",
        "ortalama güç nedir",
        "rms nedir",
        "modülasyon nedir",
        "doğrultucu nedir",
        "mantık devreleri nedir",
        "mosfet nedir",
        "bjt nedir",
        "zener diyot nedir",
        "jonksiyon nedir",

    ],
    "cevap": [
        "Site şimdilik içerik olarak Devre Teorisi, Elektronik ve Sinyaller ve Sistemler olmak üzere üç ana başlığa ayrılmış durumdadır. Yan çubukta her dersin kendine özel listeleme alanında içeriklerini görebilirsiniz. Kullanmakta zorluk çektiğiniz sayfaların açıklama alanlarına ve örneklerine göz atmayı unutmayın!",

        "Merhaba! Hoş geldiniz ⚡",
        "Merhaba! Hoş geldiniz ⚡",
        "Ben gayet iyiyim, siz nasılsınız?",
        "Güzel! Ne sormak istersiniz?",
        "Nasıl yardımcı olabilirim?",
        "**Fazör**, bir sinüzoidal büyüklüğün genlik ve fazını temsil eden **karmaşık sayıdır.** Sitede fazörler hakkında işlemler yapabileceğiniz sayfayı arama çubuğu veya listeler yardımıyla kolayca bulabilirsiniz!",
        "**Kompanzasyon**, **reaktif gücü** dengeleyerek **güç faktörünü** iyileştirme işlemidir. Sitede kompanzasyon hakkında işlemler yapabileceğiniz sayfayı arama çubuğu veya listeler yardımıyla kolayca bulabilirsiniz!",
        "**Direnç**, elektrik akımına karşı gösterilen zorluktur. **Birimi Ohm’dur (Ω).** Sitede dirençler hakkında işlemler yapabileceğiniz sayfayı arama çubuğu veya listeler yardımıyla kolayca bulabilirsiniz!",
        "**Endüktans**, **akım değişimine karşı manyetik alan oluşturan** devre özelliğidir.",
        "**Kapasitör**, elektrik yükünü **depolayan** devre elemanıdır.",
        "**Transistör**, **akımı kontrol etmek ve yükseltmek için kullanılan** yarı iletken bir elemandır.",
        "**Diyot**, elektriği **tek yönde ileten** yarı iletken devre elemanıdır.",
        "**Ohm kanunu:** V = I * R, gerilim, akım ve direnç arasındaki ilişkiyi tanımlar.",
        "**AC (Alternatif Akım)**, yönü ve şiddeti **sürekli değişen** akımdır.",
        "**DC (Doğru Akım)**, yönü ve şiddeti **sabit olan** akımdır.",
        "**Voltaj**, iki nokta arasındaki **elektrik potansiyel farkıdır.**",
        "**Akım**, bir iletken boyunca **elektronların hareketidir.**",
        "**Güç**, birim zamanda yapılan **iş veya enerji transferidir.** Birimi Watt'tır (W).",
        "**Frekans,** bir sinyalin **saniyedeki salınım sayısıdır.**",
        "Görüşürüz 👋!",
        "**Topraklama**, elektrik devresini güvenli bir şekilde **toprak ile bağlama** işlemidir.",
        "**Kısa devre**, **düşük dirençli bir yol oluşması nedeniyle** akımın normalden fazla artmasıdır.",
        "**Açık devre**, devrede **akımın akmadığı** durumdur.",
        "**Rezistans**, devrede **akıma karşı gösterilen** zorluktur.",
        "**İndüktör**, manyetik alan oluşturarak **akım değişimlerine karşı direnç gösteren** elemandır.",
        "**Seri bağlantı**, elemanların **uç uca** bağlandığı bağlantı türüdür.",
        "**Paralel bağlantı**, elemanların **uçlarının karşılıklı** bağlandığı bağlantı türüdür.",
        "**Ampermetre**, devreden **geçen akımı ölçmek için** kullanılan cihazdır.",
        "**Volmetre**, iki nokta arasındaki **gerilimi ölçmek için** kullanılır.",
        "**Multimetre**, voltaj, akım ve direnç ölçebilen **çok amaçlı** ölçü cihazıdır.",
        "**Enerji**, **iş yapabilme** kapasitesidir ve birimi Joule’dür (J).",
        "**Bobin**, **endüktans** oluşturan sarılmış iletken elemandır.",
        "**Trafo**, ***voltajı artırmak veya azaltmak** için kullanılan elektromanyetik cihazdır. Sitede trafo hakkında işlemler yapabileceğiniz sayfayı arama çubuğu veya listeler yardımıyla kolayca bulabilirsiniz!",
        "**Kapasitans**, bir kondansatörün **yük depolama** yeteneğidir.",
        "**Empedans**, AC devrelerde **toplam direnç ve reaktansın birleşimidir.**",
        "**Faz farkı**, iki sinyal arasındaki **zaman veya açı farkıdır.**",
        "**Aktif güç**, **gerçek iş** yapan güçtür ve birimi Watt'tır (W). Sitede güç hakkında işlemler yapabileceğiniz sayfayı arama çubuğu veya listeler yardımıyla kolayca bulabilirsiniz!",
        "**Reaktif güç**, devrede **manyetik** ve elektrik alanlarda depolanan güçtür. Birimi VAR'dır. Sitede güç hakkında işlemler yapabileceğiniz sayfayı arama çubuğu veya listeler yardımıyla kolayca bulabilirsiniz!",
        "**Güç faktörü**, **aktif gücün görünür güce** oranıdır. Sitede güç hakkında işlemler yapabileceğiniz sayfayı arama çubuğu veya listeler yardımıyla kolayca bulabilirsiniz!",
        "**Eşdeğer direnç**, birden fazla direncin **tek bir direnç ile** aynı etkiyi göstermesidir. Sitede eşdeğer direnç hakkında işlemler yapabileceğiniz sayfayı arama çubuğu veya listeler yardımıyla kolayca bulabilirsiniz!",
        "**Eşdeğer endüktans**, birden fazla indüktörün **tek bir indüktörle** aynı etkiyi göstermesidir. Sitede eşdeğer endüktans hakkında işlemler yapabileceğiniz sayfayı arama çubuğu veya listeler yardımıyla kolayca bulabilirsiniz!",
        "**Eşdeğer kapasitans**, birden fazla kondansatörün **tek bir kondansatörle** aynı etkiyi göstermesidir. Sitede eşdeğer kondansatör hakkında işlemler yapabileceğiniz sayfayı arama çubuğu veya listeler yardımıyla kolayca bulabilirsiniz!",
        "**Topraklama önemi**, elektriksel **güvenlik** ve cihaz koruması içindir.",
        "**Sigorta**, **aşırı akımı** önleyen koruma elemanıdır.",
        "**Devre kesici**, devreyi **aşırı akımdan koruyan** otomatik cihazdır.",
        "**Voltaj düşümü**, bir iletken boyunca **oluşan gerilim** kaybıdır.",
        "**Yük**, bir devreye **bağlanan cihaz veya elemandır.**",
        "**Kaynak**, **elektrik enerjisi sağlayan** cihazdır.",
        "**Kondansatör**, enerji **depolayan** devre elemanıdır.",
        "**İndüktans ölçümü**, LCR metre veya **multimetre** ile yapılır.",
        "**Rezistans ölçümü**, **ohmmetre** ile yapılır.",
        "**Paralel devre özellikleri**, **gerilim sabittir** ve akımlar toplanır. Sitede bağlantı türüne göre akım gerilim sonuçları hakkında işlemler yapabileceğiniz sayfayı arama çubuğu veya listeler yardımıyla kolayca bulabilirsiniz! ",
        "**Seri devre özellikleri**, **akım sabittir** ve gerilimler toplanır. Sitede bağlantı türüne göre akım gerilim sonuçları hakkında işlemler yapabileceğiniz sayfayı arama çubuğu veya listeler yardımıyla kolayca bulabilirsiniz!",
        "**Kapasitör şarjı**, devreye **gerilim uygulandığında** gerçekleşir.",
        "**İndüktör şarjı**, **manyetik alan** oluşmasıyla gerçekleşir.",
        "**Transistör tipi**, **NPN** veya **PNP** olabilir.",
        "**PN diyot**, **P** ve **N** yarı iletkenlerin birleşmesiyle oluşur. Sitede diyotlar hakkında işlemler yapabileceğiniz sayfayı arama çubuğu veya listeler yardımıyla kolayca bulabilirsiniz!",
        "**LED**, ışık yayan diyottur.",
        "**Fotosel**, **ışığa duyarlı** sensördür.",
        "**Potansiyometre**, ayarlanabilir dirençtir.",
        "**Röle**, elektrik sinyaliyle mekanik devreyi kontrol eden cihazdır.",
        "**Transformer**, voltaj dönüştüren cihazdır.",
        "**Elektrik motoru**, elektrik enerjisini mekanik enerjiye çevirir.",
        "Generatör, mekanik enerjiyi elektrik enerjisine çevirir.",
        "Alternatör, AC üreten makinedir.",
        "Topraklama türleri, eş potansiyel ve güvenlik topraklamasıdır.",
        "Faz, AC devrede akım veya gerilim dalgasının bir bileşenidir.",
        "Nötr, devrede referans noktasıdır.",
        "Aktif, gerçek iş yapan güç bileşenidir.",
        "Reaktif, enerji depolayan güç bileşenidir.",
        "Empedans ölçümü, LCR metre veya hesaplama ile yapılır.",
        "Kapasitör bağlama şekilleri: seri ve paralel.",
        "Endüktör bağlama şekilleri: seri ve paralel.",
        "Devre analizi, akım ve gerilimlerin hesaplanmasıdır.",
        "Kirchoff kanunları, akım ve gerilim yasalarıdır.",
        "Voltaj kaynağı, sabit gerilim sağlayan cihazdır.",
        "Akım kaynağı, sabit akım sağlayan cihazdır.",
        "Ohmmetre, direnç ölçmek için kullanılan cihazdır.",
        "Osiloskop, AC veya DC sinyallerin zaman grafiğini gösterir.",
        "Multimetre kullanımı, voltaj, akım ve direnç ölçmek için yapılır.",
        "Akım yönü, pozitif yük akışı ile belirlenir.",
        "Gerilim yönü, referans noktaya göre belirlenir.",
        "Seri-paralel karışık devre, hem seri hem paralel eleman içerir. Sitede karmaşık topolojileriniz için işlemler hakkında işlemler yapabileceğiniz sayfayı arama çubuğu veya listeler yardımıyla kolayca bulabilirsiniz!",
        "Fazör diyagramı, sinyallerin büyüklük ve fazlarını gösterir.",
        "Rezonans, devrenin doğal frekansında maksimum akım veya gerilim oluşturmasıdır.",
        "Rezonans frekansı, devrenin doğal titreşim frekansıdır.",
        "Gerilim bölücü, gerilimi istenen oranda bölen devredir. Sitede gerilim bölücü hakkında işlemler yapabileceğiniz sayfayı arama çubuğu veya listeler yardımıyla kolayca bulabilirsiniz!",
        "Akım bölücü, akımı istenen oranda bölen devredir. Sitede akım bölücü hakkında işlemler yapabileceğiniz sayfayı arama çubuğu veya listeler yardımıyla kolayca bulabilirsiniz!",
        "Yük dengelemesi, fazlar arasında akımın dengelenmesidir.",
        "Faz değişimi, sinyalin zaman veya açı kaymasıdır.",
        "Kaynak empedansı, kaynağın iç direncidir.",
        "Ara direnç, devrede eklenen dirençtir.",
        "Topraklama hatası, yanlış bağlantı sonucu oluşur.",
        "Şebeke, elektrik dağıtım sistemi anlamına gelir.",
        "Enerji kaynağı, elektrik üretim ve iletim cihazıdır.",
        "Elektriksel güvenlik, cihaz ve insan korumasıdır.",
        "İzolasyon, devre elemanlarını birbirinden ayırmaktır.",
        "Sigorta seçimi, akım değerine göre yapılır.",
        "Devre elemanı, devreyi oluşturan temel parçadır.",
        "Elektriksel direnç ölçümü, ohmmetre ile yapılır.",
        "Akım ölçümü, ampermetre ile yapılır.",
        "Voltaj ölçümü, voltmetre ile yapılır.",
        "Reaktif güç ölçümü, VAR metre ile yapılır.",
        "Aktif güç ölçümü, Watt metre ile yapılır.",
        "Güç ölçümü, P, Q ve S hesaplamaları ile yapılır. Sitede güç hakkında işlemler yapabileceğiniz sayfayı arama çubuğu veya listeler yardımıyla kolayca bulabilirsiniz!",
        "Faz akımı, AC devrede akımın bir faz bileşenidir.",
        "Faz gerilimi, AC devrede gerilimin bir faz bileşenidir.",
        "Üç fazlı sistem, üç ayrı AC fazı içeren sistemdir.",
        "Monofaz, tek fazlı AC sistemdir.",
        "Tristör, tetikleme ile iletime geçen yarı iletken elemandır.",
        "Triak, AC devrelerde yön değiştiren tristördür.",
        "Kontrol rölesi, devreyi otomatik açıp kapayan cihazdır.",
        "Termistör, sıcaklığa duyarlı dirençtir.",
        "Fototransistör, ışığa duyarlı transistördür.",
        "Sensör, çevresel veriyi algılayan cihazdır.",
        "Anahtar, devreyi açıp kapamaya yarayan elemandır.",
        "Dijital multimetre, sayısal ölçüm yapan cihazdır.",
        "Analog multimetre, kadranlı ölçüm cihazıdır.",
        "Osiloskop, dalga şekillerini görselleştiren cihazdır.",
        "**Gerçek güç**, bir elektrik devresinde gerilimin akımla aynı fazdaki bileşeninin yaptığı ve ısı, ışık veya mekanik iş olarak **fiilen harcanan güçtür.**",
        "**Görünür güç**, AC bir devrede gerilim ile akımın etkin (RMS) değerlerinin çarpımıyla tanımlanan ve kaynaktan çekilen **toplam güç kapasitesini** ifade eden büyüklüktür.",
        "**Ortalama güç**, zamana bağlı olarak değişen anlık gücün bir periyot boyunca ortalaması alınarak elde edilen ve devrede **net enerji aktarımını** gösteren güçtür.",
        "**RMS (Root Mean Square)**, zamana bağlı bir büyüklüğün aynı ısıl etkiyi yapan **eşdeğer DC değerini** ifade eden etkin değeridir.",
        "**Modülasyon**, bir bilgi sinyalini iletebilmek için taşıyıcı bir sinyalin genlik, frekans veya fazının bilgiye göre değiştirilmesi işlemidir.",
        "**Doğrultucu**, alternatif akımı (AC) tek yönlü akıma (DC) çeviren elektronik devredir. Sitede doğrultucu devreler hakkında işlemler yapabileceğiniz sayfayı arama çubuğu veya listeler yardımıyla kolayca bulabilirsiniz!",
        "**Mantık devreleri**, dijital sistemlerde 0 ve 1 seviyelerini kullanarak mantıksal işlemler yapan ve karar verme işlevini gerçekleştiren elektronik devrelerdir.",
        "**MOSFET**, kapısına (gate) uygulanan gerilimle akım akışını kontrol eden, yüksek giriş empedanslı bir yarı iletken anahtarlama ve yükseltme elemanıdır.",
        "**BJT (Bipolar Jonksiyon Transistör)**, küçük bir taban akımıyla kollektör–emiter arasındaki büyük akımı kontrol eden, akım kontrollü bir yarı iletken elemandır.",
        "**Zener diyot**, ters yönde belirli bir gerilimde iletime geçerek devrede **gerilim regülasyonu ve referansı** sağlayan özel bir diyottur.",
        "**Jonksiyon**, yarı iletkenlerde p ve n tipi bölgelerin birleştiği, akımın davranışını belirleyen geçiş bölgesidir.",

    ]
}
import time

def typewriter_effect(text, speed=0.02):
    placeholder = st.empty()
    displayed_text = ""

    for char in text:
        displayed_text += char
        placeholder.markdown(displayed_text)
        time.sleep(speed)


# CSV oluştur

df = pd.DataFrame(data)
df.to_csv("faq.csv", index=False)

import streamlit as st
import pandas as pd
import re
from collections import Counter


# Sayfa ayarları

TITLE = 'ElektroXLab'
st.set_page_config(
    page_title=TITLE,
    page_icon="⚡",
    layout="wide",
)

st.title("💬 Bilgi Sohbeti")
st.caption("Temel soruları cevaplamaktadır.")

# CSV den bilgi tabanını oku

try:
    faq_df = pd.read_csv("faq.csv")
    faq_df["soru_lower"] = faq_df["soru"].str.lower()
except FileNotFoundError:
    st.error("❌")
    st.stop()


# Session state: mesaj geçmişi

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "asistan", "content": "Merhaba! Sadece Elektrik Elektronik Mühendisliği alanındaki temel soruları ve ElektroXLab hakkında sorularınızı cevaplayan bir sohbet asistanıyım! Site hakkında öğrenmek için 'Site' yazmanız yeterli!"}
    ]


# Önceki mesajları göster

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# tokenizasyon fonksiyonu

def tokenize(text):
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    return words

# En iyi cevabı bulma, benzerlik skoru tutarak

def find_best_match(prompt, faq_df):
    prompt_tokens = tokenize(prompt)
    best_score = 0
    best_answer = None
    suggestions = []

    for _, row in faq_df.iterrows():
        question_tokens = tokenize(row["soru_lower"])
        common_tokens = set(prompt_tokens) & set(question_tokens)
        score = sum([1 for t in common_tokens])
        if score > best_score:
            best_score = score
            best_answer = row["cevap"]
        if score > 0:
            suggestions.append((score, row["soru"]))

    # Öneriler: skor sırasına göre
    suggestions = sorted(suggestions, reverse=True)
    top_suggestions = [s[1] for s in suggestions[1:4]]  # en yakın 3 öneri

    return best_answer, top_suggestions


# Kullanıcı mesajını al

prompt = st.chat_input("Bir soru yazın...")

if prompt:
    # Kullanıcı mesajını göster
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # En iyi eşleşmeyi bul
    answer, suggestions = find_best_match(prompt, faq_df)
    if not answer:
        answer = "Bu konuda bir bilgim yok 🤔 Belki başka şekilde sorabilirsiniz."
    else:
        if suggestions:
            answer += f"\n\n💡 Belki şunlar da ilgini çekebilir: {', '.join(suggestions)}"

    # Asistan cevabını göster
    with st.chat_message("asistan"):
        typewriter_effect(answer, speed=0.02)
    st.session_state["messages"].append({"role": "asistan", "content": answer})

