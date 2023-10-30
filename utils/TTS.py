import os
import torch
import requests
import urllib.parse
from utils.katakana import *
from utils.translate import *
from utils.kata import *
from transliterate import get_available_language_codes
import transliterate

def silero_tts(tts, language, model="ru", speaker="baya"):
    device = torch.device('cpu')
    torch.set_num_threads(4)
    local_file = 'model.pt'

    if not os.path.isfile(local_file):
        torch.hub.download_url_to_file(f'https://models.silero.ai/models/tts/{language}/{model}.pt',
                                    local_file)  

    model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
    model.to(device)

    sample_rate = 48000

    audio_paths = model.save_wav(text=tts,
                                speaker=speaker,
                                sample_rate=sample_rate)
def sileroTTS():

    language = 'ru'
    model_id = 'v3_1_ru'
    sample_rate = 48000
    speaker = 'baya'
    device = torch.device('cpu')

    model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language=language,
                                     speaker=model_id)
    model.to(device)  # gpu or cpu

    audio = model.apply_tts(text=example_text,
                        speaker=speaker,
                        sample_rate=sample_rate)   
def silero_TTS(tts="привет", language="ru", model="v3_1_ru.pt", speaker="baya"):
    device = torch.device('cpu')
    torch.set_num_threads(4)
    local_file = 'D:/AI/voice/Seliro/v3_1_ru.pt'

    model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
    model.to(device)

    sample_rate = 48000
    tts = transliterate.translit(tts,'ru')
    
    audio_paths = model.save_wav(
                                text=tts,
                                speaker=speaker,
                                sample_rate=sample_rate)
    return model

def silero_TTSF(tts="привет", speaker="baya", model = None):

    sample_rate = 48000
    tts = transliterate.translit(tts,'ru')
    
    audio_paths = model.save_wav(
                                text=tts,
                                speaker=speaker,
                                sample_rate=sample_rate)


def voicevox_tts(tts):
    voicevox_url = 'http://localhost:50021'
    katakana_text = katakana_converter(tts)
    params_encoded = urllib.parse.urlencode({'text': katakana_text, 'speaker': 46})
    request = requests.post(f'{voicevox_url}/audio_query?{params_encoded}')
    params_encoded = urllib.parse.urlencode({'speaker': 46, 'enable_interrogative_upspeak': True})
    request = requests.post(f'{voicevox_url}/synthesis?{params_encoded}', json=request.json())

    with open("test.wav", "wb") as outfile:
        outfile.write(request.content)

def voicevoxTTS(text, mk, mv, speaker_id = 43):
    result_id = translate_text(text)
    katakana_text = translit(result_id, mk, mv)
    params_encoded = urllib.parse.urlencode({'text': katakana_text, 'speaker': speaker_id})
    request = requests.post(f'http://127.0.0.1:50021/audio_query?{params_encoded}')
    params_encoded = urllib.parse.urlencode({'speaker': speaker_id, 'enable_interrogative_upspeak': True})
    request = requests.post(f'http://127.0.0.1:50021/synthesis?{params_encoded}', json=request.json())
    with open("test.wav", "wb") as outfile:
        outfile.write(request.content)        

if __name__ == "__main__":
    silero_tts()
