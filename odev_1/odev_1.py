
import cv2
import os
from matplotlib import pyplot as plt

#Dosya yolu alma
full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)

def main():
    #resim dosyasını açıp okuma
    image = cv2.imread(path+'\\'+'doga.jpg', cv2.IMREAD_GRAYSCALE)

    # Histogramı saklamak için bir dizi oluşturun
    histogram = [0] * 256

    # Görüntüyü dönerek histogramı hesaplayın
    for row in image:
        for pixel_value in row:
            histogram[pixel_value] += 1

    # Histogramı ekrana yazdırın
    for i, count in enumerate(histogram):
        print(f'Piksel değeri {i}: {count} piksel')
        
    #Histogramın grafiğini çizme matplotlib ile
    plt.plot(histogram)
    plt.show()
    
if __name__ == "__main__" :
    main()