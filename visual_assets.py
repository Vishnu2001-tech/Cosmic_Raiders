import pygame
import os
import math
import random

class VisualAssets:
    def __init__(self):
        self.sprites = {}
        self.load_all_assets()
    
    def load_all_assets(self):
        """Load all visual assets with fallbacks"""
        print("🎨 Loading visual assets...")
        
        # Try to load sprite files, create fallbacks if missing
        self.load_or_create_background()
        self.load_or_create_player_ship()
        self.load_or_create_alien_sprites()
        self.load_or_create_bullet_sprites()
        self.load_or_create_explosion_sprites()
        
        print("✅ Visual assets loaded successfully!")
    
    def load_or_create_background(self):
        """Load or create space background"""
        try:
            bg_path = "sprites/space_background.png"
            if os.path.exists(bg_path):
                self.sprites['background'] = pygame.image.load(bg_path)
                print("🌌 Loaded space background from file")
            else:
                self.sprites['background'] = self.create_space_background()
                print("🌌 Created procedural space background")
        except Exception as e:
            print(f"⚠️ Background error: {e}, using fallback")
            self.sprites['background'] = self.create_space_background()
    
    def create_space_background(self):
        """Create a procedural space background with stars and nebulae"""
        bg = pygame.Surface((800, 600))
        
        # Deep space gradient
        for y in range(600):
            color_intensity = int(20 + (y / 600) * 15)
            color = (color_intensity // 3, color_intensity // 4, color_intensity)
            pygame.draw.line(bg, color, (0, y), (800, y))
        
        # Add stars
        for _ in range(200):
            x = random.randint(0, 799)
            y = random.randint(0, 599)
            brightness = random.randint(100, 255)
            size = random.choice([1, 1, 1, 2, 2, 3])  # Mostly small stars
            color = (brightness, brightness, brightness)
            pygame.draw.circle(bg, color, (x, y), size)
        
        # Add distant galaxies/nebulae
        for _ in range(5):
            x = random.randint(100, 700)
            y = random.randint(100, 500)
            radius = random.randint(30, 80)
            color = random.choice([
                (80, 40, 120),   # Purple nebula
                (40, 80, 120),   # Blue nebula
                (120, 60, 40),   # Orange nebula
                (60, 120, 80)    # Green nebula
            ])
            # Create soft nebula effect
            for r in range(radius, 0, -5):
                alpha = max(10, 50 - (radius - r))
                nebula_surf = pygame.Surface((r*2, r*2))
                nebula_surf.set_alpha(alpha)
                nebula_surf.fill(color)
                bg.blit(nebula_surf, (x - r, y - r))
        
        return bg
    
    def load_or_create_player_ship(self):
        """Load or create detailed player spacecraft"""
        try:
            ship_path = "sprites/player_ship.png"
            if os.path.exists(ship_path):
                self.sprites['player'] = pygame.image.load(ship_path)
                print("🚀 Loaded player ship from file")
            else:
                self.sprites['player'] = self.create_player_ship()
                print("🚀 Created detailed player ship")
        except Exception as e:
            print(f"⚠️ Player ship error: {e}, using fallback")
            self.sprites['player'] = self.create_player_ship()
    
    def create_player_ship(self):
        """Create a detailed spacecraft with cockpit and thrusters"""
        ship = pygame.Surface((50, 40), pygame.SRCALPHA)
        
        # Main hull (metallic blue-gray)
        hull_color = (120, 140, 160)
        pygame.draw.polygon(ship, hull_color, [
            (25, 0), (35, 10), (45, 35), (35, 40), (15, 40), (5, 35), (15, 10)
        ])
        
        # Cockpit (glowing blue)
        cockpit_color = (100, 150, 255)
        pygame.draw.ellipse(ship, cockpit_color, (20, 8, 10, 12))
        
        # Wing details
        wing_color = (90, 110, 130)
        pygame.draw.polygon(ship, wing_color, [(5, 35), (0, 30), (0, 40), (15, 40)])
        pygame.draw.polygon(ship, wing_color, [(35, 40), (50, 40), (50, 30), (45, 35)])
        
        # Engine thrusters (glowing)
        thruster_color = (255, 100, 50)
        pygame.draw.circle(ship, thruster_color, (12, 38), 3)
        pygame.draw.circle(ship, thruster_color, (38, 38), 3)
        
        # Engine glow effect
        glow_color = (255, 150, 100)
        pygame.draw.circle(ship, glow_color, (12, 38), 2)
        pygame.draw.circle(ship, glow_color, (38, 38), 2)
        
        # Hull highlights
        highlight_color = (180, 200, 220)
        pygame.draw.lines(ship, highlight_color, False, [(15, 10), (25, 0), (35, 10)], 2)
        
        return ship
    
    def load_or_create_alien_sprites(self):
        """Load or create biomechanical alien sprites"""
        alien_types = ['basic', 'scout', 'warrior', 'commander']
        
        for alien_type in alien_types:
            try:
                alien_path = f"sprites/alien_{alien_type}.png"
                if os.path.exists(alien_path):
                    self.sprites[f'alien_{alien_type}'] = pygame.image.load(alien_path)
                    print(f"👾 Loaded {alien_type} alien from file")
                else:
                    self.sprites[f'alien_{alien_type}'] = self.create_alien_sprite(alien_type)
                    print(f"👾 Created {alien_type} alien sprite")
            except Exception as e:
                print(f"⚠️ {alien_type} alien error: {e}, using fallback")
                self.sprites[f'alien_{alien_type}'] = self.create_alien_sprite(alien_type)
    
    def create_alien_sprite(self, alien_type):
        """Create biomechanical alien sprites with glowing effects"""
        alien = pygame.Surface((35, 25), pygame.SRCALPHA)
        
        if alien_type == 'basic':
            # Green biomechanical basic alien
            body_color = (60, 120, 60)
            eye_color = (150, 255, 150)
            
            # Body
            pygame.draw.ellipse(alien, body_color, (5, 8, 25, 15))
            # Segments
            for i in range(3):
                pygame.draw.line(alien, (40, 100, 40), (8 + i*6, 8), (8 + i*6, 23), 2)
            # Glowing eyes
            pygame.draw.circle(alien, eye_color, (12, 12), 3)
            pygame.draw.circle(alien, eye_color, (23, 12), 3)
            
        elif alien_type == 'scout':
            # Cyan fast scout
            body_color = (60, 120, 120)
            eye_color = (150, 255, 255)
            
            # Sleek body
            pygame.draw.polygon(alien, body_color, [(17, 5), (30, 15), (17, 20), (5, 15)])
            # Energy core
            pygame.draw.circle(alien, (100, 200, 200), (17, 12), 4)
            # Eyes
            pygame.draw.circle(alien, eye_color, (12, 10), 2)
            pygame.draw.circle(alien, eye_color, (22, 10), 2)
            
        elif alien_type == 'warrior':
            # Red armored warrior
            body_color = (120, 60, 60)
            armor_color = (100, 40, 40)
            eye_color = (255, 150, 150)
            
            # Armored body
            pygame.draw.rect(alien, body_color, (8, 6, 20, 16))
            pygame.draw.rect(alien, armor_color, (6, 4, 24, 4))  # Armor plating
            pygame.draw.rect(alien, armor_color, (6, 18, 24, 4))
            # Menacing eyes
            pygame.draw.circle(alien, eye_color, (14, 12), 3)
            pygame.draw.circle(alien, eye_color, (21, 12), 3)
            
        elif alien_type == 'commander':
            # Purple/magenta elite commander
            body_color = (120, 60, 120)
            crown_color = (150, 80, 150)
            eye_color = (255, 150, 255)
            core_color = (200, 100, 200)
            
            # Elite body
            pygame.draw.ellipse(alien, body_color, (3, 8, 30, 15))
            # Crown/crest
            pygame.draw.polygon(alien, crown_color, [(17, 3), (12, 8), (22, 8)])
            # Pulsing energy core
            pygame.draw.circle(alien, core_color, (17, 15), 5)
            pygame.draw.circle(alien, eye_color, (17, 15), 3)
            # Elite eyes
            pygame.draw.circle(alien, eye_color, (10, 10), 2)
            pygame.draw.circle(alien, eye_color, (24, 10), 2)
        
        return alien
    
    def load_or_create_bullet_sprites(self):
        """Load or create laser/plasma bullet effects"""
        try:
            # Player laser
            laser_path = "sprites/player_laser.png"
            if os.path.exists(laser_path):
                self.sprites['player_bullet'] = pygame.image.load(laser_path)
            else:
                self.sprites['player_bullet'] = self.create_laser_bullet(True)
            
            # Alien plasma
            plasma_path = "sprites/alien_plasma.png"
            if os.path.exists(plasma_path):
                self.sprites['alien_bullet'] = pygame.image.load(plasma_path)
            else:
                self.sprites['alien_bullet'] = self.create_laser_bullet(False)
                
            print("⚡ Created laser/plasma projectiles")
        except Exception as e:
            print(f"⚠️ Bullet sprites error: {e}, using fallbacks")
            self.sprites['player_bullet'] = self.create_laser_bullet(True)
            self.sprites['alien_bullet'] = self.create_laser_bullet(False)
    
    def create_laser_bullet(self, is_player):
        """Create laser beam or plasma projectile"""
        bullet = pygame.Surface((4, 12), pygame.SRCALPHA)
        
        if is_player:
            # Blue laser beam
            core_color = (150, 200, 255)
            glow_color = (100, 150, 255)
        else:
            # Red plasma bolt
            core_color = (255, 150, 100)
            glow_color = (255, 100, 50)
        
        # Laser core
        pygame.draw.rect(bullet, core_color, (1, 0, 2, 12))
        # Glow effect
        pygame.draw.rect(bullet, glow_color, (0, 1, 4, 10))
        
        return bullet
    
    def load_or_create_explosion_sprites(self):
        """Load or create explosion animation frames"""
        try:
            self.sprites['explosion_frames'] = []
            for i in range(6):  # 6 frame explosion
                exp_path = f"sprites/explosion_{i}.png"
                if os.path.exists(exp_path):
                    self.sprites['explosion_frames'].append(pygame.image.load(exp_path))
                else:
                    self.sprites['explosion_frames'].append(self.create_explosion_frame(i))
            print("💥 Created explosion animation frames")
        except Exception as e:
            print(f"⚠️ Explosion sprites error: {e}, using fallbacks")
            self.sprites['explosion_frames'] = []
            for i in range(6):
                self.sprites['explosion_frames'].append(self.create_explosion_frame(i))
    
    def create_explosion_frame(self, frame):
        """Create explosion animation frame"""
        size = 20 + frame * 8  # Growing explosion
        explosion = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Color progression: white -> yellow -> orange -> red -> dark
        colors = [
            (255, 255, 255),  # Frame 0: Bright white
            (255, 255, 150),  # Frame 1: White-yellow
            (255, 200, 100),  # Frame 2: Yellow-orange
            (255, 150, 50),   # Frame 3: Orange
            (200, 100, 50),   # Frame 4: Red-orange
            (100, 50, 50)     # Frame 5: Dark red
        ]
        
        color = colors[frame]
        center = size // 2
        
        # Multiple circles for explosion effect
        for radius in range(center, 0, -2):
            alpha = max(50, 255 - (frame * 40) - (center - radius) * 10)
            exp_surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            exp_surf.set_alpha(alpha)
            pygame.draw.circle(exp_surf, color, (radius, radius), radius)
            explosion.blit(exp_surf, (center - radius, center - radius))
        
        return explosion
    
    def get_sprite(self, name):
        """Get sprite by name"""
        return self.sprites.get(name)
    
    def get_explosion_frame(self, frame):
        """Get specific explosion frame"""
        frames = self.sprites.get('explosion_frames', [])
        if frames and 0 <= frame < len(frames):
            return frames[frame]
        return None
