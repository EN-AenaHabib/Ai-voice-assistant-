import tkinter as tk
import threading
import speech_recognition as sr
import keyboard  # pip install keyboard
from output.assistant_response import assistant_reply
from output.open_website import open_website  # NEW for website opening

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
            label_status.config(text="Listening... Press Ctrl+X to stop")

            accumulated_text = ""

            while listening:
                try:
                    audio = recognizer.listen(source, timeout=None, phrase_time_limit=None)
                    text = recognizer.recognize_google(audio)
                    accumulated_text += " " + text
                    label_result.config(text=accumulated_text.strip())

                    # Website opening check
                    if text.lower().startswith("open"):
                        response = open_website(text)
                    else:
                        response = assistant_reply(text)

                    label_response.config(text=response)

                except sr.UnknownValueError:
                    pass
                except sr.RequestError as e:
                    label_result.config(text=f"API error: {e}")
                    break

            label_status.config(text="Stopped Listening")

    threading.Thread(target=listen).start()

def monitor_stop():
    global listening
    while True:
        if keyboard.is_pressed('ctrl+x'):
            listening = False
            break

# GUI setup
window = tk.Tk()
window.title("AI Voice Assistant")
window.geometry("600x400")

label_title = tk.Label(window, text="Voice Assistant", font=("Arial", 16))
label_title.pack(pady=10)

btn_listen = tk.Button(window, text="Start Listening", font=("Arial", 12), command=start_listening)
btn_listen.pack(pady=10)

label_status = tk.Label(window, text="Status: Idle", font=("Arial", 12))
label_status.pack(pady=10)

label_result = tk.Label(window, text="", wraplength=550, font=("Arial", 11), justify="left", fg="blue")
label_result.pack(pady=10)

label_response = tk.Label(window, text="", wraplength=550, font=("Arial", 11), justify="left", fg="green")
label_response.pack(pady=10)

threading.Thread(target=monitor_stop, daemon=True).start()

window.mainloop()
