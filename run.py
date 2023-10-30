import openai
import winsound
import sys
import pytchat
import time
import re
#import pyaudio
import keyboard
import wave
import threading
import json
import urllib
import urllib.parse
import urllib.request
import requests
#from config import *
#from utils.translate import *
from utils.TTS import *
from utils.subtitle import *
from utils.promptMaker import *
from utils.kata import *
from utils.base import *
from deep_translator import GoogleTranslator
from alphabet2kana import a2k

import pyaudio


import jaconv
import transliterate

import whisper


from pynput.keyboard import Key, Listener
from pynput.keyboard import KeyCode

def whisp(textAudio="input.wav"):

    model = whisper.load_model("base")


    audio = whisper.load_audio(textAudio)
    audio = whisper.pad_or_trim(audio)


    mel = whisper.log_mel_spectrogram(audio).to(model.device)


    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")


    options = whisper.DecodingOptions(language="ru")
    result = whisper.decode(model, mel, options)

    print(result.text)
    return result

alphaReg = re.compile(r'^[a-zA-Z]+$')

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

openai.api_key = "your api"

conversation = []

history = {"history": conversation}

mode = 0
total_characters = 0
chat = ""
chat_now = ""
chat_prev = ""
is_Speaking = False
lock = threading.Lock()
owner_name = "Mc.Quadrate"

mkeys , mvalues = 0, 0
modelSeliro = 1

ttsModes = {"s" : "seliro", "v" : "vox"}
ttsMode = "seliro"
#ttsMode = "vox"

def record_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    WAVE_OUTPUT_FILENAME = "input.wav"
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    print("Recording...")
    while keyboard.is_pressed('RIGHT_SHIFT'):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Stopped recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    transcribe_audio("input.wav")


def transcribe_audio(file):
    global chat_now
    try:
        audio_file= open(file, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        chat_now = transcript.text
        print ("Question: " + chat_now)
    except:
        print("Error transcribing audio")
        return
    speech_text(chat_now, mkeys, mvalues)

def openai_answer(mk,mv):
    global total_characters, conversation
    
    if Zbase(chat_now) == False:

        with open("conversation.json", "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)

        prompt = getPrompt()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            max_tokens=128,
            temperature=1,
            top_p=0.9
        )
        message = response['choices'][0]['message']['content']
        print(message)
        conversation.append({'role': 'assistant', 'content': message})
        speech_text(message,mk,mv)

def get_livechat(video_id):
    try:
        global chat

        live = pytchat.create(video_id=video_id)

        while live.is_alive():
            for c in live.get().sync_items():

                if c.author.name == 'Nightbot':
                    continue
                if not c.message.startswith("!"):
                    # удаление эмоджи
                    chat_raw = re.sub(r':[^\s]+:', '', c.message)
                    
                    lock.acquire()
                    try:
                        chat = c.author.name + ': ' + chat_raw
                    finally:
                        lock.release()
                    print("Live chat:")
                    print(chat)
                    
                time.sleep(1)
    except KeyboardInterrupt:
        print("Program stopped by user")


def speech_text(text, mk = 0, mv = 0, speaker_id = 43):
    global is_Speaking
    global chat_now

    print("--------------------Question-----------------------")
    try:
        print(chat_now)
        print(translate_text(chat_now))
    except Exception:
        print("Chat dies from cringe")
        if type(chat_now)!=str:
            chat_now = ""
    print("--------------------Question-----------------------")
    try:
        text = text.replace("Алиса:","")
        print(30*"-")
        print("Answer: " + text if type(text)==str else "None")
        print("Ответ: " + translate_text(text) if type(text)==str else "None" )
        print(30*"-")
    except:
        print("No answer")



    if ttsMode == "seliro":
        silero_TTSF(text, model=modelSeliro)
        
    elif ttsMode == "vox":
        voicevoxTTS(text,mk,mv)
    
    generate_subtitle(chat_now,text)
    time.sleep(1)



    winsound.PlaySound("test.wav", winsound.SND_FILENAME)

    time.sleep(1)
    with open ("output.txt", "w") as f:
        f.truncate(0)
    with open ("chat.txt", "w") as f:
        f.truncate(0)

def preparation():
    global conversation, chat_now, chat, chat_prev
    while True:

        lock.acquire()
        try:
            chat_now = chat
        finally:
            lock.release()
        if chat_now != chat_prev:
            lock.acquire()            
            # Сохранеие контекста
            try:
                conversation.append({'role': 'user', 'content': chat_now})
                chat_prev = chat_now

                openai_answer(mkeys , mvalues)
            finally:
                lock.release()
        time.sleep(1)



def change_voice_on_release(key):
        global ttsMode
        global ttsModes

        charkeys = list(ttsModes.keys())
        keycodes = [KeyCode.from_char(i) for i in charkeys]

        for i in range(len(keycodes)):
            if key == keycodes[i]:
                try:
                    ttsMode = ttsModes[charkeys[i]]
                    print("TTSMODE = " + ttsMode)
                finally:
                    pass              
        return False


def voiceTrhread():
    global ttsMode
    global ttsModes
    while True:
        with Listener(on_release=change_voice_on_release) as listener:
            listener.join()


def voiceChanger():
    lock.acquire()

    lock.release()
    
if __name__ == "__main__":


    mkeys , mvalues = keyval(dictionaryRU_JP())
    modelSeliro = silero_TTS()
    
    try:

        mode = input("Mode (1-Mic, 2-Youtube: ")

        changeVoice = threading.Thread(target=voiceTrhread)
        changeVoice.start()   

        if mode == "1":
            print("Press and Hold Right Shift to record audio")
            while True:
                if keyboard.is_pressed('RIGHT_SHIFT'):
                    record_audio()
   
        if mode == "2":
                live_id = input("Livestream ID: ")
                #Захват чата и ответы
                t = threading.Thread(target=preparation)
                t.start()
                get_livechat(live_id)
        elif mode == "3":  
            while True:
                    text = str(input("Promt:"))
                    res = owner_name + ": " + text
                    chat_now = res
                    conversation.append({'role': 'user', 'content': res})
                    openai_answer(mkeys , mvalues)
        if mode == "4":
            while True:
                s = input("phrase: ")
                speech_text(s,mkeys,mvalues)

    except KeyboardInterrupt:
        print("Stopped")

