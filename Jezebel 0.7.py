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
import requests
import json

#Author: Morteza Farrokhnejad
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

openai.api_key = "KEY GOES HERE"  # OPENAI API KEY GOES HERE
engine = pyttsx3.init()
ytmusic = ytmusicapi.YTMusic()

# External API Keys
weather_api_key = "KEY GOES HERE"  # OpenWeatherMap API key GOES HERE
news_api_key = "KEY GOES HERE"  #NewsAPI key GOES HERE

Blocked = False  # Block requests; used for opting out of speech recognition
continuous_listening = False  # Toggle for continuous listening mode
voice_enabled = True  # Toggle for voice feedback


# Core Functions
def generate_response(prompt):
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


def speak_generated(text):
    if not voice_enabled:
        return
    try:
        engine.setProperty("voice", engine.getProperty("voices")[1])
        if engine.isBusy():
            engine.stop()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        logging.error(f"Error in TTS: {e}")


def recognize_speech():
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
            elif re.match("^WEATHER", inp):
                city = re.sub("^WEATHER", "", inp)
                response = get_weather(city.strip())
            elif re.match("^NEWS", inp):
                response = get_news()
            elif re.match("^JOKE", inp):
                response = tell_joke()
            elif re.match("^REMINDER", inp):
                reminder_query = re.sub("^REMINDER", "", inp)
                response = set_reminder(reminder_query)
            elif re.match("^TIMER", inp):
                time_query = re.sub("^TIMER", "", inp)
                response = set_timer(time_query.strip())
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


def handle_speech():
    start_button.config(state="disabled")
    stop_button.config(state="normal")
    tts_thread = threading.Thread(target=recognize_speech)
    tts_thread.start()


def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            return f"Could not find weather data for {city}"

        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        return f"The current temperature in {city} is {temp}°C with {description}."
    except Exception as e:
        logging.error(f"Error getting weather: {e}")
        return "I couldn't fetch the weather."


def get_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
        response = requests.get(url)
        data = response.json()

        if "articles" in data:
            headlines = [article["title"] for article in data["articles"][:5]]
            return "Here are the top news headlines:\n" + "\n".join(headlines)
        else:
            return "I couldn't fetch the news."
    except Exception as e:
        logging.error(f"Error getting news: {e}")
        return "I couldn't fetch the news."


def tell_joke():
    try:
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        data = response.json()
        return f"{data['setup']}... {data['punchline']}"
    except Exception as e:
        logging.error(f"Error fetching joke: {e}")
        return "I couldn't fetch a joke."


def set_reminder(reminder):
    try:
        logging.info(f"Reminder set: {reminder}")
        return f"Reminder set: {reminder}"
    except Exception as e:
        logging.error(f"Error setting reminder: {e}")
        return "I couldn't set the reminder."


def set_timer(duration):
    try:
        seconds = int(re.findall(r'\d+', duration)[0])
        threading.Timer(seconds, timer_complete).start()
        return f"Timer set for {seconds} seconds."
    except Exception as e:
        logging.error(f"Error setting timer: {e}")
        return "I couldn't set the timer."


def timer_complete():
    speak_generated("Time's up!")


def toggle_voice_feedback():
    global voice_enabled
    voice_enabled = not voice_enabled
    voice_mode = "Voice On" if voice_enabled else "Voice Off"
    voice_toggle_button.config(text=voice_mode)


# GUI Setup
root = tk.Tk()
root.title("Jezebel Assistant")

start_button = tk.Button(root, text="Start", command=start_listening)
start_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop_listening, state=tk.DISABLED)
stop_button.pack()

continuous_button = tk.Button(root, text="Mode: Single", command=toggle_continuous_listening)
continuous_button.pack()

voice_toggle_button = tk.Button(root, text="Voice On", command=toggle_voice_feedback)
voice_toggle_button.pack()

user_input_label = tk.Label(root, text="You:")
user_input_label.pack()

jezebel_response_label = tk.Label(root, text="Jezebel:")
jezebel_response_label.pack()

root.mainloop()