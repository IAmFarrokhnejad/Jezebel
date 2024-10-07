
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

openai.api_key = "KEY GOES HERE"  # OPENAI API KEY GOES HERE

engine = pyttsx3.init()


#Author: Morteza Farrokhnejad


# Text to speech
def audioToText(filename):
    recognizer = sr.Recognizer()  # Fixed: recognizer should be Recognizer
    with sr.AudioFile(filename) as source:  # Fixed: audioFile should be AudioFile
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Skipping an unknown error...")


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


def speakGenerated(text):
    engine.say(text)
    engine.runAndWait()  # Fixed: runNWait should be runAndWait


def start_listening():
    while True:
        status_label.config(text="Listening...")
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()  # Fixed: recognizer should be Recognizer
            recognizer.adjust_for_ambient_noise(source, duration=0.2)  # Adjust for ambient noise, change the duration as needed
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.upper() == "JEZEBEL":
                    filename = "input.mp3"
                    status_label.config(text="Ask something...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()  # Fixed: recognizer should be Recognizer
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())  # Fixed: get_mp3_data should be get_wav_data

                        text = audioToText(filename)
                        if text:
                            user_input_label.config(text=f"You: {text}")

                            response = generateResponse(text)
                            jezebel_response_label.config(text=f"Jezebel: {response}")

                            speakGenerated(response)
            except Exception as e:
                status_label.config(text=f"An error might have occurred: {e}")
            status_label.config(text="Anything else?")
            


def stop_listening():
    status_label.config(text="Understood, let me know if you need anything else.")
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)


root = tk.Tk()
root.title("Jezebel Assistant")

start_button = tk.Button(root, text="Start", command=start_listening)
start_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop_listening, state=tk.DISABLED)
stop_button.pack()

user_input_label = tk.Label(root, text="You:")
user_input_label.pack()

jezebel_response_label = tk.Label(root, text="Nebula:")
jezebel_response_label.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
