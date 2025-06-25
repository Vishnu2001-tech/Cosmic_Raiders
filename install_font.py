#!/usr/bin/env python3
"""
Font installer for Space Invaders game
Downloads and installs the Pixeled font for authentic retro arcade styling
"""

import os
import urllib.request
import sys

def download_pixeled_font():
    """Download Pixeled font from Google Fonts"""
    print("🎮 Space Invaders Font Installer")
    print("=" * 40)
    
    # Create fonts directory if it doesn't exist
    fonts_dir = "fonts"
    if not os.path.exists(fonts_dir):
        os.makedirs(fonts_dir)
        print(f"✓ Created {fonts_dir}/ directory")
    
    font_path = os.path.join(fonts_dir, "Pixeled.ttf")
    
    # Check if font already exists
    if os.path.exists(font_path):
        print(f"✓ Pixeled.ttf already exists at {font_path}")
        return True
    
    print("\n🔍 Attempting to download Pixeled font...")
    
    # Try multiple sources for pixel fonts
    font_urls = [
        # Alternative: Press Start 2P (similar retro style)
        "https://fonts.gstatic.com/s/pressstart2p/v14/e3t4euO8T-267oIAQAu6jDQyK3nVivM.ttf",
    ]
    
    for i, url in enumerate(font_urls):
        try:
            print(f"📥 Downloading from source {i+1}...")
            urllib.request.urlretrieve(url, font_path)
            print(f"✅ Successfully downloaded font to {font_path}")
            return True
        except Exception as e:
            print(f"❌ Failed to download from source {i+1}: {e}")
            continue
    
    print("\n⚠️  Automatic download failed.")
    print("📋 Manual installation instructions:")
    print("1. Visit: https://fonts.google.com/specimen/Press+Start+2P")
    print("2. Download the font file")
    print("3. Rename it to 'Pixeled.ttf'")
    print(f"4. Place it in the {fonts_dir}/ directory")
    print("\nAlternatively, search for 'pixel fonts' or '8-bit fonts' online.")
    
    return False

def create_sample_font():
    """Create a simple bitmap-style font as fallback"""
    print("\n🎨 Creating sample retro font configuration...")
    
    config_path = "fonts/font_config.txt"
    with open(config_path, 'w') as f:
        f.write("""# Space Invaders Font Configuration
# 
# This game supports custom pixel fonts for authentic retro styling
# 
# Recommended fonts:
# - Pixeled.ttf (place in this directory)
# - Press Start 2P
# - VT323
# - Orbitron
# 
# The game will automatically detect and use any font named 'Pixeled.ttf'
# in this directory, otherwise it falls back to system monospace fonts.
""")
    
    print(f"✓ Created font configuration at {config_path}")

if __name__ == "__main__":
    print("Installing retro font for Space Invaders...")
    
    success = download_pixeled_font()
    create_sample_font()
    
    if success:
        print("\n🎉 Font installation complete!")
        print("🚀 Run 'python3 space_invaders.py' to see the retro styling!")
    else:
        print("\n🎮 Game will use system font fallback.")
        print("🚀 Run 'python3 space_invaders.py' to play anyway!")
    
    print("\n" + "=" * 40)
