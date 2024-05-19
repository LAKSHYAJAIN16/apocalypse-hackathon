import speech_recognition as sr
import requests

# Initialize the recognizer
t = 1
if t == 1:
    file = r"C:\Users\minec\OneDrive\Desktop\hackathons\apocalyse\files\1.wav"
    recognizer = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audiodata = recognizer.record(source)
        words = recognizer.recognize_google(audiodata)
        response = requests.get("http://10.93.94.131:5000/real-time?t="+"How to Protect Myself from Zombies?");

elif t == 2:
    file = r"C:\Users\minec\OneDrive\Desktop\hackathons\apocalyse\files\2.wav"
    recognizer = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audiodata = recognizer.record(source)
        words = recognizer.recognize_google(audiodata)
        response = requests.get("http://10.93.94.131:5000/real-time?t="+"How to Find Clean Drinking Water?");



