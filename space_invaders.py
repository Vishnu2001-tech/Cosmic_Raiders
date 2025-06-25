import pygame
import random
import sys
import os
from enum import Enum

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
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3
    LEVEL_COMPLETE = 4
    LEVEL_TRANSITION = 5

class FontManager:
    def __init__(self):
        self.fonts = {}
        self.font_path = "fonts/Pixeled.ttf"
        self.fallback_fonts = [
            "/usr/share/fonts/truetype/ubuntu/UbuntuMono[wght].ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "/usr/share/fonts/truetype/freefont/FreeMono.ttf"
        ]
        self.load_fonts()
        self.print_font_status()
    
    def load_fonts(self):
        """Load custom pixel font with fallback to better system fonts"""
        sizes = {
            'title': 48,
            'large': 32,
            'medium': 24,
            'small': 16
        }
        
        # Try to load custom font first
        font_to_use = None
        font_source = "default"
        
        if os.path.exists(self.font_path):
            font_to_use = self.font_path
            font_source = "custom Pixeled.ttf"
        else:
            # Try fallback fonts for better retro look
            for fallback_font in self.fallback_fonts:
                if os.path.exists(fallback_font):
                    font_to_use = fallback_font
                    font_source = f"system font ({os.path.basename(fallback_font)})"
                    break
        
        # Load fonts with chosen font file
        for name, size in sizes.items():
            try:
                if font_to_use:
                    self.fonts[name] = pygame.font.Font(font_to_use, size)
                else:
                    # Ultimate fallback to pygame default
                    self.fonts[name] = pygame.font.Font(None, size)
                    font_source = "pygame default"
            except Exception as e:
                # Ultimate fallback
                self.fonts[name] = pygame.font.Font(None, size)
                font_source = "pygame default (fallback)"
        
        self.current_font_source = font_source
    
    def print_font_status(self):
        """Print which font is being used"""
        print(f"🎮 Font System: Using {self.current_font_source}")
        if os.path.exists(self.font_path):
            print("✅ Custom pixel font loaded successfully!")
            print("🎨 Authentic retro arcade styling enabled!")
        else:
            print("ℹ️  Note: For authentic retro look, add 'Pixeled.ttf' to fonts/ directory")
    
    def get_font(self, size_name):
        """Get font by size name"""
        return self.fonts.get(size_name, self.fonts['medium'])
    
    def render_text(self, text, size_name, color=WHITE, center_pos=None):
        """Render text with specified font size"""
        font = self.get_font(size_name)
        surface = font.render(text, True, color)
        
        if center_pos:
            rect = surface.get_rect(center=center_pos)
            return surface, rect
        
        return surface, surface.get_rect()

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 30
        self.speed = 5
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def move_left(self):
        if self.x > 0:
            self.x -= self.speed
            self.rect.x = self.x
            
    def move_right(self):
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
            self.rect.x = self.x
            
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)
        # Draw a simple spaceship shape
        pygame.draw.polygon(screen, WHITE, [
            (self.x + self.width//2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ])

class Bullet:
    def __init__(self, x, y, direction, speed_multiplier=1.0):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 10
        base_speed = 8
        self.speed = base_speed * speed_multiplier
        self.direction = direction  # 1 for up (player), -1 for down (alien)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def update(self):
        self.y -= self.speed * self.direction
        self.rect.y = self.y
        
    def is_off_screen(self):
        return self.y < -10 or self.y > SCREEN_HEIGHT + 10
        
    def draw(self, screen):
        if self.direction == 1:  # Player bullet
            color = YELLOW
            # Add a glow effect for player bullets
            pygame.draw.rect(screen, color, self.rect)
            pygame.draw.rect(screen, WHITE, 
                           (self.x - 1, self.y - 1, self.width + 2, self.height + 2), 1)
        else:  # Alien bullet
            color = RED
            pygame.draw.rect(screen, color, self.rect)
            # Make alien bullets more menacing
            pygame.draw.rect(screen, (255, 100, 100), 
                           (self.x - 1, self.y - 1, self.width + 2, self.height + 2), 1)

class HitEffect:
    def __init__(self, x, y, effect_type="explosion"):
        self.x = x
        self.y = y
        self.effect_type = effect_type
        self.timer = 0
        self.max_time = 30  # frames to show effect
        self.size = 0
        
    def update(self):
        self.timer += 1
        # Grow then shrink effect
        if self.timer < self.max_time // 2:
            self.size = self.timer * 2
        else:
            self.size = (self.max_time - self.timer) * 2
        
        return self.timer < self.max_time
    
    def draw(self, screen, font_manager):
        if self.effect_type == "explosion":
            # Draw explosion effect
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
    def __init__(self, x, y, alien_type="basic", difficulty_level=1):
        self.x = x
        self.y = y
        self.initial_x = x
        self.initial_y = y
        self.width = 35
        self.height = 25
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.alien_type = alien_type
        self.difficulty_level = difficulty_level
        
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
        pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw different shapes based on alien type
        if self.alien_type == "scout":
            # Triangle shape for scouts
            pygame.draw.polygon(screen, WHITE, [
                (self.x + self.width//2, self.y + 3),
                (self.x + self.width - 3, self.y + self.height - 3),
                (self.x + 3, self.y + self.height - 3)
            ])
        elif self.alien_type == "warrior":
            # Diamond shape for warriors
            pygame.draw.polygon(screen, WHITE, [
                (self.x + self.width//2, self.y + 3),
                (self.x + self.width - 3, self.y + self.height//2),
                (self.x + self.width//2, self.y + self.height - 3),
                (self.x + 3, self.y + self.height//2)
            ])
        elif self.alien_type == "commander":
            # Star shape for commanders
            center_x = self.x + self.width // 2
            center_y = self.y + self.height // 2
            pygame.draw.circle(screen, WHITE, (center_x, center_y), 8)
            pygame.draw.circle(screen, self.color, (center_x, center_y), 5)
        else:  # basic
            # Simple oval for basic aliens
            pygame.draw.ellipse(screen, WHITE, 
                              (self.x + 3, self.y + 3, self.width - 6, self.height - 6))
    
    def is_at_bottom(self):
        """Check if alien has reached the bottom of the screen"""
        return self.y + self.height >= SCREEN_HEIGHT - 100  # More margin for player area

class CosmicFormation:
    def __init__(self, difficulty_level=1):
        self.difficulty_level = difficulty_level
        self.active_aliens = []
        self.formation_queue = []
        self.max_active_aliens = 3  # Limit active aliens on screen
        self.spawn_timer = 0
        self.spawn_delay = 180  # 3 seconds at 60 FPS for better pacing
        
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
            new_alien = Alien(x, y, alien_type, self.difficulty_level)
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
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cosmic Raiders")
        self.clock = pygame.time.Clock()
        self.font_manager = FontManager()
        
        # Game state
        self.state = GameState.MENU
        self.score = 0
        self.lives = 3
        self.max_lives = 3
        self.high_score = 0
        self.wave = 1
        self.difficulty_level = 1
        
        # Game over and transition states
        self.game_over_reason = ""
        self.level_complete_timer = 0
        self.level_complete_duration = 180  # 3 seconds at 60 FPS
        self.transition_timer = 0
        self.transition_duration = 120  # 2 seconds at 60 FPS
        
        # Player hit feedback
        self.player_hit_timer = 0
        self.player_hit_duration = 30  # frames to show hit effect
        self.player_invulnerable_timer = 0
        self.player_invulnerable_duration = 60  # frames of invulnerability after hit
        
        # Initialize game objects
        self.player = Player(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 50)
        self.player_bullets = []  # Multiple bullets allowed
        self.alien_bullets = []
        self.cosmic_formation = CosmicFormation(self.difficulty_level)
        self.hit_effects = []  # Visual effects for hits
        
        # Shooting mechanics - Fast and responsive
        self.last_shot_time = 0
        self.shot_cooldown = 150  # Minimal delay (150ms) for responsive shooting
        
        # Menu selection
        self.menu_selection = 0
        self.menu_options = ["START GAME", "QUIT"]
        
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
        self.player_bullets.append(Bullet(bullet_x, bullet_y, 1))
        print(f"🔫 Bullet fired! ({len(self.player_bullets)} bullets active)")
        
    def shoot_alien_bullet(self, alien):
        """Create a bullet from alien position with dynamic speed"""
        bullet_x = alien.x + alien.width // 2 - 2
        bullet_y = alien.y + alien.height
        speed_multiplier = 1.0 + (self.difficulty_level - 1) * 0.1  # Slight speed increase per level
        self.alien_bullets.append(Bullet(bullet_x, bullet_y, -1, speed_multiplier))
        
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
                self.cosmic_formation = CosmicFormation(self.difficulty_level)
                print(f"🌊 Advancing to Level {self.difficulty_level}! Lives reset to {self.lives}")
                
        elif self.state == GameState.LEVEL_TRANSITION:
            self.transition_timer -= 1
            if self.transition_timer <= 0:
                # Resume gameplay
                self.state = GameState.PLAYING
                print(f"🚀 Level {self.difficulty_level} begins!")
                
    def check_collisions(self):
        """Check all collision scenarios"""
        # Player bullets vs aliens (multiple bullets system)
        for bullet in self.player_bullets[:]:
            for alien in self.cosmic_formation.active_aliens[:]:
                if bullet.rect.colliderect(alien.rect):
                    # Create hit effect
                    effect_x = alien.x + alien.width // 2
                    effect_y = alien.y + alien.height // 2
                    self.hit_effects.append(HitEffect(effect_x, effect_y, "explosion"))
                    
                    # Remove bullet and alien
                    points = alien.points
                    self.player_bullets.remove(bullet)
                    self.cosmic_formation.remove_alien(alien)
                    self.score += points
                    
                    # Visual feedback
                    print(f"💥 {alien.alien_type.title()} destroyed! +{points} points (Score: {self.score}) [{len(self.player_bullets)} bullets remaining]")
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
                    self.hit_effects.append(HitEffect(effect_x, effect_y, "explosion"))
                    
                    print(f"⚠️ PLAYER HIT! Lives remaining: {self.lives}")
                    break
                
    def check_game_over_conditions(self):
        """Check if game should end or level should advance"""
        # Game over is handled in update_cosmic_formation for alien invasion
        
        # Check if formation is complete (level complete)
        if self.cosmic_formation.is_formation_complete():
            self.state = GameState.LEVEL_COMPLETE
            self.level_complete_timer = self.level_complete_duration
            print(f"🎉 Level {self.difficulty_level} completed! Score: {self.score}")
            return
            
        # Check if player died
        if self.lives <= 0:
            self.state = GameState.GAME_OVER
            self.game_over_reason = "No lives remaining!"
            if self.score > self.high_score:
                self.high_score = self.score
            print("💀 Game Over: No lives remaining!")
            
    def draw_menu(self):
        """Draw the main menu"""
        # Background
        self.screen.fill(BLACK)
        
        # Title
        title_text, title_rect = self.font_manager.render_text(
            "COSMIC RAIDERS", 'title', WHITE, (SCREEN_WIDTH//2, 150)
        )
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text, subtitle_rect = self.font_manager.render_text(
            "DYNAMIC FORMATION EDITION", 'medium', CYAN, (SCREEN_WIDTH//2, 200)
        )
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Menu options
        for i, option in enumerate(self.menu_options):
            color = YELLOW if i == self.menu_selection else WHITE
            option_text, option_rect = self.font_manager.render_text(
                option, 'large', color, (SCREEN_WIDTH//2, 300 + i * 60)
            )
            self.screen.blit(option_text, option_rect)
            
            # Selection indicator
            if i == self.menu_selection:
                indicator_text, indicator_rect = self.font_manager.render_text(
                    ">", 'large', YELLOW, (option_rect.left - 40, option_rect.centery)
                )
                self.screen.blit(indicator_text, indicator_rect)
        
        # Instructions
        instructions = [
            "USE ARROW KEYS TO NAVIGATE",
            "PRESS ENTER TO SELECT",
            "WASD OR ARROWS TO MOVE",
            "SPACEBAR FOR RAPID FIRE"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text, inst_rect = self.font_manager.render_text(
                instruction, 'small', GRAY, (SCREEN_WIDTH//2, 450 + i * 25)
            )
            self.screen.blit(inst_text, inst_rect)
        
        # High score
        if self.high_score > 0:
            high_score_text, high_score_rect = self.font_manager.render_text(
                f"HIGH SCORE: {self.high_score}", 'medium', GREEN, (SCREEN_WIDTH//2, 100)
            )
            self.screen.blit(high_score_text, high_score_rect)
    
    def draw_game_ui(self):
        """Draw game UI during gameplay"""
        # Lives (prominent display in top-left)
        lives_color = RED if self.lives == 1 else YELLOW if self.lives == 2 else GREEN
        lives_text, _ = self.font_manager.render_text(f"LIVES: {self.lives}", 'large', lives_color)
        self.screen.blit(lives_text, (10, 10))
        
        # Score
        score_text, _ = self.font_manager.render_text(f"SCORE: {self.score}", 'large', WHITE)
        self.screen.blit(score_text, (10, 50))
        
        # Wave and difficulty
        wave_text, _ = self.font_manager.render_text(f"WAVE: {self.wave}", 'large', WHITE)
        self.screen.blit(wave_text, (10, 90))
        
        difficulty_text, _ = self.font_manager.render_text(f"LEVEL: {self.difficulty_level}", 'medium', CYAN)
        self.screen.blit(difficulty_text, (10, 130))
        
        # Alien count and formation info
        active_aliens = len(self.cosmic_formation.active_aliens)
        total_remaining = self.cosmic_formation.get_total_aliens_remaining()
        aliens_text, _ = self.font_manager.render_text(f"ACTIVE: {active_aliens}/3 | REMAINING: {total_remaining}", 'medium', CYAN)
        self.screen.blit(aliens_text, (10, 155))
        
        # Formation info
        formation_names = {1: "LINE", 2: "V-SHAPE", 3: "ARC", 4: "TRIANGLE", 5: "DIAMOND", 6: "SPIRAL", 7: "CROSS", 8: "WAVE"}
        formation_name = formation_names.get(((self.difficulty_level - 1) % 8) + 1, "CUSTOM")
        formation_text, _ = self.font_manager.render_text(f"FORMATION: {formation_name}", 'medium', YELLOW)
        self.screen.blit(formation_text, (10, 180))
        
        # Active bullets counter
        bullet_count = len(self.player_bullets)
        alien_bullet_count = len(self.alien_bullets)
        bullet_color = GREEN if bullet_count > 0 else GRAY
        bullets_text, _ = self.font_manager.render_text(f"BULLETS: {bullet_count}", 'small', bullet_color)
        self.screen.blit(bullets_text, (10, 205))
        
        alien_bullets_text, _ = self.font_manager.render_text(f"ENEMY: {alien_bullet_count}", 'small', RED)
        self.screen.blit(alien_bullets_text, (10, 225))
        
        # Movement speed info
        speed_text, _ = self.font_manager.render_text(f"SPEED: {1.0 + (self.difficulty_level - 1) * 0.2:.1f}x", 'small', YELLOW)
        self.screen.blit(speed_text, (10, 245))
        
        # Player status
        if self.player_invulnerable_timer > 0:
            status_text, _ = self.font_manager.render_text("INVULNERABLE", 'small', YELLOW)
            self.screen.blit(status_text, (10, 265))
        
        # High score (top right)
        high_score_text, high_score_rect = self.font_manager.render_text(
            f"HIGH: {self.high_score}", 'medium', CYAN
        )
        high_score_rect.topright = (SCREEN_WIDTH - 10, 10)
        self.screen.blit(high_score_text, high_score_rect)
        
        # Instructions at bottom
        instruction_text, instruction_rect = self.font_manager.render_text(
            "SPACE: RAPID FIRE  |  ESC: MENU", 'small', GRAY, (SCREEN_WIDTH//2, SCREEN_HEIGHT - 20)
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
        next_rows, next_cols = self.alien_grid.get_grid_size(self.difficulty_level + 1)
        next_level_text, next_level_rect = self.font_manager.render_text(
            f"Next: Level {self.difficulty_level + 1} ({next_rows}x{next_cols} aliens)", 'medium', CYAN, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40)
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
        next_rows, next_cols = self.alien_grid.get_grid_size(self.difficulty_level + 1)
        next_level_text, next_level_rect = self.font_manager.render_text(
            f"Next: Level {self.difficulty_level + 1} ({next_rows}x{next_cols} aliens)", 'medium', CYAN, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40)
        )
        self.screen.blit(next_level_text, next_level_rect)
        
        # Countdown
        seconds_left = (self.level_complete_timer // 60) + 1
        countdown_text, countdown_rect = self.font_manager.render_text(
            f"Advancing in {seconds_left}...", 'medium', WHITE, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80)
        )
        self.screen.blit(countdown_text, countdown_rect)
    
    def draw_level_transition(self):
        """Draw level transition screen"""
        # Full overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Level title
        level_text, level_rect = self.font_manager.render_text(
            f"LEVEL {self.difficulty_level}", 'title', WHITE, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 80)
        )
        self.screen.blit(level_text, level_rect)
        
        # Grid info
        formation_names = {1: "LINE", 2: "V-SHAPE", 3: "ARC", 4: "TRIANGLE", 5: "DIAMOND", 6: "SPIRAL", 7: "CROSS", 8: "WAVE"}
        formation_name = formation_names.get(((self.difficulty_level) % 8) + 1, "CUSTOM")
        grid_text, grid_rect = self.font_manager.render_text(
            f"{formation_name} Formation", 'large', CYAN, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20)
        )
        self.screen.blit(grid_text, grid_rect)
        
        # Difficulty info
        difficulty_info = [
            f"Horizontal Speed: {1.0 + (self.difficulty_level - 1) * 0.2:.1f}x",
            f"Vertical Speed: 1.0x (Constant)",
            f"Lives: {self.lives}"
        ]
        
        for i, info in enumerate(difficulty_info):
            info_text, info_rect = self.font_manager.render_text(
                info, 'medium', YELLOW, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20 + i * 30)
            )
            self.screen.blit(info_text, info_rect)
        
        # Ready message
        ready_text, ready_rect = self.font_manager.render_text(
            "GET READY!", 'large', RED, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 120)
        )
        self.screen.blit(ready_text, ready_rect)
        
    def draw_game_over(self):
        """Draw enhanced game over screen"""
        # Full overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game Over title
        game_over_text, game_over_rect = self.font_manager.render_text(
            "GAME OVER", 'title', RED, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 120)
        )
        self.screen.blit(game_over_text, game_over_rect)
        
        # Game over reason
        reason_text, reason_rect = self.font_manager.render_text(
            self.game_over_reason, 'medium', WHITE, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 80)
        )
        self.screen.blit(reason_text, reason_rect)
        
        # Final score
        final_score_text, final_score_rect = self.font_manager.render_text(
            f"FINAL SCORE: {self.score}", 'large', WHITE, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40)
        )
        self.screen.blit(final_score_text, final_score_rect)
        
        # High score notification
        if self.score == self.high_score and self.score > 0:
            new_high_text, new_high_rect = self.font_manager.render_text(
                "🏆 NEW HIGH SCORE! 🏆", 'medium', YELLOW, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            )
            self.screen.blit(new_high_text, new_high_rect)
        else:
            high_score_text, high_score_rect = self.font_manager.render_text(
                f"High Score: {self.high_score}", 'medium', CYAN, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            )
            self.screen.blit(high_score_text, high_score_rect)
        
        # Level reached
        level_text, level_rect = self.font_manager.render_text(
            f"Level Reached: {self.difficulty_level}", 'medium', CYAN, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40)
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
        self.player = Player(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 50)
        self.player_bullets = []  # Reset multiple bullets
        self.alien_bullets = []
        self.cosmic_formation = CosmicFormation(self.difficulty_level)  # Create new cosmic formation with level 1
        self.hit_effects = []  # Clear effects
        self.last_shot_time = 0  # Reset shooting timer
        self.player_hit_timer = 0
        self.player_invulnerable_timer = 0
        print(f"🔄 Game restarted! Starting Level 1 with {self.lives} lives")
    
    def start_game(self):
        """Start a new game from menu"""
        self.restart_game()
        self.state = GameState.PLAYING
        
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == GameState.PLAYING:
                            self.state = GameState.MENU
                        elif self.state == GameState.GAME_OVER:
                            running = False  # Quit from game over
                        elif self.state == GameState.MENU:
                            running = False
                    
                    # Menu navigation
                    elif self.state == GameState.MENU:
                        if event.key == pygame.K_UP:
                            self.menu_selection = (self.menu_selection - 1) % len(self.menu_options)
                        elif event.key == pygame.K_DOWN:
                            self.menu_selection = (self.menu_selection + 1) % len(self.menu_options)
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            if self.menu_selection == 0:  # START GAME
                                self.start_game()
                            elif self.menu_selection == 1:  # QUIT
                                running = False
                    
                    # Game over screen controls
                    elif self.state == GameState.GAME_OVER:
                        if event.key == pygame.K_r:
                            self.restart_game()
                        elif event.key == pygame.K_SPACE:
                            self.state = GameState.MENU
                        
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
                
            # Clear screen
            self.screen.fill(BLACK)
            
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
            
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
