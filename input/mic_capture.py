import speech_recognition as sr
import threading

def wait_for_enter(stop_event):
    try:
        input(" Press Enter to stop listening...\n")
        stop_event.set()
    except KeyboardInterrupt:
        stop_event.set()

def capture_audio():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    stop_event = threading.Event()
    enter_thread = threading.Thread(target=wait_for_enter, args=(stop_event,))
    enter_thread.daemon = True  # Will exit when main program exits
    enter_thread.start()

    print("Listening... Speak now. (Ctrl+C or Enter to stop)")

    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)

            audio_data = None
            while not stop_event.is_set():
                try:
                    audio_data = recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    break  # Got audio, stop loop
                except sr.WaitTimeoutError:
                    continue

        if audio_data is None:
            print(" No speech detected.")
            return ""

        try:
            text = recognizer.recognize_google(audio_data)
            print(" You said:", text)
            return text
        except sr.UnknownValueError:
            print(" Couldn't understand the audio.")
            return ""
        except sr.RequestError as e:
            print(" API error:", e)
            return ""

    except KeyboardInterrupt:
        print("\n Listening manually stopped.")
        stop_event.set()
        return ""

