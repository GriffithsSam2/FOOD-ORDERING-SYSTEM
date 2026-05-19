@echo off
setlocal enabledelayedexpansion
title  Building Food Ordering System (.exe)
color 0B

echo.
echo  ============================================================
echo    FOOD ORDERING SYSTEM  -  .EXE BUILDER
echo  ============================================================
echo.

REM ── Step 1: Check Python ────────────────────────────────────────
echo  [1/4]  Checking Python installation...
where python >nul 2>nul
if errorlevel 1 (
    color 0C
    echo.
    echo  [ERROR]  Python is not installed or not in your PATH.
    echo.
    echo  Please install Python first:
    echo    1. Go to https://www.python.org/downloads
    echo    2. Download and install the latest Python 3 version
    echo    3. IMPORTANT: tick "Add Python to PATH" during install
    echo    4. Restart this script after installation completes
    echo.
    pause
    exit /b 1
)
python --version
echo.

REM ── Step 2: Check FoodOrderingSystem.py exists ──────────────────
echo  [2/4]  Checking for FoodOrderingSystem.py...
if not exist "FoodOrderingSystem.py" (
    color 0C
    echo.
    echo  [ERROR]  FoodOrderingSystem.py was not found in this folder.
    echo.
    echo  Make sure this .bat file is in the SAME folder as
    echo  FoodOrderingSystem.py and try again.
    echo.
    pause
    exit /b 1
)
echo  Found: FoodOrderingSystem.py
echo.

REM ── Step 3: Install PyInstaller ─────────────────────────────────
echo  [3/4]  Installing PyInstaller (one-time setup)...
echo  This may take a minute on first run...
echo.
python -m pip install --upgrade pyinstaller --disable-pip-version-check --quiet
if errorlevel 1 (
    color 0C
    echo.
    echo  [ERROR]  Failed to install PyInstaller.
    echo  Make sure you have an internet connection.
    echo.
    pause
    exit /b 1
)
echo  PyInstaller ready.
echo.

REM ── Step 4: Build the .exe ──────────────────────────────────────
echo  [4/4]  Building FoodOrderingSystem.exe...
echo  This will take 1-2 minutes. Please wait...
echo.

pyinstaller --onefile --windowed --name "FoodOrderingSystem" --clean ^
            --distpath . FoodOrderingSystem.py 1>nul 2>nul

if errorlevel 1 (
    color 0C
    echo.
    echo  [ERROR]  Build failed.
    echo  Try running this script as Administrator.
    echo.
    pause
    exit /b 1
)

REM ── Cleanup intermediate build artefacts ────────────────────────
echo  Cleaning up temporary build files...
if exist "build"                    rmdir /s /q "build"                    >nul 2>nul
if exist "FoodOrderingSystem.spec"  del         "FoodOrderingSystem.spec"  >nul 2>nul

REM ── Done ────────────────────────────────────────────────────────
color 0A
echo.
echo  ============================================================
echo    BUILD SUCCESSFUL!
echo  ============================================================
echo.
echo    Your .exe is ready:
echo       FoodOrderingSystem.exe
echo.
echo    You can now:
echo       - Double-click FoodOrderingSystem.exe to run it
echo       - Share it with anyone (no Python needed on their PC)
echo       - Move it anywhere you want
echo.
echo    The fos.db file will be created next to the .exe
echo    the first time it runs. That stores your menu and orders.
echo.
echo  ============================================================
echo.
pause
