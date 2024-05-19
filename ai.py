import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
import os
import subprocess
import winsound
from flask import Flask, request
from json import dumps  
import requests
import uuid
from urllib.request import urlopen
from pydub import AudioSegment
from pydub.playback import play
import time

app = Flask(__name__)

@app.route("/no-real-time")
def process_1():
    fileName = request.args.get("f")
    recognizer = sr.Recognizer()
    subprocess.call(['ffmpeg', '-i', fileName, os.path.basename(fileName).replace(".mp3",".wav")])
    with sr.AudioFile(os.path.basename(fileName).replace(".mp3",".wav")) as source:
        audio_data = recognizer.record(source)
        try:
            words = recognizer.recognize_google(audio_data)
            print(words)
            # os.delete(fileName)

            api = 'AIzaSyB9wJYUC1YZBsbMro-sUijNQsWAVra36UA'
            genai.configure(api_key=api)
            model = genai.GenerativeModel('gemini-pro')
    
            response = model.generate_content(words + " and limit it to three sentences")
            print(response)
            cleanresponse = response.text.replace("*", "")
            obj = gTTS(text=cleanresponse, lang='en', tld='com.au', slow=False)
            obj.save("output.mp3")
            voice = AudioSegment.from_mp3("output.mp3")
            voice.export(os.path.basename(fileName).replace(".mp3",""), format="wav")

            winsound.PlaySound(os.path.basename(fileName).replace(".mp3",""), winsound.SND_FILENAME)  
            return "got it"
        except Exception as e:
            print(e)
            return dumps(e)
        
@app.route("/real-time")
def process_2():
    transcript = request.args.get("t")
    api = 'AIzaSyB9wJYUC1YZBsbMro-sUijNQsWAVra36UA'
    genai.configure(api_key=api)
    model = genai.GenerativeModel('gemini-pro')
    
    response = model.generate_content(transcript + " and limit it to two sentences.")
    print(response)
    
    url = 'https://api.fakeyou.com/tts/inference'
    data = {
        "uuid_idempotency_token": str(uuid.uuid4()),
        "tts_model_token": "weight_tx47gvn95sa254jhx2ye6zf79",
        "inference_text": response.candidates[0].content.parts[0].text
    }
    print(data)

    response_2 = requests.post(url, json=data)

    print(response_2.status_code)
    print(response_2.json())
    inteference_job_token = response_2.json()["inference_job_token"]

    
    while True:
        response_loop = requests.get("https://api.fakeyou.com/tts/job/"+inteference_job_token)
        js = response_loop.json()
        print(js)
        if js["state"]["status"] != "complete_success":
            time.sleep(2)
            continue
        else:
            aud = urlopen("https://storage.googleapis.com/vocodes-public" + js["state"]["maybe_public_bucket_wav_audio_path"])
            print(aud)
            with open('./test.wav','wb') as output:
                output.write(aud.read())
                song = AudioSegment.from_wav("./test.wav")
                play(song)
                break


    return "got it"