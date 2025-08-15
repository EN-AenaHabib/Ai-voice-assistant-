import tkinter as tk
import threading
import speech_recognition as sr
import keyboard
from output.assistant_response import assistant_reply
from output.open_website import open_website
from output.open_file import open_folder_or_app
from output.close_file import handle_close_command  # ✅ Import closing logic

listening = False

# Folder aliases
folder_aliases = {
    "downloads": "Downloads", "download": "Downloads",
    "desktop": "Desktop", "pictures": "Pictures", "picture": "Pictures",
    "documents": "Documents", "document": "Documents",
    "music": "Music", "videos": "Videos"
}

# App aliases
app_aliases = {
    "word": "Microsoft Word", "ms word": "Microsoft Word",
    "excel": "Microsoft Excel", "ms excel": "Microsoft Excel",
    "powerpoint": "Microsoft PowerPoint", "ms powerpoint": "Microsoft PowerPoint",
    "chrome": "Google Chrome", "google chrome": "Google Chrome",
    "vlc": "VLC Media Player", "vlc player": "VLC Media Player"
}

# Closing keywords
closing_keywords = [
    "close", "closing", "shut", "shut down", "shut off",
    "terminate", "stop", "end", "exit", "kill"
]

def extract_target_name(text):
    """Extract target name (folder/app) from speech text."""
    text = text.lower()
    for alias, proper in {**folder_aliases, **app_aliases}.items():
        if alias in text:
            return proper
    if "open folder" in text:
        return text.split("open folder", 1)[-1].strip().title()
    if "open app" in text:
        return text.split("open app", 1)[-1].strip().title()
    if any(text.startswith(k) for k in ["open", "go to", "launch", "start"]):
        return text.split(maxsplit=1)[-1].title()
    return None

def is_close_command(text):
    return any(keyword in text.lower() for keyword in closing_keywords)

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

            while listening:
                try:
                    audio = recognizer.listen(source)
                    text = recognizer.recognize_google(audio)
                    label_result.config(text=text)

                    if is_close_command(text):
                        response = handle_close_command(text)  # ✅ Use close.py
                        label_response.config(text=response)
                        continue

                    target_name = extract_target_name(text)
                    if target_name:
                        response = open_folder_or_app(target_name)
                        if "not found" in str(response).lower():
                            response = open_website(text)
                    else:
                        if any(text.lower().startswith(v) for v in ["open", "go to", "launch", "start"]):
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

# GUI
window = tk.Tk()
window.title("AI Voice Assistant")
window.geometry("600x400")

label_title = tk.Label(window, text="Voice Assistant", font=("Arial", 16))
label_title.pack(pady=10)

btn_listen = tk.Button(window, text="Start Listening", font=("Arial", 12), command=start_listening)
btn_listen.pack(pady=10)

label_status = tk.Label(window, text="Status: Idle", font=("Arial", 12))
label_status.pack(pady=10)

label_result = tk.Label(window, text="", wraplength=550, font=("Arial", 11), fg="blue")
label_result.pack(pady=10)

label_response = tk.Label(window, text="", wraplength=550, font=("Arial", 11), fg="green")
label_response.pack(pady=10)

threading.Thread(target=monitor_stop, daemon=True).start()
window.mainloop()
