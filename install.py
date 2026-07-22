#!/usr/bin/env python3
"""
LiveMagic Pro - Install Dependencies
Run this if pip install fails
"""

import subprocess
import sys
import os

DEPENDENCIES = [
    'psutil>=5.9.0',
]

def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"❌ Python 3.9+ required. Found: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor} OK")
    return True

def install_dependencies():
    """Install required packages"""
    print("\nInstalling dependencies...")
    for package in DEPENDENCIES:
        print(f"  Installing {package}...")
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', package],
            capture_output=True
        )
        if result.returncode != 0:
            print(f"❌ Failed to install {package}")
            return False
        print(f"  ✅ {package}")
    return True

def create_directories():
    """Create required directories"""
    print("\nCreating directories...")
    dirs = ['logs', '.cache']
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
            print(f"  ✅ Created {d}/")
        else:
            print(f"  ℹ️  {d}/ exists")
    return True

def main():
    """Main installation function"""
    print("="*50)
    print("LiveMagic Pro - Dependency Installer")
    print("="*50)
    
    if not check_python():
        return False
    
    if not install_dependencies():
        print("\n❌ Installation failed")
        return False
    
    if not create_directories():
        print("\n❌ Directory creation failed")
        return False
    
    print("\n" + "="*50)
    print("✅ Installation Complete!")
    print("="*50)
    print("\nTo start streaming:")
    print("  python live_streamer_enhanced.py")
    print()
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
