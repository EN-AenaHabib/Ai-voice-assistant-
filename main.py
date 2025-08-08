import tkinter as tk
import threading
import speech_recognition as sr
import keyboard  # Make sure you install this: pip install keyboard

# Function to handle speech recognition
def start_listening():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    def listen():
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening started. Press Ctrl+X to stop.")
            label_status.config(text="🎤 Listening... Press Ctrl+X to stop")

            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=None)
                print("Got audio, recognizing...")
                text = recognizer.recognize_google(audio)
                print("You said:", text)
                label_result.config(text="You said: " + text)
            except sr.UnknownValueError:
                label_result.config(text="Could not understand audio.")
            except sr.RequestError as e:
                label_result.config(text=f"Could not request results; {e}")
            except Exception as e:
                label_result.config(text=f"Error: {e}")

            label_status.config(text="Stopped listening.")

    # Threading to avoid GUI freezing
    threading.Thread(target=listen).start()

# Stop listening when Ctrl+X is pressed
def monitor_stop():
    while True:
        if keyboard.is_pressed('ctrl+x'):
            print("Ctrl+X pressed! Stopping...")
            label_status.config(text="⛔ Stopped by Ctrl+X")
            break

# Tkinter GUI setup
window = tk.Tk()
window.title("AI Voice Assistant (Python)")
window.geometry("400x250")

label_title = tk.Label(window, text="🎙️ Voice Assistant", font=("Arial", 16))
label_title.pack(pady=10)

btn_listen = tk.Button(window, text="Start Listening", font=("Arial", 12), command=start_listening)
btn_listen.pack(pady=10)

label_status = tk.Label(window, text="Status: Idle", font=("Arial", 12))
label_status.pack(pady=10)

label_result = tk.Label(window, text="", wraplength=350, font=("Arial", 11))
label_result.pack(pady=10)

# Start Ctrl+X monitor thread
threading.Thread(target=monitor_stop, daemon=True).start()

window.mainloop()

