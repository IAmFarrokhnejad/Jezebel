
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
import ytmusicapi
import threading
import webbrowser
import re
#Author: Morteza Farrokhnejad
openai.api_key = "KEY GOES HERE"  # OPENAI API KEY GOES HERE
engine = pyttsx3.init()
ytmusic = ytmusicapi.YTMusic()

Blocked = False # Block requests; used for opting out of speech recognition

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
    engine.setProperty("voice", engine.getProperty("voices")[1])
    if engine.isBusy():
        engine.stop()
    engine.say(text)
    engine.runAndWait()

def recognizeSpeech(): # Recognize speech and generate response accordingly
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.1)
            audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            stop_listening()
            return
    if not Blocked:
        try:
            inp = recognizer.recognize_google(audio).upper()
            if re.match("^PLAY", inp):
                playSong(re.sub("^PLAY", "", inp))
                response = "Playing song..."
                jezebel_response_label.config(text=f"Jezebel: {response}")
            else:
                response = generateResponse(inp)
                user_input_label.config(text=f"You: {inp.lower()}\n")
                jezebel_response_label.config(text=f"Jezebel: {response}")
        except sr.UnknownValueError:
            response = "I couldn't understand that."
            jezebel_response_label.config(text=f"Jezebel: {response}")
        except sr.RequestError:
            response = "Something went wrong, please try again."
            jezebel_response_label.config(text=f"Jezebel: {response}")
        speakGenerated(response)
        start_button.config(state="normal")
        stop_button.config(state="disabled")

def handleSpeech(): # Start speech recognition thread
    start_button.config(state="disabled")
    stop_button.config(state="normal")
    ttsThread = threading.Thread(name="ttsThread",target=recognizeSpeech)
    ttsThread.start()
    return

def start_listening(): # Start listening for commands
    global Blocked
    Blocked = False
    start_button.config(state="disabled")
    stop_button.config(state="normal")
    jezebel_response_label.config(text="Jezebel: Listening...")    
    get_input_thread = threading.Thread(target=handleSpeech)
    get_input_thread.start()

def stop_listening(): # Stop listening for commands
    global Blocked
    Blocked = True
    jezebel_response_label.config(text="Stopped listening.")
    start_button.config(state="normal")
    stop_button.config(state="disabled")

def playSong(query):

    search_results = ytmusic.search(query, filter="songs", limit=5)

    if search_results:
        song = search_results[0]
        songUrl = f"https://music.youtube.com/watch?v={song['videoId']}"
        
        webbrowser.open(songUrl)

        return f"Now playing: {song['title']}"
    
    else:
        return "No search results found."

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
