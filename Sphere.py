from direct.showbase.ShowBase import ShowBase
import random
from panda3d.core import NodePath, CullFaceAttrib, PointLight, Vec4, Vec3
import os
import threading
import numpy as np
import math
import time
from direct.task import Task
from AnimatedObject import AnimatedObject
from math import atan2, degrees
from panda3d.core import CollisionNode, CollisionSphere



GRAVITATIONAL_CONSTANT = 6.67430e-11 *1e6 # Normal gravitational constant in m^3 kg^-1 s^-2
  # Scale up gravitational constant for simulation

SPHERE_RESTITUTION = 0.9  # Elasticity of the collision
GRAVITY = -29.81  # Gravity on the Z-axis


class Sphere:
	def __init__(self, x: float, y: float, z: float, grid_size_z: float, radius: float, engine: ShowBase, texture_path: str = None, model_name='./models/namaqualand_boulder_03_4k.egg', accorgrav=1, rotate_x=0):
		super().__init__()  # Initialize the Thread class
		self.rotate_x = rotate_x
		self._x = x
		self._y = y
		self._z = z
		self.a = None

		self._radius = radius
		self.engine = engine		
		self.model_name = model_name
		# Assign small random initial velocity
		self.velocity = Vec3(
			random.uniform(-1500, 1500),  # Random velocity in the X-axis
			random.uniform(-1500, 1500),  # Random velocity in the Y-axis
			random.uniform(-1500, 1500)   # Random velocity in the Z-axis
		)
		self.texture_path = texture_path if texture_path else self._get_random_texture()
		self.lock = threading.Lock()  # Ensure thread safety
		self._initialize_game_object()
		self.grid_size_z = grid_size_z  # Set the grid size
		self.mass = (4/3) * math.pi * self._radius**3 * (5.972e23 / (6371e3)**2) 
		# Assume mass is proportional to volume
		#print(f"Sphere mass: {self.mass}")  # Debugging mass
		self.skipper = 100
		self.count = 0
		self.accorgrav = accorgrav
		self.base =  engine  # Manually instantiate ShowBase to access 'loader'
		self.animating = False  # Flag to indicate if the animation is running
		self.animation_thread = None
		self.pop_sound = engine.loader.loadSfx("sounds/pop_sound.wav")
		self.last_execution_time = -float('inf')  # Infinite in the past
		self.time_interval = 2  # Set time interval (in

		# Create a collision node for this sphere
		self.collision_node = CollisionNode(f"sphere_collision_{id(self)}")
		self.collision_solid = CollisionSphere(0, 0, 0, self._radius)  # Sphere centered at (0, 0, 0) with radius
		self.collision_node.addSolid(self.collision_solid)

		# Attach the collision node to the sphere's model
		self.collision_np = self.model.attachNewNode(self.collision_node)
		self.collision_np.show()  # Optional: To visualize the collision sphere
		

	def _animate_textures(self, nearest):
		"""
		Animates the textures by changing them over time from the folder /textures/sphere/animate/.
		"""
		texture_folder = "textures/sphere/animate/"
		texture_files = sorted(os.listdir(texture_folder))  # Assuming all files in the folder are textures
		texture_files = [f for f in texture_files if f.endswith(".png") or f.endswith(".jpg")]  # Filter valid textures

		for texture_file in texture_files:
			# Load the texture
			texture_path = os.path.join(texture_folder, texture_file)
			texture = nearest.engine.loader.loadTexture(texture_path)

			# Apply the texture to the sphere model
			nearest.model.setTexture(texture, 1)

			# Wait for a short duration before applying the next texture
			time.sleep(0.5)  # Adjust the duration between texture changes as needed

		# After animation ends, perform the final actions
		self._finalize_sphere(nearest)

	def _finalize_sphere(self, nearest, all_spheres):
		"""
		Finalizes by playing the sound, animating the sphere, and removing it.
		"""
		if nearest:
			# Load a sound effect and play it
			sound_effect = self.pop_sound
			sound_effect.play()

			# Animate the sphere
			nearest.animate()

			# Remove the sphere from the list and detach its model
			index = all_spheres.index(nearest)
			all_spheres.pop(index)
			nearest.model.detachNode()

			print(f"Sphere at index {index} was removed.")	

	def getXYZ(self):
		return self._x, self._y, self._z 

	def _initialize_game_object(self):
		self.model = self.engine.loader.loadModel(self.model_name)
		self.model.reparentTo(self.engine.render)
		self.model.setPos(self._x, self._y, self._z)

		# Seed the random generator with the current time for more randomness
		random.seed(time.time() + random.random())

		# Set initial random rotation
		random_pitch = random.uniform(0, 360)
		random_roll = random.uniform(0, 360)
		random_heading = random.uniform(0, 360)
		self.model.setHpr(random_heading, random_pitch, random_roll)

		self.model.setScale(self._radius)
		texture = self.engine.loader.loadTexture(self.texture_path)
		self.model.setTexture(texture, 1)

		# Add unique rotation speed for each object
		self.rotation_speed_heading = random.uniform(-50, 50)  # Speed for heading (yaw)
		self.rotation_speed_pitch = random.uniform(-50, 50)    # Speed for pitch
		self.rotation_speed_roll = random.uniform(-50, 50)     # Speed for roll

		# Add a task to rotate the model continuously
		self.engine.taskMgr.add(self.rotate_model_task, "RotateModelTask")

	def rotate_model_task(self, task):
		# Increment rotation based on individual speeds
		heading, pitch, roll = self.model.getHpr()
		heading += self.rotation_speed_heading * globalClock.getDt()  # Time-based increment
		pitch += self.rotation_speed_pitch * globalClock.getDt()
		roll += self.rotation_speed_roll * globalClock.getDt()

		# Apply new rotation
		if self.accorgrav == 1:
			self.model.setHpr(heading, pitch, roll)

		return task.cont  # Continue the task
		
	def _get_random_texture(self):
		texture_folder = "textures"
		textures = [os.path.join(texture_folder, f) for f in os.listdir(texture_folder) if os.path.isfile(os.path.join(texture_folder, f))]
		return random.choice(textures)

	def _calculate_distance(self, other_sphere):
		"""Returns the distance between this sphere and another sphere, ensuring minimum distance is radius * 2."""
		pos_self = Vec3(self.model.getPos())
		pos_other = Vec3(other_sphere.model.getPos())
		actual_distance = (pos_self - pos_other).length()

		# Minimum distance should be at least the diameter of the sphere (radius * 2)
		min_distance = self._radius + other_sphere._radius

		# Return the greater of the actual distance or the minimum distance
		return max(actual_distance, min_distance)

	from math import atan2, degrees


	def _calculate_direction(self, target):
		"""Calculate the direction vector from the model to the target."""
		model_pos = self.model.getPos()
		target_pos = target.model.getPos()
		
		# Calculate direction from model to target
		direction = target_pos - model_pos
		
		# Normalize the direction to get a unit vector
		return direction.normalized()

	def _calculate_hpr(self, direction):
		"""Convert direction vector to HPR (heading, pitch, roll) angles."""
		# Assuming direction is a normalized LVector3f
		x, y, z = direction

		# Calculate heading (yaw) and pitch (tilt)
		heading = atan2(y, x)  # atan2 gives angle in radians
		pitch = atan2(z, (x**2 + y**2)**0.5)  # pitch based on the vertical component

		# Convert to degrees
		return degrees(heading), degrees(pitch), 0  # Roll is typically set to 0 unless needed

	def update_model_orientation(self, nearest):
		"""Update the model's orientation towards the nearest sphere."""
		# Calculate the direction to the nearest sphere
		direction = self._calculate_direction(nearest)
		
		# Get the heading, pitch, and roll for the calculated direction
		hpr = self._calculate_hpr(direction)
		
		# Apply a counterclockwise 90-degree adjustment on the X-axis and Z-axis
		adjusted_heading = hpr[0]  # Heading (Z-axis)
		adjusted_pitch = hpr[1] - 90  # Pitch (X-axis), counterclockwise adjustment
		adjusted_roll = 0  # Roll (Y-axis), leave this as 0 unless you need it

		# Set the new HPR values with the adjustment
		self.model.setHpr(adjusted_heading, adjusted_pitch, adjusted_roll)




	def _calculate_gravitational_force(self, other_sphere):
		"""Calculates the gravitational force between this sphere and another."""
		distance = self._calculate_distance(other_sphere)
		if distance == 0:  # Avoid division by zero
			return Vec3(0, 0, 0)		

		force_magnitude = GRAVITATIONAL_CONSTANT * (self.mass * other_sphere.mass) / (distance ** 2)
		direction = Vec3(other_sphere.model.getPos() - self.model.getPos()).normalized()

		
		if self.accorgrav == 1 and other_sphere.accorgrav == 1:
				return direction * force_magnitude
		elif self.accorgrav == 0 and other_sphere.accorgrav == 1:			
				return direction * force_magnitude * 40			
		elif self.accorgrav == 1 and other_sphere.accorgrav == 0:			
				return direction * force_magnitude * 4			
		else: 
			return direction * force_magnitude/10
	

	def update(self, dt, all_spheres, local_distance=70000):
		"""Update the sphere's position, applying gravitational forces from nearby spheres and handling wall collisions."""
		total_gravitational_force_x = 0
		total_gravitational_force_y = 0
		total_gravitational_force_z = 0

		# Wall boundaries
		min_x, max_x = -59000, 59000  # X-axis boundaries
		min_y, max_y = -30000, 50000  # Y-axis boundaries
		min_z, max_z = 0, 60000	   # Z-axis boundaries (ground and top)
		nearest = self.find_nearest_sphere(all_spheres)

		if True:
			# Calculate the gravitational forces only from nearby spheres within the local_distance
			for other_sphere in all_spheres:			
				if other_sphere is not self and self is not None:
					gravitational_force = self._calculate_gravitational_force(other_sphere)
					if self.accorgrav == 1 and other_sphere.accorgrav == 1:
						distance = self._calculate_distance(other_sphere)						
						
						# Only consider spheres that are within the specified local distance
						if distance <= local_distance or True:							
							total_gravitational_force_x += gravitational_force.x
							total_gravitational_force_y += gravitational_force.y
							total_gravitational_force_z += gravitational_force.z
						
						if distance < (self._radius + other_sphere._radius) *1.5:
							#other_sphere._radius = 5000 #this may not be the desired effect now and was a test
							total_gravitational_force_x = -gravitational_force.x * 50
							total_gravitational_force_y = -gravitational_force.y * 50
							total_gravitational_force_z = -gravitational_force.z * 50
					elif self.accorgrav == 0 and other_sphere.accorgrav == 1:
						distance = self._calculate_distance(other_sphere)
						if other_sphere != nearest:
							total_gravitational_force_x += gravitational_force.x /2
							total_gravitational_force_y += gravitational_force.y /2
							total_gravitational_force_z += gravitational_force.z /2
							total_gravitational_force = Vec3(total_gravitational_force_x, total_gravitational_force_y, total_gravitational_force_z)
						else:
							if distance < (self._radius + other_sphere._radius):
								index = all_spheres.index(other_sphere)					
								# Load a sound effect (for small sounds like effects)
								sound_effect = self.pop_sound  # Can also use .wav, .ogg, etc.
								#nearest.animate()
								# Play the sound effect
								sound_effect.play()

								all_spheres.pop(index)
								other_sphere.model.detachNode()
								# -- Animate here 

								return index, other_sphere
							
							#Note: <update_model_orientation>
							# Assuming nearest sphere is passed or found somewhere
						 # Assuming nearest sphere is passed or found somewhere
							nearest = self.find_nearest_sphere(all_spheres)

						self.update_model_orientation(nearest)

						direction = self._calculate_direction(nearest)

						normalized_direction = direction.normalized()

						# Calculate distance to the nearest sphere
						distance_to_target = direction.length()

						# Reduce acceleration based on distance to target
						# The closer the model is to the target, the smaller the acceleration
						acceleration_magnitude = max(0.05, 0.5 * distance_to_target)  # Min acceleration = 0.05
						acceleration_vector = normalized_direction * acceleration_magnitude

						dt = globalClock.getDt()

						# Update velocity
						self.velocity += acceleration_vector * dt

						# Clamp velocity to prevent excessive speeds
						max_velocity = 50  # Lower max velocity
						if self.velocity.length() > max_velocity:
							self.velocity.normalize()
							self.velocity *= max_velocity

						# Calculate the new position
						new_position = self.model.getPos() + (self.velocity * dt)

						# Print debugging info
						#print("Current position:", self.model.getPos())
						#print("Velocity:", self.velocity)
						#print("Delta time (dt):", dt)
						#print("New position:", new_position)

						# Set the new position
						self.model.setPos(new_position)
						total_gravitational_force = Vec3(0,0,0)
		
					elif self.accorgrav == 0 and other_sphere.accorgrav == 0:
						distance = self._calculate_distance(other_sphere)					
						gravitational_force = self._calculate_gravitational_force(other_sphere)
						total_gravitational_force_x =0
						total_gravitational_force_y =0
						total_gravitational_force_z =0
						total_gravitational_force = Vec3(total_gravitational_force_x, total_gravitational_force_y, total_gravitational_force_z)
					else:
						distance = self._calculate_distance(other_sphere)					
						gravitational_force = self._calculate_gravitational_force(other_sphere)
						total_gravitational_force_x += gravitational_force.x * 1
						total_gravitational_force_y += gravitational_force.y * 1
						total_gravitational_force_z += gravitational_force.z * 1
						total_gravitational_force = Vec3(total_gravitational_force_x, total_gravitational_force_y, total_gravitational_force_z)

		# Update velocity based on total gravitational force (F = ma -> a = F/m)
		if self.mass is not None:
			acceleration = total_gravitational_force / self.mass #if self.mass != 0 else Vec3(0, 0, 0)
			self.velocity += acceleration * dt	
		else:
			print("Mass nf")	
		

		
		# Get the current position of the sphere
		current_position = self.model.getPos()

		# Update position based on the updated velocity
		max_velocity = Vec3(1500, 1500, 2409)
		self.velocity.x = min(max(self.velocity.x, -max_velocity.x), max_velocity.x)
		self.velocity.y = min(max(self.velocity.y, -max_velocity.y), max_velocity.y)
		self.velocity.z = min(max(self.velocity.z, -max_velocity.z), max_velocity.z)
		if distance < (self._radius + nearest._radius)/2:
			new_position = current_position + -self.velocity * dt
		else:
			new_position = current_position + self.velocity * dt

		# Handle X-axis boundary collisions
		if new_position.x <= min_x + self._radius or new_position.x >= max_x - self._radius:
			self.velocity.setX(-self.velocity.getX())  # Reverse X velocity
			new_position.setX(current_position.x)  # Prevent the sphere from going out of bounds

		# Handle Y-axis boundary collisions
		if new_position.y <= min_y + self._radius or new_position.y >= max_y - self._radius:
			self.velocity.setY(-self.velocity.getY())  # Reverse Y velocity
			new_position.setY(current_position.y)  # Prevent the sphere from going out of bounds

		# Handle Z-axis boundary collisions (Ground and top wall)
		if new_position.z <= min_z + self._radius or new_position.z >= max_z - self._radius:
			self.velocity.setZ(-self.velocity.getZ())  # Reverse Z velocity
			new_position.setZ(current_position.z)  # Prevent the sphere from going out of bounds

		# Set the new position
		self.model.setPos(new_position)

		return None, None




	def _calculate_distance(self, other_sphere):
		"""Returns the distance between this sphere and another sphere."""
		pos_self = Vec3(self.model.getPos())
		pos_other = Vec3(other_sphere.model.getPos())
		return (pos_self - pos_other).length()

	

	def is_camera_inside(self, camera_position):
		"""Check if the camera is inside the sphere."""
		sphere_pos = self.model.getPos()
		distance = (camera_position - sphere_pos).length()
		return distance < self._radius
	
	def find_nearest_sphere(self, all_spheres):
		"""Find the nearest sphere to the current sphere from all_spheres."""
		nearest_sphere = None
		shortest_distance = float('inf')  # Initialize with infinity

		for other_sphere in all_spheres:
			if other_sphere is not self:  # Don't compare the sphere with itself
				distance = self._calculate_distance(other_sphere)
				
				if distance < shortest_distance:
					shortest_distance = distance
					nearest_sphere = other_sphere

		return nearest_sphere
	
