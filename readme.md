# Coingecko scraper

> Python/Tkinter desktop GUI app to connect to coingecko. This app uses Sqlite3 to store data
The app should be able to filter through every coin on coin gecko which 
- Price decreased by  more than X% over X days
- Price increase by more than   X% over X days
## Usage

```bash
# Install dependencies
pipenv install

# Run script
python ./src/main.py


# Compiled with Pyinstaller

# Windows
pyinstaller --onefile --windowed main.py

# MacOS
pyinstaller --onefile --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl' main.py
```

- Version: 1.0.0
- License: MIT
- Author: Annie Dang
