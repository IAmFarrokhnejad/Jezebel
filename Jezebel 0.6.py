import pyttsx3
import speech_recognition as sr
import time
import openai
import tkinter as tk
import ytmusicapi
import threading
import webbrowser
import re
import logging
import os


#Author: Morteza Farrokhnejad
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

openai.api_key = "KEY GOES HERE"  # OPENAI API KEY GOES HERE openai.apikey
engine = pyttsx3.init()
ytmusic = ytmusicapi.YTMusic()

Blocked = False  # Block requests; used for opting out of speech recognition
continuous_listening = False  # Toggle for continuous listening mode


def generate_response(prompt):  # Fixed: genereateResponse should be generateResponse
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=4000,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return "I'm having trouble generating a response right now."


def speak_generated(text):  # Speech synthesis/ text-to-speech
    try:
        engine.setProperty("voice", engine.getProperty("voices")[1])
        if engine.isBusy():
            engine.stop()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        logging.error(f"Error in TTS: {e}")


def recognize_speech():  # Recognize speech and generate response accordingly
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.1)
            audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            stop_listening()
            return
        except Exception as e:
            logging.error(f"Error capturing audio: {e}")
            return

    if not Blocked:
        try:
            inp = recognizer.recognize_google(audio).upper()
            logging.info(f"User input: {inp}")

            if re.match("^PLAY", inp):
                song_query = re.sub("^PLAY", "", inp)
                response = play_song(song_query)
            elif re.match("^OPEN", inp):
                url_query = re.sub("^OPEN", "", inp)
                response = open_website(url_query)
            elif re.match("^RUN", inp):
                command_query = re.sub("^RUN", "", inp)
                response = run_command(command_query)
            else:
                response = generate_response(inp)
                user_input_label.config(text=f"You: {inp.lower()}\n")

            jezebel_response_label.config(text=f"Jezebel: {response}")
        except sr.UnknownValueError:
            response = "I couldn't understand that."
            logging.warning("Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            response = f"Speech Recognition request failed; {e}"
            logging.error(f"Speech Recognition request error: {e}")

        speak_generated(response)

        if not continuous_listening:
            start_button.config(state="normal")
            stop_button.config(state="disabled")


def handle_speech():  # Start speech recognition thread
    start_button.config(state="disabled")
    stop_button.config(state="normal")
    tts_thread = threading.Thread(target=recognize_speech)
    tts_thread.start()


def start_listening():  # Start listening for commands
    global Blocked
    Blocked = False
    jezebel_response_label.config(text="Jezebel: Listening...")
    get_input_thread = threading.Thread(target=handle_speech)
    get_input_thread.start()


def stop_listening():  # Stop listening for commands
    global Blocked
    Blocked = True
    jezebel_response_label.config(text="Stopped listening.")
    start_button.config(state="normal")
    stop_button.config(state="disabled")


def toggle_continuous_listening():  # Toggle continuous listening mode
    global continuous_listening
    continuous_listening = not continuous_listening
    mode = "Continuous" if continuous_listening else "Single"
    continuous_button.config(text=f"Mode: {mode}")
    jezebel_response_label.config(text=f"Listening mode set to {mode}.")


def play_song(query):
    try:
        search_results = ytmusic.search(query, filter="songs", limit=1)
        if search_results:
            song = search_results[0]
            song_url = f"https://music.youtube.com/watch?v={song['videoId']}"
            webbrowser.open(song_url)
            return f"Now playing: {song['title']}"
        else:
            return "No search results found."
    except Exception as e:
        logging.error(f"Error searching song: {e}")
        return "I'm having trouble finding the song."


def open_website(query):
    try:
        url = f"https://www.google.com/search?q={query.strip()}"
        webbrowser.open(url)
        return f"Opening website related to: {query.strip()}"
    except Exception as e:
        logging.error(f"Error opening website: {e}")
        return "I couldn't open the website."


def run_command(command):
    try:
        os.system(command)
        return f"Executed command: {command.strip()}"
    except Exception as e:
        logging.error(f"Error running command: {e}")
        return "I couldn't run the command."


root = tk.Tk()
root.title("Jezebel Assistant")

start_button = tk.Button(root, text="Start", command=start_listening)
start_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop_listening, state=tk.DISABLED)
stop_button.pack()

continuous_button = tk.Button(root, text="Mode: Single", command=toggle_continuous_listening)
continuous_button.pack()

user_input_label = tk.Label(root, text="You:")
user_input_label.pack()

jezebel_response_label = tk.Label(root, text="Jezebel:")
jezebel_response_label.pack()

root.mainloop()
