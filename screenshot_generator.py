#!/usr/bin/env python3
"""
Screenshot Generator for Cosmic Raiders
Automatically captures key game moments for blog post
"""

import pygame
import sys
import os
import time
from cosmic_raiders import *

class ScreenshotGenerator:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Cosmic Raiders - Screenshot Generator")
        self.clock = pygame.time.Clock()
        self.screenshot_count = 0
        
        # Create screenshots directory
        os.makedirs("screenshots", exist_ok=True)
        
    def save_screenshot(self, filename):
        """Save current screen as screenshot"""
        filepath = f"screenshots/{filename}"
        pygame.image.save(self.screen, filepath)
        print(f"Screenshot saved: {filepath}")
        self.screenshot_count += 1
        
    def generate_main_menu_screenshot(self):
        """Generate main menu screenshot"""
        print("Generating main menu screenshot...")
        
        # Create a simple main menu representation
        self.screen.fill((10, 20, 40))  # Dark blue background
        
        # Load font
        try:
            font_large = pygame.font.Font("fonts/Pixeled.ttf", 48)
            font_medium = pygame.font.Font("fonts/Pixeled.ttf", 24)
        except:
            font_large = pygame.font.Font(None, 48)
            font_medium = pygame.font.Font(None, 24)
        
        # Title
        title_text = font_large.render("COSMIC RAIDERS", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(400, 150))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = font_medium.render("Enhanced Space Invaders", True, (150, 150, 255))
        subtitle_rect = subtitle_text.get_rect(center=(400, 200))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Menu options
        menu_options = ["START GAME", "HOW TO PLAY", "HIGH SCORES", "QUIT"]
        for i, option in enumerate(menu_options):
            color = (255, 255, 0) if i == 0 else (200, 200, 200)
            option_text = font_medium.render(option, True, color)
            option_rect = option_text.get_rect(center=(400, 300 + i * 40))
            self.screen.blit(option_text, option_rect)
        
        # Add some stars
        for _ in range(50):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 1)
        
        pygame.display.flip()
        self.save_screenshot("main_menu.png")
        
    def generate_gameplay_screenshot(self, level_type="early"):
        """Generate gameplay screenshot"""
        print(f"Generating {level_type} gameplay screenshot...")
        
        # Create space background
        self.screen.fill((5, 5, 20))
        
        # Add stars
        for _ in range(100):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            brightness = random.randint(100, 255)
            pygame.draw.circle(self.screen, (brightness, brightness, brightness), (x, y), 1)
        
        # Player ship
        player_rect = pygame.Rect(375, 520, 50, 30)
        pygame.draw.polygon(self.screen, (0, 255, 0), [
            (player_rect.centerx, player_rect.top),
            (player_rect.left, player_rect.bottom),
            (player_rect.right, player_rect.bottom)
        ])
        
        # Alien ships based on level type
        if level_type == "early":
            # Scout-class ships in line formation
            alien_color = (255, 100, 100)
            ship_size = (35, 25)
            positions = [(100 + i * 80, 100) for i in range(8)]
        else:
            # Mothership-class in spiral formation
            alien_color = (255, 50, 255)
            ship_size = (55, 35)
            # Spiral formation
            positions = []
            import math
            for i in range(6):
                angle = i * math.pi / 3
                radius = 80 + i * 20
                x = 400 + radius * math.cos(angle)
                y = 150 + radius * math.sin(angle)
                positions.append((x, y))
        
        # Draw aliens
        for pos in positions:
            alien_rect = pygame.Rect(pos[0] - ship_size[0]//2, pos[1] - ship_size[1]//2, 
                                   ship_size[0], ship_size[1])
            # Draw complex alien shape
            pygame.draw.ellipse(self.screen, alien_color, alien_rect)
            pygame.draw.rect(self.screen, (alien_color[0]//2, alien_color[1]//2, alien_color[2]//2), 
                           alien_rect, 2)
        
        # Player bullets
        for i in range(3):
            bullet_x = 395 + i * 10
            bullet_y = 480 - i * 60
            pygame.draw.rect(self.screen, (255, 255, 0), (bullet_x, bullet_y, 4, 15))
        
        # UI Elements
        try:
            font = pygame.font.Font("fonts/Pixeled.ttf", 16)
        except:
            font = pygame.font.Font(None, 16)
            
        # Score
        score_text = font.render(f"SCORE: {25000 if level_type == 'advanced' else 5000}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        # Level
        level_text = font.render(f"LEVEL: {12 if level_type == 'advanced' else 3}", True, (255, 255, 255))
        self.screen.blit(level_text, (10, 30))
        
        # Lives
        lives_text = font.render("LIVES: ♥ ♥ ♥", True, (255, 100, 100))
        self.screen.blit(lives_text, (10, 50))
        
        pygame.display.flip()
        filename = f"{level_type}_gameplay.png"
        self.save_screenshot(filename)
        
    def generate_formation_showcase(self):
        """Generate formation patterns showcase"""
        print("Generating formation showcase...")
        
        self.screen.fill((5, 5, 20))
        
        # Add stars
        for _ in range(80):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 1)
        
        # Title
        try:
            font_title = pygame.font.Font("fonts/Pixeled.ttf", 24)
            font_small = pygame.font.Font("fonts/Pixeled.ttf", 12)
        except:
            font_title = pygame.font.Font(None, 24)
            font_small = pygame.font.Font(None, 12)
            
        title_text = font_title.render("FORMATION PATTERNS", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(400, 30))
        self.screen.blit(title_text, title_rect)
        
        # Formation examples
        formations = [
            ("Line", [(50 + i * 30, 100) for i in range(6)]),
            ("V-Shape", [(200 + i * 20, 100 + abs(i-2) * 15) for i in range(6)]),
            ("Diamond", [(400, 80), (380, 100), (420, 100), (360, 120), (400, 120), (440, 120), (400, 140)]),
            ("Spiral", [])
        ]
        
        # Generate spiral formation
        import math
        spiral_positions = []
        for i in range(8):
            angle = i * math.pi / 2
            radius = 20 + i * 8
            x = 600 + radius * math.cos(angle)
            y = 300 + radius * math.sin(angle)
            spiral_positions.append((x, y))
        formations[3] = ("Spiral", spiral_positions)
        
        # Draw formations
        colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 100, 255)]
        
        for i, (name, positions) in enumerate(formations):
            color = colors[i]
            
            # Formation label
            label_y = 80 if i < 2 else 250
            label_x = 100 + (i % 2) * 300 if i < 2 else 100 + ((i-2) % 2) * 300
            label_text = font_small.render(name, True, (255, 255, 255))
            self.screen.blit(label_text, (label_x, label_y))
            
            # Draw ships in formation
            for pos in positions:
                ship_rect = pygame.Rect(pos[0] - 8, pos[1] - 6, 16, 12)
                pygame.draw.ellipse(self.screen, color, ship_rect)
        
        pygame.display.flip()
        self.save_screenshot("formations.png")
        
    def generate_particle_effects_screenshot(self):
        """Generate particle effects showcase"""
        print("Generating particle effects screenshot...")
        
        self.screen.fill((5, 5, 20))
        
        # Add stars
        for _ in range(60):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 1)
        
        # Explosion effects
        explosion_centers = [(200, 200), (400, 300), (600, 150)]
        
        for center in explosion_centers:
            # Main explosion
            for i in range(20):
                angle = random.random() * 2 * math.pi
                distance = random.randint(10, 50)
                x = center[0] + distance * math.cos(angle)
                y = center[1] + distance * math.sin(angle)
                size = random.randint(2, 8)
                color_intensity = random.randint(150, 255)
                color = (color_intensity, color_intensity // 2, 0)
                pygame.draw.circle(self.screen, color, (int(x), int(y)), size)
        
        # Engine trails
        trail_positions = [(100, 500), (300, 480), (500, 520)]
        for pos in trail_positions:
            # Ship
            ship_rect = pygame.Rect(pos[0] - 15, pos[1] - 10, 30, 20)
            pygame.draw.ellipse(self.screen, (100, 100, 255), ship_rect)
            
            # Trail
            for i in range(15):
                trail_x = pos[0] - 20 - i * 3
                trail_y = pos[1] + random.randint(-5, 5)
                alpha = 255 - i * 15
                color = (0, alpha // 3, alpha)
                pygame.draw.circle(self.screen, color, (trail_x, trail_y), 3 - i // 5)
        
        # Title
        try:
            font = pygame.font.Font("fonts/Pixeled.ttf", 24)
        except:
            font = pygame.font.Font(None, 24)
            
        title_text = font.render("PARTICLE EFFECTS", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(400, 50))
        self.screen.blit(title_text, title_rect)
        
        pygame.display.flip()
        self.save_screenshot("particle_effects.png")
        
    def generate_all_screenshots(self):
        """Generate all required screenshots"""
        print("Starting screenshot generation...")
        
        # Generate each screenshot with delays
        self.generate_main_menu_screenshot()
        time.sleep(1)
        
        self.generate_gameplay_screenshot("early")
        time.sleep(1)
        
        self.generate_gameplay_screenshot("advanced")
        time.sleep(1)
        
        self.generate_formation_showcase()
        time.sleep(1)
        
        self.generate_particle_effects_screenshot()
        time.sleep(1)
        
        print(f"\nScreenshot generation complete!")
        print(f"Generated {self.screenshot_count} screenshots in the 'screenshots' directory")
        print("\nScreenshots created:")
        print("- main_menu.png")
        print("- early_gameplay.png") 
        print("- advanced_gameplay.png")
        print("- formations.png")
        print("- particle_effects.png")

def main():
    try:
        generator = ScreenshotGenerator()
        generator.generate_all_screenshots()
    except Exception as e:
        print(f"Error generating screenshots: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
