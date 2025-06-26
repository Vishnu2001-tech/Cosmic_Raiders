# 🚀 Cosmic Raiders - Enhanced Space Invaders

An advanced Space Invaders game implemented in Python using Pygame with cutting-edge features, progressive difficulty, and stunning spaceship designs.

## ✨ Enhanced Features

### 🛸 **Spaceship Combat System**
- **20 Unique Spaceship Designs**: Detailed alien spacecraft across 4 ship classes
- **Progressive Ship Classes**: Scout → Fighter → Cruiser → Mothership
- **Visual Variety**: Each level features different spaceship variants
- **Dynamic Sizing**: Ships get larger and more complex at higher levels

### 📈 **Progressive Difficulty System**
- **8 Difficulty Tiers**: From Rookie to Legendary with distinct challenges
- **Adaptive Spawning**: 3→4→5→6→7→8 aliens per level
- **Speed Scaling**: 40% speed increase per level
- **Aggression Scaling**: 50% more aggressive shooting per level
- **Special Abilities**: Rapid fire, teleport dodge, formation shifts

### 🎨 **Advanced Visual Systems**
- **Procedural Space Backgrounds**: Dynamic starfields and nebulae
- **Enhanced Particle Effects**: Explosions, engine trails, weapon impacts
- **Compact UI System**: Non-intrusive HUD with smart information display
- **Retro Pixel Fonts**: Authentic arcade styling with fallback support

### 🎯 **Combat Enhancements**
- **Multi-Health System**: Warriors and commanders take multiple hits
- **Damage Feedback**: Visual flash effects and health bars
- **Formation Variety**: 8 unique formations (Line, V-Shape, Arc, Triangle, Diamond, Spiral, Cross, Wave)
- **Smart AI**: Different movement patterns per alien type

## 🎮 Controls

### Main Menu
- **Arrow Keys**: Navigate menu options
- **Enter/Space**: Select menu option
- **ESC**: Quit game

### Gameplay
- **Arrow Keys** or **A/D**: Move left and right
- **Spacebar**: Shoot bullets (up to 6 simultaneous)
- **ESC**: Return to main menu

### Game Over
- **R**: Restart game
- **ESC**: Return to main menu

## 🛠️ Installation

1. **Install Python 3.6 or higher**
2. **Install Pygame**:
   ```bash
   pip install -r requirements.txt
   ```
   or
   ```bash
   pip install pygame
   ```

3. **Optional - Custom Fonts**:
   - Download pixel-style fonts (like "Pixeled.ttf")
   - Place in `fonts/` directory
   - Game automatically detects and uses custom fonts

4. **Optional - Custom Spaceships**:
   - Add custom spaceship sprites to `spaceship_designs/`
   - Format: `{class}_{variant}.png` (e.g., `scout_interceptor.png`)
   - Game falls back to procedural designs if files not found

## 🚀 Running the Game

```bash
python3 cosmic_raiders.py
```

## 🎯 Game Mechanics

### **Scoring System**
- **Basic Aliens**: 10 points (Scout-class ships)
- **Scout Aliens**: 15 points (Fighter-class ships)
- **Warrior Aliens**: 25 points (Cruiser-class ships)
- **Commander Aliens**: 50 points (Mothership-class ships)

### **Difficulty Progression**
- **Level 1-3**: Rookie tier - Basic training
- **Level 4-6**: Veteran tier - Mixed alien types
- **Level 7-10**: Elite tier - Advanced formations
- **Level 11+**: Legendary tier - Ultimate challenge

### **Formation Types**
1. **Line Formation**: Simple horizontal line
2. **V-Shape Formation**: Classic V pattern
3. **Arc Formation**: Curved semicircle
4. **Triangle Formation**: Pyramid structure
5. **Diamond Formation**: Diamond pattern
6. **Spiral Formation**: Rotating spiral
7. **Cross Formation**: Plus-sign pattern
8. **Wave Formation**: Sine wave pattern

## 🏗️ Technical Architecture

### **Core Systems**
- **60 FPS Performance**: Optimized game loop
- **Modular Design**: Separate managers for different systems
- **State Management**: Clean state transitions
- **Asset Management**: Efficient loading and caching

### **Advanced Features**
- **Progressive Spawning**: Dynamic alien count scaling
- **Collision Optimization**: Efficient pygame.Rect usage
- **Memory Management**: Automatic cleanup of off-screen objects
- **Visual Effects**: Layered rendering with transparency

## 📁 File Structure

```
cosmic-raiders/
├── cosmic_raiders.py           # Main game engine
├── spaceship_designer.py       # 20 spaceship designs
├── progressive_spawner.py      # Difficulty scaling system
├── alien_design_manager.py     # Fallback alien designs
├── difficulty_manager.py       # Core difficulty logic
├── ui_manager.py              # Compact UI system
├── high_score_manager.py       # Persistent scoring
├── visual_assets.py           # Enhanced graphics
├── font_manager.py            # Font system
├── requirements.txt           # Dependencies
├── README.md                  # This file
├── .gitignore                 # Git ignore rules
├── fonts/                     # Custom fonts directory
├── spaceship_designs/         # Custom spaceship sprites
└── high_score.json           # High score data
```

## 🎨 Customization

### **Adding Custom Spaceships**
1. Create PNG files in `spaceship_designs/`
2. Use naming convention: `{class}_{variant}.png`
3. Recommended sizes: Scout (35x25), Fighter (40x30), Cruiser (45x30), Mothership (55x35)

### **Modifying Difficulty**
- Edit `difficulty_manager.py` for custom difficulty curves
- Adjust `progressive_spawner.py` for spawn rate changes
- Modify alien stats in the difficulty configuration

### **Custom Formations**
- Add new formation functions to `CosmicFormation` class
- Implement custom movement patterns in `Alien` class
- Create unique visual arrangements

## 🏆 High Score System

- **Persistent Storage**: Scores saved across sessions
- **New High Score Detection**: Visual feedback for achievements
- **Score Multipliers**: Bonus points at higher difficulty levels

## 🔧 Development

### **Requirements**
- Python 3.6+
- Pygame 2.0+
- Modern graphics support for transparency effects

### **Performance**
- Optimized for 60 FPS gameplay
- Efficient collision detection
- Memory-conscious asset management
- Scalable difficulty system

## 📜 License

This project is open source. Feel free to modify and distribute.

## 🎮 Credits

Enhanced Space Invaders implementation with modern game design principles, progressive difficulty, and advanced visual systems.

---

**🚀 Ready for cosmic combat? Launch the game and defend Earth from the alien invasion!**
