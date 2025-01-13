import librosa
import numpy as np
from essentia.standard import *

# Define the audio file path
audio_file = 'static/right here final met orch_limited.wav'

# Verify the file path
print(f"Loading file from: {audio_file}")

# Load the audio file with Librosa
try:
    print("Loading audio file with Librosa...")
    audio, sr = librosa.load(audio_file, sr=22050)
except FileNotFoundError:
    print(f"Error: The file {audio_file} was not found.")
    exit()

# Apply Harmonic-Percussive Source Separation (HPSS)
print("Applying Harmonic-Percussive Source Separation (HPSS)...")
y_harmonic, y_percussive = librosa.effects.hpss(audio)

# Key Detection Using Essentia (Primary Method)
print("Detecting key using Essentia...")
loader = MonoLoader(filename=audio_file)
audio_essentia = loader()

key_extractor = KeyExtractor()
key_essentia, scale_essentia, confidence_essentia = key_extractor(audio_essentia)
confidence_essentia *= 100  # Normalize confidence to percentage
print(f"Detected Key (Essentia): {key_essentia}, Scale: {scale_essentia}")
print(f"Key Confidence (Essentia): {confidence_essentia:.2f}%")

# Final Key Selection
final_key, final_scale, final_confidence = key_essentia, scale_essentia, confidence_essentia

print(f"Final Detected Key: {final_key}, Scale: {final_scale}")
print(f"Final Key Confidence: {final_confidence:.2f}%")

# BPM Detection Using Librosa
print("Extracting BPM with Librosa...")
tempo, _ = librosa.beat.beat_track(y=audio, sr=sr)

# Ensure tempo is a scalar value and round it
tempo = tempo[0] if isinstance(tempo, np.ndarray) else tempo  # Extract scalar if it's an ndarray
tempo = round(tempo)  # Round to the nearest integer

# Initialize BPM estimates
bpm_estimates = []
window_size = 5 * sr  # 5-second windows for BPM analysis

for start in range(0, len(audio), window_size):
    end = min(start + window_size, len(audio))
    segment = audio[start:end]
    
    # Skip too-short segments
    if len(segment) < sr:  # Minimum 1 second of audio
        continue

    try:
        bpm, _ = librosa.beat.beat_track(y=segment, sr=sr)
        
        # Append only rounded scalar BPM values
        if isinstance(bpm, (int, float)):  
            bpm_estimates.append(round(bpm))
    except Exception as e:
        print(f"Error extracting BPM for segment starting at {start}: {e}")

# Handle the case where bpm_estimates might be empty
if bpm_estimates:
    bpm_std_dev = np.std(bpm_estimates)
    bpm_confidence = max(0, 100 - bpm_std_dev * 10)  # Confidence scaling
else:
    bpm_std_dev = 0.00
    bpm_confidence = 0.00

# Output detected BPM and confidence
print(f"Detected BPM (Librosa): {tempo}")
print(f"BPM Confidence: {bpm_confidence:.2f}%")
