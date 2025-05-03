#!/usr/bin/env python3
"""
Build script for packaging the Snake Game with pygbag
"""

import os
import sys
import subprocess
import shutil

def main():
    """Main build function"""
    # Check if pygbag is installed
    try:
        import pygbag
    except ImportError:
        print("Pygbag not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygbag"])
    
    # Create build directory if it doesn't exist
    if not os.path.exists("build"):
        os.makedirs("build")
    
    # Copy main.py to build directory
    shutil.copy("snakegame/main.py", "build/main.py")
    
    # Run pygbag
    subprocess.check_call([
        sys.executable, 
        "-m", 
        "pygbag", 
        "--build", 
        "--ume_block=0",
        "build"
    ])
    
    print("Build completed successfully!")
    print("The packaged game can be found in the 'build/web' directory")

if __name__ == "__main__":
    main()
