from openai import OpenAI
from os import getenv
import re
import json
import numpy as np
import soundfile as sf
import simpleaudio as sa
import torch
from snac import SNAC

# ----------------------- Configuration -----------------------

# Set your OpenRouter API key as an environment variable for security
# For example, in your terminal:
# export OPENROUTER_API_KEY='your-api-key-here'
OPENROUTER_API_KEY = getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("Please set the OPENROUTER_API_KEY environment variable.")

# Initialize OpenAI client with OpenRouter API key
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# ----------------------- Prompt Construction -----------------------

PROMPT = """
You are an AI assistant trained to generate SNAC tokens for audio encoding. SNAC (Sound Neural Audio Codes) tokens are numerical representations of audio waveforms structured in multiple hierarchical levels...
"""

# ----------------------- Function Definitions -----------------------

def generate_snac_tokens(prompt):
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://www.thoughtflux.io",  # Optional, for including your app on openrouter.ai rankings.
                "X-Title": "ThoughtFluxAI",  # Optional. Shows in rankings on openrouter.ai.
            },
            model="liquid/lfm-40b",
            messages=[
                {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500,
            n=1,
            stop=None
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred while generating SNAC tokens: {e}")
        return None

def parse_snac_tokens(model_response):
    snac_tokens = {}
    levels = [1, 2, 3, 4]
    for level in levels:
        pattern = rf"Level {level}:\s*Shape\s*torch\.Size\(\[1,\s*\d+\]\)\s*SNAC Code Values \(Level {level}\):\s*\[\[(.*?)\]\]"
        match = re.search(pattern, model_response, re.DOTALL)
        if match:
            values_str = match.group(1)
            values = [int(v.strip()) for v in values_str.split(",") if v.strip().isdigit()]
            expected_length = {1: 44, 2: 88, 3: 176, 4: 352}[level]
            if len(values) == expected_length:
                snac_tokens[f"Level_{level}"] = values
            else:
                print(f"Warning: Level {level} expected {expected_length} values, but got {len(values)}.")
                snac_tokens[f"Level_{level}"] = values[:expected_length]
        else:
            print(f"Warning: SNAC tokens for Level {level} not found in the response.")
            snac_tokens[f"Level_{level}"] = []
    return snac_tokens

def decode_snac_tokens(snac_tokens):
    snac_encoded = []
    for level in sorted(snac_tokens.keys()):
        values = snac_tokens[level]
        if not values:
            print(f"Error: No values found for {level}. Cannot decode.")
            return None, None
        tensor = torch.tensor(values, dtype=torch.float32).unsqueeze(0)
        snac_encoded.append(tensor)

    try:
        model = SNAC.from_pretrained("hubertsiuzdak/snac_32khz").eval().cuda()
        with torch.inference_mode():
            decoded_audio = model.decode(snac_encoded)
        decoded_waveform = decoded_audio.squeeze().cpu().numpy()
        sample_rate = 32000
        return decoded_waveform, sample_rate
    except Exception as e:
        print(f"An error occurred during decoding: {e}")
        return None, None

def save_waveform_to_file(waveform, sample_rate, filename):
    try:
        sf.write(filename, waveform, sample_rate)
        print(f"Audio saved to {filename}")
    except Exception as e:
        print(f"Failed to save audio: {e}")

def play_audio(waveform, sample_rate):
    try:
        audio_data = (waveform * 32767).astype(np.int16)
        play_obj = sa.play_buffer(audio_data, 1, 2, sample_rate)
        play_obj.wait_done()
    except Exception as e:
        print(f"Failed to play audio: {e}")

# ----------------------- Main Execution -----------------------

def main():
    print("Generating SNAC tokens using lfm-40b model...")
    model_response = generate_snac_tokens(PROMPT)

    if not model_response:
        print("Failed to generate SNAC tokens.")
        return

    print("\nModel Response:")
    print(model_response)

    print("\nParsing SNAC tokens...")
    snac_tokens = parse_snac_tokens(model_response)

    for level, tokens in snac_tokens.items():
        print(f"{level}: {tokens[:10]}...")

    print("\nDecoding SNAC tokens back to audio waveform...")
    decoded_waveform, decoded_sample_rate = decode_snac_tokens(snac_tokens)

    if decoded_waveform is None:
        print("Decoding failed.")
        return

    output_filename = "decoded_audio_generated.wav"
    save_waveform_to_file(decoded_waveform, decoded_sample_rate, output_filename)

    print("\nPlaying the decoded audio...")
    play_audio(decoded_waveform, decoded_sample_rate)

    print("\nProcess completed successfully.")

if __name__ == "__main__":
    main()
