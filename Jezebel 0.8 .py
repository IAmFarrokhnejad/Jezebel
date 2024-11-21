import os
import re
import json
import logging
import threading
import webbrowser
import requests
import tkinter as tk
import pyttsx3
import speech_recognition as sr
import openai
from dotenv import load_dotenv
import ytmusicapi

# Load environment variables
load_dotenv()

#Author: Morteza Farrokhnejad
# Set up logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jezebel.log'),
        logging.StreamHandler()
    ]
)

class JezebelAssistant:
    def __init__(self):
        # Initialize API keys from .env
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.weather_api_key = os.getenv('WEATHER_API_KEY')
        self.news_api_key = os.getenv('NEWS_API_KEY')

        # Check if API keys are present
        self._validate_api_keys()

        # Text-to-Speech Engine
        self.engine = pyttsx3.init()
        
        # YouTube Music API
        self.ytmusic = ytmusicapi.YTMusic()

        # Speech Recognition
        self.recognizer = sr.Recognizer()
        
        # State Variables
        self.blocked = False
        self.continuous_listening = False
        self.voice_enabled = True

        # OpenAI Client
        openai.api_key = self.openai_api_key

        # Command Mapping
        self.command_map = {
            'PLAY': self.play_song,
            'OPEN': self.open_website,
            'RUN': self.run_command,
            'WEATHER': self.get_weather,
            'NEWS': self.get_news,
            'JOKE': self.tell_joke,
            'REMINDER': self.set_reminder,
            'TIMER': self.set_timer
        }

        # Setup GUI
        self._setup_gui()

    def _validate_api_keys(self):
        """Validate presence of required API keys"""
        required_keys = ['OPENAI_API_KEY', 'WEATHER_API_KEY', 'NEWS_API_KEY']
        for key in required_keys:
            if not os.getenv(key):
                logging.error(f"Missing API key: {key}")
                raise ValueError(f"Please set the {key} in your .env file")

    def _setup_gui(self):
        """Create the GUI for the Jezebel Assistant"""
        self.root = tk.Tk()
        self.root.title("Jezebel Assistant")
        self.root.geometry("400x500")

        # Start/Stop Buttons
        self.start_button = tk.Button(
            self.root, 
            text="Start Listening", 
            command=self.start_listening,
            width=20, 
            height=2
        )
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(
            self.root, 
            text="Stop Listening", 
            command=self.stop_listening,
            state=tk.DISABLED,
            width=20, 
            height=2
        )
        self.stop_button.pack(pady=10)

        # Mode Toggle
        self.mode_button = tk.Button(
            self.root, 
            text="Mode: Single", 
            command=self.toggle_listening_mode,
            width=20, 
            height=2
        )
        self.mode_button.pack(pady=10)

        # Voice Toggle
        self.voice_button = tk.Button(
            self.root, 
            text="Voice: On", 
            command=self.toggle_voice,
            width=20, 
            height=2
        )
        self.voice_button.pack(pady=10)

        # Display Labels
        self.user_label = tk.Label(
            self.root, 
            text="User Input: ", 
            wraplength=350
        )
        self.user_label.pack(pady=5)

        self.response_label = tk.Label(
            self.root, 
            text="Assistant Response: ", 
            wraplength=350
        )
        self.response_label.pack(pady=5)

    def start_listening(self):
        """Start speech recognition thread"""
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        threading.Thread(target=self.recognize_speech, daemon=True).start()

    def stop_listening(self):
        """Stop speech recognition"""
        self.blocked = True
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def toggle_listening_mode(self):
        """Toggle between single and continuous listening modes"""
        self.continuous_listening = not self.continuous_listening
        mode_text = "Mode: Continuous" if self.continuous_listening else "Mode: Single"
        self.mode_button.config(text=mode_text)

    def toggle_voice(self):
        """Toggle voice feedback"""
        self.voice_enabled = not self.voice_enabled
        voice_text = "Voice: On" if self.voice_enabled else "Voice: Off"
        self.voice_button.config(text=voice_text)

    def recognize_speech(self):
        """Recognize and process speech input"""
        with sr.Microphone() as source:
            try:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(
                    source, 
                    timeout=5,  # Increased timeout
                    phrase_time_limit=10  # Increased phrase time limit
                )

                # Process recognized speech
                user_input = self.recognizer.recognize_google(audio).upper()
                self.user_label.config(text=f"User Input: {user_input}")
                
                # Process commands or generate response
                response = self.process_command(user_input)
                
                self.response_label.config(text=f"Assistant Response: {response}")
                
                if self.voice_enabled:
                    self.speak(response)

            except sr.UnknownValueError:
                logging.warning("Speech Recognition could not understand audio")
                response = "I could not understand that."
            except sr.RequestError as e:
                logging.error(f"Speech Recognition error: {e}")
                response = "I'm having trouble with speech recognition."
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                response = "An unexpected error occurred."

            # Reset if not in continuous mode
            if not self.continuous_listening:
                self.stop_listening()

    def process_command(self, user_input):
        """Process user command or generate AI response"""
        for cmd, func in self.command_map.items():
            if user_input.startswith(cmd):
                # Remove command prefix and call corresponding function
                query = user_input[len(cmd):].strip()
                return func(query)
        
        # Default to AI response generation
        return self.generate_ai_response(user_input)

    def generate_ai_response(self, prompt):
        """Generate AI response using ChatCompletion API"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant named Jezebel."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            return "I'm having trouble generating a response."

    def speak(self, text):
        """Text-to-speech functionality"""
        if not self.voice_enabled:
            return
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logging.error(f"Text-to-speech error: {e}")

    def play_song(self, query):
        """Play song using YouTube Music API"""
        try:
            search_results = self.ytmusic.search(query)
            if search_results:
                first_result = search_results[0]
                return f"Playing {first_result['title']} by {first_result['artists'][0]['name']}"
            return "No matching song found."
        except Exception as e:
            logging.error(f"Song search error: {e}")
            return "Could not play the song."

    def open_website(self, url):
        """Open a website"""
        try:
            # Add http:// if not present
            if not url.startswith(('http://', 'https://')):
                url = f'https://{url}'
            webbrowser.open(url)
            return f"Opening {url}"
        except Exception as e:
            logging.error(f"Website opening error: {e}")
            return "Could not open the website."

    def run_command(self, command):
        """Placeholder for command execution (disabled for security)"""
        logging.warning(f"Attempted to run command: {command}")
        return "Command execution is currently disabled for security reasons."

    def get_weather(self, city):
        """Retrieve weather information"""
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                return f"Weather in {city}: {temp}°C, {description}"
            return f"Could not retrieve weather for {city}"
        except Exception as e:
            logging.error(f"Weather retrieval error: {e}")
            return "Weather information unavailable."

    def get_news(self):
        """Fetch top news headlines"""
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={self.news_api_key}"
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200 and 'articles' in data:
                headlines = [article['title'] for article in data['articles'][:5]]
                return "Top News Headlines:\n" + "\n".join(headlines)
            return "Could not retrieve news headlines."
        except Exception as e:
            logging.error(f"News retrieval error: {e}")
            return "News information unavailable."

    def tell_joke(self, _=None):
        """Fetch a random joke"""
        try:
            response = requests.get("https://official-joke-api.appspot.com/random_joke")
            data = response.json()
            return f"{data['setup']} ... {data['punchline']}"
        except Exception as e:
            logging.error(f"Joke retrieval error: {e}")
            return "Could not fetch a joke."

    def set_reminder(self, reminder):
        """Set a reminder"""
        logging.info(f"Reminder set: {reminder}")
        return f"Reminder set: {reminder}"

    def set_timer(self, duration):
        """Set a timer"""
        try:
            seconds = int(re.findall(r'\d+', duration)[0])
            threading.Timer(seconds, lambda: self.speak("Timer complete!")).start()
            return f"Timer set for {seconds} seconds."
        except Exception as e:
            logging.error(f"Timer setting error: {e}")
            return "Could not set the timer."

    def run(self):
        """Start the Jezebel Assistant GUI"""
        self.root.mainloop()

def main():
    """Main application entry point"""
    try:
        assistant = JezebelAssistant()
        assistant.run()
    except Exception as e:
        logging.critical(f"Application startup error: {e}")

if __name__ == "__main__":
    main()
