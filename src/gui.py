
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import os
import threading

class Application:

    
    def __init__(self, master, audio_converter, encryptor):

        self.master = master
        self.audio_converter = audio_converter
        self.encryptor = encryptor
        
        # Configuración de la ventana principal
        self.master.title("Conversor de Audio a Texto con Criptografía")
        self.master.geometry("800x750")
        self.master.resizable(False, False)
        
      
        self.ruta_archivo = ""
        
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
       
    
        titulo = tk.Label(
            self.master,
            text="Conversor de Audio a Texto con Criptografía",
            font=("Arial", 16, "bold"),
            bg="#1237db",
            fg="white",
            pady=15
        )
        titulo.pack(fill=tk.X)
        
        frame_archivo = tk.LabelFrame(
            self.master,
            text=" ARCHIVO DE AUDIO",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        frame_archivo.pack(fill=tk.X, padx=20, pady=10)
        
        # Frame para la ruta y el botón
        frame_ruta = tk.Frame(frame_archivo)
        frame_ruta.pack(fill=tk.X, pady=5)
        
        # Label para mostrar la ruta
        tk.Label(frame_ruta, text="Ruta:", font=("Arial", 10)).pack(side=tk.LEFT)
        
        # Entry para mostrar la ruta del archivo
        self.entry_ruta = tk.Entry(frame_ruta, width=50, font=("Arial", 10))
        self.entry_ruta.pack(side=tk.LEFT, padx=5)
        
        # Botón para buscar archivo
        self.btn_buscar = tk.Button(
            frame_ruta,
            text="Buscar Archivo",
            command=self._buscar_archivo_thread,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        self.btn_buscar.pack(side=tk.LEFT, padx=5)
        
        # Label para mostrar información del archivo
        self.label_info_archivo = tk.Label(
            frame_archivo,
            text="No hay archivo seleccionado",
            font=("Arial", 9),
            fg="gray"
        )
        self.label_info_archivo.pack(pady=5)
        
    
        self.progress_frame = tk.Frame(self.master)
        self.progress_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='indeterminate',
            length=760
        )
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="",
            font=("Arial", 9, "italic"),
            fg="#66ea7c"
        )
        
        
        frame_texto = tk.LabelFrame(
            self.master,
            text="📝 TEXTO CONVERTIDO",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        frame_texto.pack(fill=tk.BOTH, padx=20, pady=10, expand=True)
        
        # Área de texto con scroll para mostrar el texto convertido
        self.texto_convertido = scrolledtext.ScrolledText(
            frame_texto,
            height=6,
            font=("Arial", 10),
            wrap=tk.WORD
        )
        self.texto_convertido.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Botón para convertir a texto
        self.btn_convertir = tk.Button(
            frame_texto,
            text=" Convertir a Texto",
            command=self._convertir_a_texto_thread,
            bg="#2196F3",
            fg="white",
            font=("Arial", 11, "bold"),
            cursor="hand2",
            pady=10
        )
        self.btn_convertir.pack(pady=5)
        
        # ===== SECCIÓN DE TEXTO ENCRIPTADO =====
        frame_encriptado = tk.LabelFrame(
            self.master,
            text="TEXTO ENCRIPTADO",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        frame_encriptado.pack(fill=tk.BOTH, padx=20, pady=10, expand=True)
        
        # Área de texto con scroll para mostrar el texto encriptado
        self.texto_encriptado = scrolledtext.ScrolledText(
            frame_encriptado,
            height=6,
            font=("Arial", 10),
            wrap=tk.WORD
        )
        self.texto_encriptado.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Frame para los botones de encriptación
        frame_botones_encriptar = tk.Frame(frame_encriptado)
        frame_botones_encriptar.pack(pady=5)
        
        # Botón para encriptar
        self.btn_encriptar = tk.Button(
            frame_botones_encriptar,
            text="Encriptar Texto",
            command=self._encriptar_texto,
            bg="#FF9800",
            fg="white",
            font=("Arial", 11, "bold"),
            cursor="hand2",
            padx=15
        )
        self.btn_encriptar.pack(side=tk.LEFT, padx=5)
        
        # Botón para desencriptar
        self.btn_desencriptar = tk.Button(
            frame_botones_encriptar,
            text=" Desencriptar",
            command=self._desencriptar_texto,
            bg="#9C27B0",
            fg="white",
            font=("Arial", 11, "bold"),
            cursor="hand2",
            padx=15
        )
        self.btn_desencriptar.pack(side=tk.LEFT, padx=5)
        
        # Botón para limpiar
        self.btn_limpiar = tk.Button(
            frame_botones_encriptar,
            text=" Limpiar",
            command=self._limpiar_todo,
            bg="#F44336",
            fg="white",
            font=("Arial", 11, "bold"),
            cursor="hand2",
            padx=15
        )
        self.btn_limpiar.pack(side=tk.LEFT, padx=5)
        
        # ===== BARRA DE ESTADO =====
        self.label_estado = tk.Label(
            self.master,
            text="Estado: Listo",
            font=("Arial", 9),
            bg="#E0E0E0",
            anchor=tk.W,
            padx=10,
            pady=5
        )
        self.label_estado.pack(fill=tk.X, side=tk.BOTTOM)
    
    def _mostrar_progreso(self, mensaje):
        
        self.progress_label.config(text=mensaje)
        self.progress_label.pack(pady=2)
        self.progress_bar.pack(fill=tk.X, pady=5)
        self.progress_bar.start(10)
    
    def _ocultar_progreso(self):

        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.progress_label.pack_forget()
    
    def _deshabilitar_botones(self):
        """
        Deshabilita todos los botones durante el procesamiento.
        """
        self.btn_buscar.config(state=tk.DISABLED)
        self.btn_convertir.config(state=tk.DISABLED)
        self.btn_encriptar.config(state=tk.DISABLED)
        self.btn_desencriptar.config(state=tk.DISABLED)
        self.btn_limpiar.config(state=tk.DISABLED)
    
    def _habilitar_botones(self):
        """
        Habilita todos los botones después del procesamiento.
        """
        self.btn_buscar.config(state=tk.NORMAL)
        self.btn_convertir.config(state=tk.NORMAL)
        self.btn_encriptar.config(state=tk.NORMAL)
        self.btn_desencriptar.config(state=tk.NORMAL)
        self.btn_limpiar.config(state=tk.NORMAL)
    
    def _buscar_archivo_thread(self):
        """
        Inicia un hilo para buscar y cargar el archivo sin congelar la interfaz.
        """
        thread = threading.Thread(target=self._buscar_archivo)
        thread.daemon = True
        thread.start()
    
    def _buscar_archivo(self):
       
        # Deshabilita botones durante el procesamiento
        self.master.after(0, self._deshabilitar_botones)
        self.master.after(0, lambda: self._actualizar_estado("Cargando archivo..."))
        self.master.after(0, lambda: self._mostrar_progreso(" Procesando archivo..."))
        
        # Abre el diálogo de selección de archivo
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de audio",
            filetypes=[
                ("Archivos de Audio", "*.mp3 *.wav *.ogg *.flac *.m4a"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        # Si se seleccionó un archivo
        if ruta:
            # Valida el formato del archivo
            if self.audio_converter.validar_formato_audio(ruta):
                self.ruta_archivo = ruta
                self.master.after(0, lambda: self.entry_ruta.delete(0, tk.END))
                self.master.after(0, lambda: self.entry_ruta.insert(0, ruta))
                
                # Obtiene información del archivo
                nombre_archivo = os.path.basename(ruta)
                extension = os.path.splitext(ruta)[1]
                duracion = self.audio_converter.obtener_duracion_audio(ruta)
                
                # Actualiza la información del archivo
                info = f"Archivo: {nombre_archivo} | Formato: {extension} | Duración: {duracion:.2f}s"
                self.master.after(0, lambda: self.label_info_archivo.config(text=info, fg="green"))
                self.master.after(0, lambda: self._actualizar_estado("Archivo cargado correctamente"))
            else:
                self.master.after(0, lambda: messagebox.showerror(
                    "Formato no válido",
                    "El formato del archivo no es compatible.\nFormatos soportados: MP3, WAV, OGG, FLAC, M4A"
                ))
        
        # Oculta progreso y habilita botones
        self.master.after(0, self._ocultar_progreso)
        self.master.after(0, self._habilitar_botones)
    
    def _convertir_a_texto_thread(self):
       
        thread = threading.Thread(target=self._convertir_a_texto)
        thread.daemon = True
        thread.start()
    
    def _convertir_a_texto(self):
        
        # Verifica que haya un archivo seleccionado
        if not self.ruta_archivo:
            self.master.after(0, lambda: messagebox.showwarning("Sin archivo", "Por favor, seleccione un archivo de audio primero."))
            return
        
        # Deshabilita botones durante el procesamiento
        self.master.after(0, self._deshabilitar_botones)
        self.master.after(0, lambda: self._actualizar_estado("Convirtiendo audio a texto.."))
        self.master.after(0, lambda: self._mostrar_progreso(" Procesando audio... Por favor espere, esto puede tomar un momento."))
        
        # Convierte el audio a texto
        texto = self.audio_converter.convertir_audio_a_texto(self.ruta_archivo)
        
        # Muestra el texto en el área de texto convertido
        self.master.after(0, lambda: self.texto_convertido.delete(1.0, tk.END))
        self.master.after(0, lambda: self.texto_convertido.insert(1.0, texto))
        
        # Oculta progreso, actualiza estado y habilita botones
        self.master.after(0, self._ocultar_progreso)
        self.master.after(0, lambda: self._actualizar_estado("Conversión completada"))
        self.master.after(0, self._habilitar_botones)
    
    def _encriptar_texto(self):
        
        # Obtiene el texto del área de texto convertido
        texto = self.texto_convertido.get(1.0, tk.END).strip()
        
        # Verifica que haya texto para encriptar
        if not texto:
            messagebox.showwarning("Sin texto", "No hay texto para encriptar.")
            return
        
        # Encripta el texto
        texto_encriptado = self.encryptor.encriptar_texto(texto)
        
        # Muestra el texto encriptado
        self.texto_encriptado.delete(1.0, tk.END)
        self.texto_encriptado.insert(1.0, texto_encriptado)
        
        # Actualiza el estado
        self._actualizar_estado("Texto encriptado correctamente")
    
    def _desencriptar_texto(self):
       
        # Obtiene el texto encriptado
        texto_encriptado = self.texto_encriptado.get(1.0, tk.END).strip()
        
        # Verifica que haya texto para desencriptar
        if not texto_encriptado:
            messagebox.showwarning("Sin texto", "No hay texto encriptado para desencriptar.")
            return
        
        # Desencripta el texto
        texto_desencriptado = self.encryptor.desencriptar_texto(texto_encriptado)
        
        # Muestra el texto desencriptado
        self.texto_convertido.delete(1.0, tk.END)
        self.texto_convertido.insert(1.0, texto_desencriptado)
        
        # Actualiza el estado
        self._actualizar_estado("Texto desencriptado correctamente")
    
    def _limpiar_todo(self):
        
        # Limpia los campos de texto
        self.texto_convertido.delete(1.0, tk.END)
        self.texto_encriptado.delete(1.0, tk.END)
        self.entry_ruta.delete(0, tk.END)
        
        # Resetea las variables
        self.ruta_archivo = ""
        self.label_info_archivo.config(text="No hay archivo seleccionado", fg="gray")
        
        # Actualiza el estado
        self._actualizar_estado("Interfaz limpiada")
    
    def _actualizar_estado(self, mensaje):
       
        self.label_estado.config(text=f"Estado: {mensaje}")