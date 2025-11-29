import tkinter as tk
from gui import Application
from audio_converter import AudioConverter
from encryption import Encryptor

def main():
    """
    Función principal que inicia la aplicación.
    Crea las instancias necesarias y ejecuta la interfaz gráfica.
    """
    # Crea la ventana principal de Tkinter
    root = tk.Tk()
    
    # Crea las instancias de los módulos
    audio_converter = AudioConverter()
    encryptor = Encryptor()
    
    # Crea la aplicación con la interfaz gráfica
    app = Application(root, audio_converter, encryptor)
    
    # Inicia el loop principal de la aplicación
    root.mainloop()

# Punto de entrada del programa
if __name__ == "__main__":
    main()