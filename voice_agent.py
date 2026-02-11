import speech_recognition as sr
from openai import OpenAI
import requests
import uuid
import os
from playsound import playsound

# 🔑 PUT YOUR OPENAI KEY HERE
client = OpenAI(api_key="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")

# -------- RECORD VOICE --------
recognizer = sr.Recognizer()

with sr.Microphone() as source:
    print("🎙 Speak now...")
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

print("🔎 Converting speech to text...")

try:
    user_text = recognizer.recognize_google(audio)
    print("📝 You said:", user_text)
except:
    print("❌ Could not understand audio")
    exit()

# -------- SEND TO OPENAI --------
print("🤖 Thinking...")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_text}
    ]
)

ai_text = response.choices[0].message.content
print("💬 AI says:", ai_text)

# -------- TEXT TO SPEECH --------
print("🔊 Generating voice...")

speech_file = f"response_{uuid.uuid4()}.mp3"

speech = client.audio.speech.create(
    model="gpt-4o-mini-tts",
    voice="alloy",
    input=ai_text
)

with open(speech_file, "wb") as f:
    f.write(speech.content)

print("▶ Playing response...")
playsound(speech_file)

os.remove(speech_file)
