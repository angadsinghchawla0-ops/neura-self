#!/usr/bin/env bash
# ROOTMEOW Termux Post-Install Setup
# Run this after installation to configure Termux-specific features

set -Eeuo pipefail

RED="\033[1;31m"
GREEN="\033[1;32m"
CYAN="\033[1;36m"
YELLOW="\033[1;33m"
RESET="\033[0m"

info() { echo -e "${CYAN}[*] $1${RESET}"; }
ok() { echo -e "${GREEN}[OK] $1${RESET}"; }
warn() { echo -e "${YELLOW}[!] $1${RESET}"; }
fail() { echo -e "${RED}[X] $1${RESET}"; exit 1; }

# Check if running in Termux
if [ ! -d "/data/data/com.termux/files/usr" ]; then
    fail "This script must be run in Termux"
fi

info "ROOTMEOW Termux Setup"
echo

# 1. Install Termux:API if not present
if ! command -v termux-notification >/dev/null 2>&1; then
    info "Installing Termux:API..."
    pkg install -y termux-api || warn "Termux:API install failed (install from F-Droid)"
else
    ok "Termux:API already installed"
fi

# 2. Setup storage permission
if [ ! -d "$HOME/storage" ]; then
    info "Setting up storage permission..."
    termux-setup-storage
    echo -e "${YELLOW}Please tap 'ALLOW' on the popup.${RESET}"
    read -p "Press ENTER after allowing storage permission..."
else
    ok "Storage permission already granted"
fi

# 3. Install wake lock utility
if ! command -v termux-wake-lock >/dev/null 2>&1; then
    info "Installing termux-wake-lock..."
    pkg install -y termux-wake-lock
else
    ok "Wake lock utility available"
fi

# 4. Create ROOTMEOW config directory
CONFIG_DIR="$HOME/.config/rootmeow"
mkdir -p "$CONFIG_DIR"
ok "Config directory: $CONFIG_DIR"

# 5. Create startup script for auto-start
STARTUP_SCRIPT="$HOME/.termux/boot/rootmeow"
mkdir -p "$(dirname "$STARTUP_SCRIPT")"

cat > "$STARTUP_SCRIPT" << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
# ROOTMEOW auto-start on boot

# Acquire wake lock
termux-wake-lock

# Start ROOTMEOW
cd "$HOME/rootmeow" || cd "$HOME/storage/downloads/rootmeow" || exit 1
python rootmeow &
EOF

chmod +x "$STARTUP_SCRIPT"
ok "Boot startup script created: $STARTUP_SCRIPT"

# 6. Create widget script for Termux:Widget
WIDGET_DIR="$HOME/.shortcuts"
mkdir -p "$WIDGET_DIR"

cat > "$WIDGET_DIR/rootmeow_start" << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock
cd "$HOME/rootmeow" || cd "$HOME/storage/downloads/rootmeow"
python rootmeow &
termux-toast -b green -c white "ROOTMEOW started"
EOF

cat > "$WIDGET_DIR/rootmeow_stop" << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
pkill -f "python rootmeow"
termux-wake-unlock
termux-toast -b red -c white "ROOTMEOW stopped"
EOF

cat > "$WIDGET_DIR/rootmeow_status" << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
if pgrep -f "python rootmeow" >/dev/null; then
    termux-toast -b blue -c white "ROOTMEOW: RUNNING"
else
    termux-toast -b gray -c white "ROOTMEOW: STOPPED"
fi
EOF

chmod +x "$WIDGET_DIR/rootmeow_start"
chmod +x "$WIDGET_DIR/rootmeow_stop"
chmod +x "$WIDGET_DIR/rootmeow_status"
ok "Termux:Widget shortcuts created in $WIDGET_DIR"

# 7. Configure notification sound
NOTIFICATION_SOUND="$HOME/rootmeow/beeps/security_beep.mp3"
if [ ! -f "$NOTIFICATION_SOUND" ]; then
    warn "Notification sound not found at $NOTIFICATION_SOUND"
else
    ok "Notification sound ready"
fi

# 8. Show summary
echo
info "Termux setup complete!"
echo
echo "Next steps:"
echo "  1. Add accounts: python neura_setup.py"
echo "  2. Run ROOTMEOW: python rootmeow"
echo "  3. Access dashboard: http://localhost:8000"
echo "  4. Use Termux:Widget for quick start/stop"
echo "  5. Auto-starts on boot via ~/.termux/boot/rootmeow"
echo
echo "Commands:"
echo "  termux-wake-lock     # Keep CPU awake"
echo "  termux-wake-unlock   # Release wake lock"
echo "  termux-notification  # Test notifications"
echo "  termux-toast         # Test toasts"
echo
ok "ROOTMEOW is ready for Termux! 🐱"