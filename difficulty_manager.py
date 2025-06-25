import random

class DifficultyManager:
    def __init__(self):
        self.level_configs = self.create_level_configurations()
    
    def create_level_configurations(self):
        """Create detailed configurations for each level"""
        configs = {}
        
        for level in range(1, 21):  # Support up to level 20
            # Base difficulty scaling
            speed_multiplier = 1.0 + (level - 1) * 0.3  # 30% speed increase per level
            health_multiplier = 1 + (level - 1) // 3    # Health increases every 3 levels
            spawn_rate = max(60, 180 - (level - 1) * 8)  # Faster spawning each level
            
            # Alien type distribution changes with level
            if level <= 3:
                # Early levels: mostly basic aliens
                alien_distribution = {
                    'basic': 0.7,
                    'scout': 0.2,
                    'warrior': 0.1,
                    'commander': 0.0
                }
            elif level <= 6:
                # Mid levels: more scouts and warriors
                alien_distribution = {
                    'basic': 0.4,
                    'scout': 0.3,
                    'warrior': 0.2,
                    'commander': 0.1
                }
            elif level <= 10:
                # High levels: balanced mix
                alien_distribution = {
                    'basic': 0.3,
                    'scout': 0.3,
                    'warrior': 0.3,
                    'commander': 0.1
                }
            else:
                # Expert levels: mostly elite aliens
                alien_distribution = {
                    'basic': 0.2,
                    'scout': 0.2,
                    'warrior': 0.3,
                    'commander': 0.3
                }
            
            # Special abilities unlock at higher levels
            special_abilities = []
            if level >= 4:
                special_abilities.append('rapid_fire')
            if level >= 6:
                special_abilities.append('shield_regeneration')
            if level >= 8:
                special_abilities.append('teleport_dodge')
            if level >= 10:
                special_abilities.append('formation_shift')
            if level >= 12:
                special_abilities.append('boss_spawn')
            
            # Bullet patterns become more complex
            bullet_patterns = ['single']
            if level >= 3:
                bullet_patterns.append('double')
            if level >= 5:
                bullet_patterns.append('spread')
            if level >= 7:
                bullet_patterns.append('homing')
            if level >= 9:
                bullet_patterns.append('spiral')
            
            configs[level] = {
                'speed_multiplier': speed_multiplier,
                'health_multiplier': health_multiplier,
                'spawn_rate': spawn_rate,
                'alien_distribution': alien_distribution,
                'special_abilities': special_abilities,
                'bullet_patterns': bullet_patterns,
                'max_active_aliens': min(6, 3 + (level - 1) // 2),  # More aliens on screen
                'alien_aggression': min(0.01, 0.001 + (level - 1) * 0.0008),  # More aggressive shooting
                'formation_complexity': min(1.0, 0.5 + (level - 1) * 0.05),  # More complex formations
                'bonus_multiplier': 1.0 + (level - 1) * 0.1  # Score bonuses increase
            }
        
        return configs
    
    def get_level_config(self, level):
        """Get configuration for specific level"""
        return self.level_configs.get(level, self.level_configs[20])  # Cap at level 20 config
    
    def get_alien_type_for_level(self, level):
        """Get appropriate alien type based on level distribution"""
        config = self.get_level_config(level)
        distribution = config['alien_distribution']
        
        # Weighted random selection
        rand = random.random()
        cumulative = 0
        
        for alien_type, probability in distribution.items():
            cumulative += probability
            if rand <= cumulative:
                return alien_type
        
        return 'basic'  # Fallback
    
    def get_alien_stats(self, alien_type, level):
        """Get alien stats modified by level difficulty"""
        config = self.get_level_config(level)
        
        # Base stats
        base_stats = {
            'basic': {'health': 1, 'speed': 1.0, 'points': 10},
            'scout': {'health': 1, 'speed': 1.5, 'points': 15},
            'warrior': {'health': 2, 'speed': 0.8, 'points': 25},
            'commander': {'health': 3, 'speed': 1.2, 'points': 50}
        }
        
        stats = base_stats.get(alien_type, base_stats['basic']).copy()
        
        # Apply level modifiers
        stats['health'] *= config['health_multiplier']
        stats['speed'] *= config['speed_multiplier']
        stats['points'] = int(stats['points'] * config['bonus_multiplier'])
        
        return stats
    
    def should_use_special_ability(self, level, ability_name):
        """Check if special ability should be used this level"""
        config = self.get_level_config(level)
        return ability_name in config['special_abilities']
    
    def get_bullet_pattern(self, level):
        """Get appropriate bullet pattern for level"""
        config = self.get_level_config(level)
        return random.choice(config['bullet_patterns'])
    
    def get_level_summary(self, level):
        """Get human-readable summary of level difficulty"""
        config = self.get_level_config(level)
        
        # Determine difficulty tier
        if level <= 3:
            tier = "ROOKIE"
            color = "GREEN"
        elif level <= 6:
            tier = "VETERAN"
            color = "YELLOW"
        elif level <= 10:
            tier = "ELITE"
            color = "ORANGE"
        else:
            tier = "LEGENDARY"
            color = "RED"
        
        summary = {
            'tier': tier,
            'color': color,
            'speed_increase': f"+{int((config['speed_multiplier'] - 1) * 100)}%",
            'max_aliens': config['max_active_aliens'],
            'special_count': len(config['special_abilities']),
            'dominant_alien': max(config['alien_distribution'].items(), key=lambda x: x[1])[0].upper()
        }
        
        return summary
