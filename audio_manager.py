import pygame
import os
import sys

class AudioManager:
    def __init__(self):
        """Initialize audio system with fallback handling"""
        self.audio_enabled = True
        self.sounds_loaded = False
        self.muted = False
        self.sounds = {}
        self.music_playing = False
        self.current_music = None
        
        # Sound file paths
        self.sound_files = {
            'menu_music': 'sounds/menu_music.wav',
            'game_music': 'sounds/game_music.wav',
            'victory_sound': 'sounds/victory_music.wav',  # Renamed to victory_sound
            'player_shoot': 'sounds/laser_shoot.wav',
            'alien_hit': 'sounds/alien_hit.wav',
            'alien_destroy': 'sounds/alien_destroy.wav',
            'player_hit': 'sounds/player_hit.wav',
            'level_complete': 'sounds/level_complete.wav',
            'game_over': 'sounds/game_over.wav',
            'level_advance': 'sounds/level_advance.wav'
        }
        
        # Visual feedback alternatives using ASCII characters
        self.visual_feedback = {
            'player_shoot': '*ZAP*',
            'alien_hit': '*HIT*',
            'alien_destroy': '*BOOM*',
            'player_hit': '*OUCH*',
            'level_complete': '*WIN*',
            'game_over': '*DEAD*',
            'level_advance': '*NEXT*'
        }
        
        self.initialize_audio()
        self.load_sounds()
        
    def initialize_audio(self):
        """Initialize pygame mixer with optimized settings for low latency"""
        try:
            # Initialize mixer with low latency settings
            pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=256)  # Smaller buffer for less delay
            pygame.mixer.init()
            pygame.mixer.set_num_channels(16)  # More channels for simultaneous sounds
            self.audio_enabled = True
            print("🔊 Audio system initialized with low latency settings")
        except pygame.error as e:
            print(f"⚠️ Audio initialization failed: {e}")
            print("🔇 Running in silent mode with visual feedback")
            self.audio_enabled = False
    
    def load_sounds(self):
        """Load all sound files with fallback handling"""
        if not self.audio_enabled:
            return
            
        loaded_count = 0
        total_sounds = len(self.sound_files)
        
        for sound_name, file_path in self.sound_files.items():
            try:
                if os.path.exists(file_path):
                    if sound_name.endswith('_music'):
                        # Music files are handled separately
                        continue
                    else:
                        # Load sound effects
                        sound = pygame.mixer.Sound(file_path)
                        # Set reasonable volume levels
                        if 'shoot' in sound_name:
                            sound.set_volume(0.3)  # Quieter for frequent sounds
                        elif 'hit' in sound_name:
                            sound.set_volume(0.5)
                        else:
                            sound.set_volume(0.7)
                        
                        self.sounds[sound_name] = sound
                        loaded_count += 1
                        print(f"✅ Loaded sound: {sound_name}")
                else:
                    print(f"⚠️ Sound file not found: {file_path}")
            except pygame.error as e:
                print(f"⚠️ Failed to load {sound_name}: {e}")
        
        if loaded_count > 0:
            self.sounds_loaded = True
            print(f"🔊 Audio system ready: {loaded_count}/{total_sounds-2} sounds loaded")
        else:
            print("🔇 No sounds loaded - using visual feedback only")
    
    def play_sound(self, sound_name):
        """Play sound immediately without visual feedback"""
        # Play audio if available and not muted
        if self.audio_enabled and self.sounds_loaded and not self.muted:
            if sound_name in self.sounds:
                try:
                    self.sounds[sound_name].play()
                except pygame.error as e:
                    print(f"⚠️ Failed to play {sound_name}: {e}")
    
    def play_music(self, music_type='menu', loop=True):
        """Play background music with fallback handling"""
        if not self.audio_enabled or self.muted:
            return
            
        music_file = self.sound_files.get(f'{music_type}_music')
        if not music_file or not os.path.exists(music_file):
            return
            
        try:
            if self.current_music != music_type:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.set_volume(0.4)  # Background music quieter
                pygame.mixer.music.play(-1 if loop else 0)
                self.current_music = music_type
                self.music_playing = True
                print(f"🎵 Playing {music_type} music")
        except pygame.error as e:
            print(f"⚠️ Failed to play music: {e}")
    
    def stop_music(self):
        """Stop background music"""
        if self.audio_enabled:
            try:
                pygame.mixer.music.stop()
                self.music_playing = False
                self.current_music = None
            except pygame.error:
                pass
    
    def pause_music(self):
        """Pause background music"""
        if self.audio_enabled and self.music_playing:
            try:
                pygame.mixer.music.pause()
            except pygame.error:
                pass
    
    def resume_music(self):
        """Resume background music"""
        if self.audio_enabled and self.music_playing:
            try:
                pygame.mixer.music.unpause()
            except pygame.error:
                pass
    
    def toggle_mute(self):
        """Toggle mute state"""
        self.muted = not self.muted
        if self.muted:
            self.pause_music()
            # Stop all currently playing sounds
            if self.audio_enabled:
                pygame.mixer.stop()
            print("🔇 Audio muted")
        else:
            self.resume_music()
            print("🔊 Audio unmuted")
        return self.muted
    
    def is_muted(self):
        """Check if audio is muted"""
        return self.muted or not self.audio_enabled
    
    def get_audio_status_icon(self):
        """Get audio status icon for UI"""
        if not self.audio_enabled:
            return "[MUTE]"
        elif self.muted:
            return "[MUTE]"
        else:
            return "[AUDIO]"
    
    def cleanup(self):
        """Clean up audio resources"""
        if self.audio_enabled:
            try:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except pygame.error:
                pass

class VisualFeedback:
    """Handle visual feedback for audio events"""
    def __init__(self):
        self.active_feedback = []  # List of (text, x, y, timer, max_timer)
    
    def add_feedback(self, text, x, y, duration=30):
        """Add visual feedback at position"""
        self.active_feedback.append({
            'text': text,
            'x': x,
            'y': y,
            'timer': duration,
            'max_timer': duration,
            'alpha': 255
        })
    
    def update(self):
        """Update visual feedback timers"""
        self.active_feedback = [
            feedback for feedback in self.active_feedback
            if self._update_feedback(feedback)
        ]
    
    def _update_feedback(self, feedback):
        """Update individual feedback item"""
        feedback['timer'] -= 1
        if feedback['timer'] <= 0:
            return False
        
        # Fade out effect
        progress = feedback['timer'] / feedback['max_timer']
        feedback['alpha'] = int(255 * progress)
        feedback['y'] -= 1  # Float upward
        return True
    
    def draw(self, screen, font_manager):
        """Draw all active visual feedback"""
        for feedback in self.active_feedback:
            # Create large, bold text with bright colors
            text_surface, _ = font_manager.render_text(
                feedback['text'], 'title', (255, 255, 0)  # Large yellow text
            )
            text_surface.set_alpha(feedback['alpha'])
            
            # Draw with black outline for better visibility
            outline_surface, _ = font_manager.render_text(
                feedback['text'], 'title', (0, 0, 0)  # Black outline
            )
            outline_surface.set_alpha(feedback['alpha'])
            
            # Draw outline first (multiple positions for thick outline)
            for dx, dy in [(-2, -2), (-2, 0), (-2, 2), (0, -2), (0, 2), (2, -2), (2, 0), (2, 2)]:
                screen.blit(outline_surface, (feedback['x'] + dx, feedback['y'] + dy))
            
            # Draw main text
            screen.blit(text_surface, (feedback['x'], feedback['y']))
    
    def clear(self):
        """Clear all visual feedback"""
        self.active_feedback.clear()
