═══════════════════════════════════════════════════════════════
  FOOD ORDERING SYSTEM  —  How to Build the .exe
═══════════════════════════════════════════════════════════════

WHAT'S IN THIS FOLDER:
  • FoodOrderingSystem.py    The application source
  • build_exe.bat            One-click .exe builder
  • README.txt               This file


HOW TO CREATE THE .EXE (one-time setup):
───────────────────────────────────────────────────────────────

  Step 1.  Install Python (if you haven't already)
           → Go to:  https://www.python.org/downloads
           → Download the latest Python 3 installer
           → IMPORTANT: During install, tick the box
                        "Add Python to PATH"

  Step 2.  Put these three files in the same folder on your PC:
              FoodOrderingSystem.py
              build_exe.bat
              README.txt   (optional)

  Step 3.  Double-click  build_exe.bat
           → It will install PyInstaller (first time only)
           → Then build  FoodOrderingSystem.exe
           → Takes about 1-2 minutes total

  Step 4.  Done. You'll see  FoodOrderingSystem.exe  appear
           in the same folder.


HOW TO USE THE .EXE:
───────────────────────────────────────────────────────────────

  • Double-click  FoodOrderingSystem.exe  to launch the app
  • A file called  fos.db  will be created next to it on first
    run — that's the database storing your menu and orders
  • You can move both files anywhere; keep them together
  • You can share the .exe with anyone — they do NOT need
    Python installed


ADMIN ACCESS:
───────────────────────────────────────────────────────────────

  • Click the  🔐 Admin  button at the top right
  • Default PIN:  1234
  • To change the PIN, edit  FoodOrderingSystem.py  and change
    the line:  ADMIN_PIN = "1234"  to your preferred PIN, then
    rebuild the .exe by running build_exe.bat again


TROUBLESHOOTING:
───────────────────────────────────────────────────────────────

  Problem: "Python is not recognised"
  Fix:     Reinstall Python and tick "Add Python to PATH"

  Problem: Build script fails with permissions error
  Fix:     Right-click build_exe.bat → "Run as administrator"

  Problem: Antivirus flags the .exe
  Fix:     This is a false positive common with PyInstaller .exe
           files. Add an exception in your antivirus, or just
           run the .py file directly with Python.


═══════════════════════════════════════════════════════════════
  Developed by:  Griffiths Samuel Yankson
  Version:       2.0  (Python Edition)
═══════════════════════════════════════════════════════════════
