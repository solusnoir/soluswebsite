import librosa
import numpy as np
from essentia.standard import MonoLoader, KeyExtractor
from time import time

def find_key(audio_file_path):
    start_time = time()  # Track execution time

    # Load the audio file with Librosa (set cache=True for faster loading)
    try:
        print(f"Loading audio file from: {audio_file_path}")
        audio, sr = librosa.load(audio_file_path, sr=22050, mono=True, duration=240.0)  # Limit duration to 240 seconds to avoid long processing
    except Exception as e:
        raise Exception(f"Error loading audio file: {e}")

    # Apply Harmonic-Percussive Source Separation (HPSS) once
    print("Applying Harmonic-Percussive Source Separation (HPSS)...")
    y_harmonic, y_percussive = librosa.effects.hpss(audio)

    # Key Detection Using Essentia (using only the harmonic part)
    print("Detecting key using Essentia...")
    loader = MonoLoader(filename=audio_file_path)
    audio_essentia = loader()

    key_extractor = KeyExtractor()
    key_essentia, scale_essentia, confidence_essentia = key_extractor(y_harmonic)  # Use harmonic part for faster key detection
    confidence_essentia *= 100  # Normalize confidence to percentage
    print(f"Detected Key (Essentia): {key_essentia}, Scale: {scale_essentia}")
    print(f"Key Confidence (Essentia): {confidence_essentia:.2f}%")

    # Final Key Selection
    final_key, final_scale, final_confidence = key_essentia, scale_essentia, confidence_essentia

    # BPM Detection Using Librosa (use harmonic part for better performance)
    print("Extracting BPM with Librosa...")
    tempo, _ = librosa.beat.beat_track(y=y_harmonic, sr=sr)  # Use harmonic part for BPM detection

    # Ensure tempo is a scalar value and round it
    tempo = tempo[0] if isinstance(tempo, np.ndarray) else tempo  # Extract scalar if it's an ndarray
    tempo = round(tempo)  # Round to the nearest integer

    # Calculate execution time
    elapsed_time = time() - start_time
    print(f"Processing time: {elapsed_time:.2f} seconds")

    # Return results
    return {
        'key': final_key,
        'scale': final_scale,
        'key_confidence': f"{final_confidence:.2f}%",
        'bpm': tempo
    }
