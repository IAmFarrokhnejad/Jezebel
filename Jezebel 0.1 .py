import openai
import pyttsx3 
import speech_recognition as sr
import time

openai.api_key = "KEY GOES HERE"  # OPENAI API KEY GOES HERE

engine = pyttsx3.init()



#Author: Morteza Farrokhnejad
#Text to speech
def audioToText(filename):
    recognizer = sr.recognizer()
    with sr.audioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Skipping an unknown error...")

#self explainatory
def genereateResponse(prompt):
    response = openai.Completion.create(
        engine = "text_davinci_003",
        prompt=prompt,
        maxTokens=4000,
        n=1,
        stop = None,
        temperature = 0.5,
    )
    return response["choice"][0]["text"]


def speakGenerated (text):
    engine.say(text)
    engine.runNWait()



def main():
    print("Call her name, 'Jezebel' to begin... ")
    with sr.Microphone() as source:
        recognizer = sr.recognizer()
        audio = recognizer.listen(source)
        try:
            transcription = recognizer.recognize_google(audio)
            if transcription.upper() == "JEZEBEL":
                filename= "input.mp3"
                print("Ask something... ")
                with sr.Microphone() as source:
                    recognizer = sr.recognizer()
                    source.pause_threshold = 1
                    audio = recognizer.listen(source, time_limit= None, timeout = None)
                    with open(filename, "wb") as f:
                        f.write(audio.get_mp3_data())

                    text = audioToText(filename)
                    if text:
                        print(f"Did you say {text} ?")

                        response = genereateResponse(text)
                        print(f"GPT-3 says: {response}")

                        speakGenerated(response)
        except Exception as e:
            print("An error might have occured: {}".format(e))



if __name__== "__main__":
    main()
