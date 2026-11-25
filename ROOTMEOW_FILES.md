# ROOTMEOW - Complete File Structure

## Entry Points
| File | Purpose |
|------|---------|
| `main.py` | Main entry point for desktop/APK |
| `rootmeow` | CLI entry point (executable) |
| `rootmeow_app.py` | KivyMD native Android app |
| `rootmeow_bootstrap.py` | Auto-detect interface launcher |
| `neura.py` | Original NeuraSelf entry (kept for compatibility) |

## Build System
| File | Purpose |
|------|---------|
| `buildozer.spec` | Buildozer configuration for APK |
| `p4a_hooks.txt` | python-for-android hooks |
| `rootmeow_apk.py` | APK build script |
| `.github/workflows/build-apk.yml` | GitHub Actions CI/CD |

## Installers
| File | Platform |
|------|----------|
| `rootmeow_install.sh` | Termux/Linux/macOS |
| `rootmeow_install.bat` | Windows |
| `termux_setup.sh` | Termux post-install config |

## Android Service
| File | Purpose |
|------|---------|
| `rootmeow_service.py` | Foreground service for background running |
| `rootmeow_kv.kv` | Kivy UI definitions |

## Configuration
| File | Purpose |
|------|---------|
| `config/settings.json` | Main settings (core, stealth, security, commands) |
| `config/accounts.json` | Account credentials |
| `config/shortform.json` | Command shortcuts |
| `config/cmd_priorities.json` | Scheduler priorities |
| `config/logmisc.json` | Logging config |

## Requirements
| File | Purpose |
|------|---------|
| `requirements.txt` | Core Python dependencies |
| `requirements_apk.txt` | APK-specific dependencies |

## Documentation
| File | Purpose |
|------|---------|
| `README_ROOTMEOW.md` | Main documentation |
| `ROOTMEOW_FILES.md` | This file |
| `LICENSE` | GPLv3 license |

## Original NeuraSelf (Preserved)
| Directory | Purpose |
|-----------|---------|
| `core/` | Bot core logic (bot.py, state.py) |
| `cogs/` | Bot modules (security, grinding, gambling, etc.) |
| `dashboard/` | Web dashboard (Flask + HTML/JS/CSS) |
| `modules/` | Utility modules (captcha, identity, web_solver) |
| `neura_engines/` | Setup and quest engines |
| `utils/` | Utilities (proxy, history, platform) |
| `component_v2_neura/` | Discord UI components |
| `neuraself_ascii/` | ASCII banner art |
| `beeps/` | Notification sounds |

## Build Output (Generated)
```
bin/                    # Buildozer build directory
.buildozer/             # Buildozer cache
ROOTMEOW-v1.0.0.apk     # Final APK
```

## Quick Start Commands

### Desktop/Server
```bash
python rootmeow              # CLI interface
python rootmeow_bootstrap.py # Auto-detect
python rootmeow_app.py       # KivyMD UI
```

### Termux/Android
```bash
bash rootmeow_install.sh     # Install
bash termux_setup.sh         # Configure Termux
python rootmeow              # Run CLI
```

### Build APK
```bash
python rootmeow_apk.py       # Debug APK
python rootmeow_apk.py --aab # Release AAB
python rootmeow_apk.py --clean # Clean build
```

### Web Dashboard Only
```bash
python rootmeow_bootstrap.py --interface web --no-bot
```

## Key Changes from NeuraSelf
1. **Renamed**: NeuraSelf → ROOTMEOW
2. **Mobile-first**: Termux optimizations, APK build support
3. **Native Android UI**: KivyMD app with touch-friendly dashboard
4. **Foreground Service**: Background bot on Android
5. **Boot Auto-start**: Termux boot script
6. **Widget Support**: Termux:Widget shortcuts
7. **Simplified**: Removed subsistence/OwO-specific references
8. **Unified Config**: Single settings structure for all platforms