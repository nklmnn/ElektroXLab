import streamlit as st
import os
import importlib.util

TITLE = 'ElektroXLab'
st.set_page_config(
    page_title=TITLE,
    page_icon="⚡",
    layout="wide",
)


import streamlit.components.v1 as components

st.title("📟 Wokwi Devre Simülatörü")

# Wokwi
components.iframe("https://wokwi.com/arduino/new", height=700, width=1100, scrolling=True)


with st.expander("Nedir, nasıl kullanılır?"):
   st.caption("Wokwi, laboratuvar ortamında kurduğunuz devrelerin aynısını kurabileceğiniz bir sanal ortamdır. Sayfa açıldığında karşınıza çıkan ilk ortamda solda bir kod ekranı ve sağda ise bir 'Arduino UNO' kartı görmektesiniz.")
   st.caption("Arduino kullanmayı biliyorsanız bağlantıları yapmak sizin için daha kolay olacak olsa da, hiç bilmediğiniz bir durumda en basit şekilde bu karttan nasıl faydalanacağınızı buradan öğrenebilirsiniz.")
   st.caption("Ekranda gördüğünüz mavi daire içindeki '+' işaretine basarak çıkan komponent listesinden eklemek istediğiniz komponente tıklayıp onun ekranınıza yerleşmesini sağlayabilirsiniz. Gerekli bağlantıları yaptığınızda ve devrenizin nasıl bir mantıkta çalışmasını istediğinizi yandaki 'sketch.io' penceresinde kodlayabilirsiniz. Yeşil daire içindeki oynatma tuşuna bastığınızda ise devreniz çalışmaya başlar.")
   st.caption("Bu simulasyonda basit bir devre için arduino kartı, devrelerinize evreceğiniz gerilim kaynağı ve topraklama bağlantsını yaptığınız soket olarak kullanılır. Yani laboratuvarda gerçeklediğiniz tüm devreleri sadece kaynak olarak UNO kartını kullanıp burada simüle edebilir ve bağlantılarınızdaki hataları gözlemleyebilir, bunun da ötesine geçecek örnekler yapabilirsiniz. Standart kütüphanesinde bulamadığınız komponentleri manuel olarak eklemenize de olanak sağlamaktadır. Bir LED ve bir dirençten oluşan breadboard üzerine basit bir devre örneğinin yapılış aşamaları aşağıdaki gibidir.")
   st.caption("***1- KOMPONENTLERİ BULMA***")
   st.caption("* Mavi daire içindeki'+' sembolüne basıp komponent menüsünü açınız. menüde aşağı kayarak 'Breadboard' başlığını bulunuz. Buradaki breadboardlardan istediğinizi seçebilirsiniz, üzerine tıkladığınızda ekranınıza gelir. Komponentleri ekranda istediğiniz yere sürükleyip bırakabilirsiniz.")
   st.caption("* Aynı menüden LED komponentini de bulup tıklayın. Ekranınıza gelen LED'in üzerine tıklayarak çıkan renk seçeneklerinden LED'inizin rengini değiştirebilirsiniz.")
   st.caption("* Yine aynı menüden direnç komponentini bulup üzerine tıklayınız, ekranınıza geldiğinde direncin üzerine tekrar tıklayarak direncin değerini girebilirsiniz. Bu örnekle 330 ohm'luk bir direnç kullanıldı. (Değer giriş kutusunun hemen yanındaki SI biriminin kastettiğiniz direnç değerine ait olduğundan emin olunuz.) Ekranınızdaki direnç girdiğiniz değerin renk kodlarına göre görünüşünü değiştirir.")
   st.caption("***2- KOMPONENTLERİN BAĞLANTISINI YAPMA***")
   st.caption("Öncelikle bir hatırlatma olarak, Breadboardın '+' ve '-' ile işaretlenmiş satırları hariç olan kısmında, komponentleri seri yapan şeyin komponentlerin bacaklarının aynı sütunda takılı olması olduğunu unutmayınız. bir satır boyuncaki deliklerde birbiriyle iletkenlik yoktur, ama bir sütun boyunca delikler iletken ve seridir. Bu nedenle hiçbir komponent sütun boyunca (Dik şekilde, iki bacağı da aynı sütunda olacak şekilde) takılamaz.")
   st.caption("* Direncinizi iki ucu breadboardınızdaki herhangi iki bağlantı yuvasına denk gelecek şekilde breadboarda yerleştirin. (Komponentleri döndürmek istiyorsanız 'Ctrl+R' yapmanız gerekmektedir, bu gömülü bir yazılım olduğundan 'Ctrl+R' komutu site tarafından 'Yeniden yükleme' isteği sanılabilir. Çıkan isteme 'iptal' demeniz yeterlidir. Komponentiniz ise zaten dönmüş durumda olacaktır.)")
   st.caption("* LED'inizi pozitif tarafı direnç ile aynı düğümde olacacak şekilde breadboarda takınız. (LED lerin '+' tarafının hafif bükülmüş taraf olduğunu unutmayınız.)")
   st.caption("* Direncin diğer ucuna tıklayın, bir kablo uzatması ortaya çıkacak, bu kablo uzatmasının diğer ucunu UNO kartın üst sırasında 13 numaralı sokete iliştirin.(Bu ucu direkt alt sıradaki 5V soketine de bağlayabilirdiniz fakat burası sabit 5V verdiği için kod ekranında çok müdahaleye açık değildir.)")
   st.caption("* LED'in negatif ucunu UNO kartının üst sırasındaki 'GND' olarak adlandırılımış sokete bağlayın, burası topraklama düğümüdür.")
   st.caption("***3- DEVRENİN ÇALIŞMA MANTIĞININ YAZILMASI***")
   st.caption("* Devreyi kurduğunuz ekranın hemen solundaki pencere, otomatik olarak 'sketch.io' seçili şekilde karşınıza gelir. Kod kısmını yazacağımız temel başlıklar da burada hali hazırda verilmiş olur.")
   st.caption("* 'void setup()' kısmı ayar kısmıdır, bu kısmın süslü parantezleri içine 'pinMode(13, OUTPUT);' yazılır. (Tırnak işaretleri dahil değildir.) Bu 13 numaralı pini çıkış olarak yani devreyi besleyecek kaynak olarak ayarladığımız anlamına gelir.")
   st.caption("* 'void loop()' kısmı ise devrede yaşanacak döngünün tanımlandığı kısımdır. Bu kısmın süslü parantezleri içine ise şu satırlar yazılmalıdır:")
   st.caption("digitalWrite(13,HIGH); //LED yanar.")
   st.caption("delay(1000); //Yanma süresi 1 saniye sürer.")
   st.caption("digitalWrite(13,LOW); //LED söner")
   st.caption("delay(1000); //1 saniye boyunca sönük kalır.")
   st.caption("* Şimdi yeşil daire içindeki oynatma tuşuna bastığınızda devrenizin yaptığınız işlemlere göre çalıştığını görebilirsiniz. Simülasyonu istediğinizde durdurabilirsiniz.")
   st.caption("Ek Bilgi: Breadboard'da veyahut UNO kartındaki herhangi bir deliğe tıkladığınızda da kablo uzatma seçeneği çıkar, kabloyu yanlış bir yere bağladıysanız kablonun üzerine tıklayıp çıkan seçeneklerden çöp kutusu simgesine basıp silebilir, yanlış bir kablo çıkışı yapmış fakat henüz bir yere bağlamamışsanız sağ tık ile kabloyu yok edebilirsiniz. Kablolarınızı takip etmeyi kolaylaştırmak ve birbirinden ayrıt etmek için kablonun üzerine tıklayıp rengini değiştirebilirsiniz. Kablonuzun belirli yerlerden bir kırılma ile dönüş yapmasını istiyorsanız uzakmaya başladığınız kabloyu bir sokete bağlamadan önce ekranda kırılma yapmasını istediğiniz noktada tıklayın, kablonun şekil alacağını göreceksiniz. '//' ile başlayan kısımlar yorum satırıdır, açıklama için eklenmiştir, koda dahil değildir. Satır başlarındaki girintilerin hizzasına ve süslü parantezlerin içinde olmaya dikkat ediniz.")
   with st.expander("Tarif edilen devrenin ekran görüntüsü"):
        st.image("pages/images/img_1.png");

st.caption("Bu simülasyon aracı açık kaynak kodlu ve eğitim amaçlı siteye gömülmüş bir araçtır. Daha ayrıntılı bilgi için sitenin kendisini ziyaret ediniz.")
