#!/usr/bin/env python3
"""
Startup script for AI Collection Agent
Provides multiple options for running the Gradio app with different port configurations
"""

import os
import sys
import subprocess
import socket
import argparse
from pathlib import Path

def check_port(port):
    """Check if a port is available"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def find_available_port(start_port=7861, max_attempts=20):
    """Find an available port starting from start_port"""
    for i in range(max_attempts):
        port = start_port + i
        if check_port(port):
            return port
    return None

def kill_process_on_port(port):
    """Kill process using a specific port (macOS/Linux)"""
    try:
        if sys.platform == "darwin" or sys.platform.startswith("linux"):
            cmd = f"lsof -ti :{port} | xargs kill -9"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Killed process on port {port}")
                return True
            else:
                print(f"No process found on port {port}")
                return False
        else:
            print("Port killing not supported on this platform")
            return False
    except Exception as e:
        print(f"Error killing process on port {port}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Start AI Collection Agent")
    parser.add_argument("--port", type=int, help="Specify port to use")
    parser.add_argument("--kill-port", type=int, help="Kill process using specified port")
    parser.add_argument("--find-port", action="store_true", help="Find available port")
    parser.add_argument("--force", action="store_true", help="Force kill process on port 7861")
    
    args = parser.parse_args()
    
    if args.kill_port:
        kill_process_on_port(args.kill_port)
        return
    
    if args.find_port:
        available_port = find_available_port()
        if available_port:
            print(f"Available port found: {available_port}")
        else:
            print("No available ports found in range 7861-7880")
        return
    
    if args.force:
        print("Force killing process on port 7861...")
        if kill_process_on_port(7861):
            print("Port 7861 is now available")
        else:
            print("Could not free port 7861")
        return
    
    # Check if main app file exists
    app_file = Path("app.py")
    if not app_file.exists():
        print("Error: app.py not found in current directory")
        sys.exit(1)
    
    # Set port from argument or find available
    if args.port:
        port = args.port
        if not check_port(port):
            print(f"Warning: Port {port} is not available")
            choice = input("Continue anyway? (y/N): ")
            if choice.lower() != 'y':
                sys.exit(1)
    else:
        # Check default port first
        if check_port(7861):
            port = 7861
            print("Port 7861 is available")
        else:
            print("Port 7861 is in use. Finding available port...")
            port = find_available_port()
            if port:
                print(f"Using available port: {port}")
            else:
                print("No available ports found. Please specify a port with --port")
                sys.exit(1)
    
    # Set environment variable and run app
    env = os.environ.copy()
    env['GRADIO_SERVER_PORT'] = str(port)
    
    print(f"Starting AI Collection Agent on port {port}")
    print("Press Ctrl+C to stop")
    
    try:
        subprocess.run([sys.executable, "app.py"], env=env)
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"Error starting application: {e}")

if __name__ == "__main__":
    main()
