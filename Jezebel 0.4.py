
"""
Changes:
    -Changed messages
    -Adjustment for ambient noise
"""

import pyttsx3
import speech_recognition as sr
import time
import openai
import tkinter as tk
import webbrowser
import threading

openai.api_key = "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"  # openai.apikey
engine = pyttsx3.init()

# Self-explanatory
def generateResponse(prompt):  # Fixed: genereateResponse should be generateResponse
    response = openai.Completion.create(  # Fixed: openai.Completion.create
        engine="text-davinci-003",  # Fixed: engine name
        prompt=prompt,
        max_tokens=4000,  # Fixed: maxTokens should be max_tokens
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text  # Fixed: choice should be choices, and text instead of ["text"]

def speakGenerated(text): #Speech synthesis/ text-to-speech
    ttsEngine = pyttsx3.init()
    ttsEngine.setProperty("voice", ttsEngine.getProperty("voices")[1])
    ttsEngine.say(text)
    ttsEngine.runAndWait()

def recognizeSpeech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            stop_listening()
            return
    try:
        input = recognizer.recognize_google(audio).upper()
        response = generateResponse(input)
        user_input_label.config(text=f"You: {input.lower()}")
        jezebel_response_label.config(text=f"Jezebel: {response}")
    except sr.UnknownValueError:
        response = "I couldn't understand that."
        jezebel_response_label.config(text=f"Jezebel: {response}")
    except sr.RequestError:
        response = "Something went wrong, please try again."
        jezibel_response_label.config(text=f"Jezebel: {response}")
    start_button.config(state="normal")
    stop_button.config(state="disabled")

def handleSpeech():
    start_button.config(state="disabled")
    stop_button.config(state="normal")
    ttsThread = threading.Thread(name="ttsThread",target=recognizeSpeech)
    ttsThread.start()
    return

def start_listening():

    start_button.config(state="disabled")
    stop_button.config(state="normal")
    jezibel_response_label.config(text="Jezebel: Listening...")    
    get_input_thread = threading.Thread(target=handleSpeech)
    get_input_thread.start()

def stop_listening():
    jezibel_response_label.config(text="Stopped listening.")
    start_button.config(state="normal")
    stop_button.config(state="disabled")

root = tk.Tk()
root.title("Jezebel Assistant")

start_button = tk.Button(root, text="Start", command=start_listening)
start_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop_listening, state=tk.DISABLED)
stop_button.pack()

user_input_label = tk.Label(root, text="You:")
user_input_label.pack()

jezebel_response_label = tk.Label(root, text="Jezebel:")
jezebel_response_label.pack()
root.mainloop()
