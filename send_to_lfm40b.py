from openai import OpenAI
from os import getenv
import numpy as np
import soundfile as sf
import simpleaudio as sa
import torch
from snac import SNAC
import json

# Function to serialize SNAC tokens for sending to the model
def serialize_snac_tokens(snac_encoded):
    serialized = []
    for i, code in enumerate(snac_encoded):
        code_cpu = code.cpu().numpy()
        serialized.append({
            "level": i + 1,
            "shape": code.shape,
            "values": code_cpu.tolist()  # Convert numpy arrays to lists for JSON serialization
        })
    return json.dumps(serialized, indent=2)

# Function to send SNAC tokens to the lfm-40b model and get a response
def send_snac_tokens_to_model(client, serialized_snac):
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "https://www.thoughtflux.io",  # Optional
            "X-Title": "ThoughtFluxAI",  # Optional
        },
        model="liquid/lfm-40b",
        messages=[
            {
                "role": "user",
                "content": (
                    "Here are the SNAC tokens generated by my script:\n"
                    f"{serialized_snac}\n\n"
                    "Please provide an analysis or insights based on these tokens."
                )
            }
        ]
    )
    return completion.choices[0].message.content

# Function to generate a complex audio waveform
def generate_waveform(frequencies, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    waveform = sum(np.sin(2 * np.pi * f * t) for f in frequencies)
    waveform = waveform / np.max(np.abs(waveform))  # Normalize waveform
    return waveform

# Function to encode waveform to SNAC codes
def encode_to_snac(waveform, sample_rate=44100):
    model = SNAC.from_pretrained("hubertsiuzdak/snac_32khz").eval().cuda()
    audio_tensor = torch.tensor(waveform, dtype=torch.float32).unsqueeze(0).unsqueeze(0).cuda()
    with torch.inference_mode():
        snac_encoded = model.encode(audio_tensor)
    return snac_encoded

# Function to decode SNAC codes to audio waveform
def decode_from_snac(snac_encoded):
    model = SNAC.from_pretrained("hubertsiuzdak/snac_32khz").eval().cuda()
    with torch.inference_mode():
        decoded_audio = model.decode(snac_encoded)
    decoded_waveform = decoded_audio.squeeze().cpu().numpy()
    sample_rate = 32000  # Sample rate used by the pretrained model
    return decoded_waveform, sample_rate

# Function to save waveform to an audio file
def save_waveform_to_file(waveform, sample_rate, filename):
    sf.write(filename, waveform, sample_rate)

# Function to play the audio waveform
def play_audio(waveform, sample_rate=44100):
    audio_data = (waveform * 32767).astype(np.int16)  # Convert to 16-bit PCM format
    play_obj = sa.play_buffer(audio_data, 1, 2, sample_rate)
    play_obj.wait_done()

# Main script
if __name__ == "__main__":
    # Initialize OpenAI client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=getenv("OPENROUTER_API_KEY"),
    )
    
    # Step 1: Generate a chat completion using lfm-40b
    chat_completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "https://www.thoughtflux.io",  # Optional
            "X-Title": "ThoughtFluxAI",  # Optional
        },
        model="liquid/lfm-40b",
        messages=[
            {
                "role": "user",
                "content": "What is the meaning of life?"
            }
        ]
    )
    print("Chat Completion Response:")
    print(chat_completion.choices[0].message.content)
    
    # Step 2: Generate complex audio waveform
    frequencies = [440, 880, 1760]  # Frequencies in Hz (A4, A5, A6)
    duration = 3  # Duration in seconds
    sample_rate = 44100
    
    waveform = generate_waveform(frequencies, duration, sample_rate)
    
    # Step 3: Encode waveform to SNAC codes
    snac_encoded = encode_to_snac(waveform, sample_rate)
    
    # Step 4: Display SNAC tokens
    print("\nSNAC Tokens:")
    for i, code in enumerate(snac_encoded):
        code_cpu = code.cpu().numpy()
        print(f"\nLevel {i + 1}: Shape {code.shape}")
        print(f"SNAC Code Values (Level {i + 1}):\n{code_cpu}")
    
    # Step 5: Serialize SNAC tokens
    serialized_snac = serialize_snac_tokens(snac_encoded)
    
    # Optional: Save serialized SNAC tokens to a file
    with open("snac_tokens.json", "w") as f:
        f.write(serialized_snac)
    
    # Step 6: Send SNAC tokens to lfm-40b model for analysis
    print("\nSending SNAC tokens to lfm-40b model for analysis...")
    model_response = send_snac_tokens_to_model(client, serialized_snac)
    print("\nModel Response:")
    print(model_response)
    
    # Step 7: Decode SNAC codes back to audio waveform
    decoded_waveform, decoded_sample_rate = decode_from_snac(snac_encoded)
    
    # Step 8: Save the decoded waveform to an audio file
    save_waveform_to_file(decoded_waveform, decoded_sample_rate, "decoded_audio.wav")
    
    # Step 9: Play the decoded audio
    print("\nPlaying the decoded audio...")
    play_audio(decoded_waveform, decoded_sample_rate)
