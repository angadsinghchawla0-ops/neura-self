#!/usr/bin/env python3
"""
ROOTMEOW APK Builder Script
Builds the APK for Android/Termux deployment

NOTE: Buildozer only runs on Linux. On Windows, use WSL2 or the GitHub Actions workflow.
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def run_cmd(cmd, cwd=None, check=True):
    """Run a command and return the result."""
    print(f"[BUILD] Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed: {cmd}")
    return result

def is_wsl():
    """Check if running in WSL."""
    try:
        with open('/proc/version', 'r') as f:
            return 'microsoft' in f.read().lower() or 'wsl' in f.read().lower()
    except:
        return False

def is_linux():
    """Check if running on Linux."""
    return platform.system().lower() == 'linux'

def check_build_environment():
    """Check if build environment is suitable."""
    system = platform.system().lower()

    if system == 'windows' and not is_wsl():
        print("[BUILD] ⚠️  Windows detected - Buildozer requires Linux/WSL2")
        print("[BUILD] Options:")
        print("  1. Use WSL2 (recommended): Install Ubuntu from Microsoft Store")
        print("  2. Use GitHub Actions: Push to repo, APK builds automatically")
        print("  3. Use a Linux VM or cloud instance")
        return False

    if system == 'darwin':
        print("[BUILD] ⚠️  macOS detected - Buildozer has limited support")
        print("[BUILD] Recommended: Use Linux/WSL2 or GitHub Actions")
        return False

    return True

def install_buildozer():
    """Install buildozer and dependencies."""
    print("[BUILD] Installing buildozer...")
    run_cmd("pip install --upgrade pip")
    run_cmd("pip install buildozer cython")

    # Install system dependencies on Ubuntu/Debian
    if is_linux() or is_wsl():
        print("[BUILD] Installing system dependencies...")
        run_cmd("sudo apt-get update", check=False)
        run_cmd("sudo apt-get install -y git zip unzip openjdk-17-jdk python3-pip build-essential libssl-dev libffi-dev libncurses5-dev libncursesw5-dev libsqlite3-dev libreadline-dev libbz2-dev zlib1g-dev", check=False)

def build_apk():
    """Build the APK using buildozer."""
    project_root = Path(__file__).parent
    os.chdir(project_root)

    print("=" * 60)
    print("ROOTMEOW APK BUILDER")
    print("=" * 60)

    # Check environment
    if not check_build_environment():
        print("\n[BUILD] Cannot build APK on this platform directly.")
        print("[BUILD] Use GitHub Actions workflow instead:")
        print("  git add . && git commit -m 'build' && git push")
        print("  Then check Actions tab for APK artifact")
        return False

    # Install buildozer if needed
    try:
        run_cmd("buildozer --version", check=False)
    except FileNotFoundError:
        install_buildozer()

    # Clean previous builds
    print("[BUILD] Cleaning previous builds...")
    for dir_name in ['bin', '.buildozer']:
        dir_path = project_root / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)

    # Ensure main.py exists
    main_py = project_root / "main.py"
    if not main_py.exists():
        raise RuntimeError("main.py not found!")

    # Build the APK
    print("[BUILD] Building APK (this may take 10-30 minutes)...")
    result = run_cmd("buildozer -v android debug", check=False)

    if result.returncode != 0:
        print("[BUILD] Build failed! Check logs above.")
        return False

    # Find the APK
    bin_dir = project_root / "bin"
    apks = list(bin_dir.glob("*.apk"))
    if not apks:
        print("[BUILD] No APK found in bin/")
        return False

    apk_path = apks[0]
    print(f"[BUILD] SUCCESS! APK created: {apk_path}")
    print(f"[BUILD] Size: {apk_path.stat().st_size / 1024 / 1024:.1f} MB")

    # Copy to a friendly name
    final_apk = project_root / "ROOTMEOW-v1.0.0.apk"
    shutil.copy2(apk_path, final_apk)
    print(f"[BUILD] Copied to: {final_apk}")

    return True

def build_aab():
    """Build the AAB (Android App Bundle) for Play Store."""
    project_root = Path(__file__).parent
    os.chdir(project_root)

    if not check_build_environment():
        return False

    print("[BUILD] Building AAB...")
    result = run_cmd("buildozer -v android release", check=False)

    if result.returncode != 0:
        print("[BUILD] AAB build failed!")
        return False

    bin_dir = project_root / "bin"
    aabs = list(bin_dir.glob("*.aab"))
    if not aabs:
        print("[BUILD] No AAB found!")
        return False

    aab_path = aabs[0]
    print(f"[BUILD] AAB created: {aab_path}")
    return True

def setup_wsl_instructions():
    """Print WSL2 setup instructions."""
    print("""
============================================================
WSL2 SETUP FOR APK BUILDING
============================================================

1. Enable WSL2:
   wsl --install -d Ubuntu

2. Restart computer, then open Ubuntu from Start menu

3. In Ubuntu terminal:
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y git zip unzip openjdk-17-jdk python3-pip \
       build-essential libssl-dev libffi-dev libncurses5-dev \
       libncursesw5-dev libsqlite3-dev libreadline-dev libbz2-dev zlib1g-dev
   pip install buildozer cython

4. Clone repo in WSL:
   git clone https://github.com/your-repo/neura-self.git
   cd neura-self
   python rootmeow_apk.py

============================================================
GITHUB ACTIONS (EASIEST - NO LOCAL BUILD NEEDED)
============================================================

1. Push to GitHub:
   git add .
   git commit -m "build apk"
   git push

2. Go to: https://github.com/your-repo/neura-self/actions
3. Click "Build ROOTMEOW APK" workflow
4. Click "Run workflow"
5. Download APK from Artifacts when complete

============================================================
""")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ROOTMEOW APK Builder")
    parser.add_argument("--aab", action="store_true", help="Build AAB instead of APK")
    parser.add_argument("--clean", action="store_true", help="Clean build directories")
    parser.add_argument("--setup-wsl", action="store_true", help="Show WSL2 setup instructions")
    args = parser.parse_args()

    if args.setup_wsl:
        setup_wsl_instructions()
        sys.exit(0)

    if args.clean:
        project_root = Path(__file__).parent
        for dir_name in ['bin', '.buildozer']:
            dir_path = project_root / dir_name
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"[BUILD] Cleaned {dir_name}")
        sys.exit(0)

    if args.aab:
        success = build_aab()
    else:
        success = build_apk()

    sys.exit(0 if success else 1)