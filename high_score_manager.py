"""
Robust High Score Manager for Cosmic Raiders
Handles loading, saving, and error recovery for high scores
"""

import json
import os
from datetime import datetime

class HighScoreManager:
    def __init__(self, filename="high_score.json"):
        self.filename = filename
        self.high_score = 0
        self.high_score_level = 1
        self.high_score_date = "Never"
        self.default_data = {
            "high_score": 0,
            "level": 1,
            "date": "Never",
            "version": "1.0"
        }
        
        # Load high score with error handling
        self.load_high_score()
    
    def load_high_score(self):
        """Load high score with robust error handling"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                
                # Validate data structure
                if self._validate_data(data):
                    self.high_score = data.get("high_score", 0)
                    self.high_score_level = data.get("level", 1)
                    self.high_score_date = data.get("date", "Never")
                    print(f"🏆 Loaded high score: {self.high_score}")
                else:
                    raise ValueError("Invalid high score data structure")
            else:
                # Create default file
                self._create_default_file()
                
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            print(f"⚠️ High score file corrupted: {e}")
            self._create_default_file()
        except Exception as e:
            print(f"⚠️ Failed to load high score: {e}")
            self._create_default_file()
    
    def _validate_data(self, data):
        """Validate high score data structure"""
        if not isinstance(data, dict):
            return False
        
        required_keys = ["high_score", "level", "date"]
        for key in required_keys:
            if key not in data:
                return False
        
        # Validate data types
        if not isinstance(data["high_score"], int) or data["high_score"] < 0:
            return False
        if not isinstance(data["level"], int) or data["level"] < 1:
            return False
        if not isinstance(data["date"], str):
            return False
        
        return True
    
    def _create_default_file(self):
        """Create default high score file"""
        try:
            self.high_score = 0
            self.high_score_level = 1
            self.high_score_date = "Never"
            
            with open(self.filename, 'w') as f:
                json.dump(self.default_data, f, indent=2)
            
            print(f"📝 Created default high score file: {self.filename}")
        except Exception as e:
            print(f"⚠️ Failed to create default high score file: {e}")
    
    def save_high_score(self, score, level):
        """Save high score with error handling and backup"""
        try:
            # Create backup if file exists
            if os.path.exists(self.filename):
                backup_name = f"{self.filename}.backup"
                try:
                    import shutil
                    shutil.copy2(self.filename, backup_name)
                except:
                    pass  # Backup failed, but continue
            
            # Prepare data
            data = {
                "high_score": score,
                "level": level,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "version": "1.0",
                "last_updated": datetime.now().isoformat()
            }
            
            # Write to temporary file first
            temp_filename = f"{self.filename}.tmp"
            with open(temp_filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Atomic move (rename) to final file
            os.replace(temp_filename, self.filename)
            
            # Update internal state
            self.high_score = score
            self.high_score_level = level
            self.high_score_date = data["date"]
            
            print(f"💾 High score saved: {score} (Level {level})")
            
        except Exception as e:
            print(f"⚠️ Failed to save high score: {e}")
            # Try to restore from backup
            self._restore_from_backup()
    
    def _restore_from_backup(self):
        """Restore high score from backup file"""
        backup_name = f"{self.filename}.backup"
        try:
            if os.path.exists(backup_name):
                import shutil
                shutil.copy2(backup_name, self.filename)
                print(f"🔄 Restored high score from backup")
                self.load_high_score()  # Reload
        except Exception as e:
            print(f"⚠️ Failed to restore from backup: {e}")
    
    def update_if_high_score(self, score, level):
        """Update high score if the new score is higher"""
        if score > self.high_score:
            self.save_high_score(score, level)
            return True
        return False
    
    def get_high_score(self):
        """Get the current high score"""
        return self.high_score
    
    def get_high_score_level(self):
        """Get the level of the high score"""
        return self.high_score_level
    
    def get_high_score_date(self):
        """Get the date of the high score"""
        return self.high_score_date
    
    def reset_high_score(self):
        """Reset high score to default values"""
        self.save_high_score(0, 1)
        print("🔄 High score reset to default")
    
    def cleanup(self):
        """Cleanup method for graceful shutdown"""
        # Remove temporary files
        temp_files = [f"{self.filename}.tmp"]
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
        
        print("🧹 High score manager cleaned up")
