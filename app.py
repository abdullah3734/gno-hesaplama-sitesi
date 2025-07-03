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
    if request.method == 'POST':
        try:
            ders_sayisi = int(request.form.get('ders_sayisi'))
            if ders_sayisi > 0:
                return render_template('ders_formu.html', ders_sayisi=ders_sayisi)
        except (ValueError, TypeError):
            pass
    return render_template('anasayfa.html')

# Hesaplama sonuçlarının gösterileceği sayfa
@app.route('/hesapla', methods=['POST'])
def hesapla():
    dersler = []
    toplam_kredi = 0
    toplam_agirlikli_not = 0
    
    ders_sayisi = int(request.form.get('ders_sayisi'))

    for i in range(ders_sayisi):
        ders_adi = request.form.get(f'ders-{i}-ad', f'İsimsiz Ders {i+1}')
        kredi = float(request.form.get(f'ders-{i}-kredi', '0'))
        
        bilesen_notlari = request.form.getlist(f'ders-{i}-bilesen-not')
        bilesen_yuzdeleri = request.form.getlist(f'ders-{i}-bilesen-yuzde')

        ders_toplam_notu = 0
        ders_toplam_yuzdesi = 0
        
        for not_str, yuzde_str in zip(bilesen_notlari, bilesen_yuzdeleri):
            notu = float(not_str)
            yuzde = float(yuzde_str)
            ders_toplam_notu += notu * (yuzde / 100)
            ders_toplam_yuzdesi += yuzde
        
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
        
        if gecerli_ders:
            toplam_kredi += kredi
            toplam_agirlikli_not += kredi * katsayi
            
    gno = toplam_agirlikli_not / toplam_kredi if toplam_kredi > 0 else 0
    
    return render_template('sonuc.html', dersler=dersler, gno=round(gno, 2))

# Sunucuyu başlatan blok
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
