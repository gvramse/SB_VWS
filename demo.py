#!/usr/bin/env python3
"""
🚀 One-Stop-Shop Demo Script
Test the system functionality and show available features
"""

import os
import sys
import sqlite3
from datetime import datetime

def main():
    print("🔗 One-Stop-Shop Web UI Demo")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found in current directory")
        print("Please run this script from the one_stop_shop folder")
        return
    
    print("✅ Found main application file")
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("❌ Error: Python 3.8+ required")
        return
    
    print("✅ Python version compatible")
    
    # Try to import required packages
    required_packages = [
        'fastapi', 'uvicorn', 'gradio', 'sqlalchemy', 
        'jinja2', 'aiofiles', 'dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} imported successfully")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} not found")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return
    
    print("\n🎯 All dependencies satisfied!")
    
    # Check if database exists
    if os.path.exists("one_stop_shop.db"):
        print("✅ Database file found")
        try:
            conn = sqlite3.connect("one_stop_shop.db")
            cursor = conn.cursor()
            
            # Check tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print(f"✅ Database tables: {[table[0] for table in tables]}")
            
            # Check sample data
            cursor.execute("SELECT COUNT(*) FROM links")
            link_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM categories")
            category_count = cursor.fetchone()[0]
            
            print(f"✅ Sample data: {link_count} links, {category_count} categories")
            
            conn.close()
        except Exception as e:
            print(f"⚠️ Database check failed: {e}")
    else:
        print("ℹ️ Database will be created on first run")
    
    print("\n🚀 To run the one-stop-shop:")
    print("python main.py")
    print("\n📊 The system will start:")
    print("   - 🌐 Web Interface: http://localhost:8000")
    print("   - 🔧 API Server: http://localhost:8000")
    print("   - 📚 API Docs: http://localhost:8000/docs")
    print("   - 🎨 Gradio Interface: http://localhost:7860")
    print("   - ⚙️ Admin Panel: http://localhost:8000/admin")
    
    print("\n🔗 Key Features:")
    print("   - ✅ Dynamic link management (no code changes needed)")
    print("   - ✅ Category organization with custom colors and icons")
    print("   - ✅ Search and filter functionality")
    print("   - ✅ Admin panel for easy management")
    print("   - ✅ Gradio interface for ML/AI integration")
    print("   - ✅ RESTful API for external integrations")
    print("   - ✅ Responsive web design")
    
    print("\n💡 Usage Examples:")
    print("   1. Add new links via admin panel or API")
    print("   2. Create custom categories")
    print("   3. Organize links by project, tool, or topic")
    print("   4. Share your link hub with team members")
    print("   5. Integrate with other systems via API")

if __name__ == "__main__":
    main()
