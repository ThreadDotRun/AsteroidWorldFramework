from direct.showbase.ShowBase import ShowBase
from panda3d.core import PointLight, NodePath, Vec3, Filename
import threading
import time
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GameObject:
	def __init__(self, model_folder: str, texture_folder: str, sound_folder: str, radius: float = 1.0, time_modifier: float = 1.0, delta_time: float = 0.05, thread_delay: float = 0.1):
		self.model_folder = model_folder
		self.texture_folder = texture_folder
		self.sound_folder = sound_folder
		self.radius = radius
		self.time_modifier = time_modifier
		self.delta_time = delta_time
		self.thread_delay = thread_delay

		# Load the initial model and texture
		initial_model_path = self.get_model_path(1)
		initial_texture_path = self.get_texture_path(1)

		if initial_model_path and os.path.exists(initial_model_path):
			self.model = loader.loadModel(initial_model_path)
			self.model.setScale(radius)
			self.model.reparentTo(render)
		else:
			self.model = NodePath("GameObject")  # Placeholder node for missing models
			self.model.reparentTo(render)
			logging.warning("Initial model not found. Using placeholder NodePath.")

		if initial_texture_path and os.path.exists(initial_texture_path):
			texture = loader.loadTexture(initial_texture_path)
			self.model.setTexture(texture)
		else:
			logging.warning("Initial texture not found. No texture applied.")

		# Initialize threading flags and state control
		self.position_flag = threading.Event()
		self.direction_flag = threading.Event()
		self.model_update_flag = threading.Event()
		self.texture_update_flag = threading.Event()
		self.sound_update_flag = threading.Event()
		self.running = True
		self.update_in_progress = False  # To prevent overlapping updates

		# Start the update thread
		self.start_update()

	def get_model_path(self, index: int) -> str:
		"""Retrieve the model path based on an index."""
		model_path = os.path.join(self.model_folder, f"model_{index}.egg")  # or .egg, .obj
		return model_path if os.path.exists(model_path) else None

	def get_texture_path(self, index: int) -> str:
		"""Retrieve the texture path based on an index."""
		texture_path = os.path.join(self.texture_folder, f"texture_{index}.jpg")  # or .jpg, .tiff, etc.
		return texture_path if os.path.exists(texture_path) else None

	def apply_model(self, index: int):
		"""Apply a new model based on the given index."""
		model_path = self.get_model_path(index)
		if model_path:
			self.model.removeNode()  # Remove the current model
			self.model = loader.loadModel(model_path)  # Load the new model
			self.model.setScale(self.radius)
			self.model.reparentTo(render)
			logging.info(f"Applied model {model_path}")
		else:
			logging.warning(f"Model for index {index} not found. Model update skipped.")

	def apply_texture(self, index: int):
		"""Apply a new texture based on the given index."""
		texture_path = self.get_texture_path(index)
		if texture_path:
			texture = loader.loadTexture(texture_path)
			self.model.setTexture(texture)
			logging.info(f"Applied texture {texture_path}")
		else:
			logging.warning(f"Texture for index {index} not found. Texture update skipped.")

	# Rest of the GameObject code, including update_thread_function, etc.

	# Rest of the GameObject code, including update_thread_function, etc.


	def get_sound_path(self, index: int) -> str:
		"""Retrieve the sound path based on an index."""
		sound_path = os.path.join(self.sound_folder, f"sound_{index}.wav")  # or .mp3, .ogg, etc.
		return sound_path if os.path.exists(sound_path) else None

	def start_update(self):
		"""Start the update thread."""
		self.update_thread = threading.Thread(target=self.update_thread_function, daemon=True)
		self.update_thread.start()

	def set_position(self, x: float, y: float, z: float):
		"""Set the object's position in the game space."""
		self.model.setPos(x, y, z)

	def set_direction(self, x: float, y: float, z: float):
		"""Set the object's movement direction and trigger direction update."""
		self.direction = Vec3(x, y, z).normalized()
		self.direction_flag.set()  # Automatically triggers direction update

	def set_velocity(self, velocity: float):
		"""Set the object's velocity and trigger position update."""
		self.velocity = velocity
		self.position_flag.set()  # Automatically triggers position update

	def set_model(self, model_path: str):
		"""Change the object's model and trigger model update."""
		self.model.removeNode()  # Remove current model
		self.model = loader.loadModel(model_path)  # Load new model
		self.model.reparentTo(render)
		self.model_update_flag.set()  # Trigger model update

	def set_texture(self, texture_path: str):
		"""Change the object's texture and trigger texture update."""
		texture = loader.loadTexture(texture_path)
		self.model.setTexture(texture)
		self.texture_update_flag.set()  # Trigger texture update

	def play_sound(self, index):
		"""Placeholder to play a sound by index."""
		sound_path = self.get_sound_path(index)
		if sound_path:
			# Placeholder for actual sound playback
			logging.info(f"Playing sound {sound_path}")

	def stop_sound(self):
		"""Placeholder to stop sound playback."""
		logging.info("Stopping sound")

	def update_thread_function(self):
		"""Continuously update the object's state based on flags and delta time (dt)."""
		while self.running:
			if self.update_in_progress:
				logging.warning("Update already in progress, skipping this iteration.")
				time.sleep(self.thread_delay)
				continue

			self.update_in_progress = True
			dt = globalClock.getDt() * self.time_modifier

			if self.position_flag.is_set():
				new_pos = self.model.getPos() + self.direction * self.velocity * dt
				self.model.setPos(new_pos)
				self.position_flag.clear()

			if self.direction_flag.is_set():
				self.model.lookAt(self.model.getPos() + self.direction * dt)
				self.direction_flag.clear()

			if self.model_update_flag.is_set():
				self.apply_model(1)  # Example to load model_1
				self.model_update_flag.clear()

			if self.texture_update_flag.is_set():
				self.apply_texture(1)  # Example to load texture_1
				self.texture_update_flag.clear()

			if self.sound_update_flag.is_set():
				self.play_sound(1)  # Example to play sound_1
				self.sound_update_flag.clear()

			self.update_in_progress = False
			time.sleep(self.delta_time)

	def stop_updates(self):
		"""Stop all updates and clean up the update thread."""
		self.running = False
		self.update_thread.join()

	def destroy(self):
		"""Clean up the object when it is no longer needed."""
		self.stop_updates()
		self.model.removeNode()



class CameraObject(GameObject):
	def __init__(self, model_folder: str, texture_folder: str, sound_folder: str, radius: float = 1.0, time_modifier: float = 1.0, delta_time: float = 0.05, thread_delay: float = 0.1):
		super().__init__(model_folder, texture_folder, sound_folder, radius, time_modifier, delta_time, thread_delay)
		self.model = base.camera  # Use the camera node directly instead of a loaded model

	def set_position(self, x: float, y: float, z: float):
		"""Set camera position directly."""
		self.model.setPos(x, y, z)

	def set_fov(self, fov: float):
		"""Set the camera's field of view."""
		self.model.node().getLens().setFov(fov)


from direct.showbase.ShowBase import ShowBase
from panda3d.core import PointLight, Vec3
import logging

from direct.showbase.ShowBase import ShowBase
from panda3d.core import PointLight, Vec3, WindowProperties
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GameController(ShowBase):
	def __init__(self):
		super().__init__()

		# Folders for model, texture, and sound resources
		model_folder = "./models/eyeball/Eyeball/"
		texture_folder = "./textures/bugger/"
		sound_folder = "./sounds/"

		# Camera settings and movement speed
		self.disableMouse()  # Disable Panda3D's default mouse control
		self.move_speed = 5.0
		self.camera_velocity = Vec3(0, 0, 0)
		
		# Variables for mouse look sensitivity and initial orientation
		self.mouse_sensitivity = 0.2
		self.pitch = 0.0  # Vertical rotation
		self.yaw = 0.0	# Horizontal rotation

		# Lock the mouse to the center of the screen
		self.set_mouse_lock()

		# Create a GameObject instance with a default model and position
		self.box = GameObject(model_folder=model_folder, texture_folder=texture_folder, sound_folder=sound_folder)
		self.box.set_position(3, 5, 0)
		self.box.set_direction(1, 1, 0)
		self.box.set_velocity(0.01)

		# Set up lighting
		self.setup_lighting()
		
		# Initialize camera controls
		self.setup_controls()

		self.set_full_screen()
		
		# Task to update camera movement
		self.taskMgr.add(self.update, "update_task")

	def set_full_screen(self):
		"""
		Sets the display to full screen.
		"""
		props = WindowProperties()
		props.setFullscreen(False)  # Enable full screen mode
		props.setSize(1800, 1200)   # Set window size to 1800x1200
		self.win.requestProperties(props)

	def set_mouse_lock(self):
		"""Lock the mouse to the center of the window for consistent movement tracking."""
		props = WindowProperties()
		props.setCursorHidden(True)
		props.setMouseMode(WindowProperties.MRelative)  # Enable relative mouse mode
		self.win.requestProperties(props)

	def setup_lighting(self):
		"""Set up lighting in the scene."""
		plight = PointLight("plight")
		plight_node = self.render.attachNewNode(plight)
		plight_node.setPos(5, -10, 7)
		self.render.setLight(plight_node)

	def update_key(self, key, value):
		"""Update the key map for movement controls."""
		self.key_map[key] = value

	def setup_controls(self):
		"""Set up key mappings for movement and actions."""
		self.key_map = {
			"forward": False,
			"backward": False,
			"left": False,
			"right": False,
			"jump": False,
			"shift": False,
			"turbo": False
		}

		# Set up key bindings
		self.accept("w", self.update_key, ["forward", True])
		self.accept("w-up", self.update_key, ["forward", False])
		self.accept("s", self.update_key, ["backward", True])
		self.accept("s-up", self.update_key, ["backward", False])
		self.accept("a", self.update_key, ["left", True])
		self.accept("a-up", self.update_key, ["left", False])
		self.accept("d", self.update_key, ["right", True])
		self.accept("d-up", self.update_key, ["right", False])
		self.accept("shift", self.update_key, ["shift", True])
		self.accept("shift-up", self.update_key, ["shift", False])
		self.accept("space", self.jump)
		self.accept("shift-w-down", self.update_key, ["turbo", True])
		self.accept("shift-w-up", self.update_key, ["turbo", False])

	def jump(self):
		"""Handle jump action."""
		if self.cam.getZ() <= 0:
			self.camera_velocity.setZ(100)  # Set jump strength as desired

	def handle_mouse_look(self, dt):
		"""Update camera orientation based on mouse movement."""
		if self.mouseWatcherNode.hasMouse():
			# Get mouse movement delta
			md = self.win.getPointer(0)
			delta_x = md.getX() - self.win.getProperties().getXSize() / 2
			delta_y = md.getY() - self.win.getProperties().getYSize() / 2

			# Adjust yaw (horizontal rotation) and pitch (vertical rotation)
			self.yaw -= delta_x * self.mouse_sensitivity * dt
			self.pitch -= delta_y * self.mouse_sensitivity * dt
			self.pitch = max(-90, min(90, self.pitch))  # Limit pitch to prevent flipping

			# Apply the rotation to the camera
			self.cam.setHpr(self.yaw, self.pitch, 0)

			# Recenter the mouse pointer to keep tracking movement
			self.win.movePointer(0, int(self.win.getProperties().getXSize() / 2), int(self.win.getProperties().getYSize() / 2))

	def handle_controls(self, dt):
		"""Handle camera movement based on key states."""
		desired_pos = self.cam.getPos()  # Start with the current camera position

		if self.key_map["forward"]:
			# Move forward in the camera's direction
			self.cam.setPos(self.cam, 0, self.move_speed * dt, 0)

		if self.key_map["turbo"]:
			# Move forward faster with turbo
			self.cam.setPos(self.cam, 0, self.move_speed * dt * 10, 0)

		if self.key_map["backward"]:
			# Move backward
			self.cam.setPos(self.cam, 0, -self.move_speed * dt, 0)

		# Strafing controls
		if self.key_map["left"]:
			strafe_vector = self.cam.getRelativeVector(render, Vec3(-self.move_speed * dt, 0, 0))
			desired_pos += strafe_vector

		if self.key_map["right"]:
			strafe_vector = self.cam.getRelativeVector(render, Vec3(self.move_speed * dt, 0, 0))
			desired_pos += strafe_vector

		# Clamp camera position within the box bounds
		self.clamp_position_within_box(desired_pos)

	def clamp_position_within_box(self, desired_pos):
		"""Clamp camera position within the boundaries of the box."""
		box_x_half = self.box.radius * 0.5
		box_y_half = self.box.radius * 0.5
		box_z_half = self.box.radius * 0.5

		clamped_x = max(-box_x_half, min(desired_pos.x, box_x_half))
		clamped_y = max(-box_y_half, min(desired_pos.y, box_y_half))
		clamped_z = max(0, min(desired_pos.z, box_z_half))

		self.cam.setPos(clamped_x, clamped_y, clamped_z)

	def update(self, task):
		"""Update camera position, handle controls, and apply mouse look each frame."""
		dt = globalClock.getDt()
		self.handle_mouse_look(dt)
		self.handle_controls(dt)
		return task.cont

# Run the demo
demo = GameController()
demo.run()


# Run the demo
demo = GameController()
demo.run()
