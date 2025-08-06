import whisper

# Carga el modelo seleccionado
def cargar_modelo(nombre_modelo):
    return whisper.load_model(nombre_modelo)

# Transcribe el archivo de audio
def transcribir_audio(archivo_audio, modelo, idioma, traducir=False):
    # Determina la tarea (transcripción o traducción)
    task = "translate" if traducir else "transcribe"
    
    # Crea un diccionario de opciones
    options = {
        "language": idioma,
        "task": task
    }

    # Realiza la transcripción
    resultado = modelo.transcribe(archivo_audio, **options)
    
    return resultado["text"]