
# voice_to_text.py
# This file is used to convert recorded audio into text using Google's Speech Recognition API.

# Import the speech_recognition library
import speech_recognition as sr

# Define a function to convert audio data into text
def convert_audio_to_text(audio_data):
    # Create a recognizer object
    recognizer = sr.Recognizer()

    try:
        # Try to recognize the speech using Google’s free speech recognition API
        text = recognizer.recognize_google(audio_data)

        # Print what the user said
        print(f" You said: {text}")

        # Return the recognized text
        return text

    # If the speech could not be understood
    except sr.UnknownValueError:
        print(" Could not understand the audio.")
        return ""

    # If there was an issue connecting to the API
    except sr.RequestError:
        print(" API unavailable or network error.")
        return ""
def save_text_to_file(text, filename="input_voice.txt"):
    with open(filename, "w") as file:
        file.write(text)

