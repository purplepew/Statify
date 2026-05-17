
# Statistics Calc — Quick Start (Windows)

Simple steps for a non-programmer to run the app on Windows.

Get the project

- Clone from GitHub (recommended):

```powershell
git clone https://github.com/<username>/<repo>.git
cd "for real 3"
```

- Or download ZIP from GitHub: click "Code → Download ZIP", then extract and open the extracted `for real 3` folder.

Prerequisites

- Windows PC
- Python 3.8 or newer installed (from https://www.python.org/)

Steps
1. Open the project folder `for real 3` in File Explorer.
2. Install the program dependencies (one-time):

   - Open the folder in PowerShell: hold Shift, right-click inside the folder and choose "Open PowerShell window here" (or "Open in Terminal").
   - In the PowerShell window run:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3. Run the program:

```powershell
python main_python.py
```

4. The application window will open. Use the navigation buttons to access the Data Lab and other features.

Notes

- If double-clicking `main_python.py` doesn't open the app, use the PowerShell commands above.
- The visualization features require packages such as `matplotlib`, `pandas`, and `seaborn` (included in `requirements.txt`).
- If you prefer not to install packages system-wide, you can create a virtual environment first:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main_python.py
```

Support

- If you run into an error, copy the exact error message and share it with the developer for help.
