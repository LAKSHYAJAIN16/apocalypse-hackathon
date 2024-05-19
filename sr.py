import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

# Use the default microphone as the audio source
with sr.Microphone() as source:
    print("Listening...")

    # Adjust for ambient noise
    recognizer.adjust_for_ambient_noise(source)

    try:
        # Capture the audio
        audio = recognizer.listen(source)

        # Recognize speech using Google Speech Recognition
        text = recognizer.recognize_google_cloud(audio,)

        print("You said:", text)

    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
