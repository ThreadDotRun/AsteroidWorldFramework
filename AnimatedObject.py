from panda3d.core import Texture, TextureStage
from direct.task import Task
import os
import threading
from pydub import AudioSegment
import time

class AnimatedObject:
    def __init__(self, base, all_spheres, obj, animation_folder, sound_folder, n_frames=5):
        self.base = base  # Store the passed-in base for accessing taskMgr
        self.obj = obj  # The Panda3D object containing the model
        self.all_spheres = all_spheres
        self.animation_folder = animation_folder
        self.sound_folder = sound_folder
        self.texture_stage = TextureStage("animation")
        self.nearest = obj

        # Preload textures into memory
        self.textures = []
        texture_files = sorted([f for f in os.listdir(self.animation_folder) if f.endswith(".jpg")])
        for texture_file in texture_files:
            texture_path = os.path.join(self.animation_folder, texture_file)
            texture = Texture()
            texture.read(texture_path)
            self.textures.append(texture)

        # Preload sounds into memory
        self.sounds = []
        sound_files = sorted([f for f in os.listdir(self.sound_folder) if f.endswith(".mp3") or f.endswith(".wav")])
        for sound_file in sound_files:
            sound_path = os.path.join(self.sound_folder, sound_file)
            sound = AudioSegment.from_file(sound_path)
            self.sounds.append(sound)

        self.current_frame = 0
        self.animation_running = False
        self.sound_running = False
        self.control_running = False

        # New variable to control the number of iterations (frames to play)
        self.n_frames = n_frames  # Number of times to loop through the textures (optional)
        self.frames_played = 0  # To track the number of frames played

        # Flags to track completion
        self.animation_done = False
        self.sound_done = False
        self.stopped = False  # Track whether stop has already been called

    def start(self):
        """Start both animation and sound."""
        self.animation_running = True
        self.sound_running = True
        self.control_running = True
        
        # Start the animation task using the passed-in base's taskMgr
        self.base.taskMgr.add(self.animate_task, "AnimateTask")

        # Start sound playback in a separate thread
        self.sound_thread = threading.Thread(target=self.play_sound)
        self.sound_thread.start()

    def stop(self):
        """Stop both animation and sound."""
        # Prevent multiple calls to stop
        if self.stopped:
            return
        self.stopped = True  # Mark stop as called

        # If both tasks are done, clean up
        if self.animation_done and self.sound_done:
            self.cleanup()  # Move the clean-up logic to a separate method

    def cleanup(self):
        """Cleanup the object and remove the task."""
        # Remove the animation task
        self.base.taskMgr.remove("AnimateTask")

        # Remove the object from all_spheres and detach the model
        if self.obj in self.all_spheres:
            index = self.all_spheres.index(self.obj)
            print(f"Popping sphere {index}")
            self.all_spheres.pop(index)
            self.obj.model.detachNode()

        print("All tasks completed and object removed.")

    def animate_task(self, task):
        """Task for managing texture-based animation."""
        if not self.animation_running:
            return Task.done  # Stop the task if the animation is stopped

        # If n_frames is set and we reached the limit, stop the task
        if self.n_frames is not None and self.frames_played >= self.n_frames:
            print("Reached specified number of frames. Stopping animation.")
            self.animation_done = True  # Mark animation as done
            self.check_termination()  # Check if sound is also done
            time.sleep(0.2)
            	
            return Task.done

        # Switch to the next texture
        texture = self.textures[self.current_frame]
        self.obj.model.setTexture(self.texture_stage, texture, 1)

        # Move to the next frame
        self.current_frame = (self.current_frame + 1) % len(self.textures)

        # Increment the number of frames played
        self.frames_played += 1

        # Set the task to run again after 1/24th of a second
        return task.again  # Continue this task on the next frame

    def play_sound(self):
        """Play sound in sequence."""
        for sound in self.sounds:
            if not self.sound_running:
                break

            # Play the sound (disabled for testing)
            # play(sound)

            # Sleep until the sound finishes playing
            time.sleep(len(sound) / 10.0)

        # Mark sound as done
        self.sound_done = True
        self.check_termination()  # Check if animation is also done

    def check_termination(self):
        """Check if both sound and animation are done, then stop."""
        if self.animation_done and self.sound_done:
            self.cleanup()  # Call cleanup only if both are done
