import numpy as np
import wave
import struct

def generate_pop_sound(filename, duration=0.05, frequency=1000, sample_rate=44100):
    # Create a numpy array representing the sound wave
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # Create a pop sound (short burst of a sine wave)
    sound_wave = 0.5 * np.sin(2 * np.pi * frequency * t)

    # Apply an exponential decay to simulate a "pop"
    decay = np.exp(-20 * t)
    sound_wave = sound_wave * decay

    # Convert the sound wave to 16-bit PCM data
    sound_wave = np.int16(sound_wave * 32767)

    # Write to a .wav file
    with wave.open(filename, 'w') as wav_file:
        # Set up the WAV file parameters
        wav_file.setnchannels(1)  # Mono sound
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wav_file.setframerate(sample_rate)

        # Write the sound wave to the file
        for sample in sound_wave:
            wav_file.writeframes(struct.pack('<h', sample))

# Generate the pop sound and save it as 'pop_sound.wav'
generate_pop_sound('pop_sound.wav')

import numpy as np
import wave
import struct

def generate_jump_sound(filename, duration=0.2, start_frequency=300, end_frequency=600, sample_rate=44100):
    # Create a time array
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # Create a frequency sweep (ascending pitch) for the jump sound
    frequency_sweep = np.linspace(start_frequency, end_frequency, len(t))
    
    # Create the jump sound wave by applying the frequency sweep
    sound_wave = 0.5 * np.sin(2 * np.pi * frequency_sweep * t)

    # Apply an exponential decay to make the sound fade out towards the end
    decay = np.exp(-10 * t)
    sound_wave = sound_wave * decay

    # Convert the sound wave to 16-bit PCM data
    sound_wave = np.int16(sound_wave * 32767)

    # Write to a .wav file
    with wave.open(filename, 'w') as wav_file:
        # Set up the WAV file parameters
        wav_file.setnchannels(1)  # Mono sound
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wav_file.setframerate(sample_rate)

        # Write the sound wave to the file
        for sample in sound_wave:
            wav_file.writeframes(struct.pack('<h', sample))

# Generate the jump sound and save it as 'jump_sound.wav'
generate_jump_sound('jump_sound.wav')
