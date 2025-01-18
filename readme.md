# Space Exploration Game

A 3D space exploration game built with Panda3D where players can navigate through a vast universe filled with celestial bodies and mysterious portals.

![Demo GIF](./output.gif)

## Features

- First-person camera controls with mouse look and WASD movement
- Procedurally generated space environment with randomized celestial bodies
- Physics-based movement with gravity and jump mechanics
- Portal system allowing travel between different spaces
- Dynamic collision detection system
- Fullscreen display support
- Performance statistics overlay
- Frame capture system for recording gameplay

## Requirements

- Python 3.x
- Panda3D
- NumPy

## Installation

1. Install the required dependencies:
```bash
pip install panda3d numpy
```

2. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

3. Ensure you have the following directory structure:
```
├── models/
│   ├── namaqualand_boulder_03_4k.egg
│   ├── namaqualand_boulder_04_4k.egg
│   ├── namaqualand_boulder_05_4k.egg
│   └── spaceship.egg
├── textures/
│   └── bugger/
├── wall_textures/
└── frames/
```

## Controls

- **W** - Move forward
- **S** - Move backward
- **A** - Strafe left
- **D** - Strafe right
- **Space** - Jump
- **Shift + W** - Turbo speed
- **Mouse** - Look around
- **Shift** - Speed modifier

## Game Mechanics

### Space Navigation
- Players can freely move through a 3D space environment
- Camera movement is confined within specified boundaries
- Gravity affects player movement with realistic physics

### Portal System
- Large spherical objects in space act as portals
- Flying into a portal transports the player to a special arena area
- Exit portals allow return to the main space environment

### Environment
- Multiple types of celestial bodies with different textures and sizes
- Randomized positioning of space objects
- Dynamic lighting and visual effects

## Technical Details

### Core Components

- `MyApp` - Main game application class
- `Grid` - Manages the space environment and object placement
- `Sphere` - Handles celestial body creation and behavior
- `Box` - Creates boundary boxes and arena spaces
- `CollisionHelper` - Manages collision detection between objects

### Performance Features

- Frame capture system for recording gameplay
- Real-time statistics overlay showing FPS and other metrics
- Optimized collision detection system
- Efficient space boundary management

## Development

The game is built using Panda3D's core features:
- NodePath system for 3D object management
- Built-in physics system for movement and collisions
- Task management for game loop operations
- Event handling for user input

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your license information here]

## Credits

- Built with [Panda3D](https://www.panda3d.org/)
- Space models and textures [Add credits for assets used]
