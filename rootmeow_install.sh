#!/usr/bin/env bash
# ROOTMEOW - Termux/Android Installer
# Run this in Termux to install ROOTMEOW

set -Eeuo pipefail

APP_NAME="ROOTMEOW"
REPO_URL="https://github.com/routo-loop/neura-self.git"
BRANCH="main"

RED="\033[1;31m"
GREEN="\033[1;32m"
CYAN="\033[1;36m"
YELLOW="\033[1;33m"
RESET="\033[0m"

fail() {
    echo -e "${RED}[X] $1${RESET}"
    exit 1
}

ok() {
    echo -e "${GREEN}[OK] $1${RESET}"
}

info() {
    echo -e "${CYAN}[*] $1${RESET}"
}

warn() {
    echo -e "${YELLOW}[!] $1${RESET}"
}

# Detect platform
if [ -d "/data/data/com.termux/files/usr" ]; then
    PLATFORM="termux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PLATFORM="macos"
else
    PLATFORM="linux"
fi

case "$PLATFORM" in
    termux)
        if [ ! -d "$HOME/storage" ]; then
            warn "Termux storage permission required"
            termux-setup-storage || true
            echo -e "${YELLOW}Please tap 'ALLOW' on the popup on your screen.${RESET}"
            read -p "Press ENTER after you have allowed storage permission..."
        fi
        if [ -d "$HOME/storage/downloads" ]; then
            INSTALL_DIR="$HOME/storage/downloads/rootmeow"
        else
            INSTALL_DIR="$HOME/rootmeow"
        fi
        ;;
    macos)
        if command -v xdg-user-dir >/dev/null 2>&1; then
            INSTALL_DIR="$(xdg-user-dir DOWNLOAD)/rootmeow"
        else
            INSTALL_DIR="$HOME/Downloads/rootmeow"
        fi
        ;;
    linux)
        if command -v xdg-user-dir >/dev/null 2>&1; then
            BASE_DIR="$(xdg-user-dir DOWNLOAD)"
        elif [ -d "$HOME/Downloads" ]; then
            BASE_DIR="$HOME/Downloads"
        else
            BASE_DIR="$HOME"
        fi
        INSTALL_DIR="$BASE_DIR/rootmeow"
        ;;
esac

# Find Python
find_python() {
    for cmd in python3.10 python3 python python3.11 python3.12; do
        if command -v "$cmd" >/dev/null 2>&1; then
            if "$cmd" - <<'PY'
import sys
exit(0 if sys.version_info >= (3,10) else 1)
PY
            then
                echo "$cmd"
                return
            fi
        fi
    done
}

PY_CMD="$(find_python || true)"

install_python() {
    info "Attempting to auto-install Python 3..."
    case "$PLATFORM" in
        termux)
            pkg update -y && pkg install python -y
            ;;
        macos)
            if command -v brew >/dev/null 2>&1; then
                brew install python
            else
                fail "Homebrew missing. Install Python manually from python.org."
            fi
            ;;
        linux)
            if command -v apt >/dev/null 2>&1; then
                sudo apt update
                sudo apt install -y python3 python3-pip python3-venv
            elif command -v dnf >/dev/null 2>&1; then
                sudo dnf install -y python3 python3-pip
            elif command -v yum >/dev/null 2>&1; then
                sudo yum install -y python3 python3-pip
            elif command -v pacman >/dev/null 2>&1; then
                sudo pacman -Sy --noconfirm python python-pip
            elif command -v apk >/dev/null 2>&1; then
                sudo apk add python3 py3-pip
            else
                fail "No supported package manager found. Please install Python 3.10+ manually."
            fi
            ;;
    esac
}

if [ -z "$PY_CMD" ]; then
    warn "Python 3.10+ not found."
    install_python
    PY_CMD="$(find_python || true)"
    if [ -z "$PY_CMD" ]; then
        fail "Failed to install Python 3.10+. Please install it manually."
    fi
fi

ok "Python detected: $($PY_CMD --version)"

# Install git
install_git() {
    case "$PLATFORM" in
        termux)
            pkg update -y && pkg install git -y
            ;;
        macos)
            if command -v brew >/dev/null 2>&1; then
                brew install git
            else
                fail "Git missing. Install Homebrew or Git manually (brew install git)."
            fi
            ;;
        linux)
            if command -v apt >/dev/null 2>&1; then
                sudo apt update
                sudo apt install -y git
            elif command -v dnf >/dev/null 2>&1; then
                sudo dnf install -y git
            elif command -v yum >/dev/null 2>&1; then
                sudo yum install -y git
            elif command -v pacman >/dev/null 2>&1; then
                sudo pacman -Sy --noconfirm git
            elif command -v apk >/dev/null 2>&1; then
                sudo apk add git
            else
                fail "No supported package manager found. Please install Git manually."
            fi
            ;;
    esac
}

if ! command -v git >/dev/null 2>&1; then
    warn "Git not found"
    install_git
fi

command -v git >/dev/null 2>&1 || fail "Git installation failed"
ok "Git detected"

# Install buildozer for APK building
install_buildozer() {
    info "Installing buildozer for APK builds..."
    $PY_CMD -m pip install --upgrade pip
    $PY_CMD -m pip install buildozer cython
    ok "Buildozer installed"
}

# Clone or update
mkdir -p "$(dirname "$INSTALL_DIR")"

if [ -d "$INSTALL_DIR" ]; then
    if [ -d "$INSTALL_DIR/.git" ]; then
        info "Updating existing installation"
        cd "$INSTALL_DIR"
        git pull || fail "Update failed"
    else
        fail "Installation directory exists but is not a ROOTMEOW repository"
    fi
else
    info "Downloading ROOTMEOW"
    git clone "$REPO_URL" "$INSTALL_DIR" || fail "Clone failed"
fi

cd "$INSTALL_DIR"

# Switch to rootmeow branch if it exists, otherwise stay on main
if git show-ref --verify --quiet refs/remotes/origin/rootmeow; then
    git checkout rootmeow
elif git show-ref --verify --quiet refs/heads/rootmeow; then
    git checkout rootmeow
fi

if [ ! -f "rootmeow" ] && [ ! -f "main.py" ]; then
    fail "Entry point not found (rootmeow or main.py)"
fi

# Make entry point executable
chmod +x rootmeow 2>/dev/null || true
chmod +x main.py 2>/dev/null || true

# Install dependencies
info "Installing Python dependencies..."
$PY_CMD -m pip install --upgrade pip
$PY_CMD -m pip install -r requirements.txt || warn "Some dependencies may have failed"

# Run setup
info "Starting ROOTMEOW setup..."
$PY_CMD neura_setup.py --quick || fail "Setup failed"

echo
ok "ROOTMEOW installed successfully"
echo -e "${CYAN}Location:${RESET} $INSTALL_DIR"
echo -e "${CYAN}Run manually:${RESET} cd \"$INSTALL_DIR\" && $PY_CMD rootmeow"
echo -e "${CYAN}Build APK:${RESET} cd \"$INSTALL_DIR\" && $PY_CMD rootmeow_apk.py"
echo
echo -e "${GREEN}ROOTMEOW is ready! 🐱${RESET}"