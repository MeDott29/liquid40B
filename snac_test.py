from openai import OpenAI
from os import getenv

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=getenv("OPENROUTER_API_KEY"),
)

completion = client.chat.completions.create(
  extra_headers={
    "HTTP-Referer": "https://www.thoughtflux.io",  # Optional, for including your app on openrouter.ai rankings.
    "X-Title": "ThoughtFluxAI",  # Optional. Shows in rankings on openrouter.ai.
  },
  model="liquid/lfm-40b",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)
print(completion.choices[0].message.content)


import numpy as np
import soundfile as sf
import simpleaudio as sa
import torch
from snac import SNAC

# Generate a complex audio waveform (e.g., combining sine waves of different frequencies)
def generate_waveform(frequencies, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    waveform = sum(np.sin(2 * np.pi * f * t) for f in frequencies)
    waveform = waveform / np.max(np.abs(waveform))  # Normalize waveform
    return waveform

# Encode waveform to SNAC codes
def encode_to_snac(waveform, sample_rate=44100):
    model = SNAC.from_pretrained("hubertsiuzdak/snac_32khz").eval().cuda()
    audio_tensor = torch.tensor(waveform, dtype=torch.float32).unsqueeze(0).unsqueeze(0).cuda()
    with torch.inference_mode():
        snac_encoded = model.encode(audio_tensor)
    return snac_encoded

# Decode SNAC codes to audio waveform
def decode_from_snac(snac_encoded):
    model = SNAC.from_pretrained("hubertsiuzdak/snac_32khz").eval().cuda()
    with torch.inference_mode():
        decoded_audio = model.decode(snac_encoded)
    decoded_waveform = decoded_audio.squeeze().cpu().numpy()
    sample_rate = 32000  # Sample rate used by the pretrained model
    return decoded_waveform, sample_rate

# Save waveform to an audio file
def save_waveform_to_file(waveform, sample_rate, filename):
    sf.write(filename, waveform, sample_rate)

# Play the audio waveform
def play_audio(waveform, sample_rate=44100):
    audio_data = (waveform * 32767).astype(np.int16)  # Convert to 16-bit PCM format
    play_obj = sa.play_buffer(audio_data, 1, 2, sample_rate)
    play_obj.wait_done()

# Main script
if __name__ == "__main__":
    frequencies = [440, 880, 1760]  # Frequencies in Hz (A4, A5, A6)
    duration = 3  # Duration in seconds
    sample_rate = 44100

    # Step 1: Generate complex audio waveform
    waveform = generate_waveform(frequencies, duration, sample_rate)

    # Step 2: Encode waveform to SNAC codes
    snac_encoded = encode_to_snac(waveform, sample_rate)

    # Display SNAC tokens with their tensor sizes and values
    print("SNAC Tokens:")
    for i, code in enumerate(snac_encoded):
        # Move tensor to CPU and convert to numpy for easier readability
        code_cpu = code.cpu().numpy()
        print(f"\nLevel {i + 1}: Shape {code.shape}")
        print(f"SNAC Code Values (Level {i + 1}):\n{code_cpu}")

    # Step 3: Decode SNAC codes back to audio waveform
    decoded_waveform, decoded_sample_rate = decode_from_snac(snac_encoded)

    # Step 4: Save the decoded waveform to an audio file
    save_waveform_to_file(decoded_waveform, decoded_sample_rate, "decoded_audio.wav")

    # Step 5: Play the decoded audio
    play_audio(decoded_waveform, decoded_sample_rate)
