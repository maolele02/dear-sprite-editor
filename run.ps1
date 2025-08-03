New-Item -ItemType SymbolicLink -Path ".\scripts\icon.png" -Value ".\assets\icon.png"
& ".venv\Scripts\activate.ps1"
python "scripts\main.py"
