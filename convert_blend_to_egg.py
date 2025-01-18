import bpy
import os

# Set the path to the .blend file and the output directory for the .egg file
blend_file_path = bpy.data.filepath
output_dir = 'models'  # Change this to your desired output directory

if not blend_file_path:
    print("Error: Save the .blend file before exporting!")
    exit()

# Extract the base name of the .blend file (without extension)
file_name = os.path.basename(blend_file_path)
base_name = os.path.splitext(file_name)[0]

# Set the path for the output .egg file
egg_file_path = os.path.join(output_dir, f"{base_name}.egg")

# Ensure the YABEE exporter is available
try:
    bpy.ops.export.panda3d_egg(filepath=egg_file_path)
    print(f"Successfully exported {egg_file_path}")
except Exception as e:
    print(f"Error: {e}")
