import pygame
import os
import math
import random

class SpaceshipDesigner:
    def __init__(self):
        self.spaceship_designs = {}
        self.design_cache = {}
        self.load_all_spaceships()
    
    def load_all_spaceships(self):
        """Load spaceship designs from files or create procedural ones"""
        print("🛸 Loading alien spaceship designs...")
        
        # Define spaceship types with multiple variants
        spaceship_types = {
            'scout': ['interceptor', 'stealth', 'recon', 'dart', 'phantom'],
            'fighter': ['assault', 'heavy', 'bomber', 'destroyer', 'gunship'],
            'cruiser': ['battleship', 'dreadnought', 'carrier', 'fortress', 'titan'],
            'mothership': ['command', 'flagship', 'overlord', 'leviathan', 'colossus']
        }
        
        for ship_class, variants in spaceship_types.items():
            self.spaceship_designs[ship_class] = {}
            
            for variant in variants:
                # Try to load from file first
                ship_path = f"spaceship_designs/{ship_class}_{variant}.png"
                if os.path.exists(ship_path):
                    try:
                        sprite = pygame.image.load(ship_path)
                        self.spaceship_designs[ship_class][variant] = sprite
                        print(f"📁 Loaded {ship_class} {variant} from file")
                    except Exception as e:
                        print(f"⚠️ Error loading {ship_path}: {e}")
                        self.spaceship_designs[ship_class][variant] = self.create_spaceship(ship_class, variant)
                else:
                    # Create procedural spaceship
                    self.spaceship_designs[ship_class][variant] = self.create_spaceship(ship_class, variant)
        
        print(f"✅ Created {sum(len(variants) for variants in self.spaceship_designs.values())} alien spaceship designs")
    
    def create_spaceship(self, ship_class, variant):
        """Create procedural alien spaceship designs"""
        if ship_class == 'scout':
            return self.create_scout_ship(variant)
        elif ship_class == 'fighter':
            return self.create_fighter_ship(variant)
        elif ship_class == 'cruiser':
            return self.create_cruiser_ship(variant)
        elif ship_class == 'mothership':
            return self.create_mothership(variant)
        else:
            return self.create_basic_ship()
    
    def create_scout_ship(self, variant):
        """Create fast, agile scout ships with more distinct designs"""
        ship = pygame.Surface((35, 25), pygame.SRCALPHA)
        
        if variant == 'interceptor':
            # Sleek arrow design with bright colors
            hull_color = (100, 200, 255)  # Bright cyan
            engine_color = (255, 255, 150)  # Bright yellow
            accent_color = (255, 100, 100)  # Red accents
            
            # Main hull - more prominent
            pygame.draw.polygon(ship, hull_color, [
                (17, 2), (30, 10), (25, 23), (10, 23), (5, 10)
            ])
            # Hull outline
            pygame.draw.polygon(ship, (200, 255, 255), [
                (17, 2), (30, 10), (25, 23), (10, 23), (5, 10)
            ], 2)
            # Cockpit - larger and brighter
            pygame.draw.circle(ship, accent_color, (17, 10), 4)
            pygame.draw.circle(ship, (255, 200, 200), (17, 10), 2)
            # Engine trails - more visible
            pygame.draw.circle(ship, engine_color, (10, 20), 3)
            pygame.draw.circle(ship, engine_color, (25, 20), 3)
            pygame.draw.circle(ship, (255, 200, 100), (10, 20), 2)
            pygame.draw.circle(ship, (255, 200, 100), (25, 20), 2)
            
        elif variant == 'stealth':
            # Angular stealth design - darker but with bright edges
            hull_color = (60, 60, 120)
            edge_color = (150, 150, 255)
            
            # Stealth hull - larger
            pygame.draw.polygon(ship, hull_color, [
                (17, 3), (32, 12), (17, 22), (3, 12)
            ])
            # Bright stealth edges
            pygame.draw.polygon(ship, edge_color, [
                (17, 3), (32, 12), (17, 22), (3, 12)
            ], 2)
            # Stealth panels with glow
            pygame.draw.polygon(ship, (100, 100, 180), [
                (17, 6), (28, 12), (17, 18), (6, 12)
            ])
            # Minimal but bright engines
            pygame.draw.circle(ship, (150, 150, 255), (12, 18), 2)
            pygame.draw.circle(ship, (150, 150, 255), (22, 18), 2)
            
        elif variant == 'recon':
            # Sensor-heavy design with glowing elements
            hull_color = (100, 255, 100)  # Bright green
            sensor_color = (255, 255, 100)  # Bright yellow
            
            # Main body - larger
            pygame.draw.ellipse(ship, hull_color, (6, 8, 23, 9))
            pygame.draw.ellipse(ship, (200, 255, 200), (6, 8, 23, 9), 2)
            # Large sensor array
            pygame.draw.circle(ship, sensor_color, (17, 12), 6)
            pygame.draw.circle(ship, (255, 255, 200), (17, 12), 4)
            pygame.draw.circle(ship, hull_color, (17, 12), 2)
            # Side sensors - more prominent
            pygame.draw.circle(ship, sensor_color, (5, 10), 3)
            pygame.draw.circle(ship, sensor_color, (29, 10), 3)
            pygame.draw.circle(ship, (255, 255, 200), (5, 10), 2)
            pygame.draw.circle(ship, (255, 255, 200), (29, 10), 2)
            
        elif variant == 'dart':
            # Ultra-thin dart design with bright colors
            hull_color = (255, 100, 100)  # Bright red
            wing_color = (255, 200, 100)  # Orange
            
            # Dart body - more prominent
            pygame.draw.polygon(ship, hull_color, [
                (17, 1), (20, 12), (17, 24), (14, 12)
            ])
            pygame.draw.polygon(ship, (255, 200, 200), [
                (17, 1), (20, 12), (17, 24), (14, 12)
            ], 2)
            # Wings - larger and brighter
            pygame.draw.polygon(ship, wing_color, [(3, 10), (14, 12), (3, 14)])
            pygame.draw.polygon(ship, wing_color, [(31, 10), (20, 12), (31, 14)])
            # Bright engine
            pygame.draw.circle(ship, (255, 255, 100), (17, 22), 3)
            pygame.draw.circle(ship, (255, 200, 100), (17, 22), 2)
            
        else:  # phantom
            # Ghostly design with bright ethereal glow
            hull_color = (200, 100, 255)  # Bright purple
            glow_color = (255, 150, 255)  # Pink glow
            
            # Ethereal hull - larger
            pygame.draw.ellipse(ship, hull_color, (4, 6, 27, 13))
            pygame.draw.ellipse(ship, glow_color, (4, 6, 27, 13), 2)
            # Phantom glow - more visible
            for i in range(3):
                alpha = 150 - i * 40
                glow_surf = pygame.Surface((29 + i*4, 15 + i*4), pygame.SRCALPHA)
                glow_surf.fill((*glow_color, alpha))
                ship.blit(glow_surf, (3 - i*2, 5 - i*2))
            # Core
            pygame.draw.circle(ship, (255, 200, 255), (17, 12), 3)
        
        return ship
    
    def create_fighter_ship(self, variant):
        """Create combat-focused fighter ships with distinct designs"""
        ship = pygame.Surface((40, 30), pygame.SRCALPHA)
        
        if variant == 'assault':
            # Aggressive fighter design with bright colors
            hull_color = (255, 80, 80)  # Bright red
            weapon_color = (255, 200, 100)  # Orange weapons
            accent_color = (255, 255, 100)  # Yellow accents
            
            # Main hull - larger and more aggressive
            pygame.draw.polygon(ship, hull_color, [
                (20, 3), (35, 15), (30, 27), (10, 27), (5, 15)
            ])
            # Hull outline
            pygame.draw.polygon(ship, (255, 150, 150), [
                (20, 3), (35, 15), (30, 27), (10, 27), (5, 15)
            ], 2)
            # Large weapon pods
            pygame.draw.rect(ship, weapon_color, (0, 12, 8, 6))
            pygame.draw.rect(ship, weapon_color, (32, 12, 8, 6))
            pygame.draw.rect(ship, (255, 150, 100), (0, 12, 8, 6), 2)
            pygame.draw.rect(ship, (255, 150, 100), (32, 12, 8, 6), 2)
            # Bright cockpit
            pygame.draw.circle(ship, accent_color, (20, 12), 5)
            pygame.draw.circle(ship, (255, 200, 100), (20, 12), 3)
            # Engine exhausts
            pygame.draw.circle(ship, (100, 255, 255), (12, 25), 3)
            pygame.draw.circle(ship, (100, 255, 255), (28, 25), 3)
            
        elif variant == 'heavy':
            # Bulky heavy fighter with armor plating
            hull_color = (150, 150, 80)  # Olive
            armor_color = (200, 200, 100)  # Bright olive
            weapon_color = (255, 150, 100)  # Orange
            
            # Heavy hull - very bulky
            pygame.draw.rect(ship, hull_color, (8, 6, 24, 18))
            pygame.draw.rect(ship, armor_color, (8, 6, 24, 18), 2)
            # Thick armor plating
            pygame.draw.rect(ship, armor_color, (6, 4, 28, 6))
            pygame.draw.rect(ship, armor_color, (6, 20, 28, 6))
            # Heavy weapons - very prominent
            pygame.draw.rect(ship, weapon_color, (0, 10, 10, 10))
            pygame.draw.rect(ship, weapon_color, (30, 10, 10, 10))
            pygame.draw.rect(ship, (255, 200, 150), (0, 10, 10, 10), 2)
            pygame.draw.rect(ship, (255, 200, 150), (30, 10, 10, 10), 2)
            # Armored cockpit
            pygame.draw.rect(ship, (200, 200, 150), (16, 10, 8, 10))
            
        elif variant == 'bomber':
            # Payload-heavy bomber with visible bomb bay
            hull_color = (100, 150, 255)  # Blue
            bay_color = (80, 120, 200)  # Dark blue
            engine_color = (150, 200, 255)  # Light blue
            
            # Bomber hull - wide and sturdy
            pygame.draw.ellipse(ship, hull_color, (5, 10, 30, 10))
            pygame.draw.ellipse(ship, (150, 200, 255), (5, 10, 30, 10), 2)
            # Large bomb bay - very visible
            pygame.draw.rect(ship, bay_color, (12, 15, 16, 10))
            pygame.draw.rect(ship, (120, 160, 220), (12, 15, 16, 10), 2)
            # Bomb bay doors
            pygame.draw.line(ship, (200, 220, 255), (12, 20), (28, 20), 2)
            # Wing-mounted engines - large and bright
            pygame.draw.circle(ship, engine_color, (8, 24), 4)
            pygame.draw.circle(ship, engine_color, (32, 24), 4)
            pygame.draw.circle(ship, (200, 230, 255), (8, 24), 2)
            pygame.draw.circle(ship, (200, 230, 255), (32, 24), 2)
            
        elif variant == 'destroyer':
            # Long-range destroyer with weapon arrays
            hull_color = (200, 100, 200)  # Purple
            weapon_color = (255, 150, 255)  # Pink
            
            # Destroyer hull - elongated
            pygame.draw.polygon(ship, hull_color, [
                (20, 2), (37, 10), (37, 20), (20, 28), (3, 20), (3, 10)
            ])
            pygame.draw.polygon(ship, (230, 130, 230), [
                (20, 2), (37, 10), (37, 20), (20, 28), (3, 20), (3, 10)
            ], 2)
            # Command bridge - prominent
            pygame.draw.rect(ship, (255, 150, 255), (16, 10, 8, 10))
            pygame.draw.rect(ship, (255, 200, 255), (16, 10, 8, 10), 2)
            # Multiple weapon arrays
            for i in range(4):
                pygame.draw.circle(ship, weapon_color, (8 + i*7, 8), 3)
                pygame.draw.circle(ship, weapon_color, (8 + i*7, 22), 3)
                pygame.draw.circle(ship, (255, 200, 255), (8 + i*7, 8), 2)
                pygame.draw.circle(ship, (255, 200, 255), (8 + i*7, 22), 2)
                
        else:  # gunship
            # Multi-weapon gunship bristling with guns
            hull_color = (180, 180, 100)  # Yellow-green
            weapon_color = (255, 255, 150)  # Bright yellow
            
            # Gunship body - rectangular and sturdy
            pygame.draw.rect(ship, hull_color, (10, 8, 20, 14))
            pygame.draw.rect(ship, (210, 210, 130), (10, 8, 20, 14), 2)
            # Many weapon mounts - very visible
            for i in range(5):
                x = 5 + i * 6
                pygame.draw.circle(ship, weapon_color, (x, 10), 3)
                pygame.draw.circle(ship, weapon_color, (x, 20), 3)
                pygame.draw.circle(ship, (255, 255, 200), (x, 10), 2)
                pygame.draw.circle(ship, (255, 255, 200), (x, 20), 2)
            # Central command module
            pygame.draw.rect(ship, (220, 220, 150), (17, 12, 6, 6))
        
        return ship
    
    def create_cruiser_ship(self, variant):
        """Create large cruiser-class ships"""
        ship = pygame.Surface((45, 30), pygame.SRCALPHA)
        
        if variant == 'battleship':
            # Massive battleship
            hull_color = (100, 100, 100)
            armor_color = (80, 80, 80)
            
            # Main hull
            pygame.draw.rect(ship, hull_color, (5, 8, 35, 14))
            # Armor sections
            for i in range(5):
                pygame.draw.rect(ship, armor_color, (7 + i*7, 6, 5, 18))
            # Command tower
            pygame.draw.rect(ship, (120, 120, 120), (18, 4, 9, 8))
            # Main guns
            pygame.draw.rect(ship, (150, 150, 150), (0, 12, 10, 6))
            pygame.draw.rect(ship, (150, 150, 150), (35, 12, 10, 6))
            
        elif variant == 'dreadnought':
            # Intimidating dreadnought
            hull_color = (120, 40, 40)
            
            # Dreadnought hull
            pygame.draw.polygon(ship, hull_color, [
                (22, 2), (40, 10), (40, 20), (22, 28), (5, 20), (5, 10)
            ])
            # Weapon spines
            for i in range(6):
                pygame.draw.line(ship, (180, 60, 60), (8 + i*5, 8), (8 + i*5, 22), 2)
            # Command section
            pygame.draw.circle(ship, (160, 80, 80), (22, 15), 6)
            
        elif variant == 'carrier':
            # Ship carrier design
            hull_color = (60, 120, 180)
            
            # Carrier hull
            pygame.draw.rect(ship, hull_color, (8, 10, 29, 10))
            # Flight deck
            pygame.draw.rect(ship, (80, 140, 200), (10, 8, 25, 14))
            # Hangar bays
            for i in range(4):
                pygame.draw.rect(ship, (100, 160, 220), (12 + i*5, 12, 3, 6))
            # Bridge tower
            pygame.draw.rect(ship, (120, 180, 240), (20, 6, 5, 8))
            
        elif variant == 'fortress':
            # Defensive fortress ship
            hull_color = (80, 140, 80)
            
            # Fortress structure
            pygame.draw.rect(ship, hull_color, (10, 5, 25, 20))
            # Defense turrets
            for x in range(3):
                for y in range(2):
                    pygame.draw.circle(ship, (120, 180, 120), (15 + x*7, 10 + y*10), 3)
            # Shield generators
            pygame.draw.circle(ship, (150, 255, 150), (12, 8), 2)
            pygame.draw.circle(ship, (150, 255, 150), (33, 8), 2)
            pygame.draw.circle(ship, (150, 255, 150), (12, 22), 2)
            pygame.draw.circle(ship, (150, 255, 150), (33, 22), 2)
            
        else:  # titan
            # Colossal titan ship
            hull_color = (140, 100, 180)
            
            # Titan hull
            pygame.draw.ellipse(ship, hull_color, (2, 5, 41, 20))
            # Titan core
            pygame.draw.circle(ship, (200, 150, 255), (22, 15), 8)
            pygame.draw.circle(ship, (160, 120, 200), (22, 15), 5)
            # Energy conduits
            for angle in range(0, 360, 45):
                x = 22 + 12 * math.cos(math.radians(angle))
                y = 15 + 12 * math.sin(math.radians(angle))
                if 0 <= x <= 45 and 0 <= y <= 30:
                    pygame.draw.circle(ship, (180, 130, 220), (int(x), int(y)), 2)
        
        return ship
    
    def create_mothership(self, variant):
        """Create massive mothership designs"""
        ship = pygame.Surface((55, 35), pygame.SRCALPHA)
        
        if variant == 'command':
            # Command mothership
            hull_color = (150, 150, 100)
            
            # Command hull
            pygame.draw.ellipse(ship, hull_color, (5, 8, 45, 19))
            # Command spire
            pygame.draw.polygon(ship, (200, 200, 150), [
                (27, 5), (32, 12), (27, 19), (23, 12)
            ])
            # Communication arrays
            for i in range(8):
                angle = i * 45
                x = 27 + 15 * math.cos(math.radians(angle))
                y = 17 + 8 * math.sin(math.radians(angle))
                if 0 <= x <= 55 and 0 <= y <= 35:
                    pygame.draw.circle(ship, (220, 220, 180), (int(x), int(y)), 2)
            
        elif variant == 'flagship':
            # Royal flagship
            hull_color = (180, 120, 60)
            
            # Flagship hull
            pygame.draw.polygon(ship, hull_color, [
                (27, 0), (50, 12), (45, 35), (10, 35), (5, 12)
            ])
            # Royal chambers
            pygame.draw.rect(ship, (220, 160, 100), (22, 10, 11, 15))
            # Ceremonial wings
            pygame.draw.polygon(ship, (200, 140, 80), [(0, 15), (10, 8), (10, 22)])
            pygame.draw.polygon(ship, (200, 140, 80), [(55, 15), (45, 8), (45, 22)])
            
        elif variant == 'overlord':
            # Menacing overlord ship
            hull_color = (120, 60, 120)
            
            # Overlord hull
            pygame.draw.ellipse(ship, hull_color, (3, 3, 49, 29))
            # Dark core
            pygame.draw.circle(ship, (80, 40, 80), (27, 17), 10)
            pygame.draw.circle(ship, (160, 80, 160), (27, 17), 6)
            # Menacing spikes
            for i in range(12):
                angle = i * 30
                x1 = 27 + 18 * math.cos(math.radians(angle))
                y1 = 17 + 12 * math.sin(math.radians(angle))
                x2 = 27 + 22 * math.cos(math.radians(angle))
                y2 = 17 + 15 * math.sin(math.radians(angle))
                if 0 <= x2 <= 55 and 0 <= y2 <= 35:
                    pygame.draw.line(ship, (180, 100, 180), (x1, y1), (x2, y2), 2)
            
        elif variant == 'leviathan':
            # Organic leviathan
            hull_color = (100, 140, 100)
            
            # Organic hull
            pygame.draw.ellipse(ship, hull_color, (2, 5, 51, 25))
            # Organic segments
            for i in range(7):
                x = 8 + i * 6
                pygame.draw.ellipse(ship, (120, 160, 120), (x, 12, 8, 11))
            # Bio-luminescent spots
            for i in range(15):
                x = random.randint(5, 50)
                y = random.randint(8, 27)
                pygame.draw.circle(ship, (150, 255, 150), (x, y), 1)
                
        else:  # colossus
            # Ultimate colossus
            hull_color = (100, 100, 150)
            
            # Colossus structure
            pygame.draw.rect(ship, hull_color, (8, 3, 39, 29))
            # Massive core
            pygame.draw.circle(ship, (150, 150, 255), (27, 17), 12)
            pygame.draw.circle(ship, (200, 200, 255), (27, 17), 8)
            pygame.draw.circle(ship, (100, 100, 200), (27, 17), 4)
            # Structural supports
            for i in range(4):
                x = 12 + i * 10
                pygame.draw.rect(ship, (120, 120, 180), (x, 0, 3, 35))
        
        return ship
    
    def create_basic_ship(self):
        """Fallback basic ship design"""
        ship = pygame.Surface((30, 20), pygame.SRCALPHA)
        hull_color = (100, 100, 100)
        
        pygame.draw.ellipse(ship, hull_color, (5, 5, 20, 10))
        pygame.draw.circle(ship, (150, 150, 150), (15, 10), 3)
        
        return ship
    
    def get_spaceship_design(self, ship_class, level=1):
        """Get appropriate spaceship design for level"""
        if ship_class not in self.spaceship_designs:
            return self.create_basic_ship()
        
        variants = list(self.spaceship_designs[ship_class].keys())
        if not variants:
            return self.create_basic_ship()
        
        # Use different variants based on level
        variant_index = (level - 1) % len(variants)
        return self.spaceship_designs[ship_class][variants[variant_index]]
    
    def get_random_spaceship(self, ship_class):
        """Get random spaceship variant"""
        if ship_class not in self.spaceship_designs:
            return self.create_basic_ship()
        
        variants = list(self.spaceship_designs[ship_class].keys())
        if not variants:
            return self.create_basic_ship()
        
        variant = random.choice(variants)
        return self.spaceship_designs[ship_class][variant]
    
    def get_ship_class_for_alien_type(self, alien_type):
        """Map alien types to ship classes"""
        mapping = {
            'basic': 'scout',
            'scout': 'fighter', 
            'warrior': 'cruiser',
            'commander': 'mothership'
        }
        return mapping.get(alien_type, 'scout')
