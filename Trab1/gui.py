from concurrent.futures.process import _threads_wakeups
from re import L
from matplotlib import pyplot as plt
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMenuBar, QHBoxLayout, QMessageBox, QLineEdit
from PyQt5.QtGui import QPixmap, QFont, QColor, QImage, QIntValidator, QDoubleValidator
from PyQt5.QtCore import Qt, QSize
import matplotlib
matplotlib.use('Qt5Agg')  # Configuração do backend
from filtros import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Visualizador de Imagens')
        self.setGeometry(100, 100, 400, 400)

        self.original_pixmap = None

        # Layout principal
        self.main_layout = QVBoxLayout()
        self.setup_ui()
        self.setLayout(self.main_layout)

    def setup_ui(self):
        
        # Layout horizontal para a mensagem e o botão
        h_layout = QHBoxLayout()
        
        # Instruções
        instruction_label = QLabel("Clique no botão:")
        instruction_label.setFont(QFont('Arial', 12))
        h_layout.addWidget(instruction_label)

        # Botão para carregar a imagem
        self.button = QPushButton('Carregar Imagem', self)
        self.button.setFont(QFont('Arial', 12))
        self.button.clicked.connect(self.open_image)
        h_layout.addWidget(self.button)

        # Adiciona o layout horizontal ao layout principal
        self.main_layout.addLayout(h_layout)
        
        # Label para exibir a imagem
        self.image_label = QLabel(self) 
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.image_label)

        placeholder_pixmap = QPixmap(QSize(400, 300))
        custom_gray = QColor(200, 200, 200)
        placeholder_pixmap.fill(custom_gray)  # Cor cinza como fundo
        self.image_label.setPixmap(placeholder_pixmap)
        self.image_label.setText("Pré-visualização da imagem")
        self.image_label.setStyleSheet("QLabel { color: gray; }")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Barra de menus
        menu_bar = QMenuBar(self)
        file_menu = menu_bar.addMenu('Menu')
        if file_menu:
            exit_action = file_menu.addAction('Sair')
            if exit_action:
                exit_action.triggered.connect(self.close_app)
        
        self.algorithms_menu = menu_bar.addMenu('Algoritmos')
        if self.algorithms_menu:
            # Adiciona ações dos algoritmos e as desativa inicialmente
            self.threshold_action = self.algorithms_menu.addAction('Limiarização')
            if self.threshold_action:
                self.threshold_action.triggered.connect(self.apply_threshold)
                self.threshold_action.setEnabled(False)
            
            self.grayscale_action = self.algorithms_menu.addAction('Escala de Cinza')
            if self.grayscale_action:
                self.grayscale_action.triggered.connect(self.apply_grayscale)
                self.grayscale_action.setEnabled(False)

            self.highPass_action = self.algorithms_menu.addAction('Passa Alta')
            if self.highPass_action:
                self.highPass_action.triggered.connect(self.apply_highPass)
                self.highPass_action.setEnabled(False)
            
            self.lowPass_action = self.algorithms_menu.addAction('Passa Baixa')
            if self.lowPass_action: 
                self.lowPass_action.triggered.connect(self.apply_lowPass)
                self.lowPass_action.setEnabled(False)
                
            self.median_action = self.algorithms_menu.addAction('Mediana')
            if self.median_action:
                self.median_action.triggered.connect(self.apply_median)
                self.median_action.setEnabled(False)
            
            self.roberts_action = self.algorithms_menu.addAction('Roberts')
            if self.apply_roberts:
                self.roberts_action.triggered.connect(self.apply_roberts)
                self.roberts_action.setEnabled(False)
            
            self.prewitt_action = self.algorithms_menu.addAction('Prewitt')
            if self.apply_prewwit:
                self.prewitt_action.triggered.connect(self.apply_prewwit)
                self.prewitt_action.setEnabled(False)
                
            self.sobel_action = self.algorithms_menu.addAction('Sobel')
            if self.apply_sobel:
                self.sobel_action.triggered.connect(self.apply_sobel)
                self.sobel_action.setEnabled(False)
                
            self.LoG_action = self.algorithms_menu.addAction('LoG')
            if self.apply_LoG:
                self.LoG_action.triggered.connect(self.apply_LoG)
                self.LoG_action.setEnabled(False)
                
            self.zerocross_action = self.algorithms_menu.addAction('Zero Crossing')
            if self.apply_zerocross:
                self.zerocross_action.triggered.connect(self.apply_zerocross)
                self.zerocross_action.setEnabled(False)
                
            self.canny_action = self.algorithms_menu.addAction('Canny')
            if self.apply_canny: 
                self.canny_action.triggered.connect(self.apply_canny)
                self.canny_action.setEnabled(False)
            
            self.salt_and_pepper_action = self.algorithms_menu.addAction('Salt & Pepper')
            if self.apply_salt_and_pepper:
                self.salt_and_pepper_action.triggered.connect(self.apply_salt_and_pepper)
                self.salt_and_pepper_action.setEnabled(False)

            self.watershed_action = self.algorithms_menu.addAction('Watershed')
            if self.apply_Watershed:
                self.watershed_action.triggered.connect(self.apply_Watershed)
                self.watershed_action.setEnabled(False)

            self.histogram_action = self.algorithms_menu.addAction('Histograma')
            if self.apply_histogram:
                self.histogram_action.triggered.connect(self.apply_histogram)
                self.histogram_action.setEnabled(False)
            
            self.histogram_adaptive_action = self.algorithms_menu.addAction('Histograma Adaptativo')
            if self.apply_histogram_adaptive:
                self.histogram_adaptive_action.triggered.connect(self.apply_histogram_adaptive)
                self.histogram_adaptive_action.setEnabled(False)
            
            self.counting_objects_action = self.algorithms_menu.addAction('Contagem de Objetos')
            if self.counting_objects:
                self.counting_objects_action.triggered.connect(self.counting_objects)
                self.counting_objects_action.setEnabled(False)

        # Caixa de texto para entrada de valor do limiar com validação
        self.threshold_input = QLineEdit(self)
        self.threshold_input.setValidator(QIntValidator(0, 255))  # Apenas valores entre 0 e 255
        self.threshold_input.setPlaceholderText("Insira um valor (0-255)")
        self.threshold_input.setVisible(False)  # Inicialmente invisível
        self.threshold_input.returnPressed.connect(self.apply_threshold)  # Confirma ao pressionar Enter
        self.main_layout.addWidget(self.threshold_input)
        
        # Caixa de texto para entrada de valor do limiar com validação
        self.lowPass_input = QLineEdit(self)
        self.lowPass_input.setValidator(QIntValidator(0, 255))  # Apenas valores entre 0 e 255
        self.lowPass_input.setPlaceholderText("Insira um valor (0-255)")
        self.lowPass_input.setVisible(False)  # Inicialmente invisível
        self.lowPass_input.returnPressed.connect(self.apply_lowPass)  # Confirma ao pressionar Enter
        self.main_layout.addWidget(self.lowPass_input)
        
        # Caixa de texto para entrada de valor do kernel com validação
        self.kernel_input = QLineEdit(self)
        self.kernel_input.setValidator(QIntValidator(0, 255))  # Apenas valores entre 0 e 255
        self.kernel_input.setPlaceholderText("Insira um valor impar de (0-255)")
        self.kernel_input.setVisible(False)  # Inicialmente invisível
        self.kernel_input.returnPressed.connect(self.apply_median)  # Confirma ao pressionar Enter
        self.main_layout.addWidget(self.kernel_input)

        # Define o layout para o widget principal
        self.main_layout.setMenuBar(menu_bar)
        
    def close_app(self):
        self.close()

    def open_image(self): 
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Escolha uma imagem', '', 'Images (*.png *.xpm *.jpg *.bmp *.gif)', options=options)
        if file_name:
            self.original_pixmap = QPixmap(file_name)
            self.image_label.setPixmap(self.original_pixmap.scaled(
                self.image_label.size(), 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation))
            
            # Habilita as ações dos algoritmos após carregar a imagem
            self.enable_algorithm_actions(True)

    def resizeEvent(self, event):
        if self.original_pixmap:
            self.update_image()
    
    def update_image(self):
        if self.original_pixmap:
            label_size = self.image_label.size()
            if not label_size.isEmpty():
                original_size = self.original_pixmap.size()
                scaled_pixmap = self.original_pixmap.scaled(
                min(label_size.width(), original_size.width()),
                min(label_size.height(), original_size.height()),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)

    def enable_algorithm_actions(self, enabled):
        # Habilita ou desabilita as ações dos algoritmos
        if self.threshold_action:
            self.threshold_action.setEnabled(enabled)
        if self.grayscale_action:
            self.grayscale_action.setEnabled(enabled)
        if self.highPass_action:
            self.highPass_action.setEnabled(enabled)
        if self.lowPass_action:
            self.lowPass_action.setEnabled(enabled)
        if self.median_action:
            self.median_action.setEnabled(enabled)
        if self.roberts_action:
            self.roberts_action.setEnabled(enabled)
        if self.prewitt_action:
            self.prewitt_action.setEnabled(enabled)
        if self.sobel_action:
            self.sobel_action.setEnabled(enabled)
        if self.LoG_action:
            self.LoG_action.setEnabled(enabled)
        if self.zerocross_action:
            self.zerocross_action.setEnabled(enabled)
        if self.canny_action:
            self.canny_action.setEnabled(enabled)
        if self.salt_and_pepper_action:
            self.salt_and_pepper_action.setEnabled(enabled)
        if self.watershed_action:
            self.watershed_action.setEnabled(enabled)
        if self.histogram_action:
            self.histogram_action.setEnabled(enabled)
        if self.histogram_adaptive_action:
            self.histogram_adaptive_action.setEnabled(enabled)
        if self.counting_objects_action:
            self.counting_objects_action.setEnabled(enabled)

    def apply_threshold(self): #PRONTO
        if self.original_pixmap:
            # Torna a caixa de texto visível apenas para este algoritmo
            self.threshold_input.setVisible(True)
            self.threshold_input.setFocus()  # Dá foco na caixa de texto para facilitar a entrada
            try:
                thres_value = int(self.threshold_input.text())
                image = self.pixmap_to_cv(self.original_pixmap)
                thresh_image = threshold_filter(image, thres_value)
                result_pixmap = self.cv_to_pixmap(thresh_image)
                self.image_label.setPixmap(result_pixmap)
            except ValueError:
                QMessageBox.warning(self, "Erro", "Valor inválido. Insira um número entre 0 e 255.")
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")
            
    def apply_grayscale(self): #
        if self.original_pixmap:
            self.threshold_input.setEnabled(False)  # Desativa a caixa de texto
            image = self.pixmap_to_cv(self.original_pixmap)
            gray_image = grayscale_filter(image)
            result_pixmap = self.cv_to_pixmap(gray_image)
            self.image_label.setPixmap(result_pixmap)
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")

    def apply_highPass(self): 
        if self.original_pixmap:
            self.threshold_input.setEnabled(False)  # Desativa a caixa de texto
            image = self.pixmap_to_cv(self.original_pixmap)
            high_pass_image = highPass_filter(image)
            result_pixmap = self.cv_to_pixmap(high_pass_image)
            self.image_label.setPixmap(result_pixmap)
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")
   
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!") 

    def apply_lowPass(self): 
        if self.original_pixmap:
            self.threshold_input.setEnabled(True)  # ativa a caixa de texto
            self.threshold_input.setVisible(True)
            self.threshold_input.setFocus()
            try:
                thres_value = int(self.threshold_input.text())
                image = self.pixmap_to_cv(self.original_pixmap)
                low_pass_image = lowPass_filter(image, thres_value)
                result_pixmap = self.cv_to_pixmap(low_pass_image)
                self.image_label.setPixmap(result_pixmap)
            except ValueError:
                QMessageBox.warning(self, "Erro", "Valor inválido. Insira um número entre 0 e 255.")
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")
    
    def apply_median(self):
        if self.original_pixmap:
            self.threshold_input.setEnabled(False)  # Desativa a caixa de texto
            self.kernel_input.setVisible(True)
            self.kernel_input.setFocus()
            try:
                kernel_value = int(self.kernel_input.text())
                image = self.pixmap_to_cv(self.original_pixmap)
                if(kernel_value % 2 == 1):
                   image = median_filter(image, kernel_value)
                else:
                    QMessageBox.warning(self, "Erro", "Valor inválido. Insira um número ímpar.")

                result_pixmap = self.cv_to_pixmap(image)
                self.image_label.setPixmap(result_pixmap)
            except ValueError:
                QMessageBox.warning(self, "Erro", "Valor inválido. Insira um número ímpar.")
        else:   
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")

    def apply_roberts(self): #PRONTO
        if self.original_pixmap:
            self.threshold_input.setEnabled(False)  # Desativa a caixa de texto
            self.kernel_input.setEnabled(False)  # Desativa a caixa de texto
            image = self.pixmap_to_cv(self.original_pixmap)
            roberts_image = roberts_filter(image)
            
            result_pixmap = self.cv_to_pixmap(roberts_image)
            self.image_label.setPixmap(result_pixmap)
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")

    def apply_prewwit(self): #PRONTO
        if self.original_pixmap:
            self.threshold_input.setEnabled(False)  # Desativa a caixa de texto
            self.kernel_input.setEnabled(False)  # Desativa a caixa de texto
            image = self.pixmap_to_cv(self.original_pixmap)
            prewitt_image = prewitt_filter(image)
            result_pixmap = self.cv_to_pixmap(prewitt_image)
            self.image_label.setPixmap(result_pixmap)
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")

    def apply_sobel(self): 
        if self.original_pixmap:
            self.threshold_input.setEnabled(False)  # Desativa a caixa de texto
            self.kernel_input.setEnabled(False)  # Desativa a caixa de texto
            image = self.pixmap_to_cv(self.original_pixmap)
            sobel_image = sobel_filter(image)
           
            result_pixmap = self.cv_to_pixmap(sobel_image)
            self.image_label.setPixmap(result_pixmap)
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")

    def apply_LoG(self): 
        if self.original_pixmap:
            self.threshold_input.setEnabled(False)  # Desativa a caixa de texto
            self.kernel_input.setEnabled(False)  # Desativa a caixa de texto
            image = self.pixmap_to_cv(self.original_pixmap)
            LoG_image = LoG_filter(image)
            result_pixmap = self.cv_to_pixmap(LoG_image)
            self.image_label.setPixmap(result_pixmap)
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")

    def apply_zerocross(self): 
        if self.original_pixmap:
            self.threshold_input.setEnabled(False)  # Desativa a caixa de texto
            self.kernel_input.setEnabled(False)  # Desativa a caixa de texto
            image = self.pixmap_to_cv(self.original_pixmap)
            zeroCrossing_image = zerocross_filter(image)
            result_pixmap = self.cv_to_pixmap(zeroCrossing_image)
            self.image_label.setPixmap(result_pixmap)
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")
    
    def apply_canny(self): 
        if self.original_pixmap:
            self.threshold_input.setEnabled(False)  # Desativa a caixa de texto
            self.kernel_input.setEnabled(False)  # Desativa a caixa de texto
            image = self.pixmap_to_cv(self.original_pixmap)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            canny_image = cv2.Canny(gray_image, 100, 200) 
            result_pixmap = self.cv_to_pixmap(canny_image)
            self.image_label.setPixmap(result_pixmap)
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")

    def apply_salt_and_pepper(self):
        if self.original_pixmap:
            self.threshold_input.setEnabled(False)  # Desativa a caixa de texto
            self.kernel_input.setEnabled(False)  # Desativa a caixa de texto
            try:
                image = self.pixmap_to_cv(self.original_pixmap)
                image = salt_and_pepper_filter(image, mask_value = 0.05)
                result_pixmap = self.cv_to_pixmap(image)
                self.image_label.setPixmap(result_pixmap)
            except ValueError:
                QMessageBox.warning(self, "Erro", "Valor inválido. Insira um número entre 0 e 1.")
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")

    def apply_Watershed(self): 
        if self.original_pixmap:
            self.kernel_input.setEnabled(False)  # Desativa a caixa de texto
            self.threshold_input.setEnabled(False)  # Desativa a caixa de texto
            try:
                image = self.pixmap_to_cv(self.original_pixmap)
                image = watershed_filter(image)
                result_pixmap = self.cv_to_pixmap(image)
                self.image_label.setPixmap(result_pixmap)
            except ValueError:
                QMessageBox.warning(self, "Erro", "Valor inválido. Insira um número entre 0 e 255.")   
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")
        
    def apply_histogram(self):
        if self.original_pixmap:
            image = self.pixmap_to_cv(self.original_pixmap)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
            hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
            
            result_pixmap = self.cv_to_pixmap(gray_image)
            self.image_label.setPixmap(result_pixmap)
            
            plt.figure("Histograma da Imagem")
            plt.plot(hist, color='gray')
            plt.title("Histograma da Imagem")
            plt.xlabel("Intensidade")
            plt.ylabel("Frequência")
            plt.show()  # Exibe o gráfico
        else:   
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")
    
    def apply_histogram_adaptive(self):
        if self.original_pixmap:
            image = self.pixmap_to_cv(self.original_pixmap)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            equalized = cv2.equalizeHist(gray_image)
            hist = cv2.calcHist([equalized], [0], None, [256], [0, 256])
            
            
            result_pixmap = self.cv_to_pixmap(gray_image)
            self.image_label.setPixmap(result_pixmap)
            
            plt.figure("Histograma Adaptativo")
            plt.plot(hist, color='gray')
            plt.title("Histograma Adaptativo")
            plt.xlabel("Intensidade")
            plt.ylabel("Frequência")
            plt.show()  # Exibe o gráfico
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")
    
    def counting_objects(self): 
        if self.original_pixmap:
            image = self.pixmap_to_cv(self.original_pixmap)
            rgb_image = counting_objects_filters(image)
            result_pixmap = self.cv_to_pixmap(rgb_image)
            self.image_label.setPixmap(result_pixmap)
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")

    def pixmap_to_cv(self, pixmap):
        image = pixmap.toImage()
        image = image.convertToFormat(QImage.Format.Format_RGB888)
        width, height = image.width(), image.height()
        ptr = image.bits()
        ptr.setsize(height * width * 3)
        img = np.array(ptr).reshape(height, width, 3)
        return img

    def cv_to_pixmap(self, img):
        if len(img.shape) == 2:  # Caso de imagem em escala de cinza
            height, width = img.shape
            bytes_per_line = width
            q_image = QImage(img.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        else:  # Caso de imagem colorida
            height, width, _ = img.shape
            bytes_per_line = width * 3
            q_image = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(q_image)
