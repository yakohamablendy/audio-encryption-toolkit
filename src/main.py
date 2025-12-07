import sys
from PyQt5.QtWidgets import QApplication
from gui import Application
from audio_converter import AudioConverter
from encryption import Encryptor

def main():
    app = QApplication(sys.argv)
    
    audio_converter = AudioConverter()
    encryptor = Encryptor()
    
    ventana = Application(audio_converter, encryptor)
    ventana.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()