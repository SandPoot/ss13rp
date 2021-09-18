@echo Building main.py
cxfreeze --base-name ss13rp -c main.py --target-dir dist/main --icon icon.ico --packages pypresence,wheel,psutil --base Win32GUI
@echo Finished building main.py
@timeout 2
@echo Building install.py
cxfreeze -c install.py --target-dir dist/install --icon icon.ico
@echo Finished building install.py
@timeout 2