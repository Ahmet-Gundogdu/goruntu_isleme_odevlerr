# -*- coding: utf-8 -*-

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# 1) Görüntüyü gri seviyeye dönüştürür
def renkten_griye_donustur(resim):
    return cv2.cvtColor(resim, cv2.COLOR_BGR2GRAY)

# 2) Görüntüde sadece pirinçlerin kalması için eşikleme yapar
def esikleme(resim, esik_degeri=120):
    _, esiklenmis = cv2.threshold(resim, esik_degeri, 255, cv2.THRESH_BINARY)
    return esiklenmis

# 3) Eşikleme sonucunda kalabilecek istenmeyen arka planlar için morfolojik işlemler
def morfolojik_islemler(resim):
    kernel = np.ones((1, 1), np.uint8)
    # Kapatma işlemi uygula (genişletme sonra erozyon)
    morfolojik_resim = cv2.morphologyEx(resim, cv2.MORPH_CLOSE, kernel)
    return morfolojik_resim

# 4) Sayma ve etiketleme fonksiyonları
def nesne_say_ve_etiketle(resim, alan_esigi=100):
    # Contour (sınırlayıcı çizgi) bulma işlemi
    konturlar, _ = cv2.findContours(resim, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Her bir kontur için bir döngü ve pirinç sayma işlemi
    pirinc_sayisi = 0
    for kontur in konturlar:
        # Kontur alanını hesapla
        alan = cv2.contourArea(kontur)
        
        # Belirli bir alan eşiğinden büyük konturları say
        if alan > alan_esigi:
            pirinc_sayisi += 1
            
            # Pirinçlere Konturu orijinal görüntü üzerine çiz
            cv2.drawContours(img, [kontur], -1, (0, 255, 0), 2)
            
            # Konturun etrafına kırmızı dikdörtgen çiz
            x, y, w, h = cv2.boundingRect(kontur)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)

    return pirinc_sayisi

# Dosya yolu alma
tam_yol = os.path.realpath(__file__)
klasor, dosya_adi = os.path.split(tam_yol)

# Fotoğrafı okuma
resim_yolu = klasor + '\\' + 'pirincler2.jpg'  

img = cv2.imread(resim_yolu)
if img is None:
    print(f"Hata: Görüntü okunamadı. Dosya yolunu kontrol edin: {resim_yolu}")
    exit()

# 1) Görüntüyü gri seviyeye dönüştür
gri_resim = renkten_griye_donustur(img)

# 2) Görüntüde sadece pirinçlerin kalması için eşikleme
esiklenmis_resim = esikleme(gri_resim)

# 3) Eşikleme sonucunda kalabilecek istenmeyen arka planlar için morfolojik işlemler
morfolojik_resim = morfolojik_islemler(esiklenmis_resim)

# 4) Sayma ve etrafını 
pirinc_sayisi = nesne_say_ve_etiketle(morfolojik_resim)

# Sayımı Yapılanların görüntüsü
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Sayımı Yapılanların Görüntüsü')

# İşlenmiş görüntü
plt.subplot(1, 2, 2)
plt.imshow(morfolojik_resim, cmap='gray')
plt.title('İşlenmiş Görüntü')

# Sonuçları göster
print(">>>> Pirinç Sayısı: " + str(pirinc_sayisi) +" <<<<")
plt.show()
