"""
Optimized Audio Manager for Cosmic Raiders
Handles audio with robust error handling and fallbacks
"""

import pygame
import os
from asset_loader import asset_loader

class OptimizedAudioManager:
    def __init__(self):
        self.audio_enabled = False
        self.sounds_loaded = False
        self.muted = False
        self.current_music = None
        self.music_paused = False
        
        # Sound volume levels
        self.volumes = {
            'player_shoot': 0.3,
            'alien_hit': 0.5,
            'alien_destroy': 0.6,
            'player_hit': 0.7,
            'level_complete': 0.8,
            'game_over': 0.8,
            'level_advance': 0.7,
            'victory_sound': 0.9
        }
        
        self.initialize_audio()
        self.load_all_sounds()
    
    def initialize_audio(self):
        """Initialize pygame mixer with error handling"""
        try:
            # Audio is already initialized by asset_loader
            self.audio_enabled = True
            print("🔊 Audio system ready")
        except Exception as e:
            print(f"⚠️ Audio initialization failed: {e}")
            self.audio_enabled = False
    
    def load_all_sounds(self):
        """Load all sound effects using asset loader"""
        if not self.audio_enabled:
            return
        
        sound_files = {
            'player_shoot': 'laser_shoot.wav',
            'alien_hit': 'alien_hit.wav',
            'alien_destroy': 'alien_destroy.wav',
            'player_hit': 'player_hit.wav',
            'level_complete': 'level_complete.wav',
            'game_over': 'game_over.wav',
            'level_advance': 'level_advance.wav',
            'victory_sound': 'victory_music.wav'
        }
        
        loaded_count = 0
        for sound_name, filename in sound_files.items():
            sound = asset_loader.load_sound(sound_name, filename, self.volumes.get(sound_name, 0.7))
            if sound:
                loaded_count += 1
        
        # Load music files
        music_files = {
            'menu': 'menu_music.wav',
            'game': 'game_music.wav'
        }
        
        for music_name, filename in music_files.items():
            asset_loader.load_music(music_name, filename)
        
        self.sounds_loaded = loaded_count > 0
        print(f"🔊 Audio system ready: {loaded_count}/{len(sound_files)} sounds loaded")
    
    def play_sound(self, sound_name):
        """Play sound effect with error handling"""
        if not self.audio_enabled or self.muted:
            return
        
        sound = asset_loader.get_sound(sound_name)
        if sound:
            try:
                sound.play()
            except pygame.error:
                pass  # Ignore playback errors
    
    def play_music(self, music_name):
        """Play background music with error handling"""
        if not self.audio_enabled or self.muted:
            return
        
        music_path = asset_loader.get_music_path(music_name)
        if music_path and music_path != self.current_music:
            try:
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                pygame.mixer.music.set_volume(0.3)
                self.current_music = music_path
                print(f"🎵 Playing {music_name} music")
            except pygame.error:
                pass  # Ignore music errors
    
    def stop_music(self):
        """Stop background music"""
        if self.audio_enabled:
            try:
                pygame.mixer.music.stop()
                self.current_music = None
            except pygame.error:
                pass
    
    def pause_music(self):
        """Pause background music"""
        if self.audio_enabled and not self.music_paused:
            try:
                pygame.mixer.music.pause()
                self.music_paused = True
            except pygame.error:
                pass
    
    def resume_music(self):
        """Resume background music"""
        if self.audio_enabled and self.music_paused:
            try:
                pygame.mixer.music.unpause()
                self.music_paused = False
            except pygame.error:
                pass
    
    def toggle_mute(self):
        """Toggle mute state"""
        self.muted = not self.muted
        if self.muted:
            self.pause_music()
            print("🔇 Audio muted")
        else:
            self.resume_music()
            print("🔊 Audio unmuted")
    
    def cleanup(self):
        """Clean up audio resources"""
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            print("🧹 Audio system cleaned up")
        except:
            pass
