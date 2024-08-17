import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMenuBar, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Visualizador de Imagens')
        self.setGeometry(100, 100, 400, 400)

        self.original_pixmap = None

        # Layout principal
        layout = QVBoxLayout()

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
        layout.addLayout(h_layout)
        
        # Label para exibir a imagem
        self.image_label = QLabel(self) 
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)

        placeholder_pixmap = QPixmap(400, 300)
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

        # Define o layout para o widget principal
        layout.setMenuBar(menu_bar)
        self.setLayout(layout)

    def close_app(self):
        self.close()

    def open_image(self): 
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Escolha uma imagem', '', 'Images (*.png *.xpm *.jpg *.bmp *.gif)', options=options)
        if file_name:
            self.original_pixmap = QPixmap(file_name)
            self.image_label.setPixmap(self.original_pixmap.scaled(
                self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            
            # Habilita as ações dos algoritmos após carregar a imagem
            self.enable_algorithm_actions(True)

    def resizeEvent(self, event):
        if self.original_pixmap:
            self.update_image()
    
    def update_image(self):
        if self.original_pixmap:
            label_size = self.image_label.size()
            if not label_size.isEmpty():
                scaled_pixmap = self.original_pixmap.scaled(
                    label_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
                self.image_label.setMinimumSize(250, 250)
                self.image_label.repaint()

    def enable_algorithm_actions(self, enabled):
        # Habilita ou desabilita as ações dos algoritmos
        if self.threshold_action:
            self.threshold_action.setEnabled(enabled)
        if self.grayscale_action:
            self.grayscale_action.setEnabled(enabled)

    def apply_threshold(self):
        if self.original_pixmap:
            print("Aplicando limiarização...")  # Substitua pelo código do algoritmo
        else:
            print("Nenhuma imagem carregada!")

    def apply_grayscale(self):
        if self.original_pixmap:
            print("Aplicando escala de cinza...")  # Substitua pelo código do algoritmo
        else:
            print("Nenhuma imagem carregada!")

# Função principal
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
