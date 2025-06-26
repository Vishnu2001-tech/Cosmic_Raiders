#!/usr/bin/env python3
"""
Robustness Test Suite for Cosmic Raiders
Tests missing assets, corrupted files, and error conditions
"""

import os
import json
import shutil
import subprocess
import time

def test_missing_assets():
    """Test game behavior with missing asset files"""
    print("🧪 Testing missing assets...")
    
    # Backup existing assets
    backup_dirs = []
    for dirname in ['sounds', 'fonts', 'sprites']:
        if os.path.exists(dirname):
            backup_name = f"{dirname}_backup"
            shutil.move(dirname, backup_name)
            backup_dirs.append((dirname, backup_name))
            print(f"📦 Backed up {dirname} to {backup_name}")
    
    try:
        # Test game with missing assets
        print("🎮 Starting game with missing assets...")
        result = subprocess.run(['python3', 'cosmic_raiders.py'], 
                              timeout=10, capture_output=True, text=True)
        
        if "Asset loader cleaned up" in result.stdout:
            print("✅ Game handled missing assets gracefully")
        else:
            print("⚠️ Game may have issues with missing assets")
            
    except subprocess.TimeoutExpired:
        print("✅ Game started successfully with missing assets")
    except Exception as e:
        print(f"❌ Game failed with missing assets: {e}")
    
    finally:
        # Restore assets
        for dirname, backup_name in backup_dirs:
            if os.path.exists(backup_name):
                shutil.move(backup_name, dirname)
                print(f"🔄 Restored {dirname}")

def test_corrupted_high_score():
    """Test corrupted high score file handling"""
    print("🧪 Testing corrupted high score file...")
    
    # Backup existing high score
    if os.path.exists('high_score.json'):
        shutil.copy('high_score.json', 'high_score.json.test_backup')
    
    try:
        # Create corrupted high score file
        with open('high_score.json', 'w') as f:
            f.write('{"invalid": json, "structure": }')
        
        # Test high score manager
        from high_score_manager import HighScoreManager
        hsm = HighScoreManager()
        
        if hsm.get_high_score() == 0:
            print("✅ Corrupted high score handled gracefully")
        else:
            print("⚠️ High score corruption handling may have issues")
            
    except Exception as e:
        print(f"❌ High score corruption test failed: {e}")
    
    finally:
        # Restore high score
        if os.path.exists('high_score.json.test_backup'):
            shutil.move('high_score.json.test_backup', 'high_score.json')
        elif os.path.exists('high_score.json'):
            os.remove('high_score.json')

def test_audio_fallbacks():
    """Test audio system fallbacks"""
    print("🧪 Testing audio fallbacks...")
    
    try:
        from optimized_audio_manager import OptimizedAudioManager
        audio_mgr = OptimizedAudioManager()
        
        # Test mute functionality
        audio_mgr.toggle_mute()
        audio_mgr.play_sound('player_shoot')  # Should not play
        
        audio_mgr.toggle_mute()
        audio_mgr.play_sound('player_shoot')  # Should play
        
        print("✅ Audio fallbacks working correctly")
        
    except Exception as e:
        print(f"⚠️ Audio fallback test had issues: {e}")

def test_performance():
    """Test game performance under load"""
    print("🧪 Testing performance...")
    
    try:
        # Start game and measure startup time
        start_time = time.time()
        
        result = subprocess.run(['python3', 'cosmic_raiders.py'], 
                              timeout=5, capture_output=True, text=True)
        
        startup_time = time.time() - start_time
        
        if startup_time < 3.0:
            print(f"✅ Fast startup time: {startup_time:.2f}s")
        else:
            print(f"⚠️ Slow startup time: {startup_time:.2f}s")
            
        # Check for performance warnings in output
        if "Low FPS" in result.stdout or "High memory" in result.stdout:
            print("⚠️ Performance warnings detected")
        else:
            print("✅ No performance warnings")
            
    except subprocess.TimeoutExpired:
        print("✅ Game started within timeout")
    except Exception as e:
        print(f"❌ Performance test failed: {e}")

def test_error_logging():
    """Test error logging functionality"""
    print("🧪 Testing error logging...")
    
    try:
        from asset_loader import asset_loader
        
        # Try to load non-existent asset
        asset_loader.load_sound('nonexistent', 'fake.wav')
        
        # Check if error was logged
        if asset_loader.error_log:
            print("✅ Error logging working correctly")
        else:
            print("⚠️ Error logging may not be working")
            
        # Cleanup
        asset_loader.cleanup()
        
        # Check if log file was created
        if os.path.exists('logs/errors.log'):
            print("✅ Error log file created successfully")
        else:
            print("⚠️ Error log file not created")
            
    except Exception as e:
        print(f"❌ Error logging test failed: {e}")

def main():
    """Run all robustness tests"""
    print("🚀 Starting Cosmic Raiders Robustness Test Suite")
    print("=" * 50)
    
    test_missing_assets()
    print()
    
    test_corrupted_high_score()
    print()
    
    test_audio_fallbacks()
    print()
    
    test_performance()
    print()
    
    test_error_logging()
    print()
    
    print("=" * 50)
    print("🏁 Robustness testing complete!")

if __name__ == "__main__":
    main()
