from tkinter import filedialog
import tkinter as tk

def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de Tkinter
    ruta_archivo = filedialog.askopenfilename(
        title="Selecciona un archivo de audio",
        filetypes=[("Archivos de audio", "*.mp3 *.flac *.wav")]
    )
    return ruta_archivo