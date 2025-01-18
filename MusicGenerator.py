from pydub import AudioSegment
from pydub.generators import Sine
import random

class GameMusicGenerator:
    def __init__(self, theme="sci-fi", duration=60):
        self.theme = theme.lower()
        self.duration = duration * 1000  # Convert to milliseconds
        self.sample_rate = 44100  # Standard CD quality sample rate
        self.music = None

    def generate_music(self):
        if self.theme == "sci-fi":
            self.music = self._generate_sci_fi()
        elif self.theme == "fantasy":
            self.music = self._generate_fantasy()
        elif self.theme == "romance":
            self.music = self._generate_romance()
        elif self.theme == "drama":
            self.music = self._generate_drama()
        elif self.theme == "realism":
            self.music = self._generate_realism()
        else:
            raise ValueError("Unknown theme!")

    def _generate_sci_fi(self):
        # Generate a warbling, futuristic sound by modulating frequencies and combining sine waves
        base_freq = random.randint(500, 800)  # Base frequency for the sci-fi sound
        track = AudioSegment.silent(duration=0)

        for i in range(0, self.duration, 200):  # Split duration into smaller segments
            freq = base_freq + random.randint(-100, 100)  # Warble by randomly adjusting the frequency
            sine_wave = Sine(freq).to_audio_segment(duration=200)

            # Create a vibrato effect by adjusting the volume in a rhythmic way
            sine_wave = sine_wave.fade_in(50).fade_out(50)

            track += sine_wave

        # Add a cyclical forward thrust sound
        thrust_sound = self._generate_thrust_sound()
        track = track.overlay(thrust_sound, loop=True)  # Loop the thrust sound over the track
        
        return track

    def _generate_thrust_sound(self):
        # A cyclical thrust sound can be simulated by rising and falling frequencies over short intervals
        thrust_duration = 500  # 500 milliseconds per thrust cycle
        thrust_track = AudioSegment.silent(duration=self.duration)

        for i in range(0, self.duration, thrust_duration):
            # Simulate a forward thrust by increasing frequency and then decreasing it
            rise_freq = random.randint(600, 1000)
            fall_freq = random.randint(400, 600)

            # Generate the rising and falling parts of the thrust
            rise = Sine(rise_freq).to_audio_segment(duration=thrust_duration // 2).fade_in(50)
            fall = Sine(fall_freq).to_audio_segment(duration=thrust_duration // 2).fade_out(50)

            thrust = rise + fall
            thrust_track += thrust

        return thrust_track

    def _generate_fantasy(self):
        # Generate mystical tones using lower frequencies
        track = Sine(random.randint(200, 400)).to_audio_segment(duration=self.duration)
        return track

    def _generate_romance(self):
        # Generate softer, smoother tones
        track = Sine(random.randint(100, 300)).to_audio_segment(duration=self.duration)
        return track

    def _generate_drama(self):
        # Generate intense, deep tones for drama
        track = Sine(random.randint(50, 200)).to_audio_segment(duration=self.duration)
        return track

    def _generate_realism(self):
        # Generate more natural, neutral tones
        track = Sine(random.randint(300, 600)).to_audio_segment(duration=self.duration)
        return track

    def save_as_mp3(self, filename):
        if self.music is None:
            raise ValueError("No music generated yet!")
        self.music.export(filename, format="mp3")
        print(f"Music saved as {filename}")

# Example usage:
music_generator = GameMusicGenerator(theme="sci-fi", duration=30)  # 30 seconds of sci-fi music
music_generator.generate_music()
music_generator.save_as_mp3("sci_fi_background.mp3")
