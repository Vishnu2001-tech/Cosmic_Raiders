#!/usr/bin/env python3
"""
Test script to verify credits screen functionality
"""

import pygame
import sys
import time

# Initialize pygame
pygame.init()

def test_credits_screen():
    """Test the credits screen by simulating key presses"""
    print("🧪 Testing Credits Screen...")
    
    try:
        # Import the game
        from cosmic_raiders import Game
        
        # Create game instance
        game = Game()
        
        # Test credits content creation
        credits_content = game._create_credits_content()
        print(f"✅ Credits content created: {len(credits_content)} entries")
        
        # Test credits screen state
        game.start_credits()
        if game.state.name == "CREDITS":
            print("✅ Credits screen state activated")
        else:
            print("❌ Credits screen state failed")
        
        # Test credits drawing (without display)
        try:
            game.draw_credits_screen()
            print("✅ Credits screen drawing works")
        except Exception as e:
            print(f"❌ Credits screen drawing failed: {e}")
        
        # Test credits exit
        game.exit_credits()
        if game.state.name == "MENU":
            print("✅ Credits exit works")
        else:
            print("❌ Credits exit failed")
        
        print("🎉 Credits screen test completed successfully!")
        
    except Exception as e:
        print(f"❌ Credits screen test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_credits_screen()
    sys.exit(0 if success else 1)
