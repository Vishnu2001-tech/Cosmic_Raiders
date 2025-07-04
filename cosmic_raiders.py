import pygame
import random
import sys
import os
import math
from enum import Enum
from high_score_manager import HighScoreManager
from visual_assets import VisualAssets
from alien_design_manager import AlienDesignManager
from difficulty_manager import DifficultyManager
from ui_manager import UIManager
from spaceship_designer import SpaceshipDesigner
from progressive_spawner import ProgressiveSpawner
from audio_manager import AudioManager

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3
    LEVEL_COMPLETE = 4
    LEVEL_TRANSITION = 5
    PAUSED = 6
    VICTORY = 7
    CREDITS = 8

class FontManager:
    def __init__(self):
        self.fonts = {}
        self.font_path = "fonts/Pixeled.ttf"
        self.font_loaded = False
        
        # Try to load custom font
        if os.path.exists(self.font_path):
            try:
                # Test load the font
                test_font = pygame.font.Font(self.font_path, 16)
                self.font_loaded = True
                print("🎮 Font System: Using custom Pixeled.ttf")
                print("✅ Custom pixel font loaded successfully!")
                print("🎨 Authentic retro arcade styling enabled!")
            except pygame.error:
                print("🎮 Font System: Custom font failed to load, using system fonts")
                self.font_loaded = False
        else:
            print("🎮 Font System: Custom font not found, using system fonts")
            self.font_loaded = False
    
    def get_font(self, size):
        """Get font with caching"""
        if size not in self.fonts:
            if self.font_loaded:
                try:
                    self.fonts[size] = pygame.font.Font(self.font_path, size)
                except pygame.error:
                    self.fonts[size] = pygame.font.Font(None, size)
            else:
                self.fonts[size] = pygame.font.Font(None, size)
        return self.fonts[size]
    
    def render_text(self, text, size='medium', color=WHITE, center_pos=None):
        """Render text with different sizes"""
        size_map = {
            'small': 14,
            'medium': 18,
            'large': 24,
            'title': 32,
            'huge': 48
        }
        
        font_size = size_map.get(size, 18)
        font = self.get_font(font_size)
        text_surface = font.render(str(text), True, color)
        
        if center_pos:
            text_rect = text_surface.get_rect(center=center_pos)
            return text_surface, text_rect
        else:
            return text_surface, text_surface.get_rect()

class Player:
    def __init__(self, x, y, visual_assets=None):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 40
        self.speed = 5
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.visual_assets = visual_assets
        
    def move_left(self):
        if self.x > 0:
            self.x -= self.speed
            self.rect.x = self.x
            
    def move_right(self):
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
            self.rect.x = self.x
            
    def draw(self, screen):
        # Use enhanced ship sprite if available
        if self.visual_assets:
            ship_sprite = self.visual_assets.get_sprite('player')
            if ship_sprite:
                screen.blit(ship_sprite, (self.x, self.y))
                return
        
        # Fallback to original drawing
        pygame.draw.rect(screen, GREEN, self.rect)
        pygame.draw.polygon(screen, WHITE, [
            (self.x + self.width//2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ])

class Bullet:
    def __init__(self, x, y, direction, speed_multiplier=1.0, visual_assets=None):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 12
        base_speed = 8
        self.speed = base_speed * speed_multiplier
        self.direction = direction  # 1 for up (player), -1 for down (alien)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.visual_assets = visual_assets
        
    def update(self):
        self.y -= self.speed * self.direction
        self.rect.y = self.y
        
    def is_off_screen(self):
        return self.y < -10 or self.y > SCREEN_HEIGHT + 10
        
    def draw(self, screen):
        # Use enhanced laser sprites if available
        if self.visual_assets:
            if self.direction == 1:  # Player bullet
                bullet_sprite = self.visual_assets.get_sprite('player_bullet')
            else:  # Alien bullet
                bullet_sprite = self.visual_assets.get_sprite('alien_bullet')
            
            if bullet_sprite:
                screen.blit(bullet_sprite, (self.x, self.y))
                return
        
        # Fallback to original drawing
        if self.direction == 1:  # Player bullet
            color = YELLOW
            pygame.draw.rect(screen, color, self.rect)
            pygame.draw.rect(screen, WHITE, 
                           (self.x - 1, self.y - 1, self.width + 2, self.height + 2), 1)
        else:  # Alien bullet
            color = RED
            pygame.draw.rect(screen, color, self.rect)
            pygame.draw.rect(screen, (255, 100, 100), 
                           (self.x - 1, self.y - 1, self.width + 2, self.height + 2), 1)

class HitEffect:
    def __init__(self, x, y, effect_type="explosion", visual_assets=None):
        self.x = x
        self.y = y
        self.effect_type = effect_type
        self.timer = 0
        self.max_time = 30  # frames to show effect
        self.size = 0
        self.visual_assets = visual_assets
        self.explosion_frame = 0
        
    def update(self):
        self.timer += 1
        # Update explosion animation frame
        self.explosion_frame = min(5, self.timer // 5)  # 6 frames total
        
        # Grow then shrink effect for fallback
        if self.timer < self.max_time // 2:
            self.size = self.timer * 2
        else:
            self.size = (self.max_time - self.timer) * 2
        
        return self.timer < self.max_time
    
    def draw(self, screen, font_manager):
        if self.effect_type == "explosion":
            # Use enhanced explosion sprites if available
            if self.visual_assets:
                explosion_sprite = self.visual_assets.get_explosion_frame(self.explosion_frame)
                if explosion_sprite:
                    # Center the explosion sprite
                    sprite_rect = explosion_sprite.get_rect()
                    sprite_rect.center = (int(self.x), int(self.y))
                    screen.blit(explosion_sprite, sprite_rect)
                    return
            
            # Fallback explosion effect
            colors = [YELLOW, RED, WHITE]
            for i, color in enumerate(colors):
                radius = max(1, self.size - i * 3)
                if radius > 0:
                    pygame.draw.circle(screen, color, (int(self.x), int(self.y)), radius)
            
            # Draw explosion text
            if self.timer < 20:
                explosion_text, explosion_rect = font_manager.render_text(
                    "💥", 'medium', WHITE, (self.x, self.y - 10)
                )
                screen.blit(explosion_text, explosion_rect)

class Alien:
    def __init__(self, x, y, alien_type="basic", difficulty_level=1, visual_assets=None, 
                 alien_design_manager=None, difficulty_manager=None, spaceship_designer=None, progressive_spawner=None):
        self.x = x
        self.y = y
        self.initial_x = x
        self.initial_y = y
        self.width = 35
        self.height = 25
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.alien_type = alien_type
        self.difficulty_level = difficulty_level
        self.visual_assets = visual_assets
        self.alien_design_manager = alien_design_manager
        self.difficulty_manager = difficulty_manager
        self.spaceship_designer = spaceship_designer
        self.progressive_spawner = progressive_spawner
        
        # Get level-appropriate stats with enhanced scaling
        if difficulty_manager:
            stats = difficulty_manager.get_alien_stats(alien_type, difficulty_level)
            self.health = stats['health']
            self.max_health = stats['health']
            self.base_speed = stats['speed']
            self.points = stats['points']
        else:
            # Fallback stats
            self.health = 1
            self.max_health = 1
            self.base_speed = 1.0
            self.points = {'basic': 10, 'scout': 15, 'warrior': 25, 'commander': 50}.get(alien_type, 10)
        
        # Enhanced movement with progressive spawner scaling
        if progressive_spawner:
            speed_mult = progressive_spawner.get_speed_multiplier(difficulty_level)
            aggression_mult = progressive_spawner.get_aggression_multiplier(difficulty_level)
        else:
            speed_mult = 1.0 + (difficulty_level - 1) * 0.4
            aggression_mult = 1.0 + (difficulty_level - 1) * 0.5
        
        self.vertical_speed = 0.5 * speed_mult
        self.horizontal_speed = self.base_speed * speed_mult
        self.horizontal_direction = random.choice([-1, 1])
        
        # Enhanced shooting with progressive aggression
        base_shoot_chance = {'basic': 0.001, 'scout': 0.0015, 'warrior': 0.0008, 'commander': 0.002}.get(alien_type, 0.001)
        self.shoot_chance = base_shoot_chance * aggression_mult
        
        # Color coding for health/damage
        self.base_colors = {
            'basic': (60, 120, 60),
            'scout': (60, 120, 120), 
            'warrior': (120, 60, 60),
            'commander': (120, 60, 120)
        }
        self.color = self.base_colors.get(alien_type, (60, 120, 60))
        
        # Special abilities based on level
        self.special_abilities = []
        if difficulty_manager and difficulty_manager.should_use_special_ability(difficulty_level, 'rapid_fire'):
            self.special_abilities.append('rapid_fire')
        if difficulty_manager and difficulty_manager.should_use_special_ability(difficulty_level, 'teleport_dodge'):
            self.special_abilities.append('teleport_dodge')
        
        # Damage flash effect
        self.damage_flash = 0
        
        # Get spaceship design
        self.spaceship_sprite = None
        if spaceship_designer:
            ship_class = spaceship_designer.get_ship_class_for_alien_type(alien_type)
            self.spaceship_sprite = spaceship_designer.get_spaceship_design(ship_class, difficulty_level)
            if self.spaceship_sprite:
                # Adjust rect size to match spaceship
                self.width = self.spaceship_sprite.get_width()
                self.height = self.spaceship_sprite.get_height()
                self.rect = pygame.Rect(x, y, self.width, self.height)
                print(f"🛸 Created {alien_type} spaceship (Level {difficulty_level}) - {ship_class} class, Size: {self.width}x{self.height}")
            else:
                print(f"⚠️ Failed to create spaceship for {alien_type} (Level {difficulty_level})")
        else:
            print(f"⚠️ No spaceship designer available for {alien_type}")
        
        if not hasattr(self, 'spaceship_sprite') or not self.spaceship_sprite:
            print(f"🔧 DEBUG: {alien_type} will use fallback rendering")
    
    def take_damage(self, damage=1):
        """Take damage and return True if destroyed"""
        self.health -= damage
        self.damage_flash = 10  # Flash for 10 frames
        
        if self.health <= 0:
            return True
        return False
    
    def update(self):
        """Enhanced update with special abilities and faster movement"""
        # Reduce damage flash
        if self.damage_flash > 0:
            self.damage_flash -= 1
        
        # Enhanced movement patterns based on type and level with increased speed
        if self.alien_type == 'scout':
            # Scouts move in zigzag patterns at higher levels (faster)
            if self.difficulty_level >= 3:
                self.x += math.sin(pygame.time.get_ticks() * 0.02) * self.horizontal_speed * 0.8
            else:
                self.x += self.horizontal_direction * self.horizontal_speed * 1.2
        elif self.alien_type == 'warrior':
            # Warriors move more predictably but much faster
            self.x += self.horizontal_direction * self.horizontal_speed * 1.0
        elif self.alien_type == 'commander':
            # Commanders have complex movement patterns (faster)
            if self.difficulty_level >= 5:
                self.x += math.sin(pygame.time.get_ticks() * 0.008) * self.horizontal_speed * 1.2
            else:
                self.x += self.horizontal_direction * self.horizontal_speed * 0.9
        else:  # basic
            # Basic aliens move horizontally (faster than before)
            self.x += self.horizontal_direction * self.horizontal_speed * 1.1
        
        # Faster vertical movement
        self.y += self.vertical_speed
        
        # Boundary checking with direction reversal
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.horizontal_direction *= -1
            self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        
        # Update rect
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Special ability: teleport dodge (high level commanders)
        if 'teleport_dodge' in self.special_abilities and random.random() < 0.002:  # More frequent
            self.x = random.randint(50, SCREEN_WIDTH - 50)
    
    def should_shoot(self):
        """Enhanced shooting logic with higher frequency"""
        base_chance = random.random() < self.shoot_chance
        
        # Rapid fire ability (more frequent)
        if 'rapid_fire' in self.special_abilities:
            return base_chance or (random.random() < self.shoot_chance * 0.8)
        
        return base_chance
    
    def draw(self, screen):
        """Enhanced drawing with spaceship designs"""
        # Use spaceship designs first
        if hasattr(self, 'spaceship_sprite') and self.spaceship_sprite:
            # Apply damage flash effect to spaceship
            if self.damage_flash > 0:
                # Create flashing effect
                flash_surface = self.spaceship_sprite.copy()
                flash_surface.fill((255, 255, 255, 100), special_flags=pygame.BLEND_ADD)
                screen.blit(flash_surface, (self.x, self.y))
            else:
                screen.blit(self.spaceship_sprite, (self.x, self.y))
            
            # Health bar for multi-health aliens
            if self.max_health > 1:
                self.draw_health_bar(screen)
            return
        
        # Fallback to alien design manager
        if self.alien_design_manager:
            alien_sprite = self.alien_design_manager.get_alien_design(self.alien_type, self.difficulty_level)
            if alien_sprite:
                # Apply damage flash effect
                if self.damage_flash > 0:
                    flash_surface = alien_sprite.copy()
                    flash_surface.fill((255, 255, 255, 100), special_flags=pygame.BLEND_ADD)
                    screen.blit(flash_surface, (self.x, self.y))
                else:
                    screen.blit(alien_sprite, (self.x, self.y))
                
                # Health bar for multi-health aliens
                if self.max_health > 1:
                    self.draw_health_bar(screen)
                return
        
        # Final fallback to basic shapes (this should show what's happening)
        print(f"🔧 DEBUG: Drawing fallback shape for {self.alien_type} at ({self.x}, {self.y})")
        draw_color = self.color
        if self.damage_flash > 0:
            draw_color = (255, 255, 255)
        
        pygame.draw.rect(screen, draw_color, self.rect)
        pygame.draw.ellipse(screen, (255, 255, 255), 
                          (self.x + 3, self.y + 3, self.width - 6, self.height - 6))
        
        # Health bar for multi-health aliens
        if self.max_health > 1:
            self.draw_health_bar(screen)
    
    def draw_health_bar(self, screen):
        """Draw health bar above alien"""
        if self.health >= self.max_health:
            return  # Don't show full health bar
        
        bar_width = self.width
        bar_height = 3
        bar_x = self.x
        bar_y = self.y - 6
        
        # Background
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        
        # Health
        health_ratio = self.health / self.max_health
        health_width = int(bar_width * health_ratio)
        
        if health_ratio > 0.6:
            health_color = (0, 255, 0)
        elif health_ratio > 0.3:
            health_color = (255, 255, 0)
        else:
            health_color = (255, 0, 0)
        
        if health_width > 0:
            pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
    
    def is_at_bottom(self):
        """Check if alien reached bottom with adjusted margin"""
        return self.y + self.height >= SCREEN_HEIGHT - 100
        
        # Get level-appropriate stats
        if difficulty_manager:
            stats = difficulty_manager.get_alien_stats(alien_type, difficulty_level)
            self.health = stats['health']
            self.max_health = stats['health']
            self.base_speed = stats['speed']
            self.points = stats['points']
        else:
            # Fallback stats
            self.health = 1
            self.max_health = 1
            self.base_speed = 1.0
            self.points = {'basic': 10, 'scout': 15, 'warrior': 25, 'commander': 50}.get(alien_type, 10)
        
        # Enhanced movement with level scaling
        self.vertical_speed = 0.5 * (1.0 + (difficulty_level - 1) * 0.1)  # Slightly faster descent per level
        self.horizontal_speed = self.base_speed * (1.0 + (difficulty_level - 1) * 0.2)  # Significant horizontal speed increase
        self.horizontal_direction = random.choice([-1, 1])
        
        # Enhanced shooting with level scaling
        base_shoot_chance = {'basic': 0.001, 'scout': 0.0015, 'warrior': 0.0008, 'commander': 0.002}.get(alien_type, 0.001)
        self.shoot_chance = base_shoot_chance * (1 + difficulty_level * 0.3)  # Much more aggressive at higher levels
        
        # Color coding for health/damage
        self.base_colors = {
            'basic': (60, 120, 60),
            'scout': (60, 120, 120), 
            'warrior': (120, 60, 60),
            'commander': (120, 60, 120)
        }
        self.color = self.base_colors.get(alien_type, (60, 120, 60))
        
        # Special abilities based on level
        self.special_abilities = []
        if difficulty_manager and difficulty_manager.should_use_special_ability(difficulty_level, 'rapid_fire'):
            self.special_abilities.append('rapid_fire')
        if difficulty_manager and difficulty_manager.should_use_special_ability(difficulty_level, 'teleport_dodge'):
            self.special_abilities.append('teleport_dodge')
        
        # Damage flash effect
        self.damage_flash = 0
        
    def take_damage(self, damage=1):
        """Take damage and return True if destroyed"""
        self.health -= damage
        self.damage_flash = 10  # Flash for 10 frames
        
        if self.health <= 0:
            return True
        return False
    
    def update(self):
        """Enhanced update with special abilities"""
        # Reduce damage flash
        if self.damage_flash > 0:
            self.damage_flash -= 1
        
        # Enhanced movement patterns based on type and level
        if self.alien_type == 'scout':
            # Scouts move in zigzag patterns at higher levels
            if self.difficulty_level >= 3:
                self.x += math.sin(pygame.time.get_ticks() * 0.01) * self.horizontal_speed * 0.5
        elif self.alien_type == 'warrior':
            # Warriors move more predictably but faster
            self.x += self.horizontal_direction * self.horizontal_speed * 0.7
        elif self.alien_type == 'commander':
            # Commanders have complex movement patterns
            if self.difficulty_level >= 5:
                self.x += math.sin(pygame.time.get_ticks() * 0.005) * self.horizontal_speed
        else:  # basic
            # Basic aliens move horizontally
            self.x += self.horizontal_direction * self.horizontal_speed
        
        # Vertical movement (constant for all types)
        self.y += self.vertical_speed
        
        # Boundary checking with direction reversal
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.horizontal_direction *= -1
            self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        
        # Update rect
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Special ability: teleport dodge (high level commanders)
        if 'teleport_dodge' in self.special_abilities and random.random() < 0.001:
            self.x = random.randint(50, SCREEN_WIDTH - 50)
    
    def should_shoot(self):
        """Enhanced shooting logic"""
        base_chance = random.random() < self.shoot_chance
        
        # Rapid fire ability
        if 'rapid_fire' in self.special_abilities:
            return base_chance or (random.random() < self.shoot_chance * 0.5)
        
        return base_chance
    
    def draw(self, screen):
        """Enhanced drawing with level-appropriate designs and damage effects"""
        # Use enhanced alien designs if available
        if self.alien_design_manager:
            alien_sprite = self.alien_design_manager.get_alien_design(self.alien_type, self.difficulty_level)
            if alien_sprite:
                # Apply damage flash effect
                if self.damage_flash > 0:
                    # Create flashing effect
                    flash_surface = alien_sprite.copy()
                    flash_surface.fill((255, 255, 255, 100), special_flags=pygame.BLEND_ADD)
                    screen.blit(flash_surface, (self.x, self.y))
                else:
                    screen.blit(alien_sprite, (self.x, self.y))
                
                # Health bar for multi-health aliens
                if self.max_health > 1:
                    self.draw_health_bar(screen)
                return
        
        # Fallback to original drawing with damage effects
        draw_color = self.color
        if self.damage_flash > 0:
            # Flash white when damaged
            draw_color = (255, 255, 255)
        
        pygame.draw.rect(screen, draw_color, self.rect)
        
        # Draw different shapes based on alien type (enhanced)
        if self.alien_type == "scout":
            pygame.draw.polygon(screen, (255, 255, 255), [
                (self.x + self.width//2, self.y + 3),
                (self.x + self.width - 3, self.y + self.height - 3),
                (self.x + 3, self.y + self.height - 3)
            ])
        elif self.alien_type == "warrior":
            pygame.draw.polygon(screen, (255, 255, 255), [
                (self.x + self.width//2, self.y + 3),
                (self.x + self.width - 3, self.y + self.height//2),
                (self.x + self.width//2, self.y + self.height - 3),
                (self.x + 3, self.y + self.height//2)
            ])
        elif self.alien_type == "commander":
            center_x = self.x + self.width // 2
            center_y = self.y + self.height // 2
            pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 8)
            pygame.draw.circle(screen, draw_color, (center_x, center_y), 5)
        else:  # basic
            pygame.draw.ellipse(screen, (255, 255, 255), 
                              (self.x + 3, self.y + 3, self.width - 6, self.height - 6))
        
        # Health bar for multi-health aliens
        if self.max_health > 1:
            self.draw_health_bar(screen)
    
    def draw_health_bar(self, screen):
        """Draw health bar above alien"""
        if self.health >= self.max_health:
            return  # Don't show full health bar
        
        bar_width = self.width
        bar_height = 3
        bar_x = self.x
        bar_y = self.y - 6
        
        # Background
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        
        # Health
        health_ratio = self.health / self.max_health
        health_width = int(bar_width * health_ratio)
        
        if health_ratio > 0.6:
            health_color = (0, 255, 0)
        elif health_ratio > 0.3:
            health_color = (255, 255, 0)
        else:
            health_color = (255, 0, 0)
        
        if health_width > 0:
            pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
        
        # Constant vertical descent speed (consistent across all levels)
        self.vertical_speed = 0.5  # Slower descent for better gameplay
        
        # Horizontal speed increases with level (0.2x per level)
        self.horizontal_speed = 1.0 + (difficulty_level - 1) * 0.2
        self.horizontal_direction = random.choice([-1, 1])  # Random initial direction
        
        # Dynamic shooting based on difficulty
        base_shoot_chance = 0.001
        self.shoot_chance = base_shoot_chance * (1 + difficulty_level * 0.2)
        
        # Alien types with different characteristics
        if alien_type == "scout":
            self.color = CYAN
            self.points = 15
            self.horizontal_speed *= 1.3  # Scouts move faster
        elif alien_type == "warrior":
            self.color = RED
            self.points = 25
            self.shoot_chance *= 1.5  # Warriors shoot more
        elif alien_type == "commander":
            self.color = MAGENTA
            self.points = 40
            self.shoot_chance *= 2.0  # Commanders are most aggressive
            self.horizontal_speed *= 0.8  # But move slower
        else:  # basic
            self.color = GREEN
            self.points = 10
        
    def update(self):
        # Constant vertical descent
        self.y += self.vertical_speed
        
        # Dynamic horizontal movement
        self.x += self.horizontal_direction * self.horizontal_speed
        
        # Bounce off screen edges
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.horizontal_direction *= -1
        
        # Update rect
        self.rect.x = self.x
        self.rect.y = self.y
        
    def should_shoot(self):
        return random.random() < self.shoot_chance
        
    def draw(self, screen):
        # Use enhanced alien sprites if available
        if self.visual_assets:
            alien_sprite = self.visual_assets.get_sprite(f'alien_{self.alien_type}')
            if alien_sprite:
                screen.blit(alien_sprite, (self.x, self.y))
                return
        
        # Fallback to original drawing
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw different shapes based on alien type
        if self.alien_type == "scout":
            pygame.draw.polygon(screen, WHITE, [
                (self.x + self.width//2, self.y + 3),
                (self.x + self.width - 3, self.y + self.height - 3),
                (self.x + 3, self.y + self.height - 3)
            ])
        elif self.alien_type == "warrior":
            pygame.draw.polygon(screen, WHITE, [
                (self.x + self.width//2, self.y + 3),
                (self.x + self.width - 3, self.y + self.height//2),
                (self.x + self.width//2, self.y + self.height - 3),
                (self.x + 3, self.y + self.height//2)
            ])
        elif self.alien_type == "commander":
            center_x = self.x + self.width // 2
            center_y = self.y + self.height // 2
            pygame.draw.circle(screen, WHITE, (center_x, center_y), 8)
            pygame.draw.circle(screen, self.color, (center_x, center_y), 5)
        else:  # basic
            pygame.draw.ellipse(screen, WHITE, 
                              (self.x + 3, self.y + 3, self.width - 6, self.height - 6))
    
    def is_at_bottom(self):
        """Check if alien has reached the bottom of the screen"""
        return self.y + self.height >= SCREEN_HEIGHT - 100  # More margin for player area

class CosmicFormation:
    def __init__(self, difficulty_level=1, visual_assets=None, alien_design_manager=None, 
                 difficulty_manager=None, spaceship_designer=None, progressive_spawner=None):
        self.difficulty_level = difficulty_level
        self.visual_assets = visual_assets
        self.alien_design_manager = alien_design_manager
        self.difficulty_manager = difficulty_manager
        self.spaceship_designer = spaceship_designer
        self.progressive_spawner = progressive_spawner
        self.active_aliens = []
        self.formation_queue = []
        
        # Get progressive spawning configuration
        if progressive_spawner:
            self.max_active_aliens = progressive_spawner.get_max_active_aliens(difficulty_level)
            self.spawn_delay = progressive_spawner.get_spawn_delay(difficulty_level)
        else:
            # Fallback progressive system
            if difficulty_level == 1:
                self.max_active_aliens = 3
            elif difficulty_level == 2:
                self.max_active_aliens = 4
            elif difficulty_level <= 5:
                self.max_active_aliens = 5
            else:
                self.max_active_aliens = 6
            self.spawn_delay = max(60, 180 - (difficulty_level - 1) * 10)
        
        self.spawn_timer = 0
        
        # Generate formation based on level
        self.generate_formation()
        
        print(f"🌌 Generated {len(self.formation_queue)} aliens for Level {difficulty_level} formation")
        print(f"📊 Max active: {self.max_active_aliens}, Spawn delay: {self.spawn_delay/60:.1f}s")
    
    def generate_formation(self):
        """Generate level-appropriate formation with enhanced difficulty"""
        formation_patterns = {
            1: self.create_line_formation,
            2: self.create_v_formation, 
            3: self.create_arc_formation,
            4: self.create_triangle_formation,
            5: self.create_diamond_formation,
            6: self.create_spiral_formation,
            7: self.create_cross_formation,
            8: self.create_wave_formation
        }
        
        pattern_index = ((self.difficulty_level - 1) % 8) + 1
        formation_func = formation_patterns.get(pattern_index, self.create_line_formation)
        
        # Create formation with level-appropriate alien types
        formation_func()
        
        # Shuffle for more dynamic spawning
        random.shuffle(self.formation_queue)
    
    def create_line_formation(self):
        """Enhanced line formation with progressive scaling"""
        base_count = 5
        if self.progressive_spawner:
            size_mult = self.progressive_spawner.get_formation_size_multiplier(self.difficulty_level)
            alien_count = int(base_count * size_mult)
        else:
            alien_count = base_count + (self.difficulty_level - 1) // 2
        
        spacing = SCREEN_WIDTH // (alien_count + 1)
        
        for i in range(alien_count):
            x = spacing * (i + 1) - 17
            y = 50
            alien_type = self.get_level_appropriate_alien_type()
            self.formation_queue.append((x, y, alien_type))
    
    def create_v_formation(self):
        """Enhanced V formation with progressive scaling"""
        base_count = 8
        if self.progressive_spawner:
            size_mult = self.progressive_spawner.get_formation_size_multiplier(self.difficulty_level)
            alien_count = int(base_count * size_mult)
        else:
            alien_count = base_count + (self.difficulty_level - 1) // 2
        
        center_x = SCREEN_WIDTH // 2
        
        for i in range(alien_count):
            if i % 2 == 0:  # Left side
                x = center_x - (i // 2 + 1) * 40
                y = 50 + (i // 2) * 15
            else:  # Right side
                x = center_x + (i // 2 + 1) * 40
                y = 50 + (i // 2) * 15
            
            alien_type = self.get_level_appropriate_alien_type()
            self.formation_queue.append((x, y, alien_type))
    
    def create_arc_formation(self):
        """Enhanced arc formation with progressive scaling"""
        base_count = 12
        if self.progressive_spawner:
            size_mult = self.progressive_spawner.get_formation_size_multiplier(self.difficulty_level)
            alien_count = int(base_count * size_mult)
        else:
            alien_count = base_count + (self.difficulty_level - 1) // 2
        
        center_x = SCREEN_WIDTH // 2
        radius = 120
        
        for i in range(alien_count):
            angle = math.pi * (i / (alien_count - 1))  # Half circle
            x = center_x + radius * math.cos(angle) - 17
            y = 80 + radius * 0.3 * math.sin(angle)
            
            alien_type = self.get_level_appropriate_alien_type()
            self.formation_queue.append((x, y, alien_type))
    
    def create_triangle_formation(self):
        """Enhanced triangle formation with progressive scaling"""
        base_rows = 4
        if self.progressive_spawner:
            size_mult = self.progressive_spawner.get_formation_size_multiplier(self.difficulty_level)
            rows = int(base_rows * size_mult)
        else:
            rows = base_rows + (self.difficulty_level - 1) // 3
        
        for row in range(rows):
            aliens_in_row = row + 1
            row_width = aliens_in_row * 40
            start_x = (SCREEN_WIDTH - row_width) // 2
            
            for col in range(aliens_in_row):
                x = start_x + col * 40
                y = 50 + row * 30
                
                alien_type = self.get_level_appropriate_alien_type()
                self.formation_queue.append((x, y, alien_type))
    
    def create_diamond_formation(self):
        """Enhanced diamond formation with progressive scaling"""
        base_size = 3
        if self.progressive_spawner:
            size_mult = self.progressive_spawner.get_formation_size_multiplier(self.difficulty_level)
            size = int(base_size * size_mult)
        else:
            size = base_size + (self.difficulty_level - 1) // 4
        
        center_x = SCREEN_WIDTH // 2
        
        # Top half
        for row in range(size):
            aliens_in_row = row + 1
            for col in range(aliens_in_row):
                x = center_x + (col - aliens_in_row // 2) * 40
                y = 50 + row * 25
                
                alien_type = self.get_level_appropriate_alien_type()
                self.formation_queue.append((x, y, alien_type))
        
        # Bottom half
        for row in range(size - 1, 0, -1):
            aliens_in_row = row
            for col in range(aliens_in_row):
                x = center_x + (col - aliens_in_row // 2) * 40
                y = 50 + (2 * size - row - 1) * 25
                
                alien_type = self.get_level_appropriate_alien_type()
                self.formation_queue.append((x, y, alien_type))
    
    def create_spiral_formation(self):
        """Enhanced spiral formation with progressive scaling"""
        base_count = 15
        if self.progressive_spawner:
            size_mult = self.progressive_spawner.get_formation_size_multiplier(self.difficulty_level)
            alien_count = int(base_count * size_mult)
        else:
            alien_count = base_count + (self.difficulty_level - 1) * 2
        
        center_x = SCREEN_WIDTH // 2
        center_y = 100
        
        for i in range(alien_count):
            angle = i * 0.5
            radius = 20 + i * 3
            
            x = center_x + radius * math.cos(angle) - 17
            y = center_y + radius * math.sin(angle) * 0.5
            
            alien_type = self.get_level_appropriate_alien_type()
            self.formation_queue.append((x, y, alien_type))
    
    def create_cross_formation(self):
        """Enhanced cross formation with progressive scaling"""
        base_length = 4
        if self.progressive_spawner:
            size_mult = self.progressive_spawner.get_formation_size_multiplier(self.difficulty_level)
            arm_length = int(base_length * size_mult)
        else:
            arm_length = base_length + (self.difficulty_level - 1) // 3
        
        center_x = SCREEN_WIDTH // 2
        center_y = 100
        
        # Horizontal arm
        for i in range(-arm_length, arm_length + 1):
            x = center_x + i * 35
            y = center_y
            
            alien_type = self.get_level_appropriate_alien_type()
            self.formation_queue.append((x, y, alien_type))
        
        # Vertical arm
        for i in range(-arm_length, arm_length + 1):
            if i != 0:  # Don't duplicate center
                x = center_x
                y = center_y + i * 30
                
                alien_type = self.get_level_appropriate_alien_type()
                self.formation_queue.append((x, y, alien_type))
    
    def create_wave_formation(self):
        """Enhanced wave formation with progressive scaling"""
        base_waves = 2
        if self.progressive_spawner:
            size_mult = self.progressive_spawner.get_formation_size_multiplier(self.difficulty_level)
            wave_count = int(base_waves * size_mult)
        else:
            wave_count = base_waves + (self.difficulty_level - 1) // 4
        
        aliens_per_wave = 8
        
        for wave in range(wave_count):
            for i in range(aliens_per_wave):
                x = (SCREEN_WIDTH // aliens_per_wave) * i + 50
                y = 60 + wave * 40 + 20 * math.sin(i * 0.8)
                
                alien_type = self.get_level_appropriate_alien_type()
                self.formation_queue.append((x, y, alien_type))
    
    def get_level_appropriate_alien_type(self):
        """Get alien type appropriate for current level"""
        if self.difficulty_manager:
            return self.difficulty_manager.get_alien_type_for_level(self.difficulty_level)
        
        # Fallback distribution with more variety at higher levels
        if self.difficulty_level <= 2:
            return random.choice(['basic', 'basic', 'basic', 'scout'])
        elif self.difficulty_level <= 5:
            return random.choice(['basic', 'basic', 'scout', 'scout', 'warrior'])
        else:
            return random.choice(['basic', 'scout', 'scout', 'warrior', 'warrior', 'commander'])
    
    def update(self):
        """Update formation with enhanced spawning"""
        # Update existing aliens
        for alien in self.active_aliens[:]:
            alien.update()
            
            # Remove aliens that are off screen or at bottom
            if alien.is_at_bottom() or alien.y > SCREEN_HEIGHT:
                self.active_aliens.remove(alien)
        
        # Spawn new aliens with progressive system
        self.spawn_timer -= 1
        if (self.spawn_timer <= 0 and 
            len(self.active_aliens) < self.max_active_aliens and 
            len(self.formation_queue) > 0):
            
            x, y, alien_type = self.formation_queue.pop(0)
            new_alien = Alien(x, y, alien_type, self.difficulty_level, 
                            self.visual_assets, self.alien_design_manager, self.difficulty_manager,
                            self.spaceship_designer, self.progressive_spawner)
            self.active_aliens.append(new_alien)
            self.spawn_timer = self.spawn_delay
            
            print(f"👾 Spawned {alien_type} spaceship at ({x}, {y}) - Active: {len(self.active_aliens)}/{self.max_active_aliens}")
    
    def draw(self, screen):
        """Draw all active aliens"""
        for alien in self.active_aliens:
            alien.draw(screen)
    
    def get_total_aliens_remaining(self):
        """Get total aliens remaining"""
        return len(self.active_aliens) + len(self.formation_queue)
    
    def get_shooting_aliens(self):
        """Get aliens that can shoot"""
        return self.active_aliens
    
    def generate_formation(self):
        """Generate level-appropriate formation with enhanced difficulty"""
        formation_patterns = {
            1: self.create_line_formation,
            2: self.create_v_formation, 
            3: self.create_arc_formation,
            4: self.create_triangle_formation,
            5: self.create_diamond_formation,
            6: self.create_spiral_formation,
            7: self.create_cross_formation,
            8: self.create_wave_formation
        }
        
        pattern_index = ((self.difficulty_level - 1) % 8) + 1
        formation_func = formation_patterns.get(pattern_index, self.create_line_formation)
        
        # Create formation with level-appropriate alien types
        formation_func()
        
        # Shuffle for more dynamic spawning
        random.shuffle(self.formation_queue)
    
    def create_line_formation(self):
        """Enhanced line formation with level scaling"""
        base_count = 5
        level_bonus = (self.difficulty_level - 1) // 2  # Extra aliens every 2 levels
        alien_count = base_count + level_bonus
        
        spacing = SCREEN_WIDTH // (alien_count + 1)
        
        for i in range(alien_count):
            x = spacing * (i + 1) - 17
            y = 50
            alien_type = self.get_level_appropriate_alien_type()
            self.formation_queue.append((x, y, alien_type))
    
    def create_v_formation(self):
        """Enhanced V formation"""
        base_count = 8
        level_bonus = (self.difficulty_level - 1) // 2
        alien_count = base_count + level_bonus
        
        center_x = SCREEN_WIDTH // 2
        
        for i in range(alien_count):
            if i % 2 == 0:  # Left side
                x = center_x - (i // 2 + 1) * 40
                y = 50 + (i // 2) * 15
            else:  # Right side
                x = center_x + (i // 2 + 1) * 40
                y = 50 + (i // 2) * 15
            
            alien_type = self.get_level_appropriate_alien_type()
            self.formation_queue.append((x, y, alien_type))
    
    def create_arc_formation(self):
        """Enhanced arc formation"""
        base_count = 12
        level_bonus = (self.difficulty_level - 1) // 2
        alien_count = base_count + level_bonus
        
        center_x = SCREEN_WIDTH // 2
        radius = 120
        
        for i in range(alien_count):
            angle = math.pi * (i / (alien_count - 1))  # Half circle
            x = center_x + radius * math.cos(angle) - 17
            y = 80 + radius * 0.3 * math.sin(angle)
            
            alien_type = self.get_level_appropriate_alien_type()
            self.formation_queue.append((x, y, alien_type))
    
    def create_triangle_formation(self):
        """Enhanced triangle formation"""
        rows = 4 + (self.difficulty_level - 1) // 3  # More rows at higher levels
        
        for row in range(rows):
            aliens_in_row = row + 1
            row_width = aliens_in_row * 40
            start_x = (SCREEN_WIDTH - row_width) // 2
            
            for col in range(aliens_in_row):
                x = start_x + col * 40
                y = 50 + row * 30
                
                alien_type = self.get_level_appropriate_alien_type()
                self.formation_queue.append((x, y, alien_type))
    
    def create_diamond_formation(self):
        """Enhanced diamond formation"""
        size = 3 + (self.difficulty_level - 1) // 4  # Larger diamonds at higher levels
        center_x = SCREEN_WIDTH // 2
        
        # Top half
        for row in range(size):
            aliens_in_row = row + 1
            for col in range(aliens_in_row):
                x = center_x + (col - aliens_in_row // 2) * 40
                y = 50 + row * 25
                
                alien_type = self.get_level_appropriate_alien_type()
                self.formation_queue.append((x, y, alien_type))
        
        # Bottom half
        for row in range(size - 1, 0, -1):
            aliens_in_row = row
            for col in range(aliens_in_row):
                x = center_x + (col - aliens_in_row // 2) * 40
                y = 50 + (2 * size - row - 1) * 25
                
                alien_type = self.get_level_appropriate_alien_type()
                self.formation_queue.append((x, y, alien_type))
    
    def create_spiral_formation(self):
        """Enhanced spiral formation"""
        alien_count = 15 + (self.difficulty_level - 1) * 2
        center_x = SCREEN_WIDTH // 2
        center_y = 100
        
        for i in range(alien_count):
            angle = i * 0.5
            radius = 20 + i * 3
            
            x = center_x + radius * math.cos(angle) - 17
            y = center_y + radius * math.sin(angle) * 0.5
            
            alien_type = self.get_level_appropriate_alien_type()
            self.formation_queue.append((x, y, alien_type))
    
    def create_cross_formation(self):
        """Enhanced cross formation"""
        arm_length = 4 + (self.difficulty_level - 1) // 3
        center_x = SCREEN_WIDTH // 2
        center_y = 100
        
        # Horizontal arm
        for i in range(-arm_length, arm_length + 1):
            x = center_x + i * 35
            y = center_y
            
            alien_type = self.get_level_appropriate_alien_type()
            self.formation_queue.append((x, y, alien_type))
        
        # Vertical arm
        for i in range(-arm_length, arm_length + 1):
            if i != 0:  # Don't duplicate center
                x = center_x
                y = center_y + i * 30
                
                alien_type = self.get_level_appropriate_alien_type()
                self.formation_queue.append((x, y, alien_type))
    
    def create_wave_formation(self):
        """Enhanced wave formation"""
        wave_count = 2 + (self.difficulty_level - 1) // 4
        aliens_per_wave = 8
        
        for wave in range(wave_count):
            for i in range(aliens_per_wave):
                x = (SCREEN_WIDTH // aliens_per_wave) * i + 50
                y = 60 + wave * 40 + 20 * math.sin(i * 0.8)
                
                alien_type = self.get_level_appropriate_alien_type()
                self.formation_queue.append((x, y, alien_type))
    
    def get_level_appropriate_alien_type(self):
        """Get alien type appropriate for current level"""
        if self.difficulty_manager:
            return self.difficulty_manager.get_alien_type_for_level(self.difficulty_level)
        
        # Fallback distribution
        if self.difficulty_level <= 2:
            return random.choice(['basic', 'basic', 'basic', 'scout'])
        elif self.difficulty_level <= 5:
            return random.choice(['basic', 'basic', 'scout', 'warrior'])
        else:
            return random.choice(['basic', 'scout', 'warrior', 'commander'])
    
    def update(self):
        """Update formation with enhanced spawning"""
        # Update existing aliens
        for alien in self.active_aliens[:]:
            alien.update()
            
            # Remove aliens that are off screen or at bottom
            if alien.is_at_bottom() or alien.y > SCREEN_HEIGHT:
                self.active_aliens.remove(alien)
        
        # Spawn new aliens
        self.spawn_timer -= 1
        if (self.spawn_timer <= 0 and 
            len(self.active_aliens) < self.max_active_aliens and 
            len(self.formation_queue) > 0):
            
            x, y, alien_type = self.formation_queue.pop(0)
            new_alien = Alien(x, y, alien_type, self.difficulty_level, 
                            self.visual_assets, self.alien_design_manager, self.difficulty_manager,
                            self.spaceship_designer, self.progressive_spawner)
            self.active_aliens.append(new_alien)
            self.spawn_timer = self.spawn_delay
            
            print(f"👾 Spawned {alien_type} alien at ({x}, {y})")
    
    def draw(self, screen):
        """Draw all active aliens"""
        for alien in self.active_aliens:
            alien.draw(screen)
    
    def get_total_aliens_remaining(self):
        """Get total aliens remaining"""
        return len(self.active_aliens) + len(self.formation_queue)
        
        # Generate formation for this level
        self.generate_formation()
        
    def generate_formation(self):
        """Generate unique formation patterns based on level"""
        formations = {
            1: self.create_horizontal_line,
            2: self.create_v_formation,
            3: self.create_arc_formation,
            4: self.create_triangle_formation,
            5: self.create_diamond_formation,
            6: self.create_spiral_formation,
            7: self.create_cross_formation,
            8: self.create_wave_formation,
        }
        
        # Use modulo for levels beyond 8 to cycle through formations
        formation_func = formations.get(self.difficulty_level, formations[((self.difficulty_level - 1) % 8) + 1])
        self.formation_queue = formation_func()
        
        print(f"🌌 Generated {len(self.formation_queue)} aliens for Level {self.difficulty_level} formation")
    
    def create_horizontal_line(self):
        """Level 1: Simple horizontal line"""
        aliens = []
        num_layers = self.difficulty_level
        
        for layer in range(num_layers):
            y_pos = 50 + layer * 60
            for i in range(5):  # 5 aliens per layer
                x_pos = 150 + i * 100
                alien_type = "basic" if layer == 0 else random.choice(["basic", "scout"])
                aliens.append((x_pos, y_pos, alien_type))
        
        return aliens
    
    def create_v_formation(self):
        """Level 2: V-shaped formation"""
        aliens = []
        num_layers = self.difficulty_level
        
        for layer in range(num_layers):
            y_pos = 50 + layer * 50
            # Create V shape
            for i in range(3 + layer):
                left_x = SCREEN_WIDTH//2 - (i + 1) * 40 - layer * 20
                right_x = SCREEN_WIDTH//2 + (i + 1) * 40 + layer * 20
                
                alien_type = random.choice(["basic", "scout", "warrior"])
                aliens.append((left_x, y_pos + i * 15, alien_type))
                if i > 0:  # Don't duplicate center alien
                    aliens.append((right_x, y_pos + i * 15, alien_type))
        
        return aliens
    
    def create_arc_formation(self):
        """Level 3: Arc formation"""
        aliens = []
        num_layers = self.difficulty_level
        
        import math
        for layer in range(num_layers):
            radius = 120 + layer * 30
            center_x = SCREEN_WIDTH // 2
            center_y = 100 + layer * 40
            
            # Create arc from -90 to 90 degrees
            for angle in range(-90, 91, 30):
                rad = math.radians(angle)
                x = center_x + radius * math.cos(rad)
                y = center_y + radius * math.sin(rad) * 0.5  # Flatten the arc
                
                alien_type = random.choice(["basic", "scout", "warrior"])
                aliens.append((x, y, alien_type))
        
        return aliens
    
    def create_triangle_formation(self):
        """Level 4: Triangle formation"""
        aliens = []
        num_layers = self.difficulty_level
        
        for layer in range(num_layers):
            base_y = 50 + layer * 60
            triangle_size = 4 + layer
            
            for row in range(triangle_size):
                y_pos = base_y + row * 30
                aliens_in_row = triangle_size - row
                
                for col in range(aliens_in_row):
                    x_pos = SCREEN_WIDTH//2 - (aliens_in_row - 1) * 25 + col * 50
                    
                    # Commanders at the tip, warriors in middle, scouts at base
                    if row == 0:
                        alien_type = "commander"
                    elif row < triangle_size // 2:
                        alien_type = "warrior"
                    else:
                        alien_type = random.choice(["basic", "scout"])
                    
                    aliens.append((x_pos, y_pos, alien_type))
        
        return aliens
    
    def create_diamond_formation(self):
        """Level 5: Diamond formation"""
        aliens = []
        num_layers = self.difficulty_level
        
        for layer in range(num_layers):
            center_x = SCREEN_WIDTH // 2
            center_y = 80 + layer * 80
            size = 3 + layer
            
            # Top half of diamond
            for row in range(size):
                aliens_in_row = row + 1
                for col in range(aliens_in_row):
                    x_offset = (col - aliens_in_row // 2) * 40
                    y_offset = -row * 25
                    
                    alien_type = "commander" if row == 0 else random.choice(["warrior", "scout"])
                    aliens.append((center_x + x_offset, center_y + y_offset, alien_type))
            
            # Bottom half of diamond
            for row in range(size - 1, 0, -1):
                aliens_in_row = row
                for col in range(aliens_in_row):
                    x_offset = (col - aliens_in_row // 2) * 40
                    y_offset = (size - row) * 25
                    
                    alien_type = random.choice(["basic", "scout"])
                    aliens.append((center_x + x_offset, center_y + y_offset, alien_type))
        
        return aliens
    
    def create_spiral_formation(self):
        """Level 6: Spiral formation"""
        aliens = []
        num_layers = self.difficulty_level
        
        import math
        for layer in range(num_layers):
            center_x = SCREEN_WIDTH // 2
            center_y = 100 + layer * 60
            
            for i in range(8 + layer * 2):
                angle = i * 45 + layer * 30  # Offset each layer
                radius = 20 + i * 8
                
                rad = math.radians(angle)
                x = center_x + radius * math.cos(rad)
                y = center_y + radius * math.sin(rad) * 0.6
                
                alien_type = random.choice(["basic", "scout", "warrior", "commander"])
                aliens.append((x, y, alien_type))
        
        return aliens
    
    def create_cross_formation(self):
        """Level 7: Cross formation"""
        aliens = []
        num_layers = self.difficulty_level
        
        for layer in range(num_layers):
            center_x = SCREEN_WIDTH // 2
            center_y = 80 + layer * 70
            arm_length = 3 + layer
            
            # Horizontal arm
            for i in range(-arm_length, arm_length + 1):
                x = center_x + i * 35
                alien_type = "commander" if i == 0 else "warrior" if abs(i) == 1 else "scout"
                aliens.append((x, center_y, alien_type))
            
            # Vertical arm
            for i in range(-arm_length, arm_length + 1):
                if i != 0:  # Don't duplicate center
                    y = center_y + i * 30
                    alien_type = "warrior" if abs(i) == 1 else "basic"
                    aliens.append((center_x, y, alien_type))
        
        return aliens
    
    def create_wave_formation(self):
        """Level 8: Wave formation"""
        aliens = []
        num_layers = self.difficulty_level
        
        import math
        for layer in range(num_layers):
            y_base = 60 + layer * 50
            
            for x in range(0, SCREEN_WIDTH, 40):
                # Create sine wave
                wave_y = y_base + math.sin(x * 0.02 + layer) * 30
                
                if 50 < x < SCREEN_WIDTH - 50:  # Keep within screen bounds
                    alien_type = random.choice(["basic", "scout", "warrior"])
                    aliens.append((x, wave_y, alien_type))
        
        return aliens
    
    def update(self):
        """Update formation: spawn new aliens and update existing ones"""
        # Spawn new aliens if we have space and aliens in queue
        if (len(self.active_aliens) < self.max_active_aliens and 
            len(self.formation_queue) > 0 and 
            self.spawn_timer <= 0):
            
            x, y, alien_type = self.formation_queue.pop(0)
            new_alien = Alien(x, y, alien_type, self.difficulty_level, 
                            self.visual_assets, self.alien_design_manager, self.difficulty_manager,
                            self.spaceship_designer, self.progressive_spawner)
            self.active_aliens.append(new_alien)
            self.spawn_timer = self.spawn_delay
            print(f"👾 Spawned {alien_type} alien at ({x:.0f}, {y:.0f})")
        
        # Update spawn timer
        if self.spawn_timer > 0:
            self.spawn_timer -= 1
        
        # Update all active aliens
        for alien in self.active_aliens[:]:
            alien.update()
            
            # Remove aliens that reached the bottom or went off screen
            if alien.is_at_bottom() or alien.y > SCREEN_HEIGHT + 50:
                self.active_aliens.remove(alien)
                if alien.is_at_bottom():
                    return "game_over"  # Signal game over
        
        return "continue"
    
    def remove_alien(self, alien_to_remove):
        """Remove an alien from active aliens"""
        if alien_to_remove in self.active_aliens:
            self.active_aliens.remove(alien_to_remove)
    
    def get_shooting_aliens(self):
        """Get all active aliens that can shoot"""
        return self.active_aliens
    
    def draw(self, screen):
        """Draw all active aliens"""
        for alien in self.active_aliens:
            alien.draw(screen)
    
    def is_formation_complete(self):
        """Check if all aliens in formation have been spawned and destroyed"""
        return len(self.formation_queue) == 0 and len(self.active_aliens) == 0
    
    def get_total_aliens_remaining(self):
        """Get total aliens remaining (active + queued)"""
        return len(self.active_aliens) + len(self.formation_queue)

class Game:
    def __init__(self):
        try:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Cosmic Raiders")
            self.clock = pygame.time.Clock()
            self.font_manager = FontManager()
            
            # Enhanced visual and scoring systems
            print("🎮 Initializing Cosmic Raiders enhanced systems...")
            self.high_score_manager = HighScoreManager()
            
            # Initialize visual systems with error handling
            try:
                self.visual_assets = VisualAssets()
                self.alien_design_manager = AlienDesignManager()
                self.difficulty_manager = DifficultyManager()
                self.ui_manager = UIManager(SCREEN_WIDTH, SCREEN_HEIGHT, self.font_manager)
                self.spaceship_designer = SpaceshipDesigner()
                self.progressive_spawner = ProgressiveSpawner(self.difficulty_manager)
            except Exception as e:
                print(f"⚠️ Warning: Some visual systems failed to initialize: {e}")
                # Create minimal fallback systems
                self.visual_assets = None
                self.alien_design_manager = None
                self.difficulty_manager = DifficultyManager()
                self.ui_manager = UIManager(SCREEN_WIDTH, SCREEN_HEIGHT, self.font_manager)
                self.spaceship_designer = None
                self.progressive_spawner = ProgressiveSpawner(self.difficulty_manager)
            
            # Audio and visual feedback systems
            self.audio_manager = AudioManager()
            
        except Exception as e:
            print(f"❌ Critical error during game initialization: {e}")
            print("🔄 Attempting minimal initialization...")
            
            # Minimal fallback initialization
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Cosmic Raiders (Safe Mode)")
            self.clock = pygame.time.Clock()
            self.font_manager = FontManager()
            self.high_score_manager = HighScoreManager()
            self.audio_manager = AudioManager()
            
            # Set safe mode flag
            self.safe_mode = True
        
        # Game state
        self.state = GameState.MENU
        self.score = 0
        self.lives = 3
        self.max_lives = 3
        self.high_score = self.high_score_manager.get_high_score()
        self.wave = 1
        self.difficulty_level = 1
        self.safe_mode = False  # Initialize safe mode flag
        
        # Game over and transition states
        self.game_over_reason = ""
        self.level_complete_timer = 0
        self.level_complete_duration = 180  # 3 seconds at 60 FPS
        self.transition_timer = 0
        self.transition_duration = 120  # 2 seconds at 60 FPS
        
        # Victory system
        self.max_levels = 10  # Victory after completing 10 levels
        self.victory_fade_alpha = 0
        self.victory_fade_speed = 2
        self.victory_music_played = False
        
        # Credits system
        self.credits_scroll_y = SCREEN_HEIGHT
        self.credits_scroll_speed = 1.0
        self.credits_paused = False
        self.credits_fade_alpha = 0
        self.credits_fade_speed = 3
        self.credits_content = self._create_credits_content()
        
        # Performance optimization
        self.background_cache = None
        self.menu_cache = None
        self.last_state = None
        self.needs_redraw = True
        
        # Pause system
        self.previous_state = None  # Store state before pausing
        
        # Player hit feedback
        self.player_hit_timer = 0
        self.player_hit_duration = 30  # frames to show hit effect
        self.player_invulnerable_timer = 0
        self.player_invulnerable_duration = 60  # frames of invulnerability after hit
        
        # Initialize game objects with enhanced visuals and progressive spawning
        self.player = Player(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 50, self.visual_assets)
        self.player_bullets = []  # Multiple bullets allowed
        self.alien_bullets = []
        self.cosmic_formation = CosmicFormation(self.difficulty_level, self.visual_assets, 
                                              self.alien_design_manager, self.difficulty_manager,
                                              self.spaceship_designer, self.progressive_spawner)
        self.hit_effects = []  # Visual effects for hits
        
        # Shooting mechanics - Fast and responsive
        self.last_shot_time = 0
        self.shot_cooldown = 150  # Minimal delay (150ms) for responsive shooting
        
        # Menu selection
        self.menu_selection = 0
        self.menu_options = ["START GAME", "CREDITS", "QUIT"]
        
    def handle_input(self):
        """Handle player input based on game state"""
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        
        if self.state == GameState.MENU:
            # Menu navigation is handled in event loop
            pass
        elif self.state == GameState.PLAYING:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.move_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.move_right()
            
            # Fast, responsive shooting system
            if (keys[pygame.K_SPACE] and 
                current_time - self.last_shot_time > self.shot_cooldown):
                self.shoot_player_bullet()
                self.last_shot_time = current_time
            
    def shoot_player_bullet(self):
        """Create multiple bullets from player position - fast and responsive"""
        bullet_x = self.player.x + self.player.width // 2 - 2
        bullet_y = self.player.y
        self.player_bullets.append(Bullet(bullet_x, bullet_y, 1, 1.0, self.visual_assets))
        
        # Play shoot sound immediately without visual feedback
        self.audio_manager.play_sound('player_shoot')
        
        print(f"🔫 Bullet fired! ({len(self.player_bullets)} bullets active)")
        
    def shoot_alien_bullet(self, alien):
        """Create a bullet from alien position with dynamic speed"""
        bullet_x = alien.x + alien.width // 2 - 2
        bullet_y = alien.y + alien.height
        speed_multiplier = 1.0 + (self.difficulty_level - 1) * 0.1  # Slight speed increase per level
        self.alien_bullets.append(Bullet(bullet_x, bullet_y, -1, speed_multiplier, self.visual_assets))
        
    def update_cosmic_formation(self):
        """Update cosmic formation and handle alien shooting"""
        result = self.cosmic_formation.update()
        
        # Check if any alien reached the bottom
        if result == "game_over":
            self.state = GameState.GAME_OVER
            self.game_over_reason = "Cosmic Raiders reached Earth!"
            if self.score > self.high_score:
                self.high_score = self.score
            print("💀 Game Over: Cosmic Raiders reached the bottom!")
            return
        
        # Handle alien shooting
        shooting_aliens = self.cosmic_formation.get_shooting_aliens()
        for alien in shooting_aliens:
            if alien.should_shoot():
                self.shoot_alien_bullet(alien)
                
    def update_bullets(self):
        """Update all bullets and remove off-screen ones"""
        # Update player bullets (multiple bullets system)
        for bullet in self.player_bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.player_bullets.remove(bullet)
                
        # Update alien bullets
        for bullet in self.alien_bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.alien_bullets.remove(bullet)
                
    def update_effects(self):
        """Update visual effects and player hit timers"""
        # Update hit effects
        for effect in self.hit_effects[:]:
            if not effect.update():
                self.hit_effects.remove(effect)
        
        # Update player hit feedback timer
        if self.player_hit_timer > 0:
            self.player_hit_timer -= 1
        
        # Update player invulnerability timer
        if self.player_invulnerable_timer > 0:
            self.player_invulnerable_timer -= 1
    
    def update_level_transitions(self):
        """Handle level complete and transition states"""
        if self.state == GameState.LEVEL_COMPLETE:
            self.level_complete_timer -= 1
            if self.level_complete_timer <= 0:
                # Start level transition
                self.state = GameState.LEVEL_TRANSITION
                self.transition_timer = self.transition_duration
                
                # Advance to next level
                self.wave += 1
                self.difficulty_level += 1
                
                # Life management options:
                # Option 1: Reset lives to 3 each level (easier)
                self.lives = self.max_lives
                
                # Option 2: Keep current lives but add bonus life every few levels (balanced)
                # if self.difficulty_level % 3 == 0 and self.lives < self.max_lives:
                #     self.lives += 1
                #     print(f"🎁 Bonus life! Lives: {self.lives}")
                
                # Create new cosmic formation for next level
                self.cosmic_formation = CosmicFormation(self.difficulty_level, self.visual_assets,
                                                      self.alien_design_manager, self.difficulty_manager,
                                                      self.spaceship_designer, self.progressive_spawner)
                
                # Play level advance sound immediately
                self.audio_manager.play_sound('level_advance')
                
                print(f"🌊 Advancing to Level {self.difficulty_level}! Lives reset to {self.lives}")
                
        elif self.state == GameState.LEVEL_TRANSITION:
            self.transition_timer -= 1
            if self.transition_timer <= 0:
                # Resume gameplay
                self.state = GameState.PLAYING
                print(f"🚀 Level {self.difficulty_level} begins!")
                
    def check_collisions(self):
        """Check all collision scenarios with enhanced damage system"""
        # Player bullets vs aliens (multiple bullets system with health)
        for bullet in self.player_bullets[:]:
            for alien in self.cosmic_formation.active_aliens[:]:
                if bullet.rect.colliderect(alien.rect):
                    # Remove bullet first
                    self.player_bullets.remove(bullet)
                    
                    # Alien takes damage
                    if alien.take_damage():
                        # Alien destroyed
                        self.score += alien.points
                        print(f"💥 {alien.alien_type.capitalize()} destroyed! +{alien.points} points (Score: {self.score}) [{len(self.player_bullets)} bullets remaining]")
                        
                        # Create explosion effect
                        effect_x = alien.x + alien.width // 2
                        effect_y = alien.y + alien.height // 2
                        self.hit_effects.append(HitEffect(effect_x, effect_y, "explosion", self.visual_assets))
                        
                        # Play destruction sound immediately
                        self.audio_manager.play_sound('alien_destroy')
                        
                        # Remove alien
                        self.cosmic_formation.active_aliens.remove(alien)
                    else:
                        # Alien damaged but not destroyed
                        print(f"🎯 {alien.alien_type.capitalize()} hit! Health: {alien.health}/{alien.max_health}")
                        
                        # Play hit sound immediately
                        self.audio_manager.play_sound('alien_hit')
                    
                    break
                    
        # Alien bullets vs player (with invulnerability frames)
        if self.player_invulnerable_timer <= 0:  # Only check if not invulnerable
            for bullet in self.alien_bullets[:]:
                if bullet.rect.colliderect(self.player.rect):
                    self.alien_bullets.remove(bullet)
                    self.lives -= 1
                    
                    # Activate hit feedback and invulnerability
                    self.player_hit_timer = self.player_hit_duration
                    self.player_invulnerable_timer = self.player_invulnerable_duration
                    
                    # Create hit effect on player
                    effect_x = self.player.x + self.player.width // 2
                    effect_y = self.player.y + self.player.height // 2
                    self.hit_effects.append(HitEffect(effect_x, effect_y, "explosion", self.visual_assets))
                    
                    # Play player hit sound immediately
                    self.audio_manager.play_sound('player_hit')
                    
                    print(f"⚠️ PLAYER HIT! Lives remaining: {self.lives}")
                    break
                
    def check_game_over_conditions(self):
        """Check if game should end or level should advance"""
        # Game over is handled in update_cosmic_formation for alien invasion
        
        # Check if formation is complete (level complete)
        if self.cosmic_formation.is_formation_complete():
            # Check for victory condition (completed max levels)
            if self.difficulty_level >= self.max_levels:
                self.state = GameState.VICTORY
                self.victory_fade_alpha = 0
                self.victory_music_played = False
                
                # Update high score if needed
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.high_score_manager.save_high_score(self.score, self.difficulty_level)
                
                print(f"🏆 VICTORY! Completed all {self.max_levels} levels! Final Score: {self.score}")
                return
            
            # Regular level completion
            self.state = GameState.LEVEL_COMPLETE
            self.level_complete_timer = self.level_complete_duration
            
            # Play level complete sound immediately
            self.audio_manager.play_sound('level_complete')
            
            print(f"🎉 Level {self.difficulty_level} completed! Score: {self.score}")
            return
            
        # Check if player died
        if self.lives <= 0:
            self.state = GameState.GAME_OVER
            self.game_over_reason = "No lives remaining!"
            if self.score > self.high_score:
                self.high_score = self.score
            
            # Play game over sound and stop music immediately
            self.audio_manager.stop_music()
            self.audio_manager.play_sound('game_over')
            
            print("💀 Game Over: No lives remaining!")
            
    def draw_background(self):
        """Draw enhanced space background"""
        bg_sprite = self.visual_assets.get_sprite('background')
        if bg_sprite:
            self.screen.blit(bg_sprite, (0, 0))
        else:
            # Fallback to gradient
            self.screen.fill(BLACK)
    
    def draw_menu_background(self):
        """Draw enhanced background specifically for menu with animated elements"""
        # Base background
        self.draw_background()
        
        # Add animated twinkling stars for menu
        import math, random
        time_offset = pygame.time.get_ticks() * 0.001
        
        # Create some animated stars
        random.seed(42)  # Fixed seed for consistent star positions
        for i in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            
            # Twinkling effect
            alpha = int(100 + 155 * abs(math.sin(time_offset * 2 + i * 0.5)))
            star_color = (255, 255, 255, alpha)
            
            # Different star sizes
            if i % 3 == 0:
                pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 2)
            elif i % 3 == 1:
                pygame.draw.circle(self.screen, (200, 200, 255), (x, y), 1)
            else:
                self.screen.set_at((x, y), (255, 255, 200))
    
    def draw_menu(self):
        """Draw the enhanced main menu with retro effects"""
        # Enhanced background with animated stars
        self.draw_menu_background()
        
        # Add some visual flair with animated elements
        import math
        time_offset = pygame.time.get_ticks() * 0.003  # Slow animation
        
        # High score display (moved to top to avoid overlap)
        current_high_score = self.high_score_manager.get_high_score()
        if current_high_score > 0:
            # High score with glow effect
            high_score_text, high_score_rect = self.font_manager.render_text(
                f"HIGH SCORE: {current_high_score:,}", 'medium', GREEN, (SCREEN_WIDTH//2, 40)
            )
            # Create glow effect
            glow_surface = pygame.Surface((high_score_rect.width + 10, high_score_rect.height + 10), pygame.SRCALPHA)
            glow_text, _ = self.font_manager.render_text(f"HIGH SCORE: {current_high_score:,}", 'medium', (0, 255, 0, 100))
            glow_surface.blit(glow_text, (5, 5))
            self.screen.blit(glow_surface, (high_score_rect.x - 5, high_score_rect.y - 5))
            self.screen.blit(high_score_text, high_score_rect)
            
            # High score details
            high_score_date = self.high_score_manager.get_high_score_date()
            high_score_level = self.high_score_manager.get_high_score_level()
            details_text, details_rect = self.font_manager.render_text(
                f"Level {high_score_level} • {high_score_date}", 'small', GRAY, (SCREEN_WIDTH//2, 65)
            )
            self.screen.blit(details_text, details_rect)
        
        # Main title with enhanced effects
        title_y = 140
        
        # Title shadow/outline effect
        for offset_x, offset_y in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
            shadow_text, shadow_rect = self.font_manager.render_text(
                "COSMIC RAIDERS", 'title', (50, 50, 50), (SCREEN_WIDTH//2 + offset_x, title_y + offset_y)
            )
            self.screen.blit(shadow_text, shadow_rect)
        
        # Main title with color cycling
        title_color_r = int(255 * (0.8 + 0.2 * math.sin(time_offset)))
        title_color_g = int(255 * (0.8 + 0.2 * math.sin(time_offset + 2)))
        title_color_b = int(255 * (0.9 + 0.1 * math.sin(time_offset + 4)))
        title_color = (title_color_r, title_color_g, title_color_b)
        
        title_text, title_rect = self.font_manager.render_text(
            "COSMIC RAIDERS", 'title', title_color, (SCREEN_WIDTH//2, title_y)
        )
        self.screen.blit(title_text, title_rect)
        
        # Subtitle with pulsing effect
        subtitle_alpha = int(200 + 55 * math.sin(time_offset * 2))
        subtitle_color = (*CYAN[:3], subtitle_alpha) if len(CYAN) == 4 else CYAN
        subtitle_text, subtitle_rect = self.font_manager.render_text(
            "DYNAMIC FORMATION EDITION", 'medium', CYAN, (SCREEN_WIDTH//2, 190)
        )
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Enhanced developer branding with better visibility
        branding_y = 220
        
        # Branding background for better readability
        branding_bg = pygame.Surface((400, 35), pygame.SRCALPHA)
        branding_bg.fill((0, 0, 0, 120))  # Semi-transparent black background
        branding_bg_rect = branding_bg.get_rect(center=(SCREEN_WIDTH//2, branding_y))
        self.screen.blit(branding_bg, branding_bg_rect)
        
        # Branding text with enhanced styling
        branding_text, branding_rect = self.font_manager.render_text(
            "By: Vishnu Anurag Thonukunoori", 'medium', WHITE, (SCREEN_WIDTH//2, branding_y)  # Changed to medium size and white
        )
        self.screen.blit(branding_text, branding_rect)
        
        # Menu options with enhanced spacing
        menu_start_y = 280  # Moved further down to accommodate branding
        for i, option in enumerate(self.menu_options):
            # Menu option background for selected item
            if i == self.menu_selection:
                option_bg = pygame.Surface((200, 40), pygame.SRCALPHA)
                option_bg.fill((255, 255, 0, 30))  # Yellow highlight
                option_bg_rect = option_bg.get_rect(center=(SCREEN_WIDTH//2, menu_start_y + i * 60))
                self.screen.blit(option_bg, option_bg_rect)
            
            color = YELLOW if i == self.menu_selection else WHITE
            option_text, option_rect = self.font_manager.render_text(
                option, 'large', color, (SCREEN_WIDTH//2, menu_start_y + i * 60)
            )
            self.screen.blit(option_text, option_rect)
            
            # Enhanced selection indicator with animation using ASCII characters
            if i == self.menu_selection:
                indicator_offset = int(3 * math.sin(time_offset * 8))  # Animated indicator
                indicator_text, indicator_rect = self.font_manager.render_text(
                    ">>", 'large', YELLOW, (option_rect.left - 60 + indicator_offset, option_rect.centery)
                )
                self.screen.blit(indicator_text, indicator_rect)
        
        # Instructions with better positioning
        instructions_start_y = 450  # Moved down to accommodate menu changes
        instructions = [
            "USE ARROW KEYS TO NAVIGATE",
            "PRESS ENTER TO SELECT",
            "PRESS C FOR CREDITS",
            "WASD OR ARROWS TO MOVE",
            "SPACEBAR FOR RAPID FIRE"
        ]
        
        # Instructions background
        instructions_bg = pygame.Surface((500, 140), pygame.SRCALPHA)
        instructions_bg.fill((0, 0, 0, 80))
        instructions_bg_rect = instructions_bg.get_rect(center=(SCREEN_WIDTH//2, instructions_start_y + 60))
        self.screen.blit(instructions_bg, instructions_bg_rect)
        
        for i, instruction in enumerate(instructions):
            inst_text, inst_rect = self.font_manager.render_text(
                instruction, 'small', GRAY, (SCREEN_WIDTH//2, instructions_start_y + i * 25)
            )
            self.screen.blit(inst_text, inst_rect)
    
    def draw_game_ui(self):
        """Draw compact, non-intrusive game UI with progressive info"""
        # Prepare game data for UI manager
        formation_names = {1: "LINE", 2: "V-SHAPE", 3: "ARC", 4: "TRIANGLE", 5: "DIAMOND", 6: "SPIRAL", 7: "CROSS", 8: "WAVE"}
        formation_name = formation_names.get(((self.difficulty_level - 1) % 8) + 1, "CUSTOM")
        
        # Get progressive spawning info
        max_aliens = self.cosmic_formation.max_active_aliens if hasattr(self.cosmic_formation, 'max_active_aliens') else 3
        
        game_data = {
            'lives': self.lives,
            'level': self.difficulty_level,
            'wave': self.wave,
            'score': self.score,
            'high_score': self.high_score,
            'active_aliens': len(self.cosmic_formation.active_aliens),
            'remaining_aliens': self.cosmic_formation.get_total_aliens_remaining(),
            'total_aliens': len(self.cosmic_formation.formation_queue) + len(self.cosmic_formation.active_aliens),
            'formation_name': formation_name,
            'active_bullets': len(self.player_bullets),
            'max_aliens': max_aliens,
            'in_game': True,
            'show_progress': True,
            'show_stats': len(self.player_bullets) > 3  # Only show bullet count when many active
        }
        
        # Use compact UI manager - it handles all UI elements including high score
        self.ui_manager.draw_compact_hud(self.screen, game_data)
        
        # Player status (only additional UI element not handled by UI manager)
        if self.player_invulnerable_timer > 0:
            status_text, _ = self.font_manager.render_text("INVULNERABLE", 'small', YELLOW)
            self.screen.blit(status_text, (10, 265))
        
        # Instructions at bottom (updated to include mute key)
        instruction_text, instruction_rect = self.font_manager.render_text(
            "SPACE: RAPID FIRE  |  ESC: PAUSE  |  M: MUTE", 'small', GRAY, (SCREEN_WIDTH//2, SCREEN_HEIGHT - 20)
        )
        self.screen.blit(instruction_text, instruction_rect)
    
    def draw_level_complete(self):
        """Draw level complete screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Level Complete title
        complete_text, complete_rect = self.font_manager.render_text(
            "LEVEL COMPLETE!", 'title', GREEN, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100)
        )
        self.screen.blit(complete_text, complete_rect)
        
        # Current level info
        level_text, level_rect = self.font_manager.render_text(
            f"Level {self.difficulty_level} Cleared!", 'large', WHITE, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40)
        )
        self.screen.blit(level_text, level_rect)
        
        # Score info
        score_text, score_rect = self.font_manager.render_text(
            f"Score: {self.score}", 'large', YELLOW, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        )
        self.screen.blit(score_text, score_rect)
        
        # Next level preview
        next_formation_names = {1: "LINE", 2: "V-SHAPE", 3: "ARC", 4: "TRIANGLE", 5: "DIAMOND", 6: "SPIRAL", 7: "CROSS", 8: "WAVE"}
        next_formation_index = ((self.difficulty_level) % 8) + 1
        next_formation = next_formation_names.get(next_formation_index, "CUSTOM")
        next_level_text, next_level_rect = self.font_manager.render_text(
            f"Next: Level {self.difficulty_level + 1} ({next_formation} Formation)", 'medium', CYAN, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40)
        )
        self.screen.blit(next_level_text, next_level_rect)
        
        # Countdown
        seconds_left = (self.level_complete_timer // 60) + 1
        countdown_text, countdown_rect = self.font_manager.render_text(
            f"Advancing in {seconds_left}...", 'medium', WHITE, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80)
        )
        self.screen.blit(countdown_text, countdown_rect)
    
    def draw_level_complete(self):
        """Draw level complete screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Level Complete title
        complete_text, complete_rect = self.font_manager.render_text(
            "LEVEL COMPLETE!", 'title', GREEN, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100)
        )
        self.screen.blit(complete_text, complete_rect)
        
        # Current level info
        level_text, level_rect = self.font_manager.render_text(
            f"Level {self.difficulty_level} Cleared!", 'large', WHITE, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40)
        )
        self.screen.blit(level_text, level_rect)
        
        # Score info
        score_text, score_rect = self.font_manager.render_text(
            f"Score: {self.score}", 'large', YELLOW, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        )
        self.screen.blit(score_text, score_rect)
        
        # Next level preview
        next_formation_names = {1: "LINE", 2: "V-SHAPE", 3: "ARC", 4: "TRIANGLE", 5: "DIAMOND", 6: "SPIRAL", 7: "CROSS", 8: "WAVE"}
        next_formation_index = ((self.difficulty_level) % 8) + 1
        next_formation = next_formation_names.get(next_formation_index, "CUSTOM")
        next_level_text, next_level_rect = self.font_manager.render_text(
            f"Next: Level {self.difficulty_level + 1} ({next_formation} Formation)", 'medium', CYAN, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40)
        )
        self.screen.blit(next_level_text, next_level_rect)
        
        # Countdown
        seconds_left = (self.level_complete_timer // 60) + 1
        countdown_text, countdown_rect = self.font_manager.render_text(
            f"Advancing in {seconds_left}...", 'medium', WHITE, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80)
        )
        self.screen.blit(countdown_text, countdown_rect)
    
    def draw_level_transition(self):
        """Draw enhanced level transition screen"""
        # Get level configuration
        formation_names = {1: "LINE", 2: "V-SHAPE", 3: "ARC", 4: "TRIANGLE", 5: "DIAMOND", 6: "SPIRAL", 7: "CROSS", 8: "WAVE"}
        formation_name = formation_names.get(((self.difficulty_level - 1) % 8) + 1, "CUSTOM")
        
        difficulty_summary = self.difficulty_manager.get_level_summary(self.difficulty_level)
        
        # Add additional info to difficulty summary
        difficulty_summary['lives'] = self.lives
        difficulty_summary['horizontal_speed'] = f"{1.0 + (self.difficulty_level - 1) * 0.2:.1f}x"
        difficulty_summary['vertical_speed'] = "1.0x (Constant)"
        
        level_data = {
            'level': self.difficulty_level,
            'formation_name': formation_name,
            'difficulty_summary': difficulty_summary
        }
        
        # Use UI manager for consistent styling - it handles all the text rendering
        self.ui_manager.draw_level_transition(self.screen, level_data)
        
    def draw_game_over(self):
        """Draw enhanced game over screen with high score system"""
        # Full overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over title
        game_over_text, game_over_rect = self.font_manager.render_text(
            "GAME OVER", 'title', RED, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 150)
        )
        self.screen.blit(game_over_text, game_over_rect)
        
        # Game over reason
        reason_text, reason_rect = self.font_manager.render_text(
            self.game_over_reason, 'medium', WHITE, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 110)
        )
        self.screen.blit(reason_text, reason_rect)
        
        # Check and update high score
        is_new_high = self.high_score_manager.update_if_high_score(self.score, self.difficulty_level)
        
        # Final score
        final_score_text, final_score_rect = self.font_manager.render_text(
            f"FINAL SCORE: {self.score:,}", 'large', WHITE, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60)
        )
        self.screen.blit(final_score_text, final_score_rect)
        
        # High score information
        if is_new_high:
            new_high_text, new_high_rect = self.font_manager.render_text(
                "🎉 NEW HIGH SCORE! 🎉", 'large', GREEN, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20)
            )
            self.screen.blit(new_high_text, new_high_rect)
            
            # Update our local high score for display
            self.high_score = self.score
        else:
            high_score_text, high_score_rect = self.font_manager.render_text(
                f"HIGH SCORE: {self.high_score:,}", 'large', YELLOW, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20)
            )
            self.screen.blit(high_score_text, high_score_rect)
        
        # High score details
        high_score_date = self.high_score_manager.get_high_score_date()
        high_score_level = self.high_score_manager.get_high_score_level()
        details_text, details_rect = self.font_manager.render_text(
            f"Best: Level {high_score_level} on {high_score_date}", 'medium', GRAY, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20)
        )
        self.screen.blit(details_text, details_rect)
        
        # Level reached
        level_text, level_rect = self.font_manager.render_text(
            f"LEVEL REACHED: {self.difficulty_level}", 'medium', CYAN, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)
        )
        self.screen.blit(level_text, level_rect)
        
        # Controls
        controls = [
            "PRESS R TO RESTART FROM LEVEL 1",
            "PRESS SPACE TO RETURN TO MENU", 
            "PRESS ESC TO QUIT"
        ]
        
        for i, control in enumerate(controls):
            color = GREEN if i == 0 else YELLOW if i == 1 else GRAY
            control_text, control_rect = self.font_manager.render_text(
                control, 'small', color, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100 + i * 25)
            )
            self.screen.blit(control_text, control_rect)
    
    def draw_victory_screen(self):
        """Draw victory screen for completing all levels"""
        # Gradually fade background to black
        if self.victory_fade_alpha < 220:
            self.victory_fade_alpha += self.victory_fade_speed
        
        # Play victory music once
        if not self.victory_music_played:
            self.audio_manager.stop_music()
            # Play victory sound effect
            self.audio_manager.play_sound('victory_sound')
            self.victory_music_played = True
        
        # Faded background overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(self.victory_fade_alpha)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Victory title with cosmic theme
        victory_text, victory_rect = self.font_manager.render_text(
            "YOU DEFEATED THE", 'title', YELLOW, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 180)
        )
        self.screen.blit(victory_text, victory_rect)
        
        cosmic_text, cosmic_rect = self.font_manager.render_text(
            "COSMIC RAIDERS!", 'title', GREEN, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 140)
        )
        self.screen.blit(cosmic_text, cosmic_rect)
        
        # Victory subtitle
        subtitle_text, subtitle_rect = self.font_manager.render_text(
            f"All {self.max_levels} Levels Conquered!", 'large', CYAN, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 90)
        )
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Final score
        final_score_text, final_score_rect = self.font_manager.render_text(
            f"FINAL SCORE: {self.score:,}", 'large', WHITE, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40)
        )
        self.screen.blit(final_score_text, final_score_rect)
        
        # High score information
        if self.score >= self.high_score:
            new_high_text, new_high_rect = self.font_manager.render_text(
                "🏆 ULTIMATE HIGH SCORE! 🏆", 'large', YELLOW, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            )
            self.screen.blit(new_high_text, new_high_rect)
        else:
            high_score_text, high_score_rect = self.font_manager.render_text(
                f"HIGH SCORE: {self.high_score:,}", 'large', YELLOW, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            )
            self.screen.blit(high_score_text, high_score_rect)
        
        # Victory achievement
        achievement_text, achievement_rect = self.font_manager.render_text(
            "GALACTIC DEFENDER ACHIEVEMENT UNLOCKED", 'medium', GREEN, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40)
        )
        self.screen.blit(achievement_text, achievement_rect)
        
        # Controls
        controls = [
            "PRESS R TO PLAY AGAIN",
            "PRESS SPACE TO RETURN TO MENU"
        ]
        
        for i, control in enumerate(controls):
            color = GREEN if i == 0 else YELLOW
            control_text, control_rect = self.font_manager.render_text(
                control, 'medium', color, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 90 + i * 30)
            )
            self.screen.blit(control_text, control_rect)
    
    def draw_credits_screen(self):
        """Draw scrolling credits screen with fade effects"""
        # Fade in effect
        if self.credits_fade_alpha < 255:
            self.credits_fade_alpha += self.credits_fade_speed
            self.credits_fade_alpha = min(255, self.credits_fade_alpha)
        
        # Dark space background with fade
        background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background_surface.fill((5, 5, 15))  # Very dark blue
        background_surface.set_alpha(self.credits_fade_alpha)
        self.screen.blit(background_surface, (0, 0))
        
        # Add some stars to the background
        if self.credits_fade_alpha > 100:
            for i in range(50):
                star_x = (i * 137) % SCREEN_WIDTH
                star_y = (i * 211 + int(self.credits_scroll_y * 0.1)) % SCREEN_HEIGHT
                star_brightness = min(255, self.credits_fade_alpha - 50)
                star_color = (star_brightness, star_brightness, star_brightness)
                pygame.draw.circle(self.screen, star_color, (star_x, star_y), 1)
        
        # Draw credits text
        current_y = self.credits_scroll_y
        
        for text, size, spacing in self.credits_content:
            if text:  # Only draw non-empty text
                # Choose color based on content
                if size == "huge":
                    color = YELLOW
                elif size == "large":
                    color = GREEN
                elif "🚀" in text or "👾" in text or "🏆" in text or "⭐" in text:
                    color = CYAN
                elif text.startswith("Press"):
                    color = WHITE if (pygame.time.get_ticks() // 500) % 2 else GRAY
                else:
                    color = WHITE
                
                # Render text with fade
                text_surface, text_rect = self.font_manager.render_text(
                    text, size, color, (SCREEN_WIDTH // 2, current_y)
                )
                
                # Apply fade alpha
                if self.credits_fade_alpha < 255:
                    text_surface.set_alpha(self.credits_fade_alpha)
                
                # Only draw if visible on screen
                if -50 < current_y < SCREEN_HEIGHT + 50:
                    self.screen.blit(text_surface, text_rect)
            
            current_y += spacing
        
        # Update scroll position if not paused
        if not self.credits_paused:
            self.credits_scroll_y -= self.credits_scroll_speed
            
            # Reset scroll when credits finish
            total_height = sum(spacing for _, _, spacing in self.credits_content)
            if self.credits_scroll_y < -total_height:
                self.credits_scroll_y = SCREEN_HEIGHT
        
        # Draw pause indicator if paused
        if self.credits_paused:
            pause_text, pause_rect = self.font_manager.render_text(
                "PAUSED - Press P to continue", 'small', YELLOW, 
                (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)
            )
            self.screen.blit(pause_text, pause_rect)
        
    def restart_game(self):
        """Reset game to initial state (Level 1)"""
        self.state = GameState.PLAYING
        self.score = 0
        self.lives = self.max_lives
        self.wave = 1
        self.difficulty_level = 1
        self.game_over_reason = ""
        self.level_complete_timer = 0
        self.transition_timer = 0
        
        # Reset victory state
        self.victory_fade_alpha = 0
        self.victory_music_played = False
        
        self.player = Player(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 50, self.visual_assets)
        self.player_bullets = []  # Reset multiple bullets
        self.alien_bullets = []
        self.cosmic_formation = CosmicFormation(self.difficulty_level, self.visual_assets,
                                              self.alien_design_manager, self.difficulty_manager,
                                              self.spaceship_designer, self.progressive_spawner)  # Create new cosmic formation
        self.hit_effects = []  # Clear effects
        self.last_shot_time = 0  # Reset shooting timer
        self.player_hit_timer = 0
        self.player_invulnerable_timer = 0
        
        # Start game music
        self.audio_manager.play_music('game_music')
        print(f"🔄 Game restarted! Starting Level 1 with {self.lives} lives")
    
    def start_credits(self):
        """Start the credits screen"""
        self.state = GameState.CREDITS
        self.credits_scroll_y = SCREEN_HEIGHT
        self.credits_fade_alpha = 0
        self.credits_paused = False
        
        # Play ambient menu music for credits
        self.audio_manager.play_music('menu')
        print("🎬 Starting credits screen")
    
    def exit_credits(self):
        """Exit credits and return to menu"""
        self.state = GameState.MENU
        self.credits_fade_alpha = 0
        print("🔙 Returning to main menu")
        
    def _create_credits_content(self):
        """Create the credits content with proper formatting"""
        credits = [
            ("", "huge", 60),  # Spacer
            ("COSMIC RAIDERS", "huge", 80),
            ("", "medium", 80),
            
            ("CREATED BY", "large", 60),
            ("Vishnu Anurag Thonukunoori", "medium", 80),
            ("", "medium", 60),
            
            ("POWERED BY", "large", 60),
            ("Python 3.12", "medium", 40),
            ("Pygame 2.5.2", "medium", 80),
            ("", "medium", 60),
            
            ("TYPOGRAPHY", "large", 60),
            ("Pixeled.ttf", "medium", 40),
            ("Retro Pixel Font", "small", 80),
            ("", "medium", 60),
            
            ("AUDIO & MUSIC", "large", 60),
            ("Procedurally Generated", "medium", 40),
            ("Dynamic Sound Effects", "small", 40),
            ("Ambient Space Music", "small", 80),
            ("", "medium", 60),
            
            ("VISUAL ASSETS", "large", 60),
            ("Custom Pixel Art", "medium", 40),
            ("Procedural Spaceships", "small", 40),
            ("Dynamic Backgrounds", "small", 80),
            ("", "medium", 60),
            
            ("GAME FEATURES", "large", 60),
            ("20 Unique Spaceship Designs", "small", 30),
            ("Progressive Difficulty System", "small", 30),
            ("8 Formation Patterns", "small", 30),
            ("10 Challenging Levels", "small", 30),
            ("High Score Persistence", "small", 80),
            ("", "medium", 60),
            
            ("SPECIAL THANKS", "large", 60),
            ("Amazon Web Services", "medium", 40),
            ("Python Community", "medium", 40),
            ("Pygame Developers", "medium", 40),
            ("Retro Gaming Enthusiasts", "medium", 40),
            ("Space Invaders Legacy", "medium", 80),
            ("", "medium", 100),
            
            ("ACHIEVEMENTS UNLOCKED", "large", 60),
            ("🚀 Galactic Defender", "medium", 40),
            ("👾 Alien Hunter", "medium", 40),
            ("🏆 High Score Master", "medium", 40),
            ("⭐ Cosmic Champion", "medium", 80),
            ("", "medium", 100),
            
            ("Thank you for playing!", "large", 80),
            ("", "medium", 60),
            ("Press SPACE to return to menu", "medium", 100),
            ("", "huge", 200),  # Final spacer
        ]
        
        return credits
    
    def restart_level(self):
        """Restart current level while keeping score and progress"""
        self.state = GameState.PLAYING
        self.previous_state = None
        self.lives = self.max_lives  # Reset lives for the level
        self.player = Player(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 50, self.visual_assets)
        self.player_bullets = []  # Clear bullets
        self.alien_bullets = []
        self.cosmic_formation = CosmicFormation(self.difficulty_level, self.visual_assets,
                                              self.alien_design_manager, self.difficulty_manager,
                                              self.spaceship_designer, self.progressive_spawner)  # Recreate formation for current level
        self.hit_effects = []  # Clear effects
        self.last_shot_time = 0  # Reset shooting timer
        self.player_hit_timer = 0
        self.player_invulnerable_timer = 0
        print(f"🔄 Level {self.difficulty_level} restarted! Lives reset to {self.lives}")
    
    def start_game(self):
        """Start a new game from menu"""
        self.restart_game()
        self.state = GameState.PLAYING
        # Start game music
        self.audio_manager.play_music('game')
        
    def run(self):
        """Main game loop"""
        running = True
        
        # Start menu music
        self.audio_manager.play_music('menu')
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # Global mute key (works in any state)
                    if event.key == pygame.K_m:
                        self.audio_manager.toggle_mute()
                    
                    elif event.key == pygame.K_ESCAPE:
                        if self.state == GameState.PLAYING:
                            # Pause the game and music
                            self.previous_state = GameState.PLAYING
                            self.state = GameState.PAUSED
                            self.audio_manager.pause_music()
                        elif self.state == GameState.PAUSED:
                            # Resume the game and music
                            self.state = self.previous_state
                            self.previous_state = None
                            self.audio_manager.resume_music()
                        elif self.state == GameState.GAME_OVER:
                            running = False  # Quit from game over
                        elif self.state == GameState.VICTORY:
                            running = False  # Quit from victory screen
                        elif self.state == GameState.MENU:
                            running = False
                    
                    # Pause screen controls
                    elif self.state == GameState.PAUSED:
                        if event.key == pygame.K_p:
                            # Resume with P key
                            self.state = self.previous_state
                            self.previous_state = None
                            self.audio_manager.resume_music()
                        elif event.key == pygame.K_r:
                            # Restart level
                            self.restart_level()
                        elif event.key == pygame.K_SPACE:
                            # Quit to menu
                            self.state = GameState.MENU
                            self.previous_state = None
                            self.audio_manager.play_music('menu')
                    
                    # Menu navigation
                    elif self.state == GameState.MENU:
                        if event.key == pygame.K_UP:
                            self.menu_selection = (self.menu_selection - 1) % len(self.menu_options)
                        elif event.key == pygame.K_DOWN:
                            self.menu_selection = (self.menu_selection + 1) % len(self.menu_options)
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            if self.menu_selection == 0:  # START GAME
                                self.start_game()
                            elif self.menu_selection == 1:  # CREDITS
                                self.start_credits()
                            elif self.menu_selection == 2:  # QUIT
                                running = False
                        elif event.key == pygame.K_c:  # Direct credits shortcut
                            self.start_credits()
                    
                    # Credits screen controls
                    elif self.state == GameState.CREDITS:
                        if event.key == pygame.K_SPACE:
                            self.exit_credits()
                        elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                            self.credits_paused = not self.credits_paused
                    
                    # Game over screen controls
                    elif self.state == GameState.GAME_OVER:
                        if event.key == pygame.K_r:
                            self.restart_game()
                        elif event.key == pygame.K_SPACE:
                            self.state = GameState.MENU
                    
                    # Victory screen controls
                    elif self.state == GameState.VICTORY:
                        if event.key == pygame.K_r:
                            self.restart_game()
                        elif event.key == pygame.K_SPACE:
                            self.state = GameState.MENU
                            self.audio_manager.play_music('menu_music')
                        
            # Update game logic
            if self.state == GameState.PLAYING:
                self.handle_input()
                self.update_cosmic_formation()
                self.update_bullets()
                self.update_effects()  # Update visual effects
                self.check_collisions()
                self.check_game_over_conditions()
            elif self.state in [GameState.LEVEL_COMPLETE, GameState.LEVEL_TRANSITION]:
                # Handle level transitions
                self.update_level_transitions()
                # Still update effects during transitions
                self.update_effects()
            elif self.state == GameState.PAUSED:
                # Only update effects when paused, not game logic
                pass
                
            # Draw enhanced background
            self.draw_background()
            
            # Draw based on game state
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.PLAYING:
                # Draw game objects
                
                # Draw player with hit feedback
                if self.player_hit_timer > 0 and self.player_hit_timer % 6 < 3:
                    # Flash red when hit
                    player_surface = pygame.Surface((self.player.width, self.player.height))
                    player_surface.fill(RED)
                    player_surface.set_alpha(128)
                    self.screen.blit(player_surface, (self.player.x, self.player.y))
                
                # Draw player (with invulnerability flashing)
                if self.player_invulnerable_timer <= 0 or self.player_invulnerable_timer % 8 < 4:
                    self.player.draw(self.screen)
                
                # Draw cosmic formation
                self.cosmic_formation.draw(self.screen)
                
                # Draw player bullets (multiple bullets)
                for bullet in self.player_bullets:
                    bullet.draw(self.screen)
                    
                # Draw alien bullets
                for bullet in self.alien_bullets:
                    bullet.draw(self.screen)
                
                # Draw hit effects
                for effect in self.hit_effects:
                    effect.draw(self.screen, self.font_manager)
                
                # Draw warning if player is low on lives
                if self.lives == 1:
                    warning_text, warning_rect = self.font_manager.render_text(
                        "⚠️ LAST LIFE! ⚠️", 'medium', RED, (SCREEN_WIDTH//2, 50)
                    )
                    self.screen.blit(warning_text, warning_rect)
                
                # Draw UI
                self.draw_game_ui()
                
            elif self.state == GameState.LEVEL_COMPLETE:
                # Draw frozen game state
                self.player.draw(self.screen)
                self.cosmic_formation.draw(self.screen)
                for bullet in self.player_bullets:
                    bullet.draw(self.screen)
                for bullet in self.alien_bullets:
                    bullet.draw(self.screen)
                for effect in self.hit_effects:
                    effect.draw(self.screen, self.font_manager)
                self.draw_game_ui()
                
                # Draw level complete overlay
                self.draw_level_complete()
                
            elif self.state == GameState.LEVEL_TRANSITION:
                # Draw level transition screen
                self.draw_level_transition()
                
            elif self.state == GameState.GAME_OVER:
                # Draw frozen game state
                self.player.draw(self.screen)
                self.cosmic_formation.draw(self.screen)
                for bullet in self.player_bullets:
                    bullet.draw(self.screen)
                for bullet in self.alien_bullets:
                    bullet.draw(self.screen)
                for effect in self.hit_effects:
                    effect.draw(self.screen, self.font_manager)
                self.draw_game_ui()
                
                # Draw game over overlay
                self.draw_game_over()
            
            elif self.state == GameState.VICTORY:
                # Draw the current game state in background (faded)
                if self.player_hit_timer > 0 and self.player_hit_timer % 6 < 3:
                    # Flash red when hit
                    player_surface = pygame.Surface((self.player.width, self.player.height))
                    player_surface.fill(RED)
                    player_surface.set_alpha(128)
                    self.screen.blit(player_surface, (self.player.x, self.player.y))
                else:
                    self.player.draw(self.screen)
                
                # Draw cosmic formation
                self.cosmic_formation.draw(self.screen)
                
                # Draw bullets
                for bullet in self.player_bullets:
                    bullet.draw(self.screen)
                for bullet in self.alien_bullets:
                    bullet.draw(self.screen)
                
                # Draw effects
                for effect in self.hit_effects:
                    effect.draw(self.screen, self.font_manager)
                self.draw_game_ui()
                
                # Draw victory overlay
                self.draw_victory_screen()
            
            elif self.state == GameState.CREDITS:
                # Draw credits screen
                self.draw_credits_screen()
            
            elif self.state == GameState.PAUSED:
                # Draw frozen game state (same as playing but without updates)
                if self.player_hit_timer > 0 and self.player_hit_timer % 6 < 3:
                    # Flash red when hit
                    player_surface = pygame.Surface((self.player.width, self.player.height))
                    player_surface.fill(RED)
                    player_surface.set_alpha(128)
                    self.screen.blit(player_surface, (self.player.x, self.player.y))
                else:
                    self.player.draw(self.screen)
                
                # Draw cosmic formation
                self.cosmic_formation.draw(self.screen)
                
                # Draw bullets
                for bullet in self.player_bullets:
                    bullet.draw(self.screen)
                for bullet in self.alien_bullets:
                    bullet.draw(self.screen)
                
                # Draw hit effects
                for effect in self.hit_effects:
                    effect.draw(self.screen, self.font_manager)
                
                # Draw warning if player is low on lives
                if self.lives == 1:
                    warning_text, warning_rect = self.font_manager.render_text(
                        "⚠️ LAST LIFE! ⚠️", 'medium', RED, (SCREEN_WIDTH//2, 50)
                    )
                    self.screen.blit(warning_text, warning_rect)
                
                # Draw UI
                self.draw_game_ui()
                
                # Draw pause overlay
                self.ui_manager.draw_pause_screen(self.screen)
            
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
            
        # Cleanup audio system
        self.audio_manager.cleanup()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
