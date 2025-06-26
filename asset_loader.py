"""
Centralized Asset Loader for Cosmic Raiders
Handles loading of sprites, sounds, fonts with fallbacks and error logging
"""

import pygame
import os
import json
from datetime import datetime

class AssetLoader:
    def __init__(self):
        self.sprites = {}
        self.sounds = {}
        self.fonts = {}
        self.music_files = {}
        self.error_log = []
        
        # Asset paths
        self.sprite_path = "sprites/"
        self.sound_path = "sounds/"
        self.font_path = "fonts/"
        self.log_path = "logs/"
        
        # Ensure directories exist
        self._ensure_directories()
        
        # Initialize pygame components
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=256)
        pygame.mixer.init()
        pygame.mixer.set_num_channels(16)
        
    def _ensure_directories(self):
        """Create asset directories if they don't exist"""
        for path in [self.sprite_path, self.sound_path, self.font_path, self.log_path]:
            os.makedirs(path, exist_ok=True)
    
    def _log_error(self, error_type, asset_name, error_msg):
        """Log asset loading errors"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_entry = f"[{timestamp}] {error_type}: {asset_name} - {error_msg}"
        self.error_log.append(error_entry)
        print(f"⚠️ {error_entry}")
    
    def _save_error_log(self):
        """Save error log to file"""
        if self.error_log:
            try:
                log_file = os.path.join(self.log_path, "errors.log")
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"\n=== Game Session {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
                    for error in self.error_log:
                        f.write(error + "\n")
                print(f"📝 Error log saved to {log_file}")
            except Exception as e:
                print(f"⚠️ Failed to save error log: {e}")
    
    def create_fallback_sprite(self, width, height, color=(255, 255, 255)):
        """Create a fallback sprite as a colored rectangle"""
        surface = pygame.Surface((width, height))
        surface.fill(color)
        return surface
    
    def create_fallback_sound(self, frequency=440, duration=0.1):
        """Create a fallback beep sound"""
        try:
            sample_rate = 22050
            frames = int(duration * sample_rate)
            import numpy as np
            
            # Generate simple beep
            t = np.linspace(0, duration, frames)
            wave = np.sin(2 * np.pi * frequency * t) * 0.3
            
            # Convert to pygame sound
            sound_array = (wave * 32767).astype(np.int16)
            sound = pygame.sndarray.make_sound(sound_array.reshape(-1, 1))
            return sound
        except:
            # If numpy isn't available, return None
            return None
    
    def load_sprite(self, name, filename, fallback_size=(32, 32), fallback_color=(255, 255, 255)):
        """Load a sprite with fallback"""
        if name in self.sprites:
            return self.sprites[name]
        
        filepath = os.path.join(self.sprite_path, filename)
        
        try:
            if os.path.exists(filepath):
                sprite = pygame.image.load(filepath).convert_alpha()
                self.sprites[name] = sprite
                print(f"✅ Loaded sprite: {name}")
                return sprite
            else:
                raise FileNotFoundError(f"Sprite file not found: {filepath}")
                
        except Exception as e:
            self._log_error("SPRITE_ERROR", name, str(e))
            # Create fallback sprite
            fallback = self.create_fallback_sprite(fallback_size[0], fallback_size[1], fallback_color)
            self.sprites[name] = fallback
            return fallback
    
    def load_sound(self, name, filename, volume=0.7):
        """Load a sound effect with fallback"""
        if name in self.sounds:
            return self.sounds[name]
        
        filepath = os.path.join(self.sound_path, filename)
        
        try:
            if os.path.exists(filepath):
                sound = pygame.mixer.Sound(filepath)
                sound.set_volume(volume)
                self.sounds[name] = sound
                print(f"✅ Loaded sound: {name}")
                return sound
            else:
                raise FileNotFoundError(f"Sound file not found: {filepath}")
                
        except Exception as e:
            self._log_error("SOUND_ERROR", name, str(e))
            # Create fallback sound
            fallback = self.create_fallback_sound()
            if fallback:
                fallback.set_volume(volume)
                self.sounds[name] = fallback
            else:
                self.sounds[name] = None
            return self.sounds[name]
    
    def load_music(self, name, filename):
        """Load background music file"""
        filepath = os.path.join(self.sound_path, filename)
        
        try:
            if os.path.exists(filepath):
                self.music_files[name] = filepath
                print(f"✅ Loaded music: {name}")
                return filepath
            else:
                raise FileNotFoundError(f"Music file not found: {filepath}")
                
        except Exception as e:
            self._log_error("MUSIC_ERROR", name, str(e))
            self.music_files[name] = None
            return None
    
    def load_font(self, name, filename, size):
        """Load a custom font with system font fallback"""
        font_key = f"{name}_{size}"
        
        if font_key in self.fonts:
            return self.fonts[font_key]
        
        filepath = os.path.join(self.font_path, filename)
        
        try:
            if os.path.exists(filepath):
                font = pygame.font.Font(filepath, size)
                self.fonts[font_key] = font
                print(f"✅ Loaded font: {name} (size {size})")
                return font
            else:
                raise FileNotFoundError(f"Font file not found: {filepath}")
                
        except Exception as e:
            self._log_error("FONT_ERROR", name, str(e))
            # Fallback to system font
            try:
                fallback_font = pygame.font.Font(None, size)
                self.fonts[font_key] = fallback_font
                return fallback_font
            except:
                # Ultimate fallback
                self.fonts[font_key] = None
                return None
    
    def get_sprite(self, name):
        """Get a loaded sprite"""
        return self.sprites.get(name)
    
    def get_sound(self, name):
        """Get a loaded sound"""
        return self.sounds.get(name)
    
    def get_music_path(self, name):
        """Get a music file path"""
        return self.music_files.get(name)
    
    def get_font(self, name, size):
        """Get a loaded font"""
        font_key = f"{name}_{size}"
        return self.fonts.get(font_key)
    
    def cleanup(self):
        """Clean up resources and save error log"""
        self._save_error_log()
        
        # Clear cached assets
        self.sprites.clear()
        self.sounds.clear()
        self.fonts.clear()
        self.music_files.clear()
        
        print("🧹 Asset loader cleaned up")

# Global asset loader instance
asset_loader = AssetLoader()
