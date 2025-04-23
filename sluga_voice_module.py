import whisper
import sounddevice as sd
import numpy as np
import wave
import threading

model = None  
is_recording = False  # Global state variable

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
    global is_recording
    is_recording = True  # Move this line outside the thread, right at the start

    def run():
        print("Recording started...")

        audio_data = sd.rec(int(SAM_RT * DUR), samplerate=SAM_RT, channels=CHN, dtype=np.int16)
        sd.wait()

        global is_recording
        is_recording = False
        print("Recording stopped.")

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


def get_audio_state():
    return is_recording
