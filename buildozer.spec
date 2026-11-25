[app]

# Application name
title = ROOTMEOW

# Package name (reverse domain notation)
package.name = rootmeow

# Package domain
package.domain = org.rootmeow

# Source directory
source.dir = .

# Source files to include
source.include_exts = py,png,jpg,kv,atlas,json,md,txt,html,css,js,ico,svg,webp,gif,mp3,wav,ogg

# Version
version = 1.0.0

# Application requirements
requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests==2.31.0,aiohttp==3.12.15,aiohttp-socks==0.10.1,plyer==2.1.0,playsound3==3.3.0,python-dotenv==1.2.1,rich==14.2.0,certifi,urllib3,charset-normalizer,idna

# Android specific
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,WAKE_LOCK,VIBRATE,FOREGROUND_SERVICE,FOREGROUND_SERVICE_MEDIA_PLAYBACK,POST_NOTIFICATIONS

# Android features
android.features = android.hardware.wifi,android.hardware.touchscreen

# Android api
android.api = 33
android.minapi = 24
android.ndk = 27c
android.ndk_api = 24

# Android gradle
android.gradle_dependencies =
android.add_jar =
android.add_src =
android.add_aars =
android.enable_androidx = True
android.gradle_repositories =

# Gradle settings for memory
android.gradle_args = -Dorg.gradle.jvmargs="-Xmx2g -XX:MaxMetaspaceSize=512m"

# Orientation
orientation = portrait

# Icon
icon.filename = dashboard/static/assets/neura.ico

# Presplash
presplash.filename = dashboard/static/assets/neuraselfbanner.png

# Fullscreen
fullscreen = 1

# Wake lock
android.wakelock = True

# Copy libs
android.copy_libs = 1

# Private storage
android.private_storage =

# Whitelist
android.release_artifact = aab

# Build
p4a.branch = master
p4a.bootstrap = sdl2

# Log level
log_level = 2

# Warning filter
warning_filter = 0

[buildozer]

# Log level
log_level = 2

# Warn on root
warn_on_root = 1

# Profiler
# p4a.profile = 1