import wave
import contextlib
import speech_recognition as sr

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()

    # Obtener la duración del archivo de audio
    with contextlib.closing(wave.open(file_path, 'r')) as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / float(rate)

    # Definir tamaño del fragmento (en segundos)
    chunk_duration = 10  # Duración de cada fragmento de audio a procesar
    total_chunks = int(duration // chunk_duration) + 1

    full_text = ""
    
    for i in range(total_chunks):
        start_time = i * chunk_duration
        end_time = min((i + 1) * chunk_duration, duration)

        with wave.open(file_path, 'rb') as wf:
            wf.setpos(int(start_time * rate))
            chunk_data = wf.readframes(int((end_time - start_time) * rate))
            
            with wave.open("temp_chunk.wav", 'wb') as temp_wav:
                temp_wav.setnchannels(wf.getnchannels())
                temp_wav.setsampwidth(wf.getsampwidth())
                temp_wav.setframerate(rate)
                temp_wav.writeframes(chunk_data)

            with sr.AudioFile("temp_chunk.wav") as source:
                audio_data = recognizer.record(source)

            # Reconocer el audio utilizando Google Web Speech API
            try:
                text = recognizer.recognize_google(audio_data, language='es-ES')
                full_text += text + " "
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
# Utilizar el conversor de audio
transcribe_audio('./your_audio.wav')