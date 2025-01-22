import os
# os.environ["PHONEMIZER_ESPEAK_PATH"] = "/opt/homebrew/bin/espeak-ng"  
# os.environ["PHONEMIZER_ESPEAK_LIBRARY"] = "/opt/homebrew/lib/libespeak-ng.dylib"

import torch
import pandas as pd
from kokoro import generate
from models import build_model
from news_fetcher import fetch_news, process_articles_to_df
import summarizer
import numpy as np

device = 'cuda' if torch.cuda.is_available() else 'cpu'
MODEL = build_model('kokoro-v0_19.pth', device)
VOICE_NAME = [
    'af',
    'af_bella', 'af_sarah', 'am_adam', 'am_michael',
    'bf_emma', 'bf_isabella', 'bm_george', 'bm_lewis',
    'af_nicole', 'af_sky',
][0]
VOICEPACK = torch.load(f'voices/{VOICE_NAME}.pt', weights_only=True).to(device)
print(f'Loaded voice: {VOICE_NAME}')


device = 'cuda' if torch.cuda.is_available() else 'cpu'
MODEL = build_model('kokoro-v0_19.pth', device)
VOICE_NAME = 'af_bella'
VOICEPACK = torch.load(f'voices/{VOICE_NAME}.pt', weights_only=True).to(device)
print(f"Loaded voice: {VOICE_NAME}")

#####################################
# 3. Generate audio from text
#####################################
def generate_audio(text, model=MODEL, voicepack=VOICEPACK, sample_rate=24000):
    """
    Generate audio from text and return the float array and phonemes.
    """
    lang_key = VOICE_NAME[0]
    float_array, phonemes = generate(model, text, voicepack, lang=lang_key)
    return float_array, phonemes


def split_text_by_sentence(text):
    """
    A naive approach, splitting on '.'
    and keeping sentences with trailing '.'
    """
    sentences = text.split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    sentences = [s + '.' for s in sentences if not s.endswith('.')]
    return sentences
#####################################
# 4. Concatenate audio chunks (using float arrays)
#####################################
def generate_and_concatenate(long_text, sample_rate=24000):
    """
    1. Split text into smaller sentences.
    2. Generate audio for each chunk.
    3. Concatenate the float arrays directly.
    4. Normalize the final concatenated array to avoid clipping.
    5. Return the final float array for playback or export.
    """
    chunks = split_text_by_sentence(long_text)
    all_float_arrays = []

    # Generate audio for each chunk
    for chunk in chunks:
        float_array, _ = generate_audio(chunk)
        all_float_arrays.append(float_array)

    # Concatenate all float arrays
    concatenated_float_array = np.concatenate(all_float_arrays)

    # Normalize the final concatenated array to avoid clipping
    max_amplitude = np.max(np.abs(concatenated_float_array))
    if max_amplitude > 1.0:
        concatenated_float_array = concatenated_float_array / max_amplitude * 0.9  # Scale to 90% of max amplitude

    print("Concatenated audio duration:", len(concatenated_float_array) / sample_rate, "seconds")
    return concatenated_float_array

print("finished compiling!")

# # Optionally export to a WAV file
# from scipy.io.wavfile import write as write_wav
# write_wav("final_output.wav", 24000, final_audio_float_array)