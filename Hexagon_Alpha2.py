from panda3d.core import Point3, Vec3, WindowProperties, NodePath
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import numpy as np
import random
from panda3d.core import NodePath, CullFaceAttrib, PointLight, Vec4, Vec3
import threading
import time
import random
import os
from panda3d.core import CardMaker
from direct.showbase.ShowBase import ShowBase
import numpy as np
from Box import Box
from Sphere import Sphere
from panda3d.core import CollisionNode, CollisionSphere, CollisionHandlerQueue, CollisionTraverser
from direct.showbase.ShowBase import ShowBase

# Constants for physics
GRAVITY = -12  # Gravity constant along the Y-axis
SPHERE_RESTITUTION = 1.0  # Infinite bounce for spheres
CAMERA_RESTITUTION = .1  # Minimal bounce for the camera
JUMP_STRENGTH = 25000.0  # Initial upward momentum for jumping
PAN_SPEED = 20.0  # Speed of panning when Shift is held
ROTATE_SPEED = 50.0  # Speed of camera rotation when using A and D
TURN_SPEED = 25

import math
from panda3d.core import Vec3
import threading
import random
import os

from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode

def overlay_stats(engine_class):
    """
    This function accepts an instance of a class that contains ShowBase and overlays text stats
    on the lower right corner of the screen.
    """
    # Sample stats data to display (you can modify this as needed)
    sample_stats = {
        "Frame Rate": "60 FPS",
        "Objects": "123",
        "Memory Usage": "50 MB",
    }

    # Create a string to display stats
    stats_text = "\n".join([f"{key}: {value}" for key, value in sample_stats.items()])

    # Overlay text on the lower right corner using OnscreenText
    stats_display = OnscreenText(
        text=stats_text,  # The text to display
        pos=(1.25, -0.95),  # Position: lower-right corner
        scale=0.05,  # Text scale
        fg=(1, 1, 1, 1),  # Text color (white)
        align=TextNode.ARight,  # Right-align the text
        parent=engine_class.render2d,  # Attach to render2d (overlay on the screen)
        mayChange=True  # Allows dynamic changes to the text
    )

    # Return the OnscreenText instance for later modifications
    return stats_display



def local_to_global(node, local_pos):
	"""
	Converts local coordinates to global/world coordinates.
	
	:param node: The NodePath whose local coordinate system we are converting from.
	:param local_pos: A Point3 representing the local coordinates.
	:return: A Point3 representing the global/world coordinates.
	"""
	return node.getPos(render) + node.getQuat(render).xform(local_pos)

def global_to_local(node, global_pos):
	"""
	Converts global/world coordinates to local coordinates.
	
	:param node: The NodePath whose local coordinate system we are converting to.
	:param global_pos: A Point3 representing the global coordinates.
	:return: A Point3 representing the local coordinates.
	"""
	return node.getRelativePoint(render, global_pos)


import random
import os
from panda3d.core import Texture

class Grid:
	def __init__(self, grid_size_x: int, grid_size_y: int, grid_size_z: int, engine: ShowBase):
		"""
		Initialize the grid in Panda3D's coordinate system:
		- X-axis: left/right
		- Y-axis: forward/backward
		- Z-axis: up/down
		"""
		self.grid_size_x = grid_size_x  # Number of spheres along the X-axis
		self.grid_size_y = grid_size_y  # Number of spheres along the Z-axis
		self.grid_size_z = grid_size_z  # Number of spheres along the Y-axis
		self.engine = engine
		self.grid_node = NodePath('grid')  # Parent node for all spheres
		self.grid, self.all_spheres = self._initialize_grid(".\\textures\\bugger\\98736f6e-97cb-46cb-ace6-b998a0cd1254.jpg")  # Initialize the grid of spheres and the list of all spheres



	def _initialize_grid(self, custom_sphere_texture="None"):
		"""
		Initialize a 3D grid of spheres aligned with Panda3D's coordinate system.
		Additionally, add one custom sphere (NP_Sphere) with a specified texture.
		"""
		grid = []
		all_spheres = []
		sphere_radius_spacing = 900
		spacing =  1 # Define spacing between spheres

		# Calculate the starting positions to center the grid


		for x in range(self.grid_size_x):			
			row = []
			for y in range(self.grid_size_z):
				print(y)
				sphere_radius = random.uniform(4250, 4750)  # Random Z position
				start_x = random.uniform(-50000, 50000)
				start_y = random.uniform(-50000, 50000)
				start_z = random.uniform(-50000, 50000)  # Grid will be on the X-Y plane at Z = 0
				pos_x = start_x  * spacing  # Position alWWWWWWWWWWWWWWWWong the X-axis
				pos_y = start_y  * spacing  # Position along the Y-axis
				pos_z = start_z  * spacing
				

				# Create a sphere with a random texture
				# List of models
				models = ["models\\namaqualand_boulder_03_4k.egg", "models\\namaqualand_boulder_04_4k.egg", "models\\namaqualand_boulder_05_4k.egg"]

				# Select a random model
				s_model_name = random.choice(models)
				

				sphere = Sphere(pos_x, pos_y, pos_z, self.grid_size_z, radius=sphere_radius, engine=self.engine, model_name=s_model_name)
				
				sphere.model.reparentTo(self.grid_node)  # Parent the sphere to the grid node

				row.append(sphere)
				all_spheres.append(sphere)  # Add the sphere to the flat list of all spheres
			
			grid.append(row)

		# Prepare the path for the texture file in './textures/bugger/' folder
		texture_path = '.\\textures\\bugger'

		# Initialize custom texture variable
		custom_texture = None
		
		if custom_sphere_texture:
			# Construct the full path to the texture file
			full_texture_path = os.path.join(texture_path, custom_sphere_texture)
		print(full_texture_path)
		# Load texture from the file system if it exists
		if os.path.isfile(full_texture_path):
			print(full_texture_path)
			custom_texture = Texture()
			success = custom_texture.read(full_texture_path)
			if not success:
				print(f"Failed to load texture from {full_texture_path}")
			else:
				print(f"Loaded texture from {full_texture_path}")
		else:
			print(f"Texture file {full_texture_path} does not exist.")

		for bug_count in range (0,5):
			# Add a custom sphere called NP_Sphere
			sphere_radius = random.uniform(400, 800)  # Random Z position
			pos_x = random.uniform(-50000, 50000)  # Position along the X-axis
			pos_y = random.uniform(-50000, 50000)  # Positwion along the Y-axis
			pos_z = random.uniform(-50000, 50000)  # Random Z position

			# Create NP_Sphere with custom texture
			NP_Sphere = Sphere(pos_x * 1.5, pos_y * 1.5, pos_z * 1.5, self.grid_size_z, radius=sphere_radius, engine=self.engine, model_name = ".\\models\\spaceship.egg", texture_path = ".\\textures\\bugger\\texture_2.jpg", accorgrav = 0, rotate_x=90)
			
			# Set custom texture if it was loaded successfully
			if custom_texture:
				NP_Sphere.model.setTexture(custom_texture, 1)
			
			# Parent NP_Sphere to the grid node
			NP_Sphere.model.reparentTo(self.grid_node)

			all_spheres.append(NP_Sphere)  # Add NP_Sphere to the list of all spheres
			
			# Attach the entire grid to the render node
			self.grid_node.reparentTo(self.engine.render)
		print(len(all_spheres))
		return grid, all_spheres

	def update(self, dt):
		"""
		Update all spheres in the grid, passing the list of all spheres for gravitational calculations.
		"""
		for sphere in self.all_spheres:			
			result, spherepop= sphere.update(dt, self.all_spheres)  # Pass all spheres to calculate gravitational forces
			#Not acutally using spherepop here just recieving. Action done so far in another function
			if result is None:
				pass

	def get_sphere_room(self, x: int, y: int):
		"""
		Retrieve the room associated with a sphere at grid coordinates (x, y).
		"""
		if 0 <= x < self.grid_size_x and 0 <= y < self.grid_size_z:
			return self.grid[x][y].get_room()
		else:
			raise IndexError("Grid coordinates are out of bounds.")

	def hide_grid(self):
		"""
		Hide the entire grid.
		"""
		self.grid_node.hide()

	def show_grid(self):
		"""
		Show the entire grid.
		"""
		self.grid_node.show()

# CollisionHelper class: Manages collision detection between objects
class CollisionHelper:
    def __init__(self, engine, spheres):
        self.engine = engine
        self.spheres = spheres  # List of Sphere objects

        # Set up a collision traverser
        self.traverser = CollisionTraverser()

        # Set up a collision handler queue
        self.collision_queue = CollisionHandlerQueue()

        # Add each sphere's collision node to the traverser
        for sphere in spheres:
            self.traverser.addCollider(sphere.collision_np, self.collision_queue)

        # Add a task to detect collisions
        self.engine.taskMgr.add(self.detect_collisions, "detect_collision_task")

    def detect_collisions(self, task):
        self.traverser.traverse(self.engine.render)

        if self.collision_queue.getNumEntries() > 0:
            # Sort entries and handle collision events
            self.collision_queue.sortEntries()
            for entry in range(self.collision_queue.getNumEntries()):
                collision_entry = self.collision_queue.getEntry(entry)
                print(f"Collision detected between {collision_entry.getFromNodePath()} and {collision_entry.getIntoNodePath()}")

        return task.cont

class MyApp(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		self.set_full_screen()
		self.disableMouse()
		self.grid = Grid(5, 1, 5, self)
		self.box = Box(engine=self)  # Create the box around the grid
		self.Arena_Box = None
		self.current_box = self.box
		self.cam.setPos(0, 0, 0)
		self.cam.lookAt(1, 0, 0)
		self.setup_controls()
		self.taskMgr.add(self.update_camera, "updateCameraTask")
		self.mouse_speed = 000.0
		self.move_speed = 5000.0
		self.mouse_sensitivity = 0.2
		self.camera_velocity = Vec3(0, 0, 0)
		self.props = WindowProperties()
		self.props.setCursorHidden(True)
		self.win.requestProperties(self.props)
		self.win.movePointer(0, int(self.win.getProperties().getXSize() / 2), int(self.win.getProperties().getYSize() / 2))
		self.last_mouse_x = self.win.getPointer(0).getX()
		self.last_mouse_y = self.win.getPointer(0).getY()
		self.active_room = False
		self.time_modifier = 1
		self.portal_sphere = None
		self.stats_overlay = overlay_stats(self)
		self.last_loc = None

		# Adjust the camera's FOV
		lens = self.cam.node().getLens()
		lens.setFov(90, 60)  # 90 degrees horizontal and 60 degrees vertical FOV
		lens.setAspectRatio(self.getAspectRatio())  # Ensure aspect ratio is correct
		#self.jump_sound = self.loader.loadSfx("sounds\\jump_sound.wav")
		self.in_arena = False

		self.animated_objects = []
		self.Arena_Exit_Box = None

	import numpy as np


	import numpy as np
	import math

	def is_camera_pointing_at_sphere(self, camera, sphere, camera_fov):
		"""
		Determines if the camera is pointing at the sphere by transforming the sphere's position
		to the camera's local coordinate system.
		
		Parameters:
		camera: The camera object (e.g., base.camera).
		sphere: The Sphere object whose position and radius we will check.
		camera_fov: The camera's field of view in degrees (horizontal or vertical depending on how you wanwwwwwwwwwwwwwat to calculate).
		
		Returns:
		bool: True if the camera is pointing directly at the sphere, False otherwise.
		"""
		# 1. Get the sphere's position in the camera's local coordinate space
		sphere_pos_world = sphere.model.getPos(self.cam)  # Get the sphere's world position
		sphere_pos_camera = camera.getRelativePoint(self.cam, sphere_pos_world)  # Transform into camera's local space
		#print(f"sphere_pos_world{sphere_pos_world}")
		# 2. Check if the sphere is behind the camera (negative Y in camera space)
		if sphere_pos_camera[1] <= 0:
			# Sphere is behind the camera, return False immediately
			return False

		# 3. Calculate the vector from the camera to the sphere in camera space
		camera_to_sphere_vec = np.array([sphere_pos_camera[0], sphere_pos_camera[1], sphere_pos_camera[2]])
		
		# Normalize the vector to the sphere
		camera_to_sphere_vec_normalized = camera_to_sphere_vec / np.linalg.norm(camera_to_sphere_vec)
		
		# 4. Define the camera's forward direction in camera space (along positive Y-axis)
		camera_forward_vec = np.array([0, 1, 0])  # Camera's forward direction in its own space
		
		# 5. Calculate the dot product between the camera's forward vector and the camera-to-sphere vector
		dot_product = np.dot(camera_forward_vec, camera_to_sphere_vec_normalized)
		
		# If dot product is negative, the sphere is behind the camera (redundant check)
		if dot_product < 0:
			return False

		# 6. Calculate the angle between the camera's forward direction and the vector to the sphere
		angle_to_sphere = math.degrees(math.acos(dot_product))

		# 7. Calculate the half-FOV in degrees (half of the total FOV)
		half_fov = camera_fov / 2

		# 9. Check if the angle to the sphere is within the camera's field of view
		if abs(angle_to_sphere) <= half_fov:			
			# The camera is pointing at the sphere
			return True
		else:
			# The sphere is outside the camera's field of view
			return False


	def setup_controls(self):
		self.key_map = {
			"forward": False,
			"backward": False,
			"left": False,
			"right": False,
			"jump": False,
			"shift": False,
			"turbo": False
		}
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
		print("Jump")
		if self.cam.getZ() <= 0:
			self.camera_velocity.setZ(JUMP_STRENGTH)
		camera_position = self.cam.getPos(self.render)        
		camera_hpr = self.cam.getHpr(self.render)
		#object_local_pos = object.getRelativePoint(self.render, camera_position)
		#object_local_hpr = object.getRelativeHpr(self.render, camera_hpr)
				
		if self.cam.getZ() <= 0:
			self.camera_velocity.setZ(100)
		

	def set_full_screen(self):
		"""
		Sets the display to full screen.
		"""
		props = WindowProperties()
		props.setFullscreen(False)  # Enable full screen mode
		props.setSize(1800, 1200)   # Set window size to 1800x1200
		self.win.requestProperties(props)

	def is_camera_out_of_bounds(self, box, camera):
		 # Get the box's half size (half-extents)
		box_half_x = box.x /2 # Half-width of the box
		box_half_y = box.y /2 # Half-depth of the box
		box_half_z = box.z /2 # Half-height of the box
		box_offset = box.x_offset  # Offset along the X-axis

		# Calculate the min and max values for x, y, and z based on the box's position, size, and offset
		box_min_x = -(box_half_x) - box_offset
		box_max_x = (box_half_x) - box_offset
		box_min_y = -(box_half_y)
		box_max_y = (box_half_y)
		box_min_z = -(box_half_z)
		box_max_z = (box_half_z)

		# Print the calculated min and max bounds (optional for debugging)
		#print(f"Box Min X: {box_min_x}, Box Max X: {box_max_x}")
		#print(f"Box Min Y: {box_min_y}, Box Max Y: {box_max_y}")
		#print(f"Box Min Z: {box_min_z}, Box Max Z: {box_max_z}")

		# Get the camera's global position
		camera_pos = camera.getPos(render)
		camera_in_sphere_space = render.getRelativePoint(render, camera_pos)
		#print(f"camera_in_sphere_space  {camera_in_sphere_space}")

		# Clamp the camera position within the bounds
		clamped_x = max(box_min_x+1000, min(camera_pos.x, box_max_x-1000))
		clamped_y = max(box_min_y+1000, min(camera_pos.y, box_max_y-1000))
		clamped_z = max(box_min_z+1000, min(camera_pos.z, box_max_z-1000))

		# Set the camera's position to the clamped values
		self.cam.setPos(render, clamped_x, clamped_y, clamped_z)

		#print(f"Camera position clamped to: {clamped_x}, {clamped_y}, {clamped_z}")


	def update_camera(self, task):
		# -- debug		
		dt = globalClock.getDt() * self.time_modifier * 1
		self.handle_mouse()

		if self.current_box == self.Arena_Box:
			GRAVITY = -50000
			self.move_speed = 10000.0
		else:
			GRAVITY = -50
			self.move_speed = 50000.0
		#print(f"Gravity {GRAVITY}")

		# Apply gravity to camera's Z velocity
		self.camera_velocity.setZ(self.camera_velocity.getZ() + GRAVITY * dt)
		
		# Update the camera's position based on velocity
		self.cam.setPos(self.cam.getPos() + self.camera_velocity * dt)
		
		# Get the camera's global position
		camera_pos = self.cam.getPos(self.render)
		
		# Convert the camera's global position into the sphere's local space
		camera_in_sphere_space = self.render.getRelativePoint(self.render, camera_pos)
		
		print(f"Camera position: {self.cam.getPos()}" + f" - Box position: {self.box.box_center.getPos()}" + f"camera_in_sphere_space = {print(camera_in_sphere_space)}")

		# Define the minimum allowed Z position in the sphere's local space
		#print(camera_pos.z, camera_in_sphere_space.z)
		min_z_in_sphere = -65000

		# Check for outside bounds
		if self.is_camera_out_of_bounds(self.current_box, self.cam):
			print("oob")

		# Check if the camera's Z position in the sphere's space is below the threshold
		if camera_in_sphere_space.z <= min_z_in_sphere:
			# Reflect the camera's Z velocity with a restitution factor
			#self.camera_velocity.setZ(-self.camera_velocity.getZ() * CAMERA_RESTITUTION)

			# Adjust the camera's position to be exactly at the threshold
			camera_in_sphere_space.setZ(min_z_in_sphere)

			# Convert the sphere's local space back to global space and set the camera's position
			new_camera_position = self.render.getRelativePoint(self.camera, camera_in_sphere_space)
			self.cam.setPos(new_camera_position)

		# Handle other controls and logic
		self.handle_controls(dt, self.current_box)
		if not self.in_arena:
			self.grid.update(dt)
			self.last_loc = self.cam.getPos()
		self.check_camera_inside_sphere()

		# Getting the camera's position relative to global space (render)
		camera_position = self.camera.getPos(self.render)  # Use render, not self
		camera_direction = self.camera.getQuat(self.render).getForward()  # Camera forward direction vector in global space
		spheres = self.grid.all_spheres  # All spheres in the scene

		for sphere in spheres:
			# Convert the local point to global coordinates
			local_point = Point3(0, 0, 0)
			camera_pos = self.camera.getPos(self.cam)
			# Convert the camera's global position into the sphere's local space
			camera_in_sphere_space = sphere.model.getRelativePoint(self.render, camera_pos)
			
			camera_fov = self.camLens.getFov()[0]
			if self.is_camera_pointing_at_sphere(self.camera, sphere, camera_fov):
				#print("Camera is pointing at the sphere!")
				pass
			else:
				pass #print("Camera is not pointing at the sphere.")
		
		# Check if the camera is inside the Arena_Exit_Box		
		if self.Arena_Exit_Box is not None:
			if self.Arena_Exit_Box.is_camera_inside(self.cam.getPos()):
				self.in_arena = False		
				#self.camera_velocity = Vec3(0, 0, 0)  # Reset the camera's velocity			
				self.cam.setPos(self.last_loc)
				self.last_loc = None
				self.portal_sphere = None
				self.current_box = self.box	
				
				
		
		return Task.cont

	def handle_mouse(self):
		if self.mouseWatcherNode.hasMouse():
			mouse_x = self.win.getPointer(0).getX()
			mouse_y = self.win.getPointer(0).getY()
			delta_x = mouse_x - self.last_mouse_x
			delta_y = mouse_y - self.last_mouse_y
			new_heading = self.cam.getH() - delta_x * self.mouse_sensitivity
			new_pitch = self.cam.getP() - delta_y * self.mouse_sensitivity
			new_pitch = max(min(new_pitch, 90), -90)
			self.cam.setHpr(new_heading, new_pitch, 0)
			self.win.movePointer(0, int(self.win.getProperties().getXSize() / 2), int(self.win.getProperties().getYSize() / 2))
			self.last_mouse_x = self.win.getPointer(0).getX()
			self.last_mouse_y = self.win.getPointer(0).getY()

	def handle_controls(self, dt, box):
		# Camera movement control logic aligned with the camera's facing direction
		desired_pos = self.cam.getPos()  # Start with the current camera position

		if self.key_map["forward"]:
			# Move forward in the direction the camera is facing (along Y-axis)
			self.cam.setPos(self.cam, 0, self.move_speed * dt, 0)
			desired_pos = self.cam.getPos()

		if self.key_map["turbo"]:
			# Move forward in the direction the camera is facing (along Y-axis)
			self.cam.setPos(self.cam, 0, self.move_speed * dt * 100, 0)
			desired_pos = self.cam.getPos()

		if self.key_map["backward"]:
			# Move backward in the opposite direction (along Y-axis)
			self.cam.setPos(self.cam, 0, -self.move_speed * dt, 0)
			desired_pos = self.cam.getPos()

		# Strafing control logic for "A" and "D" keys
		STRAFE_SPEED = -self.move_speed  # Define a speed for strafing

		if self.key_map["left"]:
			# Strafe to the left (move camera left relative to its orientation)
			strafe_vector = self.cam.getRelativeVector(render, (STRAFE_SPEED * dt, 0, 0))
			desired_pos += strafe_vector

		if self.key_map["right"]:
			# Strafe to the right (move camera right relative to its orientation)
			strafe_vector = self.cam.getRelativeVector(render, (-STRAFE_SPEED * dt, 0, 0))
			desired_pos += strafe_vector

		# Clamp the desired position based on the box bounds before updating the camera position
		clamped_x = max(-(box.x/2) - box.x_offset, min(desired_pos.x, (box.x/2) - box.x_offset))
		clamped_y = max(-(box.y/2), min(desired_pos.y, (box.y/2)))
		clamped_z = max(-(box.z/2), min(desired_pos.z, (box.z/2)))

		# Set the camera's position to the clamped position
		self.cam.setPos(clamped_x, clamped_y, clamped_z)

		#print(f"Camera position clamped to: {clamped_x}, {clamped_y}, {clamped_z}")


	
	def update_key(self, key, value):
		self.key_map[key] = value

	def check_camera_inside_sphere(self):		
		cam_pos = self.cam.getPos()
		inside_any_sphere = False

		# Check if the camera is inside any sphere
		for x in range(self.grid.grid_size_x):
			for z in range(self.grid.grid_size_z):
				sphere = self.grid.grid[x][z]
				if sphere.is_camera_inside(cam_pos) and not self.current_box is None:
					self.last_loc = self.cam.getPos()
					inside_any_sphere = True

					# Clean up previous boxes and objects before creating new ones
					if self.current_box is not None:
						self.current_box = None  # Destroy or clean up the box
					if self.Arena_Exit_Box is not None:
						self.Arena_Exit_Box = None  # Clean up exit box

					# Teleport logic here (if applicable)

					# Create new boxes
					
					print(f"self.last_loc if sphere.is_camera_inside {self.last_loc}")

					self.current_box = self.Arena_Box = Box(self, x=250000, y=250000, z=150000/3, x_offset=-251000, texture_path=sphere.texture_path, far=250100)
					
					self.Arena_Exit_Box = Box(self, x=5000, y=5000, z=5000, x_offset=-251000, z_offset=25000, texture_path=".\\wall_textures\\9a1b7e53-116c-4fce-8adb-f78b4e1849a1.jpg", far=250100)

					# Update the portal sphere
					self.portal_sphere = sphere
					self.in_arena = True	
					
								
					return  # Exit the loop early once inside a sphere

		

	



if __name__ == "__main__":
	app = MyApp()
	app.run()
