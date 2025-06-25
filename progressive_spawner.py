class ProgressiveSpawner:
    def __init__(self, difficulty_manager):
        self.difficulty_manager = difficulty_manager
        self.level_spawn_configs = self.create_spawn_configurations()
    
    def create_spawn_configurations(self):
        """Create progressive spawning configurations"""
        configs = {}
        
        for level in range(1, 21):
            # Progressive max aliens on screen
            if level == 1:
                max_active = 3  # Start with 3
            elif level == 2:
                max_active = 4  # Level 2: 4 aliens
            elif level <= 5:
                max_active = 5  # Levels 3-5: 5 aliens
            elif level <= 10:
                max_active = 6  # Levels 6-10: 6 aliens
            elif level <= 15:
                max_active = 7  # Levels 11-15: 7 aliens
            else:
                max_active = 8  # Levels 16+: 8 aliens (chaos mode)
            
            # Faster spawning at higher levels
            base_spawn_delay = 180  # 3 seconds at 60 FPS
            spawn_delay = max(60, base_spawn_delay - (level - 1) * 8)  # Minimum 1 second
            
            # Speed multiplier increases significantly
            speed_multiplier = 1.0 + (level - 1) * 0.4  # 40% speed increase per level
            
            # More aggressive shooting
            aggression_multiplier = 1.0 + (level - 1) * 0.5  # 50% more aggressive per level
            
            configs[level] = {
                'max_active_aliens': max_active,
                'spawn_delay': spawn_delay,
                'speed_multiplier': speed_multiplier,
                'aggression_multiplier': aggression_multiplier,
                'formation_size_multiplier': 1.0 + (level - 1) * 0.3  # Larger formations
            }
        
        return configs
    
    def get_spawn_config(self, level):
        """Get spawning configuration for level"""
        return self.level_spawn_configs.get(level, self.level_spawn_configs[20])
    
    def get_max_active_aliens(self, level):
        """Get maximum active aliens for level"""
        config = self.get_spawn_config(level)
        return config['max_active_aliens']
    
    def get_spawn_delay(self, level):
        """Get spawn delay for level"""
        config = self.get_spawn_config(level)
        return config['spawn_delay']
    
    def get_speed_multiplier(self, level):
        """Get speed multiplier for level"""
        config = self.get_spawn_config(level)
        return config['speed_multiplier']
    
    def get_aggression_multiplier(self, level):
        """Get aggression multiplier for level"""
        config = self.get_spawn_config(level)
        return config['aggression_multiplier']
    
    def get_formation_size_multiplier(self, level):
        """Get formation size multiplier for level"""
        config = self.get_spawn_config(level)
        return config['formation_size_multiplier']
    
    def get_level_summary(self, level):
        """Get human-readable level summary"""
        config = self.get_spawn_config(level)
        
        return {
            'max_aliens': config['max_active_aliens'],
            'spawn_speed': f"{3.0 - (config['spawn_delay'] / 60.0):.1f}s",
            'alien_speed': f"+{int((config['speed_multiplier'] - 1) * 100)}%",
            'aggression': f"+{int((config['aggression_multiplier'] - 1) * 100)}%",
            'formation_size': f"+{int((config['formation_size_multiplier'] - 1) * 100)}%"
        }
