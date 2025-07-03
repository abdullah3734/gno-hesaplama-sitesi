# Gerekli kütüphaneleri ve fonksiyonları içeri aktarıyoruz
from flask import Flask, render_template, request

# Flask uygulamamızı oluşturuyoruz
app = Flask(__name__)

# Puanı harf notuna ve 4'lük sistemdeki karşılığına çeviren fonksiyon
def harf_notu_hesapla(puan):
    if puan >= 91: return "AA", 4.00
    elif puan >= 81: return "BA", 3.75
    elif puan >= 71: return "BB", 3.50
    elif puan >= 61: return "CB", 3.00
    elif puan >= 51: return "CC", 2.50
    elif puan >= 41: return "CD", 2.00
    elif puan >= 36: return "DD", 1.50
    elif puan >= 31: return "DF", 1.00
    else: return "FF", 0.00

# Ana sayfa: Ders sayısını soran formun gösterildiği yer
@app.route('/', methods=['GET', 'POST'])
def anasayfa():
    # Eğer kullanıcı form gönderdiyse (POST metoduyla)
    if request.method == 'POST':
        try:
            # Formdan ders sayısını alıp tam sayıya çevir
            ders_sayisi = int(request.form.get('ders_sayisi'))
            # Eğer ders sayısı 0'dan büyükse, ders bilgilerinin girileceği formu göster
            if ders_sayisi > 0:
                return render_template('ders_formu.html', ders_sayisi=ders_sayisi)
        except (ValueError, TypeError):
            # Eğer kullanıcı sayı girmemişse bir şey yapma, ana sayfada kal
            pass
    # Eğer sayfa ilk defa açılıyorsa (GET metoduyla) veya formda hata varsa, ana sayfayı göster
    return render_template('anasayfa.html')

# Hesaplama sonuçlarının gösterileceği sayfa
@app.route('/hesapla', methods=['POST'])
def hesapla():
    dersler = []
    toplam_kredi = 0
    toplam_agirlikli_not = 0
    
    ders_sayisi = int(request.form.get('ders_sayisi'))

    # Her bir ders için formdan verileri çek
    for i in range(ders_sayisi):
        ders_adi = request.form.get(f'ders-{i}-ad', f'İsimsiz Ders {i+1}')
        kredi = float(request.form.get(f'ders-{i}-kredi', '0'))
        
        # Dinamik olarak eklenen bileşenleri liste olarak al
        bilesen_notlari = request.form.getlist(f'ders-{i}-bilesen-not')
        bilesen_yuzdeleri = request.form.getlist(f'ders-{i}-bilesen-yuzde')

        ders_toplam_notu = 0
        ders_toplam_yuzdesi = 0
        
        # Her dersin kendi bileşenlerini hesapla
        for not_str, yuzde_str in zip(bilesen_notlari, bilesen_yuzdeleri):
            notu = float(not_str)
            yuzde = float(yuzde_str)
            ders_toplam_notu += notu * (yuzde / 100)
            ders_toplam_yuzdesi += yuzde
        
        # Yüzdelerin toplamı 100 değilse veya kredi 0'dan küçükse dersi geçersiz say
        gecerli_ders = True
        if round(ders_toplam_yuzdesi) != 100:
            harf, katsayi = "Geçersiz Yüzde", 0.0
            gecerli_ders = False
        else:
            harf, katsayi = harf_notu_hesapla(ders_toplam_notu)
        
        if kredi <= 0:
            gecerli_ders = False

        dersler.append({
            'ad': ders_adi,
            'kredi': kredi,
            'son_not': round(ders_toplam_notu, 2),
            'harf': harf,
            'katsayi': katsayi
        })
        
        # Sadece geçerli dersleri GNO hesabına kat
        if gecerli_ders:
            toplam_kredi += kredi
            toplam_agirlikli_not += kredi * katsayi
            
    # GNO'yu hesapla
    gno = toplam_agirlikli_not / toplam_kredi if toplam_kredi > 0 else 0
    
    # Sonuçları göstermek için sonuc.html'yi render et
    return render_template('sonuc.html', dersler=dersler, gno=round(gno, 2))

# Bu kodun doğrudan çalıştırıldığından emin olan ve sunucuyu başlatan blok
# Eğer bu blok olmazsa, sunucu başlamaz!
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)