# doktor_randevu.py - Arayüz (Frontend)

import tkinter as tk
from tkinter import ttk, messagebox
from DoktorRandevu_Backend import Hasta, Doktor, Randevu

# ===== MODERN ARAYÜZ SİSTEMİ =====
class ModernRandevuApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hospital Management Dashboard")
        self.geometry("950x650")
        self.configure(bg="#0b111b")

        self.bg_color = "#0b111b"
        self.card_color = "#162031"
        self.accent_color = "#3498db"
        self.text_color = "#ffffff"

        self.doktorlar = [
            Doktor(1, "Dr. Ahmet Yılmaz", "Kardiyoloji"),
            Doktor(2, "Dr. Elif Kaya", "Göz Hastalıkları"),
            Doktor(3, "Dr. Can Demir", "Dahiliye"),
            Doktor(4, "Dr. Yaren Taşkala", "Kalp ve Damar Cerrahisi"),
            Doktor(5, "Dr. Lujayen Ajahar", "Beyin Cerrahisi")
        ]
        
        self.randevular = []  # Aktif randevu nesnelerini tutan liste
        self.hasta_sayac = 1  # Yeni hastalar için otomatik ID

        # UI bileşenlerini başlat
        self.arayuz_olustur()

    def arayuz_olustur(self):
        # --- Üst Bilgi Paneli (Header) ---
        header = tk.Frame(self, bg=self.bg_color, padx=20, pady=20)
        header.pack(fill="x")
        tk.Label(header, text="DASHBOARD", font=("Segoe UI", 24, "bold"), fg=self.text_color, bg=self.bg_color).pack(side="left")
        tk.Label(header, text="Randevu Kayıt Sistemi — Otomatik Güncelleme", font=("Segoe UI", 10), fg="#6b7c93", bg=self.bg_color).place(x=5, y=45)

        # --- Ana İçerik Alanı ---
        main_container = tk.Frame(self, bg=self.bg_color)
        main_container.pack(fill="both", expand=True, padx=20)

        # --- Sol Panel: Yeni Randevu Giriş Formu ---
        form_card = tk.Frame(main_container, bg=self.card_color, padx=20, pady=20, highlightthickness=1, highlightbackground="#253347")
        form_card.place(relx=0, rely=0, relwidth=0.42, relheight=0.95)

        tk.Label(form_card, text="YENİ RANDEVU KAYDI", font=("Segoe UI", 12, "bold"), fg=self.accent_color, bg=self.card_color).pack(anchor="w", pady=(0,20))

        self.create_label_entry(form_card, "Hasta Ad Soyad:", "ent_ad")
        self.create_label_entry(form_card, "T.C. Kimlik:", "ent_tc")
        self.create_label_entry(form_card, "Telefon:", "ent_tel")

        # Doktor Seçim Kutusu (Combobox)
        tk.Label(form_card, text="Doktor Seçimi:", fg="#6b7c93", bg=self.card_color).pack(anchor="w", pady=(10,0))
        self.cmb_doktor = ttk.Combobox(form_card, values=[f"{d.ad} ({d.uzmanlik})" for d in self.doktorlar], state="readonly")
        self.cmb_doktor.pack(fill="x", pady=5)
        self.cmb_doktor.bind("<<ComboboxSelected>>", self.saatleri_guncelle) # Doktor değişince saatleri yenile

        # Saat Seçim Listesi (Listbox)
        tk.Label(form_card, text="Uygun Saatler:", fg="#6b7c93", bg=self.card_color).pack(anchor="w", pady=(10,0))
        self.saat_listesi = tk.Listbox(form_card, bg="#0b111b", fg="white", borderwidth=0, highlightthickness=1, highlightbackground="#253347", selectbackground=self.accent_color)
        self.saat_listesi.pack(fill="both", expand=True, pady=10)

        tk.Button(form_card, text="RANDEVU OLUŞTUR", command=self.randevu_olustur, bg=self.accent_color, fg="white", font=("Segoe UI", 10, "bold"), borderwidth=0, cursor="hand2", pady=10).pack(fill="x")

        # --- Sağ Panel: Aktif Randevuları Görüntüleme Listesi ---
        list_card = tk.Frame(main_container, bg=self.card_color, padx=20, pady=20, highlightthickness=1, highlightbackground="#253347")
        list_card.place(relx=0.45, rely=0, relwidth=0.55, relheight=0.95)

        tk.Label(list_card, text="AKTİF RANDEVU SİSTEMİ", font=("Segoe UI", 12, "bold"), fg="#2ecc71", bg=self.card_color).pack(anchor="w", pady=(0,10))
        tk.Label(list_card, text="* Detay ve İptal için randevuya tıklayın.", font=("Segoe UI", 8, "italic"), fg="#6b7c93", bg=self.card_color).pack(anchor="w", pady=(0,10))
        
        # Randevuların listelendiği alan
        self.lb_aktif_randevular = tk.Listbox(list_card, bg="#0b111b", fg="#bdc3c7", borderwidth=0, font=("Consolas", 10), highlightthickness=1, highlightbackground="#253347", selectbackground="#e74c3c")
        self.lb_aktif_randevular.pack(fill="both", expand=True)
        self.lb_aktif_randevular.bind("<Double-Button-1>", self.randevu_detay_penceresi) # Çift tıklayınca detayı aç

    # Form alanları için yardımcı fonksiyon (Etiket + Giriş Kutusu oluşturur)
    def create_label_entry(self, parent, label_text, attr_name):
        tk.Label(parent, text=label_text, fg="#6b7c93", bg=self.card_color).pack(anchor="w")
        entry = tk.Entry(parent, bg="#0b111b", fg="white", insertbackground="white", borderwidth=0, highlightthickness=1, highlightbackground="#253347")
        entry.pack(fill="x", pady=(0, 10), ipady=5)
        setattr(self, attr_name, entry)

    # Seçilen doktora göre müsait saatleri Listbox'a yükler
    def saatleri_guncelle(self, event=None):
        idx = self.cmb_doktor.current()
        if idx != -1:
            doktor = self.doktorlar[idx]
            self.saat_listesi.delete(0, tk.END)
            for s in doktor.uygun_saatler:
                self.saat_listesi.insert(tk.END, s)

    # Formdaki verileri alıp yeni randevu oluşturur
    def randevu_olustur(self):
        # Girişleri al
        ad = self.ent_ad.get()
        tc = self.ent_tc.get()
        tel = self.ent_tel.get()
        idx = self.cmb_doktor.current()
        saat_sec = self.saat_listesi.curselection()

        if not (ad and tc and tel and idx != -1 and saat_sec):
            messagebox.showwarning("Hata", "Lütfen tüm hasta bilgilerini doldurup saat seçin.")
            return

        doktor = self.doktorlar[idx]
        saat = self.saat_listesi.get(saat_sec)

        # Arka planda uygunluk kontrolü yap
        if doktor.uygunluk_kontrol(saat):
            # Saati doktordan rezerve et
            doktor.randevu_saatini_kullan(saat)
            # Nesneleri oluştur
            yeni_hasta = Hasta(self.hasta_sayac, ad, tc, tel)
            yeni_randevu = Randevu("06.05.2026", saat, doktor, yeni_hasta)
            
            self.randevular.append(yeni_randevu) # Listeye ekle
            self.hasta_sayac += 1
            
            # Formu temizle ve listeyi anında güncelle
            self.ent_ad.delete(0, tk.END)
            self.ent_tc.delete(0, tk.END)
            self.ent_tel.delete(0, tk.END)
            self.liste_guncelle()
            self.saatleri_guncelle()
            messagebox.showinfo("Başarılı", "Randevu başarıyla sisteme eklendi.")
        else:
            messagebox.showerror("Hata", "Bu saat artık uygun değil.")

    # Sağ taraftaki randevu listesini görsel olarak yeniler
    def liste_guncelle(self):
        self.lb_aktif_randevular.delete(0, tk.END)
        for r in self.randevular:
            self.lb_aktif_randevular.insert(tk.END, r.randevu_bilgi())

    # Mevcut randevuya çift tıklandığında açılan küçük pencere
    def randevu_detay_penceresi(self, event):
        secili_index = self.lb_aktif_randevular.curselection()
        if not secili_index:
            return
        
        randevu = self.randevular[secili_index[0]]
        
        # Detay Penceresi (Popup)
        detay_penceresi = tk.Toplevel(self)
        detay_penceresi.title("Randevu Detayı")
        detay_penceresi.geometry("350x300")
        detay_penceresi.configure(bg=self.card_color)

        bilgi_metni = (
            f"--- RANDEVU BİLGİLERİ ---\n\n"
            f"Hasta: {randevu.hasta.ad}\n"
            f"TC: {randevu.hasta.tc}\n"
            f"Tel: {randevu.hasta.telefon}\n"
            f"Doktor: {randevu.doktor.ad}\n"
            f"Saat: {randevu.saat}\n"
            f"Tarih: {randevu.tarih}"
        )

        # Detay metni
        tk.Label(detay_penceresi, text=bilgi_metni, bg=self.card_color, fg="white", font=("Segoe UI", 10), justify="left").pack(pady=20)
        
        # İptal butonu
        tk.Button(detay_penceresi, text="RANDEVUYU İPTAL ET", bg="#e74c3c", fg="white", 
                  command=lambda: self.randevu_iptal_et(secili_index[0], detay_penceresi), 
                  font=("Segoe UI", 9, "bold"), padx=10, pady=5).pack(pady=10)

    # Randevuyu silen ve saati iade eden fonksiyon
    def randevu_iptal_et(self, index, pencere):
        soru = messagebox.askyesno("İptal Onayı", "Bu randevuyu iptal etmek istediğinize emin misiniz?")
        if soru:
            randevu = self.randevular.pop(index) # Listeden çıkar
            randevu.doktor.saati_iade_et(randevu.saat) # Saati doktora geri ver
            
            self.liste_guncelle()
            self.saatleri_guncelle()
            pencere.destroy()
            messagebox.showinfo("İptal Edildi", "Randevu iptal edildi ve saat boşa çıktı.")

if __name__ == "__main__":
    app = ModernRandevuApp()
    app.mainloop()