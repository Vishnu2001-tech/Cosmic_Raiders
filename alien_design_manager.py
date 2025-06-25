import pygame
import os
import random
import math

class AlienDesignManager:
    def __init__(self):
        self.alien_designs = {}
        self.design_variations = {}
        self.load_all_designs()
    
    def load_all_designs(self):
        """Load alien designs from files or create procedural ones"""
        print("👾 Loading alien design variations...")
        
        # Create multiple design variations for each alien type
        alien_types = ['basic', 'scout', 'warrior', 'commander']
        
        for alien_type in alien_types:
            self.design_variations[alien_type] = []
            
            # Try to load from files first
            for variation in range(1, 6):  # 5 variations per type
                design_path = f"alien_designs/{alien_type}_v{variation}.png"
                if os.path.exists(design_path):
                    try:
                        sprite = pygame.image.load(design_path)
                        self.design_variations[alien_type].append(sprite)
                        print(f"📁 Loaded {alien_type} variation {variation} from file")
                    except Exception as e:
                        print(f"⚠️ Error loading {design_path}: {e}")
                        self.design_variations[alien_type].append(self.create_alien_variation(alien_type, variation))
                else:
                    # Create procedural variation
                    self.design_variations[alien_type].append(self.create_alien_variation(alien_type, variation))
        
        print(f"✅ Created {sum(len(v) for v in self.design_variations.values())} alien design variations")
    
    def create_alien_variation(self, alien_type, variation):
        """Create procedural alien design variations"""
        alien = pygame.Surface((35, 25), pygame.SRCALPHA)
        
        if alien_type == 'basic':
            # Basic aliens - different bio-mechanical designs
            base_colors = [
                (60, 120, 60),   # Green
                (80, 140, 80),   # Bright green
                (40, 100, 40),   # Dark green
                (70, 130, 70),   # Medium green
                (50, 110, 50)    # Forest green
            ]
            body_color = base_colors[variation - 1]
            eye_color = (150, 255, 150)
            
            if variation == 1:
                # Segmented body
                pygame.draw.ellipse(alien, body_color, (5, 8, 25, 15))
                for i in range(3):
                    pygame.draw.line(alien, (40, 100, 40), (8 + i*6, 8), (8 + i*6, 23), 2)
                pygame.draw.circle(alien, eye_color, (12, 12), 3)
                pygame.draw.circle(alien, eye_color, (23, 12), 3)
            
            elif variation == 2:
                # Rounded with spikes
                pygame.draw.ellipse(alien, body_color, (6, 9, 23, 13))
                # Spikes
                for i in range(4):
                    x = 8 + i * 5
                    pygame.draw.polygon(alien, body_color, [(x, 9), (x+2, 5), (x+4, 9)])
                pygame.draw.circle(alien, eye_color, (14, 14), 2)
                pygame.draw.circle(alien, eye_color, (21, 14), 2)
            
            elif variation == 3:
                # Crystalline structure
                pygame.draw.polygon(alien, body_color, [(17, 8), (28, 15), (17, 22), (6, 15)])
                pygame.draw.polygon(alien, (40, 100, 40), [(17, 10), (25, 15), (17, 20), (9, 15)])
                pygame.draw.circle(alien, eye_color, (13, 13), 2)
                pygame.draw.circle(alien, eye_color, (21, 13), 2)
            
            elif variation == 4:
                # Tentacled
                pygame.draw.ellipse(alien, body_color, (8, 10, 19, 11))
                # Tentacles
                for i in range(3):
                    x = 10 + i * 5
                    pygame.draw.line(alien, body_color, (x, 21), (x-2, 24), 3)
                pygame.draw.circle(alien, eye_color, (13, 14), 2)
                pygame.draw.circle(alien, eye_color, (22, 14), 2)
            
            else:  # variation 5
                # Armored segments
                for i in range(3):
                    y = 9 + i * 4
                    pygame.draw.rect(alien, body_color, (7 + i, y, 21 - i*2, 3))
                pygame.draw.circle(alien, eye_color, (12, 12), 2)
                pygame.draw.circle(alien, eye_color, (23, 12), 2)
        
        elif alien_type == 'scout':
            # Scout aliens - fast and agile designs
            base_colors = [
                (60, 120, 120),  # Cyan
                (80, 140, 140),  # Bright cyan
                (40, 100, 100),  # Dark cyan
                (70, 130, 130),  # Medium cyan
                (50, 110, 110)   # Teal
            ]
            body_color = base_colors[variation - 1]
            eye_color = (150, 255, 255)
            
            if variation == 1:
                # Sleek arrow
                pygame.draw.polygon(alien, body_color, [(17, 5), (30, 15), (17, 20), (5, 15)])
                pygame.draw.circle(alien, (100, 200, 200), (17, 12), 4)
                pygame.draw.circle(alien, eye_color, (12, 10), 2)
                pygame.draw.circle(alien, eye_color, (22, 10), 2)
            
            elif variation == 2:
                # Wing-like extensions
                pygame.draw.ellipse(alien, body_color, (10, 10, 15, 10))
                pygame.draw.polygon(alien, body_color, [(5, 12), (10, 8), (10, 17)])
                pygame.draw.polygon(alien, body_color, [(25, 8), (30, 12), (25, 17)])
                pygame.draw.circle(alien, eye_color, (14, 13), 2)
                pygame.draw.circle(alien, eye_color, (21, 13), 2)
            
            elif variation == 3:
                # Streamlined with fins
                pygame.draw.ellipse(alien, body_color, (8, 11, 19, 8))
                # Fins
                pygame.draw.polygon(alien, body_color, [(8, 11), (3, 8), (8, 15)])
                pygame.draw.polygon(alien, body_color, [(27, 11), (32, 8), (27, 15)])
                pygame.draw.circle(alien, eye_color, (13, 14), 2)
                pygame.draw.circle(alien, eye_color, (22, 14), 2)
            
            elif variation == 4:
                # Multi-segmented
                for i in range(3):
                    x = 9 + i * 6
                    pygame.draw.ellipse(alien, body_color, (x, 11, 6, 8))
                pygame.draw.circle(alien, eye_color, (12, 13), 2)
                pygame.draw.circle(alien, eye_color, (23, 13), 2)
            
            else:  # variation 5
                # Energy trail design
                pygame.draw.ellipse(alien, body_color, (12, 10, 11, 10))
                # Energy trail
                for i in range(3):
                    alpha = 150 - i * 40
                    trail_surf = pygame.Surface((8 - i*2, 6), pygame.SRCALPHA)
                    trail_surf.fill((*body_color, alpha))
                    alien.blit(trail_surf, (4 + i*2, 12))
                pygame.draw.circle(alien, eye_color, (15, 13), 2)
                pygame.draw.circle(alien, eye_color, (20, 13), 2)
        
        elif alien_type == 'warrior':
            # Warrior aliens - heavily armored designs
            base_colors = [
                (120, 60, 60),   # Red
                (140, 80, 80),   # Bright red
                (100, 40, 40),   # Dark red
                (130, 70, 70),   # Medium red
                (110, 50, 50)    # Crimson
            ]
            body_color = base_colors[variation - 1]
            armor_color = tuple(max(0, c - 20) for c in body_color)
            eye_color = (255, 150, 150)
            
            if variation == 1:
                # Heavy armor plating
                pygame.draw.rect(alien, body_color, (8, 6, 20, 16))
                pygame.draw.rect(alien, armor_color, (6, 4, 24, 4))
                pygame.draw.rect(alien, armor_color, (6, 18, 24, 4))
                pygame.draw.circle(alien, eye_color, (14, 12), 3)
                pygame.draw.circle(alien, eye_color, (21, 12), 3)
            
            elif variation == 2:
                # Spiked armor
                pygame.draw.rect(alien, body_color, (9, 8, 17, 12))
                # Spikes
                for i in range(4):
                    x = 10 + i * 4
                    pygame.draw.polygon(alien, armor_color, [(x, 8), (x+1, 4), (x+2, 8)])
                pygame.draw.circle(alien, eye_color, (13, 12), 2)
                pygame.draw.circle(alien, eye_color, (22, 12), 2)
            
            elif variation == 3:
                # Shield-like
                pygame.draw.ellipse(alien, body_color, (7, 7, 21, 16))
                pygame.draw.ellipse(alien, armor_color, (9, 9, 17, 12))
                pygame.draw.circle(alien, eye_color, (14, 13), 2)
                pygame.draw.circle(alien, eye_color, (21, 13), 2)
            
            elif variation == 4:
                # Segmented armor
                for i in range(4):
                    y = 6 + i * 3
                    pygame.draw.rect(alien, body_color if i % 2 else armor_color, (8, y, 19, 3))
                pygame.draw.circle(alien, eye_color, (13, 11), 2)
                pygame.draw.circle(alien, eye_color, (22, 11), 2)
            
            else:  # variation 5
                # Battle-scarred
                pygame.draw.rect(alien, body_color, (8, 7, 19, 14))
                # Battle scars (darker lines)
                pygame.draw.line(alien, armor_color, (10, 9), (15, 14), 2)
                pygame.draw.line(alien, armor_color, (20, 10), (25, 15), 2)
                pygame.draw.circle(alien, eye_color, (14, 12), 2)
                pygame.draw.circle(alien, eye_color, (21, 12), 2)
        
        elif alien_type == 'commander':
            # Commander aliens - elite designs
            base_colors = [
                (120, 60, 120),  # Purple
                (140, 80, 140),  # Bright purple
                (100, 40, 100),  # Dark purple
                (130, 70, 130),  # Medium purple
                (110, 50, 110)   # Magenta
            ]
            body_color = base_colors[variation - 1]
            crown_color = tuple(min(255, c + 30) for c in body_color)
            eye_color = (255, 150, 255)
            core_color = (200, 100, 200)
            
            if variation == 1:
                # Royal crown
                pygame.draw.ellipse(alien, body_color, (3, 8, 30, 15))
                pygame.draw.polygon(alien, crown_color, [(17, 3), (12, 8), (22, 8)])
                # Crown jewels
                pygame.draw.circle(alien, eye_color, (17, 6), 2)
                pygame.draw.circle(alien, core_color, (17, 15), 5)
                pygame.draw.circle(alien, eye_color, (17, 15), 3)
                pygame.draw.circle(alien, eye_color, (10, 10), 2)
                pygame.draw.circle(alien, eye_color, (24, 10), 2)
            
            elif variation == 2:
                # Multi-crowned
                pygame.draw.ellipse(alien, body_color, (4, 9, 27, 13))
                # Multiple crown spikes
                for i in range(5):
                    x = 8 + i * 4
                    height = 3 + (i % 2) * 2
                    pygame.draw.polygon(alien, crown_color, [(x, 9), (x+1, 9-height), (x+2, 9)])
                pygame.draw.circle(alien, core_color, (17, 14), 4)
                pygame.draw.circle(alien, eye_color, (11, 12), 2)
                pygame.draw.circle(alien, eye_color, (23, 12), 2)
            
            elif variation == 3:
                # Energy aura
                pygame.draw.ellipse(alien, body_color, (5, 9, 25, 12))
                # Aura effect
                for i in range(3):
                    alpha = 100 - i * 30
                    aura_surf = pygame.Surface((29 + i*4, 16 + i*4), pygame.SRCALPHA)
                    aura_surf.fill((*crown_color, alpha))
                    alien.blit(aura_surf, (3 - i*2, 7 - i*2))
                pygame.draw.circle(alien, core_color, (17, 14), 4)
                pygame.draw.circle(alien, eye_color, (12, 12), 2)
                pygame.draw.circle(alien, eye_color, (22, 12), 2)
            
            elif variation == 4:
                # Crystalline commander
                pygame.draw.polygon(alien, body_color, [(17, 6), (28, 12), (22, 20), (12, 20), (6, 12)])
                pygame.draw.polygon(alien, crown_color, [(17, 8), (25, 13), (20, 18), (14, 18), (9, 13)])
                pygame.draw.circle(alien, core_color, (17, 14), 3)
                pygame.draw.circle(alien, eye_color, (13, 11), 2)
                pygame.draw.circle(alien, eye_color, (21, 11), 2)
            
            else:  # variation 5
                # Ancient commander
                pygame.draw.ellipse(alien, body_color, (2, 8, 31, 14))
                # Ancient symbols
                pygame.draw.line(alien, crown_color, (8, 10), (12, 14), 2)
                pygame.draw.line(alien, crown_color, (12, 10), (8, 14), 2)
                pygame.draw.line(alien, crown_color, (23, 10), (27, 14), 2)
                pygame.draw.line(alien, crown_color, (27, 10), (23, 14), 2)
                pygame.draw.circle(alien, core_color, (17, 14), 5)
                pygame.draw.circle(alien, eye_color, (10, 11), 2)
                pygame.draw.circle(alien, eye_color, (24, 11), 2)
        
        return alien
    
    def get_alien_design(self, alien_type, level=1):
        """Get alien design based on type and level"""
        if alien_type not in self.design_variations:
            return None
        
        variations = self.design_variations[alien_type]
        if not variations:
            return None
        
        # Use different variations based on level
        variation_index = (level - 1) % len(variations)
        return variations[variation_index]
    
    def get_random_design(self, alien_type):
        """Get random design variation for alien type"""
        if alien_type not in self.design_variations:
            return None
        
        variations = self.design_variations[alien_type]
        if not variations:
            return None
        
        return random.choice(variations)
