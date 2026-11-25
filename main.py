#!/usr/bin/env python3
"""
ROOTMEOW - Mobile Discord Self-Bot Automation
Entry point for APK builds and desktop
"""

import sys
import os

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Ensure we can import from project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Run the rootmeow entry point
from rootmeow import main

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())