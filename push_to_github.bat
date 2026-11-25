@echo off
:: Initialize git repo and push to GitHub for APK build via Actions

set REPO_URL=%1
if "%REPO_URL%"=="" set REPO_URL=https://github.com/USERNAME/neura-self.git

echo Initializing git repository...
git init
git add .
git commit -m "ROOTMEOW mobile build - APK ready for GitHub Actions"

echo Adding remote...
git remote add origin %REPO_URL%

echo Pushing to GitHub...
git push -u origin main

echo.
echo Done! Go to: https://github.com/USERNAME/neura-self/actions
echo Click 'Build ROOTMEOW APK' -> 'Run workflow' -> Download APK from Artifacts