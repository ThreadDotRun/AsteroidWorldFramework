from panda3d.core import LVector3
from panda3d.core import Vec3

class Box:
    def __init__(self, engine, x=150000, y=150000, z=150000, x_offset=0, y_offset=0, z_offset=0, 
                 model_path="models/box", texture_path="./wall_textures/658a4fc1-ebbc-43bc-8c3e-5dd9a0dac54d.jpg", far=155000):
        near = 1
        self.set_camera_clipping(engine, near, far)
        self.x = x
        self.y = y
        self.z = z
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.z_offset = z_offset
        self.engine = engine

        # Load and set up the box model with custom model and texture paths
        self.box = engine.loader.load_model(model_path)
        self.texture_path = texture_path
        texture = engine.loader.loadTexture(self.texture_path)
        self.box.setTexture(texture, 1)
        self.box.set_scale(x, y, z)

        # Set position of the box with offsets
        self.pos = (-(x / 2)) - x_offset, -(y / 2) - y_offset, -(z / 2) - z_offset
        self.box.set_pos(*self.pos)
        self.box.set_two_sided(True)

        # Reparent the box to the render
        self.box.reparent_to(engine.render)

        # Create and store the box_center node
        self.box_center = engine.render.attach_new_node("box_center")
        self.box.reparent_to(self.box_center)

    def destroy(self):
        """Remove the box and all attached elements from the render."""
        if self.box_center:
            self.box_center.remove_node()  # This will remove both the box and the box center node
            self.box_center = None
            self.box = None
        else:
            print("Box has already been removed.")

    def set_camera_clipping(self, engine, near: float, far: float):
        """
        Set the camera's near and far clipping planes to control rendering distance.
        """
        engine.camLens.setNear(near)  # Near clipping plane
        engine.camLens.setFar(far)    # Far clipping plane

    def is_camera_inside(self, cam_pos):
        """
        Check if the camera is inside the box.
        
        :param cam_pos: The position of the camera (Vec3).
        :return: True if the camera is inside, False otherwise.
        """
        # Get the box's position in world space
        box_world_pos = self.box.getPos()

        # Calculate the box's min and max boundaries in world space
        x_min = box_world_pos.getX()
        x_max = x_min + self.x
        y_min = box_world_pos.getY()
        y_max = y_min + self.y
        z_min = box_world_pos.getZ()
        z_max = z_min + self.z

        # Calculate the camera's position relative to the box_center
        camera_in_sphere_space = self.box.get_relative_point(self.box, cam_pos)

        # Check if the camera's position is within the box's boundaries
        return (x_min <= camera_in_sphere_space.x <= x_max and 
                y_min <= camera_in_sphere_space.y <= y_max and 
                z_min <= camera_in_sphere_space.z <= z_max)


# Debug testing
from panda3d.core import Vec3
from direct.showbase.ShowBase import ShowBase

class MyApp(ShowBase):
    def __init__(self):
        super().__init__()
        
        # Provide custom paths for the model and texture
        model_path = "models/custom_box"
        texture_path = "./wall_textures/custom_texture.jpg"
        
        self.box = Box(self, x=10, y=10, z=10, x_offset=0, y_offset=0, z_offset=0,
                       model_path=model_path, texture_path=texture_path)

        # Test the `is_camera_inside` function with some camera positions
        test_positions = [Vec3(0, 0, 0), Vec3(5, 5, 5), Vec3(20, 20, 20)]
        for pos in test_positions:
            result = self.box.is_camera_inside(pos)
            print(f"Camera at {pos} inside box: {result}")

if __name__ == "__main__":
    app = MyApp()
    app.run()
