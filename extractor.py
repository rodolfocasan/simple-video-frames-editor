# extractor.py
import os
import re
import cv2
from pathlib import Path
from typing import Union, List

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

from utils import verificar_rutas_almacenamiento










'''
>>> Funciones utilitarias
'''
def extraer_frames(video_paths: Union[str, List[str]], frame_interval: int = 1) -> dict:
    """
    Extrae frames de uno o varios videos, creando carpetas específicas para cada uno.
    
    Args:
        video_paths: Puede ser una sola ruta (str) o una lista de rutas de videos
        frame_interval: Intervalo de frames a guardar (1 = todos los frames)
    
    Returns:
        dict: Diccionario con el conteo de frames guardados por cada video
    """
    # Si no se seleccionó ningún video, terminar
    if not video_paths:
        print("No se seleccionó ningún video.")
        return {}
    
    # Convertir entrada única a lista para procesamiento uniforme
    if isinstance(video_paths, str):
        video_paths = [video_paths]
    
    # Verificar ruta base de almacenamiento
    storage_path = verificar_rutas_almacenamiento()
    base_output_path = Path(storage_path)
    
    # Diccionario para almacenar resultados
    results = {}
    
    # Procesar cada video
    for video_path in video_paths:
        # Obtener nombre del video sin extensión para crear la carpeta
        video_name = Path(video_path).stem
        
        # Crear carpeta específica para este video
        video_output_path = base_output_path / video_name
        video_output_path.mkdir(parents=True, exist_ok=True)
        
        print("\n[ Extracción de FRAMES de vídeo ]")
        print(f" - Procesando vídeo: {video_name}")
        
        # Abrir el video
        video = cv2.VideoCapture(video_path)
        
        # Verificar si el video se abrió correctamente
        if not video.isOpened():
            print(f" - Error al abrir el video: {video_path}")
            results[video_name] = 0
            continue
        
        # Obtener información del video
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = video.get(cv2.CAP_PROP_FPS)
        
        print(f" - Total frames en el video: {total_frames}")
        print(f" - FPS: {fps}\n")
        
        frame_count = 0
        saved_count = 0
        
        while True:
            # Leer el siguiente frame
            success, frame = video.read()
            
            if not success:
                break
                
            # Guardar frame según el intervalo especificado
            if frame_count % frame_interval == 0:
                # Generar nombre del archivo
                frame_filename = video_output_path / f"frame_{frame_count:06d}.png"
                
                # Guardar el frame como PNG
                cv2.imwrite(str(frame_filename), frame)
                saved_count += 1
                
                # Mostrar progreso
                if saved_count % 100 == 0:
                    print(f"(OK) Frames guardados para {video_name}: {saved_count}")
            
            frame_count += 1
        
        # Liberar recursos
        video.release()
        
        print(f"\n(OK) Proceso completado para {video_name}.")
        print(f"Se guardaron {saved_count} frames en {video_output_path}")
        results[video_name] = saved_count
    return results


def unir_frames_en_video(frames_path: Union[str, Path], output_path: Union[str, Path] = None, fps: int = 30) -> bool:
    """
    Une una secuencia de frames en un archivo de video.
    
    Args:
        frames_path: Ruta de la carpeta que contiene los frames
        output_path: Ruta donde se guardará el video. Si es None, se usa la misma carpeta
        fps: Frames por segundo del video resultante
    
    Returns:
        bool: True si el proceso fue exitoso, False en caso contrario
    """
    try:
        frames_path = Path(frames_path)
        
        # Verificar que la carpeta existe
        if not frames_path.exists() or not frames_path.is_dir():
            print(f"Error: La carpeta {frames_path} no existe o no es válida")
            return False
            
        # Listar todos los archivos PNG en la carpeta
        frames = sorted(frames_path.glob("frame_*.png"))
        if not frames:
            print(f"Error: No se encontraron frames en la carpeta {frames_path}")
            return False
            
        # Leer el primer frame para obtener dimensiones
        first_frame = cv2.imread(str(frames[0]))
        if first_frame is None:
            print(f"Error: No se pudo leer el primer frame")
            return False
            
        height, width = first_frame.shape[:2]
        
        # Si no se especifica ruta de salida, usar la misma carpeta
        if output_path is None:
            output_path = frames_path / f"output_{fps}fps.mp4"
        else:
            output_path = Path(output_path)
            
        # Crear el escritor de video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        total_frames = len(frames)
        print(f"\n[ Uniendo frames en video ]")
        print(f" - Carpeta de origen: {frames_path}")
        print(f" - Total frames: {total_frames}")
        print(f" - FPS objetivo: {fps}")
        print(f" - Resolución: {width}x{height}")
        
        # Procesar cada frame
        for i, frame_path in enumerate(frames, 1):
            frame = cv2.imread(str(frame_path))
            if frame is not None:
                out.write(frame)
                
                # Mostrar progreso cada 100 frames
                if i % 100 == 0:
                    print(f"(OK) Procesando frame {i}/{total_frames}")
        
        # Liberar recursos
        out.release()
        
        print(f"\n(OK) Video creado exitosamente en: {output_path}")
        return True
    except Exception as e:
        print(f"Error durante la creación del video: {str(e)}")
        return False










'''
>>> Funciones para interacción con UI
'''
def opcion_seleccionar_videos():
    """Función para seleccionar videos desde una ventana modal."""

    def seleccionar_videos() -> List[str]:
        """Abre un diálogo de selección de archivos de video."""
        filetypes = [('Archivos de video', '*.mp4;*.avi;*.mkv;*.mov;*.wmv'), ('Todos los archivos', '*.*')]
        video_paths = filedialog.askopenfilenames(title='Selecciona los videos para extraer frames', filetypes=filetypes)
        return list(video_paths)

    def process_videos(parent):
        """Función que procesa los videos seleccionados."""
        videos = seleccionar_videos()
        if videos:
            log_area.configure(state='normal')  # Habilitar el área de log para escribir en ella
            log_area.insert(tk.END, f"Procesando {len(videos)} video(s)...\n")
            log_area.see(tk.END)
            parent.update_idletasks()  # Actualizar la interfaz para mostrar el log

            # Procesar cada video y mostrar los resultados en tiempo real
            resultados = extraer_frames(videos)
            for name, count in resultados.items():
                log_area.insert(tk.END, f"{name}: {count} frames extraídos\n")
                log_area.see(tk.END)
                parent.update_idletasks()  # Actualizar para cada entrada de log
            
            # Mostrar resumen en ventana emergente
            summary = "\n".join(f"{name}: {count} frames extraídos" for name, count in resultados.items())
            messagebox.showinfo("Resumen de extracción", f"Resumen de extracción:\n{summary}")
            log_area.insert(tk.END, "Extracción completada.\n")
            log_area.see(tk.END)
            parent.update_idletasks()
        else:
            messagebox.showinfo("Selección vacía", "No se seleccionó ningún video.")
            log_area.configure(state='normal')
            log_area.insert(tk.END, "No se seleccionó ningún video.\n")
            log_area.see(tk.END)
            parent.update_idletasks()
        
        log_area.configure(state='disabled')  # Deshabilitar el área de log para evitar edición
        parent.destroy()  # Cerrar la ventana modal al terminar

    # Crear ventana modal
    root = tk.Toplevel()
    root.title("Seleccionar Videos")
    root.geometry("500x400")
    root.minsize(400, 300)
    root.transient()
    root.grab_set()

    # Colores del tema oscuro
    colors = {
        'bg': '#1E1E1E',
        'secondary_bg': '#252526',
        'accent': '#007ACC',
        'text': '#FFFFFF',
        'text_secondary': '#CCCCCC'
    }
    root.configure(bg=colors['bg'])

    # Frame principal (responsive)
    main_frame = tk.Frame(root, bg=colors['bg'], padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    main_frame.grid_columnconfigure(0, weight=1)

    # Área de log
    log_area = ScrolledText(
        main_frame,
        font=("Helvetica", 9),
        bg=colors['secondary_bg'],
        fg=colors['text_secondary'],
        height=6,
        wrap=tk.WORD,
        state='disabled',  # Inicia deshabilitada para evitar edición
        relief="flat",
        borderwidth=0
    )
    log_area.grid(row=0, column=0, sticky="nsew", pady=(0, 15))

    # Etiqueta de título
    title_label = tk.Label(
        main_frame,
        text="Selecciona Videos para Extraer Frames",
        font=("Helvetica", 16, "bold"),
        bg=colors['bg'],
        fg=colors['text'],
        pady=10
    )
    title_label.grid(row=1, column=0, sticky="n", pady=(0, 15))

    # Mensaje de instrucción
    instruction_label = tk.Label(
        main_frame,
        text="Haz clic en el botón para seleccionar uno o varios videos",
        font=("Helvetica", 10),
        bg=colors['bg'],
        fg=colors['text_secondary'],
        pady=5
    )
    instruction_label.grid(row=2, column=0, sticky="ew")

    # Botón para seleccionar videos
    select_button = tk.Button(
        main_frame,
        text="Seleccionar Videos",
        command=lambda: process_videos(root),
        font=("Helvetica", 11, "bold"),
        bg=colors['accent'],
        fg=colors['text'],
        activebackground=colors['bg'],
        activeforeground=colors['text'],
        relief="flat",
        cursor="hand2",
        pady=10
    )
    select_button.grid(row=3, column=0, pady=20, sticky="ew")

    # Etiqueta de estado (para mostrar mensajes)
    status_label = tk.Label(
        main_frame,
        text="Esperando selección...",
        font=("Helvetica", 9),
        bg=colors['bg'],
        fg=colors['text_secondary'],
    )
    status_label.grid(row=4, column=0, sticky="ew", pady=(10, 0))

    # Ajustar el diseño para que sea responsive
    main_frame.grid_rowconfigure(0, weight=1)  # El área de log puede expandirse
    main_frame.grid_rowconfigure(3, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)

    # Configurar área de log como no editable inicialmente
    log_area.configure(state='disabled')


def opcion_seleccionar_carpeta_y_fps():
    """Función para seleccionar una carpeta de frames y configurar FPS desde una ventana modal."""

    def procesar(parent, fps, folder):
        """Función que une frames en un video."""
        try:
            fps = int(fps_entry.get())
            if fps <= 0:
                raise ValueError("Los FPS deben ser un número positivo")
        except ValueError:
            messagebox.showerror("Error", "FPS inválido. Ingrese un número positivo.")
            return
        
        if not folder.get():
            messagebox.showerror("Error", "Seleccione una carpeta de frames.")
            return

        # Notificar al usuario que el proceso ha comenzado
        status_label.config(text="Procesando video...", fg=colors['accent'])
        parent.update_idletasks()  # Actualizar la interfaz para mostrar el mensaje

        # Intentar unir frames y mostrar resultados
        success = unir_frames_en_video(folder.get(), fps=fps)
        if success:
            messagebox.showinfo("Éxito", "Video creado exitosamente.")
        else:
            messagebox.showerror("Error", "No se pudo crear el video.")
        
        # Restablecer el estado después del procesamiento
        status_label.config(text="")
        parent.destroy()  # Cerrar la ventana modal al terminar

    def seleccionar_carpeta():
        """Función para seleccionar una carpeta y actualizar la entrada."""
        carpeta = filedialog.askdirectory()
        if carpeta:
            folder_var.set(carpeta)  # Mostrar la ruta seleccionada en el campo de entrada

    # Crear ventana modal
    root = tk.Toplevel()
    root.title("Unir Frames en Video")
    root.geometry("500x300")
    root.minsize(400, 250)
    root.transient()
    root.grab_set()

    # Colores del tema oscuro
    colors = {
        'bg': '#1E1E1E',
        'secondary_bg': '#252526',
        'accent': '#007ACC',
        'text': '#FFFFFF',
        'text_secondary': '#CCCCCC'
    }
    root.configure(bg=colors['bg'])

    # Variables de entrada
    folder_var = tk.StringVar()

    # Frame principal (responsive)
    main_frame = tk.Frame(root, bg=colors['bg'], padx=20, pady=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    main_frame.grid_columnconfigure(1, weight=1)  # Segunda columna expandible

    # Etiqueta de título
    title_label = tk.Label(
        main_frame,
        text="Convertidor de Frames a Video",
        font=("Helvetica", 16, "bold"),
        bg=colors['bg'],
        fg=colors['text'],
        pady=10
    )
    title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))

    # Carpeta de frames
    folder_label = tk.Label(
        main_frame,
        text="Carpeta de frames:",
        font=("Helvetica", 10),
        bg=colors['bg'],
        fg=colors['text_secondary']
    )
    folder_label.grid(row=1, column=0, sticky="w", pady=5)

    folder_entry = tk.Entry(
        main_frame,
        textvariable=folder_var,
        font=("Helvetica", 10),
        bg="#FFFFFF",  # Fondo blanco para mejor legibilidad
        fg="#000000",  # Texto negro para contraste
        relief="flat"
    )
    folder_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0))

    folder_button = tk.Button(
        main_frame,
        text="Seleccionar Carpeta",
        command=seleccionar_carpeta,
        font=("Helvetica", 9, "bold"),
        bg=colors['accent'],
        fg=colors['text'],
        activebackground=colors['bg'],
        activeforeground=colors['text'],
        relief="flat",
        cursor="hand2"
    )
    folder_button.grid(row=1, column=2, padx=(10, 0), pady=5)

    # FPS
    fps_label = tk.Label(
        main_frame,
        text="FPS deseados:",
        font=("Helvetica", 10),
        bg=colors['bg'],
        fg=colors['text_secondary']
    )
    fps_label.grid(row=2, column=0, sticky="w", pady=5)

    fps_entry = tk.Entry(
        main_frame,
        width=10,
        font=("Helvetica", 10),
        bg=colors['secondary_bg'],
        fg=colors['text'],
        relief="flat",
        justify="center"
    )
    fps_entry.insert(0, "30")  # Valor por defecto
    fps_entry.grid(row=2, column=1, sticky="w", padx=(10, 0))

    # Botón de proceso
    process_button = tk.Button(
        main_frame,
        text="Crear Video",
        command=lambda: procesar(root, fps_entry.get(), folder_var),
        font=("Helvetica", 11, "bold"),
        bg=colors['accent'],
        fg=colors['text'],
        activebackground=colors['bg'],
        activeforeground=colors['text'],
        relief="flat",
        cursor="hand2",
        pady=10
    )
    process_button.grid(row=3, column=0, columnspan=3, pady=(20, 0), sticky="ew")

    # Etiqueta de estado para notificaciones en tiempo real
    status_label = tk.Label(
        main_frame,
        text="",
        font=("Helvetica", 10),
        bg=colors['bg'],
        fg=colors['text_secondary']
    )
    status_label.grid(row=4, column=0, columnspan=3, pady=(10, 0))

    # Ajustar el diseño para que sea responsive
    for i in range(4):
        main_frame.grid_rowconfigure(i, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)