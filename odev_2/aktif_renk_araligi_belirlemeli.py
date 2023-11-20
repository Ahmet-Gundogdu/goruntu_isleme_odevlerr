import cv2
import numpy as np
import json
import os
#from matplotlib import pyplot as plt

def nothing(x):
    pass

def main():
    #Dosya yolu alma işlemleri
    full_path = os.path.realpath(__file__)
    path, filename = os.path.split(full_path)
    
    # Video girişi için kamera tanımlaması
    cap = cv2.VideoCapture(0)
    
    #Kayıtlı arayarlı çekme
    with open(path+'\\settings'+'\\'+'low_ayar.json',) as f:
        lower_colors_sett = json.load(f)
    with open(path+'\\settings'+'\\'+'up_ayar.json') as f:
        upper_colors_sett = json.load(f)
    # lower_colors_sett = {
    # 'a1': 0,
    # 'a2': 180,
    # 'a3': 20
    # }
    # upper_colors_sett = {
    # 'b1': 10,
    # 'b2': 255,
    # 'b3': 255
    # }
    
    #pencere isimlendirmesi
    window_name='Renk Parametreleri Ayarlama'
    cv2.namedWindow(window_name)
    

    # print ('lower_color = np.array([a1,a2,a3])')
    # print ('upper_color = np.array([b1,b2,b3])')


    # renk değişimi için kaydırma çubukları (trackbar) oluşturma
    cv2.createTrackbar('a1',window_name,lower_colors_sett['a1'],255,nothing)
    cv2.createTrackbar('a2',window_name,lower_colors_sett['a2'],255,nothing)
    cv2.createTrackbar('a3',window_name,lower_colors_sett['a3'],255,nothing)

    cv2.createTrackbar('b1',window_name,upper_colors_sett['b1'],255,nothing)
    cv2.createTrackbar('b2',window_name,upper_colors_sett['b2'],255,nothing)
    cv2.createTrackbar('b3',window_name,upper_colors_sett['b3'],255,nothing)

    while True:
         # Giriş karesini okuma
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        lower_colors_sett['a1'] = cv2.getTrackbarPos('a1',window_name)
        lower_colors_sett['a2'] = cv2.getTrackbarPos('a2',window_name)
        lower_colors_sett['a3'] = cv2.getTrackbarPos('a3',window_name)

        upper_colors_sett['b1'] = cv2.getTrackbarPos('b1',window_name)
        upper_colors_sett['b2'] = cv2.getTrackbarPos('b2',window_name)
        upper_colors_sett['b3'] = cv2.getTrackbarPos('b3',window_name)

        # hsv hue değerlerini ayarlama
        lower_color = np.array([lower_colors_sett['a1'],lower_colors_sett['a2'],lower_colors_sett['a3']])
        upper_color = np.array([upper_colors_sett['b1'],upper_colors_sett['b2'],upper_colors_sett['b3']])
        mask = cv2.inRange(hsv, lower_color, upper_color)
        res = cv2.bitwise_and(frame, frame, mask = mask)
        
        #pencereleri gösterme
        cv2.imshow('mask',mask)
        cv2.imshow('res',res)
        #Foto üstüne yazı ekleme
        cv2.putText(frame, 'Cikmak icin "ESC", Ayarlari ve ekran goruntusunu kaydedip cikmak icin "S" tusuna basin.', (0,20), 3,  0.4, (255, 255, 255))
        cv2.imshow(window_name,frame)

         #Kapatmak veya kaydedip kapatmak için gerekli işlemler.
        k = cv2.waitKey(1) & 0xFF
        if k == 27:         # Çıkış için 'ESC' girişi beklemesi
            break
        elif k == ord('s'): # Kaydetmek için 'S' girişi beklemesi
            
            cv2.imwrite(path+'\\screen_shots'+'\\'+'Img_screen_mask.jpg',mask)
            cv2.imwrite(path+'\\screen_shots'+'\\'+'Img_screen_res.jpg',res)
            
                # JSON'a ayrı ayrı kaydetme
            
            with open(path+'\\settings'+'\\'+'low_ayar.json', 'w') as json_dosya:
                json.dump(lower_colors_sett, json_dosya)
            with open(path+'\\settings'+'\\'+'up_ayar.json', 'w') as json_dosya:
                json.dump(upper_colors_sett, json_dosya)
            break
    
        
    # Kamera kullanımını kapatma    
    cap.release()
    # Pencereleri kapatma
    cv2.destroyAllWindows()
    
# Main metodunu çalıştırma
if __name__ == "__main__" :
    main()