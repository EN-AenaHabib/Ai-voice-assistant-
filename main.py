import tkinter as tk
import threading
import speech_recognition as sr
import keyboard  # pip install keyboard

listening = False

def start_listening():
    global listening
    listening = True
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    def listen():
        global listening
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            label_status.config(text="🎤 Listening... Press Ctrl+X to stop")
            print("Listening...")

            accumulated_text = ""

            while listening:
                try:
                    audio = recognizer.listen(source, timeout=None, phrase_time_limit=None)
                    text = recognizer.recognize_google(audio)
                    accumulated_text += " " + text
                    label_result.config(text=accumulated_text.strip())
                    print("You said:", text)
                except sr.UnknownValueError:
                    pass  # Ignore unintelligible speech
                except sr.RequestError as e:
                    label_result.config(text=f"API error: {e}")
                    break

            label_status.config(text="⛔ Stopped Listening")

    threading.Thread(target=listen).start()

def monitor_stop():
    global listening
    while True:
        if keyboard.is_pressed('ctrl+x'):
            listening = False
            print("Ctrl+X pressed! Stopping...")
            break

# GUI setup
window = tk.Tk()
window.title("AI Voice Assistant (Python)")
window.geometry("500x300")

label_title = tk.Label(window, text="🎙️ Voice Assistant", font=("Arial", 16))
label_title.pack(pady=10)

btn_listen = tk.Button(window, text="Start Listening", font=("Arial", 12), command=start_listening)
btn_listen.pack(pady=10)

label_status = tk.Label(window, text="Status: Idle", font=("Arial", 12))
label_status.pack(pady=10)

label_result = tk.Label(window, text="", wraplength=450, font=("Arial", 11), justify="left")
label_result.pack(pady=10)

threading.Thread(target=monitor_stop, daemon=True).start()

window.mainloop()
