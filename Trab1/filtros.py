from matplotlib import pyplot as plt
import cv2
import numpy as np
from PyQt5.QtWidgets import QMessageBox
import matplotlib
matplotlib.use('Qt5Agg')  # Configuração do backend


def threshold_filter(image, threshold_value):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh_image = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)
    return thresh_image

def grayscale_filter(image):   
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
def highPass_filter(image):  
    kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    high_pass_image = cv2.filter2D(image, -1, kernel)
    return high_pass_image

def lowPass_filter(image, kernel):
    return cv2.blur(image, (kernel, kernel))

def median_filter(image, kernel):
    return cv2.medianBlur(image, kernel)

def roberts_filter(image):

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Aplicar o filtro de Roberts
    kernel_x = np.array([[1, 0], [0, -1]], dtype=int)
    kernel_y = np.array([[0, 1], [-1, 0]], dtype=int)
    
    roberts_x = cv2.filter2D(image, -1, kernel_x)
    roberts_y = cv2.filter2D(image, -1, kernel_y)
    
    # Usando NumPy para calcular a magnitude do gradiente
    roberts_image = np.sqrt(np.square(roberts_x) + np.square(roberts_y))
    roberts_image = np.uint8(roberts_image)
    
    return roberts_image

def prewitt_filter(image): 

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Aplicar o filtro de Prewitt
    kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=int)
    kernel_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=int)
    
    prewitt_x = cv2.filter2D(image, -1, kernel_x)
    prewitt_y = cv2.filter2D(image, -1, kernel_y)
    
    # Usando NumPy para calcular a magnitude do gradiente
    prewitt_image = np.sqrt(np.square(prewitt_x) + np.square(prewitt_y))
    prewitt_image = np.uint8(prewitt_image)
    
    return prewitt_image

def sobel_filter(image): 
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Aplicar o filtro de Sobel
    kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=int)
    kernel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype=int)
    
    sobel_x = cv2.filter2D(image, -1, kernel_x)
    sobel_y = cv2.filter2D(image, -1, kernel_y)
    
    # Usando NumPy para calcular a magnitude do gradiente
    sobel_image = np.sqrt(np.square(sobel_x) + np.square(sobel_y))
    sobel_image = np.uint8(sobel_image)
    
    return sobel_image
           
def LoG_filter(image): 
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    LoG_image = cv2.GaussianBlur(image, (5, 5), 0) 
    LoG_image = cv2.Laplacian(LoG_image,  cv2.CV_64F)
    LoG_image = cv2.convertScaleAbs(LoG_image)
    
    return LoG_image

def apply_zerocross_auxiliar(image):
    zero_crossings = np.zeros_like(image, dtype=np.uint8)
    rows, cols = image.shape
    
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            # Verificar vizinhos para cruzamento de zero
            if (image[i, j] * image[i + 1, j] < 0 or  # Vertical
            image[i, j] * image[i, j + 1] < 0): # Diagonal secundária
                zero_crossings[i, j] = 255  # Marca o pixel como borda
        
    return zero_crossings

def zerocross_filter(image): 
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image =  cv2.GaussianBlur(gray_image, (5, 5), 0) 
    log_image = cv2.Laplacian(blurred_image, cv2.CV_64F)
    zeroCrossing_image = apply_zerocross_auxiliar(log_image)
    
    return zeroCrossing_image

def salt_and_pepper_filter(image, mask_value): 
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    salt_mask = np.random.rand(*gray_image.shape) < mask_value
    gray_image[salt_mask] = 255
    pepper_mask = np.random.rand(*gray_image.shape) < mask_value
    gray_image[pepper_mask] = 0
    return gray_image

def watershed_filter(image): 
   
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, 0.5 * dist_transform.max(), 255, cv2.THRESH_BINARY)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0
    markers = cv2.watershed(image, markers)
    image[markers == -1] = [255,0,0]
    
    return image
   

def counting_objects_filters(image):
   
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_image = cv2.GaussianBlur(gray_image, (11, 11), 0)
    canny_image = cv2.Canny(blur_image, 30, 150)
    dilated_image = cv2.dilate(canny_image, (1,1), iterations=2)
    contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rgb_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(rgb_image, contours, -1, (0, 255, 0), 2)
    text = "{} objetos".format(len(contours))
    cv2.putText(rgb_image, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (240, 0, 159), 2)
    
    return rgb_image
        
   
