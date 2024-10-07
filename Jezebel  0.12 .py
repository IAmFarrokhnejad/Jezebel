
import pyttsx3 
import speech_recognition as sr
import time
from openai import Completion, api_key

api_key = "KEY GOES HERE"  # OPENAI API KEY GOES HERE

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
    response = Completion.create(  # Fixed: openai.Completion.create
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

def main():
    print("Call her name, 'Jezebel' to begin... ")
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()  # Fixed: recognizer should be Recognizer
        audio = recognizer.listen(source)
        try:
            transcription = recognizer.recognize_google(audio)
            if transcription.upper() == "JEZEBEL":
                filename = "input.mp3"
                print("Ask something... ")
                with sr.Microphone() as source:
                    recognizer = sr.Recognizer()  # Fixed: recognizer should be Recognizer
                    source.pause_threshold = 1
                    audio = recognizer.listen(source, time_limit=None, timeout=None)
                    with open(filename, "wb") as f:
                        f.write(audio.get_wav_data())  # Fixed: get_mp3_data should be get_wav_data

                    text = audioToText(filename)
                    if text:
                        print(f"Did you say {text} ?")

                        response = generateResponse(text)
                        print(f"GPT-3 says: {response}")

                        speakGenerated(response)
        except Exception as e:
            print("An error might have occurred: {}".format(e))

if __name__ == "__main__":
    main()
