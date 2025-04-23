import whisper
import sounddevice as sd
import numpy as np
import wave
import threading

model = None  
state = False  # Initialize state as False

def load_model():
    global model
    print("Loading Whisper model...")
    model = whisper.load_model("base") 
    print("Model loaded successfully.")

threading.Thread(target=load_model, daemon=True).start()

SAM_RT = 16000  
CHN = 1 
DUR = 5  

def record_audio(callback):
    def run():
        global state
        state = True  
        print("\nListening...")
        audio_data = sd.rec(int(SAM_RT * DUR), samplerate=SAM_RT, channels=CHN, dtype=np.int16)
        sd.wait()
        state = False  

        filename = "temp_audio.wav"
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(CHN)
            wf.setsampwidth(2)  
            wf.setframerate(SAM_RT)
            wf.writeframes(audio_data.tobytes())

        result = model.transcribe(filename)
        text = result["text"]
        callback(text)
    threading.Thread(target=run, daemon=True).start()

def transcribe_audio(filename):
    result = model.transcribe(filename)
    return result["text"]

def record_and_transcribe(callback):
    def run():
        audio_file = record_audio()
        text = transcribe_audio(audio_file)
        callback(text)

    threading.Thread(target=run, daemon=True).start()

