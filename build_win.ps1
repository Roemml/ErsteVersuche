Remove-Item .\dist\* -Recurse
pyinstaller --onefile --windowed --icon=.\data\Game.ico --log-level WARN 2DPower.py
# Copy-Item *.png .\dist\
# Copy-Item *.ico .\dist\
# Copy-Item *.mp3 .\dist\
New-Item -Path ".\dist" -Name "data" -ItemType "Directory"
Copy-Item .\data\* .\dist\data\ 
Remove-Item .\dist\data\Highscore.bin
Compress-Archive .\dist\* .\dist\2DPower_win64