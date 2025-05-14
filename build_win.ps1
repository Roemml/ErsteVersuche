Remove-Item .\dist\*
pyinstaller --onefile --windowed --icon=Game.ico --log-level WARN 2DPower.py
Copy-Item *.png .\dist\
Copy-Item *.ico .\dist\
Copy-Item *.mp3 .\dist\
Compress-Archive .\dist\* .\dist\2DPower