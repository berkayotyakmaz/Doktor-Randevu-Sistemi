# backend.py - Veri Modelleri ve Randevu Mantığı

# Sisteme kayıt olacak hastaların temel bilgilerini tutan sınıf
class Hasta:
    def __init__(self, hasta_id, ad, tc, telefon):
        self.hasta_id = hasta_id    # Benzersiz hasta numarası
        self.ad = ad                # Ad Soyad
        self.tc = tc                # T.C. Kimlik Numarası
        self.telefon = telefon      # İletişim numarası

# Doktor bilgilerini ve çalışma saatlerini yöneten sınıf
class Doktor:
    def __init__(self, doktor_id, ad, uzmanlik):
        self.doktor_id = doktor_id  # Benzersiz doktor numarası
        self.ad = ad                # Doktorun adı
        self.uzmanlik = uzmanlik    # Uzmanlık alanı (Örn: Kalp Cerrahisi)
        # Her doktor için varsayılan boş randevu saatleri
        self.uygun_saatler = ["09:00", "10:00", "11:00", "14:00", "15:00"]

    # Seçilen saatin hala müsait olup olmadığını kontrol eder
    def uygunluk_kontrol(self, saat):
        return saat in self.uygun_saatler

    # Randevu alındığında seçilen saati listeden çıkarır
    def randevu_saatini_kullan(self, saat):
        if saat in self.uygun_saatler:
            self.uygun_saatler.remove(saat)
    
    # Randevu iptal edildiğinde saati tekrar müsait listesine ekler ve sıralar
    def saati_iade_et(self, saat):
        self.uygun_saatler.append(saat)
        self.uygun_saatler.sort()

# Hasta ve Doktoru bir araya getiren randevu kayıt sınıfı
class Randevu:
    sayac = 1 # Tüm randevular için otomatik artan ID sayacı

    def __init__(self, tarih, saat, doktor, hasta):
        self.randevu_id = Randevu.sayac # Statik sayaçtan ID ata
        Randevu.sayac += 1
        self.tarih = tarih
        self.saat = saat
        self.doktor = doktor # Doktor nesnesi referansı
        self.hasta = hasta   # Hasta nesnesi referansı

    # Listenin arayüzde nasıl görüneceğini belirleyen metin formatı
    def randevu_bilgi(self):
        return f"ID:{self.randevu_id} | {self.hasta.ad} -> {self.doktor.ad} | Saat: {self.saat}"