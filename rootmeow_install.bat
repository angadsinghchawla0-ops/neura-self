@echo off
:: ROOTMEOW - Windows Installer
:: Run this on Windows to install ROOTMEOW

set APP_NAME=ROOTMEOW
set REPO_URL=https://github.com/routo-loop/neura-self.git

set RED=\033[1;31m
set GREEN=\033[1;32m
set CYAN=\033[1;36m
set YELLOW=\033[1;33m
set RESET=\033[0m

:: Enable ANSI colors on Windows 10+
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 /f >nul 2>&1

echo %CYAN%[*] ROOTMEOW Windows Installer%RESET%
echo.

:: Check for Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%[X] Python not found. Please install Python 3.10+ from python.org%RESET%
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PY_VERSION=%%i
echo %GREEN%[OK] Python detected: %PY_VERSION%%RESET%

:: Check for Git
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo %YELLOW%[!] Git not found. Installing...%RESET%
    winget install Git.Git 2>nul || choco install git -y 2>nul || (
        echo %RED%[X] Failed to install Git. Please install manually.%RESET%
        pause
        exit /b 1
    )
)
echo %GREEN%[OK] Git detected%RESET%

:: Set install directory
set INSTALL_DIR=%USERPROFILE%\Downloads\rootmeow

:: Clone or update
if exist "%INSTALL_DIR%\.git" (
    echo %CYAN%[*] Updating existing installation...%RESET%
    cd /d "%INSTALL_DIR%"
    git pull
    if %errorlevel% neq 0 (
        echo %RED%[X] Update failed%RESET%
        pause
        exit /b 1
    )
) else (
    if exist "%INSTALL_DIR%" (
        echo %RED%[X] Directory exists but is not a git repository%RESET%
        pause
        exit /b 1
    )
    echo %CYAN%[*] Downloading ROOTMEOW...%RESET%
    git clone %REPO_URL% "%INSTALL_DIR%"
    if %errorlevel% neq 0 (
        echo %RED%[X] Clone failed%RESET%
        pause
        exit /b 1
    )
)

cd /d "%INSTALL_DIR%"

:: Check for entry point
if not exist "rootmeow" if not exist "main.py" (
    echo %RED%[X] Entry point not found%RESET%
    pause
    exit /b 1
)

:: Install dependencies
echo %CYAN%[*] Installing Python dependencies...%RESET%
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo %YELLOW%[!] Some dependencies may have failed%RESET%
)

:: Run setup
echo %CYAN%[*] Starting ROOTMEOW setup...%RESET%
python neura_setup.py --quick
if %errorlevel% neq 0 (
    echo %RED%[X] Setup failed%RESET%
    pause
    exit /b 1
)

echo.
echo %GREEN%ROOTMEOW installed successfully!%RESET%
echo %CYAN%Location:%RESET% %INSTALL_DIR%
echo %CYAN%Run manually:%RESET% cd "%INSTALL_DIR%" && python rootmeow
echo %CYAN%Build APK:%RESET% cd "%INSTALL_DIR%" && python rootmeow_apk.py
echo.
echo %GREEN%ROOTMEOW is ready! 🐱%RESET%
pause