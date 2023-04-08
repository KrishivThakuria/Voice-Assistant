import openai
import pyttsx3
import speech_recognition as sr
import time
from playsound import playsound
from gtts import gTTS

openai.api_key = "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"
engine=pyttsx3.init()
   
def transcribe_audio_to_text(filename):
    recogizer=sr.Recognizer()
    with sr.AudioFile(filename)as source:
        audio=recogizer.record(source) 
    try:
        return recogizer.recognize_google(audio)
    except:
        print("skipping unkown error")

def generate_response(prompt):
    response= openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response ["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        print("Say 'Jake' to start recording your question")
        with sr.Microphone() as source:
            recognizer=sr.Recognizer()
            audio=recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower()=="jake":
                    filename ="input.wav"
                    print("Say your question")
                    with sr.Microphone() as source:
                        recognizer=sr.Recognizer()
                        source.pause_threshold=1
                        audio=recognizer.listen(source,phrase_time_limit=None,timeout=None)
                        with open(filename,"wb")as f:
                            f.write(audio.get_wav_data())
                
                    text=transcribe_audio_to_text(filename)
                    if text:
                        print(f"you said {text}")
                        response = generate_response(text)
                        print(f"Jake: {response}")
                        tts = gTTS(text=response, lang='en')
                        tts.save("sample.mp3")
                        speak_text(response)
            except Exception as e:
                print("An error ocurred : {}".format(e))
                
if __name__=="__main__":
    main()