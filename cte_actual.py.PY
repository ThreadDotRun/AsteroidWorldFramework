import subprocess

# Path to Blender executable
BLENDER_PATH = './blender/blender.exe'  # Path to blender.exe

# Path to the script that will be executed inside Blender
SCRIPT_PATH = './convert_blend_to_egg.py'  # Python script using bpy to convert .blend to .egg

# Use subprocess to run Blender and execute the Blender script
try:
    subprocess.run([BLENDER_PATH, "--background", "--python", SCRIPT_PATH], check=True)
    print("Blender script executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Blender script failed with error: {e}")
except FileNotFoundError:
    print(f"Error: Blender executable not found at {BLENDER_PATH}")
