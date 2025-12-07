from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QTextEdit, 
                             QFileDialog, QMessageBox, QProgressBar, QGroupBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import os

class WorkerThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, func, *args):
        super().__init__()
        self.func = func
        self.args = args
    
    def run(self):
        try:
            result = self.func(*self.args)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class Application(QMainWindow):
    
    def __init__(self, audio_converter, encryptor):
        super().__init__()
        self.audio_converter = audio_converter
        self.encryptor = encryptor
        self.ruta_archivo = ""
        
        self.setWindowTitle("Conversor de Audio a Texto con Criptografia")
        self.setGeometry(100, 100, 1000, 800)
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        titulo = QLabel("Conversor de Audio a Texto con Criptografia")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setFont(QFont("Arial", 18, QFont.Bold))
        titulo.setStyleSheet("background-color: #1237db; color: white; padding: 20px;")
        main_layout.addWidget(titulo)
        
        grupo_archivo = QGroupBox("ARCHIVO DE AUDIO")
        grupo_archivo.setFont(QFont("Arial", 11, QFont.Bold))
        layout_archivo = QVBoxLayout()
        
        layout_ruta = QHBoxLayout()
        
        label_ruta = QLabel("Ruta:")
        self.entry_ruta = QLineEdit()
        self.entry_ruta.setReadOnly(True)
        self.entry_ruta.setMinimumHeight(30)
        
        self.btn_buscar = QPushButton("Buscar Archivo")
        self.btn_buscar.setMinimumHeight(30)
        self.btn_buscar.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 5px 15px;")
        self.btn_buscar.clicked.connect(self.buscar_archivo)
        
        layout_ruta.addWidget(label_ruta)
        layout_ruta.addWidget(self.entry_ruta)
        layout_ruta.addWidget(self.btn_buscar)
        
        self.label_info_archivo = QLabel("No hay archivo seleccionado")
        self.label_info_archivo.setStyleSheet("color: gray;")
        
        layout_archivo.addLayout(layout_ruta)
        layout_archivo.addWidget(self.label_info_archivo)
        grupo_archivo.setLayout(layout_archivo)
        main_layout.addWidget(grupo_archivo)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        grupo_texto = QGroupBox("TEXTO CONVERTIDO")
        grupo_texto.setFont(QFont("Arial", 11, QFont.Bold))
        layout_texto = QVBoxLayout()
        
        self.texto_convertido = QTextEdit()
        self.texto_convertido.setMinimumHeight(100)
        layout_texto.addWidget(self.texto_convertido)
        
        self.btn_convertir = QPushButton("Convertir a Texto")
        self.btn_convertir.setMinimumHeight(40)
        self.btn_convertir.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold;")
        self.btn_convertir.clicked.connect(self.convertir_a_texto)
        layout_texto.addWidget(self.btn_convertir)
        
        grupo_texto.setLayout(layout_texto)
        main_layout.addWidget(grupo_texto)
        
        grupo_codigo = QGroupBox("REPRESENTACION EN CODIGO MAQUINA")
        grupo_codigo.setFont(QFont("Arial", 11, QFont.Bold))
        layout_codigo = QVBoxLayout()
        
        self.texto_hexadecimal = QTextEdit()
        self.texto_hexadecimal.setMinimumHeight(100)
        self.texto_hexadecimal.setStyleSheet("background-color: #f5f5f5; font-family: Courier;")
        layout_codigo.addWidget(self.texto_hexadecimal)
        
        grupo_codigo.setLayout(layout_codigo)
        main_layout.addWidget(grupo_codigo)
        
        grupo_encriptado = QGroupBox("TEXTO ENCRIPTADO")
        grupo_encriptado.setFont(QFont("Arial", 11, QFont.Bold))
        layout_encriptado = QVBoxLayout()
        
        self.texto_encriptado = QTextEdit()
        self.texto_encriptado.setMinimumHeight(100)
        layout_encriptado.addWidget(self.texto_encriptado)
        
        layout_botones = QHBoxLayout()
        
        self.btn_encriptar = QPushButton("Encriptar Texto")
        self.btn_encriptar.setMinimumHeight(35)
        self.btn_encriptar.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold;")
        self.btn_encriptar.clicked.connect(self.encriptar_texto)
        
        self.btn_desencriptar = QPushButton("Desencriptar")
        self.btn_desencriptar.setMinimumHeight(35)
        self.btn_desencriptar.setStyleSheet("background-color: #9C27B0; color: white; font-weight: bold;")
        self.btn_desencriptar.clicked.connect(self.desencriptar_texto)
        
        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_limpiar.setMinimumHeight(35)
        self.btn_limpiar.setStyleSheet("background-color: #F44336; color: white; font-weight: bold;")
        self.btn_limpiar.clicked.connect(self.limpiar_todo)
        
        layout_botones.addWidget(self.btn_encriptar)
        layout_botones.addWidget(self.btn_desencriptar)
        layout_botones.addWidget(self.btn_limpiar)
        
        layout_encriptado.addLayout(layout_botones)
        grupo_encriptado.setLayout(layout_encriptado)
        main_layout.addWidget(grupo_encriptado)
        
        self.label_estado = QLabel("Estado: Listo")
        self.label_estado.setStyleSheet("background-color: #E0E0E0; padding: 8px;")
        main_layout.addWidget(self.label_estado)
    
    def buscar_archivo(self):
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.actualizar_estado("Cargando archivo...")
        
        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo de audio",
            "",
            "Archivos de Audio (*.mp3 *.wav *.ogg *.flac *.m4a);;Todos los archivos (*.*)"
        )
        
        if ruta:
            if self.audio_converter.validar_formato_audio(ruta):
                self.ruta_archivo = ruta
                self.entry_ruta.setText(ruta)
                
                nombre_archivo = os.path.basename(ruta)
                extension = os.path.splitext(ruta)[1]
                duracion = self.audio_converter.obtener_duracion_audio(ruta)
                
                info = f"Archivo: {nombre_archivo} | Formato: {extension} | Duracion: {duracion:.2f}s"
                self.label_info_archivo.setText(info)
                self.label_info_archivo.setStyleSheet("color: green;")
                self.actualizar_estado("Archivo cargado correctamente")
            else:
                QMessageBox.critical(self, "Formato no valido", 
                                   "El formato del archivo no es compatible.\nFormatos soportados: MP3, WAV, OGG, FLAC, M4A")
        
        self.progress_bar.setVisible(False)
    
    def convertir_a_texto(self):
        if not self.ruta_archivo:
            QMessageBox.warning(self, "Sin archivo", "Por favor, seleccione un archivo de audio primero.")
            return
        
        self.deshabilitar_botones()
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.actualizar_estado("Convirtiendo audio a texto...")
        
        self.worker = WorkerThread(self.audio_converter.convertir_audio_a_texto, self.ruta_archivo)
        self.worker.finished.connect(self.mostrar_texto_convertido)
        self.worker.error.connect(self.mostrar_error)
        self.worker.start()
    
    def mostrar_texto_convertido(self, texto):
        self.texto_convertido.setText(texto)
        
        texto_bytes = texto.encode('utf-8')
        texto_hex = ' '.join([f'{byte:02X}' for byte in texto_bytes])
        
        mensaje_hex = f"Total de bytes: {len(texto_bytes)}\n"
        mensaje_hex += f"Codificacion: UTF-8\n\n"
        mensaje_hex += f"Representacion Hexadecimal:\n{texto_hex}\n\n"
        mensaje_hex += f"Representacion Binaria (primeros 50 bytes):\n"
        
        for i, byte in enumerate(texto_bytes[:50]):
            mensaje_hex += f'{byte:08b} '
            if (i + 1) % 8 == 0:
                mensaje_hex += '\n'
        
        if len(texto_bytes) > 50:
            mensaje_hex += f"\n... ({len(texto_bytes) - 50} bytes adicionales)"
        
        self.texto_hexadecimal.setText(mensaje_hex)
        
        self.progress_bar.setVisible(False)
        self.actualizar_estado("Conversion completada")
        self.habilitar_botones()
    
    def mostrar_error(self, error):
        QMessageBox.critical(self, "Error", f"Error al procesar el audio: {error}")
        self.progress_bar.setVisible(False)
        self.habilitar_botones()
    
    def encriptar_texto(self):
        texto = self.texto_convertido.toPlainText().strip()
        
        if not texto:
            QMessageBox.warning(self, "Sin texto", "No hay texto para encriptar.")
            return
        
        texto_encriptado = self.encryptor.encriptar_texto(texto)
        self.texto_encriptado.setText(texto_encriptado)
        
        self.texto_convertido.clear()
        self.texto_hexadecimal.clear()
        
        self.actualizar_estado("Texto encriptado correctamente")
    
    def desencriptar_texto(self):
        texto_encriptado = self.texto_encriptado.toPlainText().strip()
        
        if not texto_encriptado:
            QMessageBox.warning(self, "Sin texto", "No hay texto encriptado para desencriptar.")
            return
        
        texto_desencriptado = self.encryptor.desencriptar_texto(texto_encriptado)
        self.texto_convertido.setText(texto_desencriptado)
        
        texto_bytes = texto_desencriptado.encode('utf-8')
        texto_hex = ' '.join([f'{byte:02X}' for byte in texto_bytes])
        
        mensaje_hex = f"Total de bytes: {len(texto_bytes)}\n"
        mensaje_hex += f"Codificacion: UTF-8\n\n"
        mensaje_hex += f"Representacion Hexadecimal:\n{texto_hex}\n\n"
        mensaje_hex += f"Representacion Binaria (primeros 50 bytes):\n"
        
        for i, byte in enumerate(texto_bytes[:50]):
            mensaje_hex += f'{byte:08b} '
            if (i + 1) % 8 == 0:
                mensaje_hex += '\n'
        
        if len(texto_bytes) > 50:
            mensaje_hex += f"\n... ({len(texto_bytes) - 50} bytes adicionales)"
        
        self.texto_hexadecimal.setText(mensaje_hex)
        
        self.texto_encriptado.clear()
        
        self.actualizar_estado("Texto desencriptado correctamente")
    
    def limpiar_todo(self):
        self.texto_convertido.clear()
        self.texto_hexadecimal.clear()
        self.texto_encriptado.clear()
        self.entry_ruta.clear()
        self.ruta_archivo = ""
        self.label_info_archivo.setText("No hay archivo seleccionado")
        self.label_info_archivo.setStyleSheet("color: gray;")
        self.actualizar_estado("Interfaz limpiada")
    
    def deshabilitar_botones(self):
        self.btn_buscar.setEnabled(False)
        self.btn_convertir.setEnabled(False)
        self.btn_encriptar.setEnabled(False)
        self.btn_desencriptar.setEnabled(False)
        self.btn_limpiar.setEnabled(False)
    
    def habilitar_botones(self):
        self.btn_buscar.setEnabled(True)
        self.btn_convertir.setEnabled(True)
        self.btn_encriptar.setEnabled(True)
        self.btn_desencriptar.setEnabled(True)
        self.btn_limpiar.setEnabled(True)
    
    def actualizar_estado(self, mensaje):
        self.label_estado.setText(f"Estado: {mensaje}")