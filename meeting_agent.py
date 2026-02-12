import speech_recognition as sr
import requests
import os
import pygame
import uuid
import base64
import pyttsx3

# 🔐 Load API Key
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

# 🎤 Speech to Text
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙 Speak now...")
        audio = recognizer.listen(source)

    try:
        print("🔎 Converting speech to text...")
        text = recognizer.recognize_google(audio)
        print("📝 You said:", text)
        return text
    except:
        print("❌ Could not understand audio")
        return None


# 🧠 Send text to Sarvam AI
def ask_sarvam(text):
    url = "https://api.sarvam.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {SARVAM_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "sarvam-m",
        "messages": [
            {"role": "system", "content": "You are a helpful meeting assistant."},
            {"role": "user", "content": text}
        ]
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    reply = data["choices"][0]["message"]["content"]
    print("🤖 Assistant:", reply)
    return reply


# 🔊 Text to Speech using Sarvam



def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)   # speed
    engine.setProperty('volume', 1.0) # max volume

    engine.say(text)
    engine.runAndWait()
    engine.stop()



# 🔁 Main Loop
while True:
    user_text = listen()

    if user_text:
        if "have a nice day" in user_text.lower():
            speak("You too! Have a wonderful day ahead. Goodbye!")
            break

        reply = ask_sarvam(user_text)
        speak(reply)

