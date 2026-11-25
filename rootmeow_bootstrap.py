#!/usr/bin/env python3
"""
ROOTMEOW Bootstrap Script
Initializes the environment and launches the appropriate interface
"""

import sys
import os
import asyncio
import argparse

# Add project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def detect_interface():
    """Detect which interface to launch"""
    # Check for Android
    if 'ANDROID_ARGUMENT' in os.environ or 'ANDROID_PRIVATE' in os.environ:
        return 'kivy'

    # Check for Termux
    if "TERMUX_VERSION" in os.environ or "com.termux" in os.environ.get("PREFIX", ""):
        return 'cli'

    # Check for display
    if sys.platform.startswith("linux") and not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
        return 'cli'

    # Default to CLI for servers, Kivy for desktop
    if os.name == "nt" or sys.platform == "darwin" or os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"):
        return 'kivy'

    return 'cli'

def launch_cli():
    """Launch CLI interface (rootmeow)"""
    from rootmeow import main
    asyncio.run(main())

def launch_kivy():
    """Launch KivyMD interface (rootmeow_app)"""
    from rootmeow_app import main
    main()

def launch_web():
    """Launch web dashboard only"""
    from dashboard.app import app
    app.run(host='0.0.0.0', port=8000, debug=False)

def main():
    parser = argparse.ArgumentParser(description="ROOTMEOW Bootstrap")
    parser.add_argument('--interface', choices=['cli', 'kivy', 'web', 'auto'],
                       default='auto', help='Interface to launch')
    parser.add_argument('--no-bot', action='store_true',
                       help='Run dashboard only without bot')
    args = parser.parse_args()

    if args.interface == 'auto':
        interface = detect_interface()
    else:
        interface = args.interface

    print(f"[ROOTMEOW] Launching {interface} interface...")

    if args.no_bot:
        launch_web()
    elif interface == 'kivy':
        launch_kivy()
    elif interface == 'cli':
        launch_cli()
    elif interface == 'web':
        launch_web()

if __name__ == "__main__":
    main()