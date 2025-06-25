import pygame

class UIManager:
    def __init__(self, screen_width, screen_height, font_manager):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font_manager = font_manager
        
        # UI Layout zones
        self.ui_zones = {
            'top_left': pygame.Rect(5, 5, 150, 80),
            'top_right': pygame.Rect(screen_width - 155, 5, 150, 80),
            'bottom_left': pygame.Rect(5, screen_height - 85, 200, 80),
            'bottom_right': pygame.Rect(screen_width - 205, screen_height - 85, 200, 80)
        }
        
        # UI Colors
        self.colors = {
            'background': (0, 0, 0, 120),  # Semi-transparent black
            'border': (100, 100, 100),
            'text_primary': (255, 255, 255),
            'text_secondary': (200, 200, 200),
            'text_accent': (255, 255, 0),
            'health_high': (0, 255, 0),
            'health_medium': (255, 255, 0),
            'health_low': (255, 0, 0),
            'score_normal': (255, 255, 255),
            'score_high': (255, 255, 0),
            'score_new': (0, 255, 0)
        }
    
    def draw_compact_hud(self, screen, game_data):
        """Draw compact, non-intrusive HUD"""
        
        # Top-left: Essential game info
        self.draw_essential_info(screen, game_data)
        
        # Top-right: Score information
        self.draw_score_info(screen, game_data)
        
        # Bottom-left: Level progress (only when relevant)
        if game_data.get('show_progress', False):
            self.draw_level_progress(screen, game_data)
        
        # Bottom-right: Quick stats (minimal)
        self.draw_quick_stats(screen, game_data)
    
    def draw_essential_info(self, screen, game_data):
        """Draw essential game information in top-left"""
        zone = self.ui_zones['top_left']
        
        # Semi-transparent background
        bg_surface = pygame.Surface((zone.width, zone.height), pygame.SRCALPHA)
        bg_surface.fill(self.colors['background'])
        screen.blit(bg_surface, zone.topleft)
        
        # Lives with color coding
        lives = game_data.get('lives', 3)
        if lives >= 3:
            lives_color = self.colors['health_high']
        elif lives == 2:
            lives_color = self.colors['health_medium']
        else:
            lives_color = self.colors['health_low']
        
        lives_text, _ = self.font_manager.render_text(f"♥ {lives}", 'medium', lives_color)
        screen.blit(lives_text, (zone.x + 5, zone.y + 5))
        
        # Level
        level = game_data.get('level', 1)
        level_text, _ = self.font_manager.render_text(f"LV {level}", 'medium', self.colors['text_accent'])
        screen.blit(level_text, (zone.x + 5, zone.y + 30))
        
        # Wave (if different from level)
        wave = game_data.get('wave', 1)
        if wave != level:
            wave_text, _ = self.font_manager.render_text(f"W{wave}", 'small', self.colors['text_secondary'])
            screen.blit(wave_text, (zone.x + 5, zone.y + 55))
    
    def draw_score_info(self, screen, game_data):
        """Draw score information in top-right"""
        zone = self.ui_zones['top_right']
        
        # Semi-transparent background
        bg_surface = pygame.Surface((zone.width, zone.height), pygame.SRCALPHA)
        bg_surface.fill(self.colors['background'])
        screen.blit(bg_surface, zone.topleft)
        
        # Current score
        score = game_data.get('score', 0)
        high_score = game_data.get('high_score', 0)
        
        # Determine score color
        if score > high_score:
            score_color = self.colors['score_new']
        elif score > high_score * 0.8:
            score_color = self.colors['score_high']
        else:
            score_color = self.colors['score_normal']
        
        score_text, score_rect = self.font_manager.render_text(f"{score:,}", 'medium', score_color)
        score_rect.topright = (zone.right - 5, zone.y + 5)
        screen.blit(score_text, score_rect)
        
        # High score (smaller, less prominent)
        if high_score > 0:
            high_text, high_rect = self.font_manager.render_text(f"HI:{high_score:,}", 'small', self.colors['text_secondary'])
            high_rect.topright = (zone.right - 5, zone.y + 35)
            screen.blit(high_text, high_rect)
        
        # New high score indicator
        if score > high_score and score > 0:
            new_text, new_rect = self.font_manager.render_text("NEW!", 'small', self.colors['score_new'])
            new_rect.topright = (zone.right - 5, zone.y + 55)
            screen.blit(new_text, new_rect)
    
    def draw_level_progress(self, screen, game_data):
        """Draw level progress in bottom-left (when needed)"""
        zone = self.ui_zones['bottom_left']
        
        # Only show during active gameplay
        if not game_data.get('in_game', False):
            return
        
        # Semi-transparent background
        bg_surface = pygame.Surface((zone.width, zone.height), pygame.SRCALPHA)
        bg_surface.fill(self.colors['background'])
        screen.blit(bg_surface, zone.topleft)
        
        # Formation name
        formation = game_data.get('formation_name', 'UNKNOWN')
        form_text, _ = self.font_manager.render_text(formation, 'small', self.colors['text_accent'])
        screen.blit(form_text, (zone.x + 5, zone.y + 5))
        
        # Aliens remaining with max active info
        active = game_data.get('active_aliens', 0)
        remaining = game_data.get('remaining_aliens', 0)
        max_aliens = game_data.get('max_aliens', 3)
        aliens_text, _ = self.font_manager.render_text(f"{active}/{max_aliens} | {remaining}", 'small', self.colors['text_secondary'])
        screen.blit(aliens_text, (zone.x + 5, zone.y + 25))
        
        # Progress bar
        if remaining > 0:
            progress = 1.0 - (remaining / game_data.get('total_aliens', remaining))
            bar_width = zone.width - 20
            bar_height = 8
            
            # Background bar
            bar_bg = pygame.Rect(zone.x + 10, zone.y + 50, bar_width, bar_height)
            pygame.draw.rect(screen, self.colors['border'], bar_bg)
            
            # Progress bar
            progress_width = int(bar_width * progress)
            if progress_width > 0:
                progress_bar = pygame.Rect(zone.x + 10, zone.y + 50, progress_width, bar_height)
                pygame.draw.rect(screen, self.colors['text_accent'], progress_bar)
    
    def draw_quick_stats(self, screen, game_data):
        """Draw quick stats in bottom-right (minimal)"""
        zone = self.ui_zones['bottom_right']
        
        # Only show if there are active bullets or special info
        bullets = game_data.get('active_bullets', 0)
        if bullets == 0 and not game_data.get('show_stats', False):
            return
        
        # Semi-transparent background
        bg_surface = pygame.Surface((100, 30), pygame.SRCALPHA)  # Smaller area
        bg_surface.fill(self.colors['background'])
        screen.blit(bg_surface, (zone.right - 100, zone.bottom - 30))
        
        # Active bullets
        if bullets > 0:
            bullet_text, bullet_rect = self.font_manager.render_text(f"⚡{bullets}", 'small', self.colors['text_secondary'])
            bullet_rect.bottomright = (zone.right - 5, zone.bottom - 5)
            screen.blit(bullet_text, bullet_rect)
    
    def draw_level_transition(self, screen, level_data):
        """Draw level transition screen"""
        # Full screen overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        # Level number
        level = level_data.get('level', 1)
        level_text, level_rect = self.font_manager.render_text(
            f"LEVEL {level}", 'title', self.colors['text_accent'], (center_x, center_y - 80)
        )
        screen.blit(level_text, level_rect)
        
        # Formation name
        formation = level_data.get('formation_name', 'UNKNOWN')
        form_text, form_rect = self.font_manager.render_text(
            f"{formation} FORMATION", 'large', self.colors['text_primary'], (center_x, center_y - 30)
        )
        screen.blit(form_text, form_rect)
        
        # Difficulty info
        difficulty = level_data.get('difficulty_summary', {})
        if difficulty:
            tier = difficulty.get('tier', 'ROOKIE')
            tier_text, tier_rect = self.font_manager.render_text(
                f"DIFFICULTY: {tier}", 'medium', self.colors['text_secondary'], (center_x, center_y + 20)
            )
            screen.blit(tier_text, tier_rect)
            
            # Quick stats
            stats = [
                f"Speed: {difficulty.get('speed_increase', '+0%')}",
                f"Max Aliens: {difficulty.get('max_aliens', 3)}",
                f"Abilities: {difficulty.get('special_count', 0)}"
            ]
            
            for i, stat in enumerate(stats):
                stat_text, stat_rect = self.font_manager.render_text(
                    stat, 'small', self.colors['text_secondary'], (center_x, center_y + 50 + i * 20)
                )
                screen.blit(stat_text, stat_rect)
        
        # Ready message
        ready_text, ready_rect = self.font_manager.render_text(
            "GET READY!", 'large', self.colors['health_low'], (center_x, center_y + 120)
        )
        screen.blit(ready_text, ready_rect)
    
    def get_ui_zones(self):
        """Get UI zones for collision detection"""
        return self.ui_zones
