from cryptography.fernet import Fernet
import base64

class Encryptor:
   
    
    def __init__(self):

        # Genera una clave única para encriptar/desencriptar
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
    
    def encriptar_texto(self, texto):
        try:
            # Convierte el texto a bytes
            texto_bytes = texto.encode('utf-8')
            
            # Encripta los bytes
            texto_encriptado = self.cipher.encrypt(texto_bytes)
            
            # Retorna el texto encriptado como string decodificado
            return texto_encriptado.decode('utf-8')
        
        except Exception as e:
            # Captura cualquier error durante la encriptación
            return f"Error al encriptar: {str(e)}"
    
    def desencriptar_texto(self, texto_encriptado):
        try:
            # Convierte el texto encriptado a bytes
            texto_bytes = texto_encriptado.encode('utf-8')
            
            # Desencripta los bytes
            texto_desencriptado = self.cipher.decrypt(texto_bytes)
            
            # Retorna el texto desencriptado como string
            return texto_desencriptado.decode('utf-8')
        
        except Exception as e:
            # Captura cualquier error durante la desencriptación
            return f"Error al desencriptar: {str(e)}"
    
    def obtener_clave(self):
        return self.key
    
    def establecer_clave(self, clave):
        self.key = clave
        self.cipher = Fernet(self.key)


# Función de prueba del módulo (solo para testing)
if __name__ == "__main__":
    
    encriptador = Encryptor()
    
    # Texto de prueba
    texto_original = "Hola, este es un texto de prueba para encriptar"
    print(f"Texto original: {texto_original}")
    
    # Encripta el texto
    texto_cifrado = encriptador.encriptar_texto(texto_original)
    print(f"Texto encriptado: {texto_cifrado}")
    
    # Desencripta el texto
    texto_recuperado = encriptador.desencriptar_texto(texto_cifrado)
    print(f"Texto desencriptado: {texto_recuperado}")