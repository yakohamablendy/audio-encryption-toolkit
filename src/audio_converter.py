import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

class AudioConverter:
    
    def __init__(self):
        # Crea una instancia del reconocedor de voz de Google
        self.recognizer = sr.Recognizer()
    
    def convertir_audio_a_texto(self, ruta_archivo):
        try:
            # Obtiene la extensión del archivo
            extension = os.path.splitext(ruta_archivo)[1].lower()
            
            # Si es MP3, lo convierte a WAV primero
            if extension == '.mp3':
                ruta_wav = self._convertir_mp3_a_wav(ruta_archivo)
            else:
                ruta_wav = ruta_archivo
            
            # Carga el audio completo
            audio = AudioSegment.from_wav(ruta_wav)
            
            # Obtiene la duración en segundos
            duracion = len(audio) / 1000
            
            # Si el audio es corto (menos de 60 segundos), procesa normal
            if duracion <= 60:
                texto = self._procesar_audio_corto(ruta_wav)
            else:
                # Si el audio es largo, lo divide en segmentos
                texto = self._procesar_audio_largo(audio, ruta_wav)
            
            # Elimina el archivo WAV temporal si fue convertido
            if extension == '.mp3' and os.path.exists(ruta_wav):
                os.remove(ruta_wav)
            
            return texto
        
        except sr.UnknownValueError:
            return "No se pudo entender el audio. Intente con un audio más claro."
        
        except sr.RequestError as e:
            return f"Error con el servicio de reconocimiento: {str(e)}"
        
        except Exception as e:
            return f"Error al procesar el audio: {str(e)}"
    
    def _procesar_audio_corto(self, ruta_wav):
       
        with sr.AudioFile(ruta_wav) as source:
            # Ajusta el ruido ambiente
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Graba el audio del archivo
            audio_data = self.recognizer.record(source)
            
            # Convierte el audio a texto
            texto = self.recognizer.recognize_google(audio_data, language='es-ES')
            
            return texto
    
    def _procesar_audio_largo(self, audio, ruta_wav):
    
        # Lista para almacenar los textos de cada segmento
        textos = []
        
        # Duración de cada segmento en milisegundos (60 segundos = 60000 ms)
        duracion_segmento = 60000
        
        # Divide el audio en segmentos
        for i in range(0, len(audio), duracion_segmento):
            # Extrae el segmento actual
            segmento = audio[i:i + duracion_segmento]
            
            # Crea un archivo temporal para este segmento
            nombre_temp = f"temp_segmento_{i}.wav"
            segmento.export(nombre_temp, format="wav")
            
            try:
                # Procesa este segmento
                with sr.AudioFile(nombre_temp) as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    audio_data = self.recognizer.record(source)
                    
                    # Convierte a texto
                    texto_segmento = self.recognizer.recognize_google(audio_data, language='es-ES')
                    textos.append(texto_segmento)
            
            except sr.UnknownValueError:
                # Si no se entiende este segmento, agrega un mensaje
                textos.append("[Segmento no reconocido]")
            
            except Exception as e:
                textos.append(f"[Error en segmento: {str(e)}]")
            
            finally:
                # Elimina el archivo temporal
                if os.path.exists(nombre_temp):
                    os.remove(nombre_temp)
        
        # Une todos los textos con un espacio
        texto_completo = " ".join(textos)
        
        return texto_completo
    
    def _convertir_mp3_a_wav(self, ruta_mp3):
      
        try:
            # Carga el archivo MP3
            audio = AudioSegment.from_mp3(ruta_mp3)
            
            # Genera el nombre del archivo WAV temporal
            ruta_wav = ruta_mp3.replace('.mp3', '_temp.wav')
            
            # Exporta como WAV
            audio.export(ruta_wav, format="wav")
            
            return ruta_wav
        
        except Exception as e:
            raise Exception(f"Error al convertir MP3 a WAV: {str(e)}")
    
    def validar_formato_audio(self, ruta_archivo):
     
        # Formatos de audio soportados
        formatos_validos = ['.mp3', '.wav', '.ogg', '.flac', '.m4a']
        
        # Obtiene la extensión del archivo
        extension = os.path.splitext(ruta_archivo)[1].lower()
        
        # Verifica si la extensión está en la lista de formatos válidos
        return extension in formatos_validos
    
    def obtener_duracion_audio(self, ruta_archivo):
        
        try:
            # Carga el archivo de audio
            audio = AudioSegment.from_file(ruta_archivo)
            
            # Retorna la duración en segundos
            return len(audio) / 1000.0
        
        except Exception as e:
            return 0.0


# Función de prueba del módulo (solo para testing)
if __name__ == "__main__":
    convertidor = AudioConverter()
    
    ruta_prueba = "audio_prueba.mp3"
    
    if convertidor.validar_formato_audio(ruta_prueba):
        print("Formato válido")
        
        duracion = convertidor.obtener_duracion_audio(ruta_prueba)
        print(f"Duración: {duracion} segundos")
        
        texto = convertidor.convertir_audio_a_texto(ruta_prueba)
        print(f"Texto: {texto}")
    else:
        print("Formato no válido")