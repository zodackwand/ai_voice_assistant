import speech_recognition as sr
import pyttsx3
import openai
import os
from dotenv import load_dotenv

# Load OpenAi API from .env file
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')
openai.api_key = OPENAI_KEY



def speak(message):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[14].id)
    voice_rate = 145
    engine.setProperty('rate', voice_rate)
    engine.say(message)
    engine.runAndWait()

recognizer = sr.Recognizer()

def record_text():
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                print("Speak!")
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                return text

        except sr.RequestError as e:
            print(f'Could not request: {e}')

        except sr.UnknownValueError:
            print('Unknown value error')


def send_to_GPT(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        n=1,
        stop=None,
        temperature=0.5
    )

    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message

messages = []

while True:
    text = record_text()
    messages.append({"role": "user", "content": text})
    response = send_to_GPT(messages)
    speak(response)