# ROOTMEOW

**Mobile Discord Self-Bot Automation** — Built for Termux/Android, renamed from NeuraSelf.

---

## What is ROOTMEOW?

ROOTMEOW is a powerful, fully-featured Discord self-bot automation tool offering a premium web dashboard. It allows you to monitor all your data in real-time through an easy-to-manage, beautifully designed interface.

Optimized for **mobile (Termux)** and **desktop** deployment with APK building support.

---

## Features

- **Full Web Dashboard**: Real-time stats, charts, and live configuration editor via an elegant interface
- **Mobile Support (Termux)**: Fully functional on Android devices with toast notifications and vibrations
- **Smart Captcha Solvers**: Multiple captcha services (YesCaptcha, NopeCHA, Anti-Captcha, Captchaly) + ONNX model for letterword captchas + fallback to manual solve
- **Multi-Account Manager**: Safely run unlimited accounts simultaneously with independent settings
- **Advanced Stealth & Security**: Realistic typing simulation, auto-pause on detection, multi-layer security
- **Advanced Gambling**: Strategies (martingale, flat) with stoploss and take profit
- **Dynamic Quest Intelligence**: Automatically completes checklists and tracks progression
- **Advanced AutoGems**: Automatically equip gems
- **APK Building**: Build native Android APKs with buildozer
- **Easy Setup**: Automated installers for Termux, Linux, macOS, and Windows

---

## Installation

### Termux / Android (Recommended)

```bash
# Run in Termux (install Termux and Termux:API from F-Droid first)
bash <(curl -s https://raw.githubusercontent.com/routo-loop/neura-self/main/rootmeow_install.sh)
```

### Linux / macOS

```bash
bash <(curl -s https://raw.githubusercontent.com/routo-loop/neura-self/main/rootmeow_install.sh)
```

### Windows

```powershell
# Run in PowerShell
irm https://raw.githubusercontent.com/routo-loop/neura-self/main/rootmeow_install.bat | iex
```

### Manual Installation

```bash
git clone https://github.com/routo-loop/neura-self.git
cd neura-self
pip install -r requirements.txt
python neura_setup.py --quick
python rootmeow
```

---

## Building the APK

ROOTMEOW includes a complete buildozer configuration for building native Android APKs.

### Prerequisites

- Linux (Ubuntu/Debian recommended) or WSL2 on Windows
- Python 3.10+
- buildozer dependencies (see buildozer documentation)

### Build Commands

```bash
# Install buildozer
pip install buildozer cython

# Build debug APK
python rootmeow_apk.py

# Build release AAB (for Play Store)
python rootmeow_apk.py --aab

# Clean build directories
python rootmeow_apk.py --clean
```

The APK will be output to `./ROOTMEOW-v1.0.0.apk`

---

## Dashboard

Once the bot is running, access the beautiful dashboard at:

**http://localhost:8000**

Default credentials (change on first login):
- Username: `admin`
- Password: `neuraself_default_password_change_me`

---

## Mobile Optimizations

ROOTMEOW includes several mobile-specific optimizations:

- **Termux notifications** with vibration and TTS support
- **Toast notifications** with customizable colors and positions
- **Media player integration** for alert sounds
- **Wake lock** to keep bot running in background
- **Responsive dashboard** that works on mobile browsers
- **Touch-friendly UI** with mobile control panel

---

## Configuration

Configuration is managed through the web dashboard or JSON files in the config directory:

- `settings.json` - Global settings
- `settings_<user_id>.json` - Per-account settings
- `accounts.json` - Account credentials and channels
- `proxies.json` - Proxy pool

Key configuration categories:
- **Core**: Prefix, channels, main switches
- **Stealth**: Human-like delays, typing simulation
- **Security**: Captcha solvers, ban detection, notifications
- **Commands**: Per-command automation (hunt, battle, owo, etc.)
- **Gambling**: Strategies, stoploss, take profit
- **Quests**: Auto-quest tracking and completion

---

## Disclaimer

> [!IMPORTANT]
> This tool is for **educational purposes only**. Using self-bots violates Discord's Terms of Service. WE ARE NOT responsible if you get banned. Use only in private servers and do not openly share that you are using automation.

---

## Credits

**ROOTMEOW** — Mobile-optimized fork of NeuraSelf
- Original: NeuraSelf by ROUTO
- Mobile adaptation: killywilly
- Built with ❤️ for the Termux/Android community

---

## License

GNU General Public License v3.0 — See LICENSE file for details.