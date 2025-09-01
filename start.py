#!/usr/bin/env python3
"""
🚀 One-Stop-Shop Startup Script
Simple launcher for the one-stop-shop application
"""

import os
import sys
import subprocess
import time

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'fastapi', 'uvicorn', 'gradio', 'sqlalchemy', 
        'jinja2', 'aiofiles', 'dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n📦 Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    return True

def main():
    print("🔗 One-Stop-Shop Startup")
    print("=" * 40)
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        return
    
    print("\n🚀 Starting One-Stop-Shop...")
    print("=" * 40)
    
    try:
        # Start the main application
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error starting application: {e}")
    except FileNotFoundError:
        print("\n❌ Error: main.py not found")
        print("Make sure you're in the one_stop_shop directory")

if __name__ == "__main__":
    main()

