from matplotlib import pyplot as plt
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMenuBar, QHBoxLayout, QMessageBox, QLineEdit
from PyQt5.QtGui import QPixmap, QFont, QColor, QImage, QIntValidator
from PyQt5.QtCore import Qt, QSize
import matplotlib
matplotlib.use('Qt5Agg')  # Configuração do backend

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
            
            self.roberts_action = self.algorithms_menu.addAction('Roberts')
            if self.apply_roberts:
                self.roberts_action.triggered.connect(self.apply_roberts)
                self.roberts_action.setEnabled(False)
            
            self.prewitt_action = self.algorithms_menu.addAction('Prewitt')
            if self.apply_prewwit:
                self.prewitt_action.triggered.connect(self.apply_prewwit)
                self.prewitt_action.setEnabled(False)

            if self.apply_sobel:
                self.sobel_action = self.algorithms_menu.addAction('Sobel')
                self.sobel_action.triggered.connect(self.apply_sobel)
                self.sobel_action.setEnabled(False)
            
            if self.apply_LoG:
                self.LoG_action = self.algorithms_menu.addAction('LoG')
                self.LoG_action.triggered.connect(self.apply_LoG)
                self.LoG_action.setEnabled(False)
            
            if self.apply_zerocross:
                self.zerocross_action = self.algorithms_menu.addAction('Zero Crossing')
                self.zerocross_action.triggered.connect(self.apply_zerocross)
                self.zerocross_action.setEnabled(False)
            
            if self.apply_canny: 
                self.canny_action = self.algorithms_menu.addAction('Canny')
                self.canny_action.triggered.connect(self.apply_canny)
                self.canny_action.setEnabled(False)
            
            if self.apply_salt_and_pepper:
                self.salt_and_pepper_action = self.algorithms_menu.addAction('Salt & Pepper')
                self.salt_and_pepper_action.triggered.connect(self.apply_salt_and_pepper)
                self.salt_and_pepper_action.setEnabled(False)
            
            if self.apply_Watershed:
                self.watershed_action = self.algorithms_menu.addAction('Watershed')
                self.watershed_action.triggered.connect(self.apply_Watershed)
                self.watershed_action.setEnabled(False)
            
            if self.apply_histogram:
                self.histogram_action = self.algorithms_menu.addAction('Histograma')
                self.histogram_action.triggered.connect(self.apply_histogram)
                self.histogram_action.setEnabled(False)
            
            if self.apply_histogram_adaptive:
                self.histogram_adaptive_action = self.algorithms_menu.addAction('Histograma Adaptativo')
                self.histogram_adaptive_action.triggered.connect(self.apply_histogram_adaptive)
                self.histogram_adaptive_action.setEnabled(False)
            
            if self.counting_objects:
                self.counting_objects_action = self.algorithms_menu.addAction('Contagem de Objetos')
                self.counting_objects_action.triggered.connect(self.counting_objects)
                self.counting_objects_action.setEnabled(False)

        # Caixa de texto para entrada de valor do limiar com validação
        self.threshold_input = QLineEdit(self)
        self.threshold_input.setValidator(QIntValidator(0, 255))  # Apenas valores entre 0 e 255
        self.threshold_input.setPlaceholderText("Insira um valor (0-255)")
        self.threshold_input.setVisible(False)  # Inicialmente invisível
        self.threshold_input.returnPressed.connect(self.confirm_threshold)  # Confirma ao pressionar Enter
        self.main_layout.addWidget(self.threshold_input)

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

    def apply_threshold(self):
        if self.original_pixmap:
            # Torna a caixa de texto visível apenas para este algoritmo
            self.threshold_input.setVisible(True)
            self.threshold_input.setFocus()  # Dá foco na caixa de texto para facilitar a entrada
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")

    def confirm_threshold(self):
        # Função chamada quando o usuário pressiona Enter na caixa de texto 
        try:
            thres_value = int(self.threshold_input.text())
            image = self.pixmap_to_cv(self.original_pixmap)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, thresh_image = cv2.threshold(gray_image, thres_value, 255, cv2.THRESH_BINARY)
            result_pixmap = self.cv_to_pixmap(thresh_image)
            self.image_label.setPixmap(result_pixmap)
        except ValueError:
            QMessageBox.warning(self, "Erro", "Valor inválido. Insira um número entre 0 e 255.")
    
    def apply_grayscale(self): 
        if self.original_pixmap:
            self.threshold_input.setEnabled(False)  # Desativa a caixa de texto
            image = self.pixmap_to_cv(self.original_pixmap)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            result_pixmap = self.cv_to_pixmap(gray_image)
            self.image_label.setPixmap(result_pixmap)
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")

    def apply_highPass(self): #Falta colocar o Alto reforço (não sei o que é isso)
        if self.original_pixmap:
            self.threshold_input.setEnabled(False)  # Desativa a caixa de texto
            image = self.pixmap_to_cv(self.original_pixmap)
            kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
            high_pass_image = cv2.filter2D(image, -1, kernel)
            result_pixmap = self.cv_to_pixmap(high_pass_image)
            self.image_label.setPixmap(result_pixmap)
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")

    def apply_lowPass(self): #Falta colocar a Mediana
        if self.original_pixmap:
            image = self.pixmap_to_cv(self.original_pixmap)
            kernel = 10 #o usuario pode modificar 
            low_pass_image = cv2.blur(image, (kernel, kernel))
            result_pixmap = self.cv_to_pixmap(low_pass_image)
            self.image_label.setPixmap(result_pixmap)
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")

    def apply_roberts(self):
        if self.original_pixmap:
            self.threshold_input.setEnabled(False)  # Desativa a caixa de texto
            image = self.pixmap_to_cv(self.original_pixmap)

            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Aplicar o filtro de Roberts
            kernel_x = np.array([[1, 0], [0, -1]], dtype=int)
            kernel_y = np.array([[0, 1], [-1, 0]], dtype=int)
            
            roberts_x = cv2.filter2D(image, -1, kernel_x)
            roberts_y = cv2.filter2D(image, -1, kernel_y)
            
            # Usando NumPy para calcular a magnitude do gradiente
            roberts_image = np.sqrt(np.square(roberts_x) + np.square(roberts_y))
            roberts_image = np.uint8(roberts_image)
            
            result_pixmap = self.cv_to_pixmap(roberts_image)
            self.image_label.setPixmap(result_pixmap)
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")

    def apply_prewwit(self): #O usuario tem que escolher o horizonta/vertical/horizontal e vertical/edge
        if self.original_pixmap:
            self.threshold_input.setEnabled(False)  # Desativa a caixa de texto
            image = self.pixmap_to_cv(self.original_pixmap)

            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Aplicar o filtro de Prewitt
            kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=int)
            kernel_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=int)
            
            prewitt_x = cv2.filter2D(image, -1, kernel_x)
            prewitt_y = cv2.filter2D(image, -1, kernel_y)
            
            # Usando NumPy para calcular a magnitude do gradiente
            prewitt_image = np.sqrt(np.square(prewitt_x) + np.square(prewitt_y))
            prewitt_image = np.uint8(prewitt_image)
            
            result_pixmap = self.cv_to_pixmap(prewitt_image)
            self.image_label.setPixmap(result_pixmap)
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")

    def apply_sobel(self): #O usuario tem que escolher o horizonta/vertical/horizontal e vertical/edge
        if self.original_pixmap:
            self.threshold_input.setEnabled(False)  # Desativa a caixa de texto
            image = self.pixmap_to_cv(self.original_pixmap)

            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Aplicar o filtro de Sobel
            kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=int)
            kernel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype=int)
            
            sobel_x = cv2.filter2D(image, -1, kernel_x)
            sobel_y = cv2.filter2D(image, -1, kernel_y)
            
            # Usando NumPy para calcular a magnitude do gradiente
            sobel_image = np.sqrt(np.square(sobel_x) + np.square(sobel_y))
            sobel_image = np.uint8(sobel_image)
            
            result_pixmap = self.cv_to_pixmap(sobel_image)
            self.image_label.setPixmap(result_pixmap)
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")

    def apply_LoG(self): #pode escolher a janela e o sigma
        if self.original_pixmap:
            image = self.pixmap_to_cv(self.original_pixmap)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            LoG_image = cv2.GaussianBlur(image, (3, 3), 0) #O usuario pode escolher o numero

            LoG_image = cv2.Laplacian(LoG_image,  cv2.CV_64F)
            LoG_image = cv2.convertScaleAbs(LoG_image)

            result_pixmap = self.cv_to_pixmap(LoG_image)
            self.image_label.setPixmap(result_pixmap)
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")

    def apply_zerocross_auxiliar(self, image):
        zero_crossings = np.zeros_like(image, dtype=np.uint8)
        rows, cols = image.shape
        
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                # Verificar vizinhos para cruzamento de zero
                if (image[i, j] * image[i + 1, j] < 0 or  # Vertical
                image[i, j] * image[i, j + 1] < 0): # Diagonal secundária
                    zero_crossings[i, j] = 255  # Marca o pixel como borda
           
        return zero_crossings

    def apply_zerocross(self): #O usuario pode escolher AS MASCARAS
        if self.original_pixmap:
            image = self.pixmap_to_cv(self.original_pixmap)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blurred_image =  cv2.GaussianBlur(gray_image, (5, 5), 0) #O usuario pode escolher o numero
            log_image = cv2.Laplacian(blurred_image, cv2.CV_64F)
            zeroCrossing_image = self.apply_zerocross_auxiliar(log_image)
            result_pixmap = self.cv_to_pixmap(zeroCrossing_image)
            self.image_label.setPixmap(result_pixmap)
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")
    
    def apply_canny(self): #O USUARIO PODE ESCOLHER AS MASCARAS
        if self.original_pixmap:
            image = self.pixmap_to_cv(self.original_pixmap)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            canny_image = cv2.Canny(gray_image, 100, 200) #O usuario pode escolher os numeros
            result_pixmap = self.cv_to_pixmap(canny_image)
            self.image_label.setPixmap(result_pixmap)
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")

    def apply_salt_and_pepper(self): #O USUARIO PODE COLOCAR COLOCAR O VALOR DA MASCARA
        if self.original_pixmap:
            image = self.pixmap_to_cv(self.original_pixmap)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            salt_mask = np.random.rand(*gray_image.shape) < 0.05
            gray_image[salt_mask] = 255
            pepper_mask = np.random.rand(*gray_image.shape) < 0.05
            gray_image[pepper_mask] = 0
            result_pixmap = self.cv_to_pixmap(gray_image)
            self.image_label.setPixmap(result_pixmap)
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")

    def apply_Watershed(self): 
        if self.original_pixmap:
            image = self.pixmap_to_cv(self.original_pixmap)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            kernel = np.ones((3, 3), np.uint8)
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
            sure_bg = cv2.dilate(opening, kernel, iterations=3)
            dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
            _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
            sure_fg = np.uint8(sure_fg)
            unknown = cv2.subtract(sure_bg, sure_fg)
            _, markers = cv2.connectedComponents(sure_fg)
            markers = markers + 1
            markers[unknown == 255] = 0
            markers = cv2.watershed(image, markers)
            image[markers == -1] = [255, 0, 0]
            result_pixmap = self.cv_to_pixmap(image)
            self.image_label.setPixmap(result_pixmap)
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")
        
    def apply_histogram(self):
        if self.original_pixmap:
            image = self.pixmap_to_cv(self.original_pixmap)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            mask = np.zeros(gray_image.shape[:2], np.uint8)
            mask[100:300, 100:400] = 255
            masked_image = cv2.bitwise_and(gray_image, gray_image, mask=mask)
            hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])
            
            result_pixmap = self.cv_to_pixmap(image)
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
            gray_image = cv2.equalizeHist(gray_image)
            result_pixmap = self.cv_to_pixmap(gray_image)
            self.image_label.setPixmap(result_pixmap)
        else:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem carregada!")
    
    def counting_objects(self):
        if self.original_pixmap:
            image = self.pixmap_to_cv(self.original_pixmap)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blur_image = cv2.GaussianBlur(gray_image, (11, 11), 0)
            canny_image = cv2.Canny(blur_image, 30, 150)
            dilated_image = cv2.dilate(canny_image, (1,1), iterations=2)
            contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            rgb_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
            cv2.drawContours(rgb_image, contours, -1, (0, 255, 0), 2)
            text = "{} objetos".format(len(contours))
            cv2.putText(rgb_image, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (240, 0, 159), 2)
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
