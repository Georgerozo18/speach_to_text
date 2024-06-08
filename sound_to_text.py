import soundfile as sf
import speech_recognition as sr

def transcribe_audio(file_path):
    # Leer el archivo de audio (MP3 o WAV)
    data, samplerate = sf.read(file_path)
    
    recognizer = sr.Recognizer()
    full_text = ""

    chunk_duration = 10  # Duración de cada fragmento de audio a procesar
    chunk_samples = int(chunk_duration * samplerate)

    total_chunks = (len(data) + chunk_samples - 1) // chunk_samples

    for i in range(total_chunks):
        start_sample = i * chunk_samples
        end_sample = min((i + 1) * chunk_samples, len(data))

        # Extraer el fragmento de audio
        chunk_data = data[start_sample:end_sample]

        # Guardar el fragmento temporalmente en un archivo WAV
        temp_wav_path = "temp_chunk.wav"
        sf.write(temp_wav_path, chunk_data, samplerate)

        # Cargar el fragmento de audio
        with sr.AudioFile(temp_wav_path) as source:
            audio_data = recognizer.record(source)

        # Reconocer el audio utilizando Google Web Speech API
        try:
            text = recognizer.recognize_google(audio_data, language='es-ES')
            # Dividir el texto en bloques de 13 palabras y agregar saltos de línea
            words = text.split()
            for j in range(0, len(words), 13):
                text_with_newlines = ' '.join(words[j:j+13])
                print(text_with_newlines)
                full_text += text_with_newlines + "\n"
        except sr.UnknownValueError:
            print(f"Fragmento {i + 1}/{total_chunks}: No se pudo entender el audio")
        except sr.RequestError as e:
            print(f"Fragmento {i + 1}/{total_chunks}: Error al conectar con Google Web Speech API; {e}")

        # Mostrar progreso
        progress = ((i + 1) / total_chunks) * 100
        print(f"Progreso: {progress:.2f}%")

    # Escribir la transcripción completa a un archivo de texto
    with open("transcripcion.txt", "w", encoding="utf-8") as f:
        f.write(full_text)

    print("Transcripción completa. Guardada en 'transcripcion.txt'.")

# Ejemplo de uso con un archivo MP3
transcribe_audio('./your_audio.wav')
