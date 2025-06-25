import json
import os
from datetime import datetime

class HighScoreManager:
    def __init__(self, filename="high_score.json"):
        self.filename = filename
        self.high_score_data = self.load_high_score()
    
    def load_high_score(self):
        """Load high score from JSON file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    print(f"🏆 Loaded high score: {data.get('score', 0)}")
                    return data
            else:
                print("📝 Creating new high score file")
                return {"score": 0, "date": None, "level": 1}
        except Exception as e:
            print(f"⚠️ Error loading high score: {e}")
            return {"score": 0, "date": None, "level": 1}
    
    def save_high_score(self, score, level):
        """Save new high score to JSON file"""
        try:
            self.high_score_data = {
                "score": score,
                "date": datetime.now().isoformat(),
                "level": level
            }
            with open(self.filename, 'w') as f:
                json.dump(self.high_score_data, f, indent=2)
            print(f"🎉 New high score saved: {score} (Level {level})")
            return True
        except Exception as e:
            print(f"⚠️ Error saving high score: {e}")
            return False
    
    def get_high_score(self):
        """Get current high score"""
        return self.high_score_data.get("score", 0)
    
    def get_high_score_level(self):
        """Get level reached for high score"""
        return self.high_score_data.get("level", 1)
    
    def get_high_score_date(self):
        """Get date of high score"""
        date_str = self.high_score_data.get("date")
        if date_str:
            try:
                date_obj = datetime.fromisoformat(date_str)
                return date_obj.strftime("%Y-%m-%d %H:%M")
            except:
                return "Unknown"
        return "Never"
    
    def is_new_high_score(self, score):
        """Check if score is a new high score"""
        return score > self.get_high_score()
    
    def update_if_high_score(self, score, level):
        """Update high score if new score is higher"""
        if self.is_new_high_score(score):
            self.save_high_score(score, level)
            return True
        return False
